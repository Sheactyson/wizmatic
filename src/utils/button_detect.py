from __future__ import annotations
from pathlib import Path
from typing import Dict, Tuple, Optional, List
import cv2
import numpy as np

# ---------------------------------------
# Template bank cache: button -> [(name, gray_img), ...]
# ---------------------------------------
_TEMPLATE_BANK: Dict[str, List[Tuple[str, np.ndarray]]] = {}

def _load_template_bank(button: str, base_dir: Path) -> List[Tuple[str, np.ndarray]]:
    """
    Loads all PNG templates from: base_dir / button / *.png
    Caches results in-memory so it only loads once.
    """
    button = button.lower().strip()
    if button in _TEMPLATE_BANK:
        return _TEMPLATE_BANK[button]

    folder = base_dir / button
    if not folder.exists():
        raise FileNotFoundError(f"Template folder not found: {folder}")

    paths = sorted(folder.glob("*.png"))
    if not paths:
        raise FileNotFoundError(f"No .png templates found in: {folder}")

    bank: List[Tuple[str, np.ndarray]] = []
    for p in paths:
        img = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Failed to load template: {p}")
        bank.append((p.stem, img))

    _TEMPLATE_BANK[button] = bank
    return bank


def _crop_relative(frame_bgr: np.ndarray, rel_roi: Tuple[float, float, float, float]) -> np.ndarray:
    """
    rel_roi = (x1, y1, x2, y2) in 0..1 relative coordinates.
    """
    h, w = frame_bgr.shape[:2]
    x1 = int(rel_roi[0] * w); y1 = int(rel_roi[1] * h)
    x2 = int(rel_roi[2] * w); y2 = int(rel_roi[3] * h)

    x1 = max(0, min(x1, w)); x2 = max(0, min(x2, w))
    y1 = max(0, min(y1, h)); y2 = max(0, min(y2, h))

    if x2 <= x1 or y2 <= y1:
        return frame_bgr[0:0, 0:0]

    return frame_bgr[y1:y2, x1:x2]


def _draw_relative_roi(frame_bgr: np.ndarray, rel_roi: Tuple[float, float, float, float], label: str) -> np.ndarray:
    vis = frame_bgr.copy()
    h, w = vis.shape[:2]
    x1 = int(rel_roi[0] * w); y1 = int(rel_roi[1] * h)
    x2 = int(rel_roi[2] * w); y2 = int(rel_roi[3] * h)
    cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(vis, label, (x1, max(0, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
    return vis


def detect_button(
    frame_bgr: np.ndarray,
    button: str,
    *,
    templates_base_dir: Path = Path("src/assets/buttons"),
    rel_roi: Optional[Tuple[float, float, float, float]] = None,
    threshold: float = 0.78,
    debug: bool = False,
    vis: bool = False,
    debug_window_prefix: str = "wizmatic",
    print_every_frame: bool = False,
) -> bool:
    """
    Returns True if the button template bank is detected in frame_bgr, else False.

    Parameters:
      frame_bgr: normalized capture frame (BGR), e.g. bundle.normalized(1280,720,allow_upscale=True)
      button: folder name under templates_base_dir, e.g. "pass", "flee", "draw"
      templates_base_dir: directory containing subfolders per button
      rel_roi: relative ROI (x1,y1,x2,y2). If None, uses entire screen.
      threshold: matchTemplate score threshold
      debug: if True, print score info
      vis: if True, show ROI overlay
      print_every_frame: if False, prints only when debug is True AND detection state changes
                         (this function stores last state per button when debug enabled)

    Template layout expected:
      src/assets/buttons/pass/*.png
      src/assets/buttons/flee/*.png
      src/assets/buttons/draw/*.png
    """

    # Default ROI: entire screen
    if rel_roi is None:
        rel_roi = (0.0, 0.0, 1.0, 1.0)

    bank = _load_template_bank(button, templates_base_dir)

    roi_bgr = _crop_relative(frame_bgr, rel_roi)
    if roi_bgr.size == 0:
        if debug:
            print(f"[{button}] Empty ROI (rel_roi={rel_roi})")
        return False

    roi_gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)

    best_score = -1.0
    best_name = None

    rh, rw = roi_gray.shape[:2]
    for name, templ in bank:
        th, tw = templ.shape[:2]
        if tw > rw or th > rh:
            continue

        res = cv2.matchTemplate(roi_gray, templ, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        if max_val > best_score:
            best_score = float(max_val)
            best_name = name

    hit = (best_score >= threshold) if best_score >= 0 else False

    # Debug visualization + printing
    if vis:
        # Show overlay
        overlay = _draw_relative_roi(frame_bgr, rel_roi, f"{button} score={best_score:.3f} thr={threshold:.3f}")
        cv2.imshow(f"{debug_window_prefix}:overlay", overlay)

        # Print scores (either always, or only on state changes per button)
        if not hasattr(detect_button, "_last_state"):
            detect_button._last_state = {}  # type: ignore[attr-defined]

        last_state = detect_button._last_state.get(button)  # type: ignore[attr-defined]
        state_now = hit

        if print_every_frame or (last_state is None) or (state_now != last_state):
            status = "DETECTED" if hit else "not detected"
            print(f"[{button}] {status} | score={best_score:.3f} | thr={threshold:.3f} | template={best_name}")
            detect_button._last_state[button] = state_now  # type: ignore[attr-defined]

    return hit
