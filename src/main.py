import re
import time
import dxcam
import cv2
import win32gui
import win32api
import win32con

import utils.paths as pth
from pathlib import Path

# ---------------------------------
# Window discovery
# ---------------------------------

def find_wizard101_window():
    def callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if re.fullmatch(r"Wizard101", title):
                results.append(hwnd)
        return True

    matches = []
    win32gui.EnumWindows(callback, matches)
    return matches[0] if matches else None


def get_client_rect_global(hwnd):
    """Returns Wizard101 client rect in GLOBAL desktop coords (x1,y1,x2,y2)."""
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    x1, y1 = win32gui.ClientToScreen(hwnd, (left, top))
    x2, y2 = win32gui.ClientToScreen(hwnd, (right, bottom))
    return (x1, y1, x2, y2)


# ---------------------------------
# Monitor helpers
# ---------------------------------

def get_monitor_handle_for_window(hwnd):
    return win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)


def get_monitor_bounds(monitor_handle):
    """Returns (left, top, right, bottom) in GLOBAL desktop coords."""
    info = win32api.GetMonitorInfo(monitor_handle)
    return info["Monitor"]


def _colorref_to_bgr(colorref: int):
    # COLORREF is 0x00bbggrr
    r = colorref & 0xFF
    g = (colorref >> 8) & 0xFF
    b = (colorref >> 16) & 0xFF
    return (b, g, r)


def _get_screen_pixel_bgr(x: int, y: int):
    hdc = win32gui.GetDC(0)
    try:
        colorref = win32gui.GetPixel(hdc, x, y)
        return _colorref_to_bgr(colorref)
    finally:
        win32gui.ReleaseDC(0, hdc)


# ---------------------------------
# dxcam output calibration (robust mapping)
# ---------------------------------

_OUTPUT_CACHE = {}  # monitor_handle -> dxcam output_idx

