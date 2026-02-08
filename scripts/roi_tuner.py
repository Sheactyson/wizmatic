import argparse
import sys
import time
from pathlib import Path
from typing import Dict, Tuple

import cv2
import tkinter as tk
from tkinter import ttk

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from utils.capture_wiz import Wizard101Capture
from utils.capture_thread import FrameSource
from utils.roi import crop_relative, draw_status_list


WINDOW_FULL = "ROI Tuner - Full Capture"
WINDOW_ROI = "ROI Tuner - ROI Preview"
COORD_KEYS = ("x1", "y1", "x2", "y2")


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


class ROITunerApp:
    def __init__(
        self,
        *,
        width: int,
        height: int,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        zoom_percent: int,
        fps: int,
        hz: int,
    ) -> None:
        self.width = max(1, int(width))
        self.height = max(1, int(height))
        self.closed = False

        self.cap = Wizard101Capture(fps=max(1, int(fps)))
        self.frames = FrameSource(self.cap, hz=max(1, int(hz)))
        self.frames.start()

        self.root = tk.Tk()
        self.root.title("ROI Tuner Controls")
        self.root.geometry("560x320")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.coord_vars: Dict[str, tk.DoubleVar] = {
            "x1": tk.DoubleVar(value=float(x1)),
            "y1": tk.DoubleVar(value=float(y1)),
            "x2": tk.DoubleVar(value=float(x2)),
            "y2": tk.DoubleVar(value=float(y2)),
        }
        self.coord_entry_vars: Dict[str, tk.StringVar] = {
            key: tk.StringVar(value=f"{self.coord_vars[key].get():.4f}") for key in COORD_KEYS
        }
        self.zoom_var = tk.DoubleVar(value=float(zoom_percent))
        self.zoom_entry_var = tk.StringVar(value=str(int(zoom_percent)))
        self._last_roi_window_size: Tuple[int, int] = (0, 0)
        self._last_roi_resize_at: float = 0.0
        self.coord_entries: Dict[str, ttk.Entry] = {}
        self.zoom_entry: ttk.Entry | None = None

        self._build_controls()

        window_flags = cv2.WINDOW_NORMAL
        if hasattr(cv2, "WINDOW_KEEPRATIO"):
            window_flags |= cv2.WINDOW_KEEPRATIO
        cv2.namedWindow(WINDOW_FULL, window_flags)
        cv2.namedWindow(WINDOW_ROI, window_flags)

        self.root.after(1, self._tick)
        self.root.mainloop()

    def _build_controls(self) -> None:
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        row = 0
        for key in COORD_KEYS:
            ttk.Label(frame, text=key.upper(), width=6).grid(row=row, column=0, sticky=tk.W, pady=4)
            slider = ttk.Scale(
                frame,
                from_=0.0,
                to=1.0,
                variable=self.coord_vars[key],
                orient=tk.HORIZONTAL,
                command=lambda _v, k=key: self._on_slider_change(k),
            )
            slider.grid(row=row, column=1, sticky=tk.EW, padx=6)

            entry = ttk.Entry(frame, textvariable=self.coord_entry_vars[key], width=10)
            entry.grid(row=row, column=2, sticky=tk.W)
            entry.bind("<Return>", lambda _e, k=key: self._on_coord_entry_commit(k))
            entry.bind("<FocusOut>", lambda _e, k=key: self._on_coord_entry_commit(k))
            self.coord_entries[key] = entry
            row += 1

        ttk.Separator(frame).grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=8)
        row += 1

        ttk.Label(frame, text="Zoom %", width=6).grid(row=row, column=0, sticky=tk.W, pady=4)
        zoom_slider = ttk.Scale(
            frame,
            from_=25.0,
            to=1600.0,
            variable=self.zoom_var,
            orient=tk.HORIZONTAL,
            command=self._on_zoom_slider_change,
        )
        zoom_slider.grid(row=row, column=1, sticky=tk.EW, padx=6)

        zoom_entry = ttk.Entry(frame, textvariable=self.zoom_entry_var, width=10)
        zoom_entry.grid(row=row, column=2, sticky=tk.W)
        zoom_entry.bind("<Return>", self._on_zoom_entry_commit)
        zoom_entry.bind("<FocusOut>", self._on_zoom_entry_commit)
        self.zoom_entry = zoom_entry
        row += 1

        ttk.Separator(frame).grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=8)
        row += 1

        btns = ttk.Frame(frame)
        btns.grid(row=row, column=0, columnspan=3, sticky=tk.EW)
        ttk.Button(btns, text="Copy ROI Tuple", command=self._copy_roi).pack(side=tk.LEFT)
        ttk.Button(btns, text="Quit", command=self.close).pack(side=tk.RIGHT)
        row += 1

        self.status_var = tk.StringVar(value="ROI: (0.0000, 0.0000, 1.0000, 1.0000)")
        ttk.Label(frame, textvariable=self.status_var).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))

        frame.columnconfigure(1, weight=1)

    def _on_slider_change(self, key: str) -> None:
        if self._coord_entry_has_focus(key):
            return
        self.coord_entry_vars[key].set(f"{self.coord_vars[key].get():.4f}")

    def _on_coord_entry_commit(self, key: str) -> None:
        raw = self.coord_entry_vars[key].get().strip()
        try:
            value = float(raw)
        except ValueError:
            self.coord_entry_vars[key].set(f"{self.coord_vars[key].get():.4f}")
            return
        value = _clamp(value, 0.0, 1.0)
        self.coord_vars[key].set(value)
        self.coord_entry_vars[key].set(f"{value:.4f}")

    def _on_zoom_slider_change(self, _value: str) -> None:
        if self._zoom_entry_has_focus():
            return
        self.zoom_entry_var.set(str(int(round(self.zoom_var.get()))))

    def _on_zoom_entry_commit(self, _event) -> None:
        raw = self.zoom_entry_var.get().strip()
        try:
            value = float(raw)
        except ValueError:
            self.zoom_entry_var.set(str(int(round(self.zoom_var.get()))))
            return
        value = _clamp(value, 25.0, 1600.0)
        self.zoom_var.set(value)
        self.zoom_entry_var.set(str(int(round(value))))

    def _coord_entry_has_focus(self, key: str) -> bool:
        widget = self.coord_entries.get(key)
        return widget is not None and self.root.focus_get() is widget

    def _zoom_entry_has_focus(self) -> bool:
        return self.zoom_entry is not None and self.root.focus_get() is self.zoom_entry

    def _sanitize_roi(self, *, sync_entries: bool) -> Tuple[float, float, float, float]:
        x1 = _clamp(self.coord_vars["x1"].get(), 0.0, 1.0)
        y1 = _clamp(self.coord_vars["y1"].get(), 0.0, 1.0)
        x2 = _clamp(self.coord_vars["x2"].get(), 0.0, 1.0)
        y2 = _clamp(self.coord_vars["y2"].get(), 0.0, 1.0)

        if x2 <= x1:
            x2 = min(1.0, x1 + 0.001)
            if x2 <= x1:
                x1 = max(0.0, x2 - 0.001)
        if y2 <= y1:
            y2 = min(1.0, y1 + 0.001)
            if y2 <= y1:
                y1 = max(0.0, y2 - 0.001)

        fixed = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
        for key, value in fixed.items():
            if abs(self.coord_vars[key].get() - value) > 1e-9:
                self.coord_vars[key].set(value)
            if sync_entries and (not self._coord_entry_has_focus(key)):
                self.coord_entry_vars[key].set(f"{value:.4f}")

        return (x1, y1, x2, y2)

    def _copy_roi(self) -> None:
        roi = self._sanitize_roi(sync_entries=True)
        text = f"({roi[0]:.4f}, {roi[1]:.4f}, {roi[2]:.4f}, {roi[3]:.4f})"
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set(f"Copied ROI: {text}")

    def _tick(self) -> None:
        if self.closed:
            return

        bundle = self.frames.get_latest()
        if bundle is not None:
            frame = bundle.normalized(self.width, self.height, allow_upscale=True)
            roi = self._sanitize_roi(sync_entries=False)
            h, w = frame.shape[:2]

            x1_px = int(roi[0] * w)
            y1_px = int(roi[1] * h)
            x2_px = int(roi[2] * w)
            y2_px = int(roi[3] * h)
            roi_w = max(0, x2_px - x1_px)
            roi_h = max(0, y2_px - y1_px)

            vis = frame.copy()
            cv2.rectangle(vis, (x1_px, y1_px), (max(x1_px, x2_px - 1), max(y1_px, y2_px - 1)), (0, 255, 255), 2)
            vis = draw_status_list(
                vis,
                [
                    (f"ROI: ({roi[0]:.4f}, {roi[1]:.4f}, {roi[2]:.4f}, {roi[3]:.4f})", (0, 255, 255)),
                    (f"Pixels: ({x1_px}, {y1_px}) -> ({x2_px}, {y2_px}) | {roi_w}x{roi_h}", (0, 255, 255)),
                    ("Keys: Q / ESC to quit, Copy button for tuple", (180, 180, 180)),
                ],
                x=8,
                y=22,
                copy=False,
            )
            cv2.imshow(WINDOW_FULL, vis)

            roi_crop = crop_relative(frame, roi)
            zoom_factor = max(0.25, self.zoom_var.get() / 100.0)
            interp = cv2.INTER_NEAREST if zoom_factor >= 1.0 else cv2.INTER_AREA
            if roi_crop.size > 0:
                src_h, src_w = roi_crop.shape[:2]
                dst_w = max(1, int(round(src_w * zoom_factor)))
                dst_h = max(1, int(round(src_h * zoom_factor)))
                roi_vis = cv2.resize(
                    roi_crop,
                    (dst_w, dst_h),
                    interpolation=interp,
                )
            else:
                blank = max(1, int(round(48 * zoom_factor)))
                roi_vis = frame[0:1, 0:1].copy()
                roi_vis[:] = (0, 0, 0)
                roi_vis = cv2.resize(roi_vis, (blank, blank), interpolation=cv2.INTER_NEAREST)
            roi_h, roi_w = roi_vis.shape[:2]
            roi_win_size = (roi_w, roi_h)
            now = time.perf_counter()
            if roi_win_size != self._last_roi_window_size and (now - self._last_roi_resize_at) >= 0.15:
                cv2.resizeWindow(WINDOW_ROI, roi_win_size[0], roi_win_size[1])
                self._last_roi_window_size = roi_win_size
                self._last_roi_resize_at = now
            cv2.imshow(WINDOW_ROI, roi_vis)

            roi_text = f"ROI: ({roi[0]:.4f}, {roi[1]:.4f}, {roi[2]:.4f}, {roi[3]:.4f})"
            self.status_var.set(roi_text)

        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord("q"), ord("Q")):
            self.close()
            return

        self.root.after(33, self._tick)

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        try:
            self.frames.stop()
        finally:
            self.cap.close()
            cv2.destroyAllWindows()
            try:
                self.root.quit()
                self.root.destroy()
            except Exception:
                pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive ROI tuner for Wizard101 capture.")
    parser.add_argument("--width", type=int, default=1280, help="Reference width for normalized capture.")
    parser.add_argument("--height", type=int, default=720, help="Reference height for normalized capture.")
    parser.add_argument("--x1", type=float, default=0.0, help="Initial ROI x1 (0..1).")
    parser.add_argument("--y1", type=float, default=0.0, help="Initial ROI y1 (0..1).")
    parser.add_argument("--x2", type=float, default=1.0, help="Initial ROI x2 (0..1).")
    parser.add_argument("--y2", type=float, default=1.0, help="Initial ROI y2 (0..1).")
    parser.add_argument("--zoom", type=int, default=300, help="Initial ROI preview zoom percent.")
    parser.add_argument("--fps", type=int, default=60, help="Capture FPS for Wizard101Capture.")
    parser.add_argument("--hz", type=int, default=60, help="Background frame poll rate.")
    args = parser.parse_args()

    ROITunerApp(
        width=args.width,
        height=args.height,
        x1=args.x1,
        y1=args.y1,
        x2=args.x2,
        y2=args.y2,
        zoom_percent=args.zoom,
        fps=args.fps,
        hz=args.hz,
    )


if __name__ == "__main__":
    main()