def dxcam_output_idx_for_monitor(monitor_handle, max_outputs=None):
    """
    Robustly maps a Windows monitor handle to the correct dxcam output_idx
    by matching a few pixel samples. Cached per monitor handle.
    """
    if monitor_handle in _OUTPUT_CACHE:
        return _OUTPUT_CACHE[monitor_handle]

    ml, mt, mr, mb = get_monitor_bounds(monitor_handle)
    w = mr - ml
    h = mb - mt

    # Sample a few points that are unlikely all identical
    sample_points_local = [
        (10, 10),
        (w // 2, h // 2),
        (max(0, w - 11), max(0, h - 11)),
        (w // 4, h // 3),
        (w // 3, h // 2),
    ]

    expected = []
    for lx, ly in sample_points_local:
        gx, gy = ml + lx, mt + ly
        expected.append(_get_screen_pixel_bgr(gx, gy))

    if max_outputs is None:
        max_outputs = len(win32api.EnumDisplayMonitors()) + 3

    best_idx = 0
    best_score = -1

    for idx in range(max_outputs):
        cam = None
        try:
            cam = dxcam.create(output_idx=idx, output_color="BGR")
            frame = cam.grab()
            if frame is None:
                continue

            fh, fw = frame.shape[:2]
            if fw != w or fh != h:
                continue  # wrong monitor

            score = 0
            for (lx, ly), exp_bgr in zip(sample_points_local, expected):
                b, g, r = frame[ly, lx]
                if (int(b), int(g), int(r)) == exp_bgr:
                    score += 1

            if score > best_score:
                best_score = score
                best_idx = idx

        except Exception:
            continue
        finally:
            try:
                if cam is not None:
                    cam.release()
            except Exception:
                pass

    _OUTPUT_CACHE[monitor_handle] = best_idx
    return best_idx


# ---------------------------------
# Cropping helpers (smooth drag-safe)
# ---------------------------------

def compute_crop_rect_local(global_client_rect, monitor_handle, full_w, full_h):
    """
    Convert global client rect -> monitor-local crop rect, clamped to the frame size.
    Returns (x1,y1,x2,y2) in local coords, or None if invalid.
    """
    ml, mt, _, _ = get_monitor_bounds(monitor_handle)
    gx1, gy1, gx2, gy2 = global_client_rect

    # Convert to local
    x1 = int(gx1 - ml)
    y1 = int(gy1 - mt)
    x2 = int(gx2 - ml)
    y2 = int(gy2 - mt)

    # Ensure ordering
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1

    # Clamp to captured frame bounds
    x1 = max(0, min(x1, full_w))
    x2 = max(0, min(x2, full_w))
    y1 = max(0, min(y1, full_h))
    y2 = max(0, min(y2, full_h))

    # Require at least a small crop area
    if (x2 - x1) < 32 or (y2 - y1) < 32:
        return None

    return (x1, y1, x2, y2)


# ---------------------------------
# Tracker: rect + monitor (time-throttled)
# ---------------------------------

class WindowTracker:
    def __init__(self, hwnd, min_update_interval=0.03):
        self.hwnd = hwnd
        self.last_rect = get_client_rect_global(hwnd)
        self.last_monitor = get_monitor_handle_for_window(hwnd)
        self.last_update_time = 0.0
        self.min_update_interval = min_update_interval

    def poll(self):
        rect = get_client_rect_global(self.hwnd)
        monitor = get_monitor_handle_for_window(self.hwnd)

        if rect == self.last_rect and monitor == self.last_monitor:
            return None

        now = time.time()
        if now - self.last_update_time < self.min_update_interval:
            return None

        self.last_rect = rect
        self.last_monitor = monitor
        self.last_update_time = now

        return rect, monitor


# ---------------------------------
# Capture manager: full-monitor capture + crop (smooth)
# ---------------------------------

class CaptureManager:
    def __init__(self, monitor_handle, fps=60):
        self.monitor_handle = monitor_handle
        self.output_idx = dxcam_output_idx_for_monitor(monitor_handle)
        self.fps = fps
        self.camera = None
        self.start()

    def start(self):
        # FULL MONITOR CAPTURE (no region) -> avoids invalid region errors mid-drag
        self.camera = dxcam.create(output_idx=self.output_idx, output_color="BGR")
        self.camera.start(target_fps=self.fps)

    def restart_for_monitor(self, monitor_handle):
        # Only restart when monitor changes
        self.stop()
        self.monitor_handle = monitor_handle
        self.output_idx = dxcam_output_idx_for_monitor(monitor_handle)
        print(f"[INFO] Switched monitor → dxcam output_idx={self.output_idx}")
        self.start()

    def stop(self):
        if self.camera:
            try:
                self.camera.stop()
            except Exception:
                pass
            try:
                self.camera.release()
            except Exception:
                pass
            self.camera = None

    def get_full_frame(self):
        return self.camera.get_latest_frame() if self.camera else None


# ---------------------------------
# Main
# ---------------------------------

def main():
    hwnd = find_wizard101_window()
    if not hwnd:
        raise RuntimeError("Wizard101 window not found (exact title required).")

    tracker = WindowTracker(hwnd)
    capture = CaptureManager(tracker.last_monitor, fps=60)

    last_good = None  # last good cropped frame (for ultra smooth dragging)

    print("Wizard101 capture running (smooth mode: full-monitor + crop)")
    print("Drag/resize freely, including across monitors")
    print("Press Q to quit")

    while True: 
        # Skip if minimized
        if win32gui.IsIconic(hwnd):
            time.sleep(0.02)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue

        update = tracker.poll()
        if update:
            rect, mon = update
            if mon != capture.monitor_handle:
                capture.restart_for_monitor(mon)

        frame = capture.get_full_frame()
        if frame is None:
            continue

        fh, fw = frame.shape[:2]
        crop_rect = compute_crop_rect_local(tracker.last_rect, capture.monitor_handle, fw, fh)

        if crop_rect is not None:
            x1, y1, x2, y2 = crop_rect
            cropped = frame[y1:y2, x1:x2]
            last_good = cropped
            cv2.imshow("Wizard101 Capture", cropped)
        else:
            # During extreme mid-drag states, show last good crop (smoothness)
            if last_good is not None:
                cv2.imshow("Wizard101 Capture", last_good)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break



if __name__ == "__main__":
    main()
