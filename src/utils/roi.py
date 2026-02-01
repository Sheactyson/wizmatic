from __future__ import annotations
from typing import Optional, Tuple
import cv2
import numpy as np


def crop_relative(frame_bgr: np.ndarray, rel_roi: Tuple[float, float, float, float]) -> np.ndarray:
    """
    rel_roi = (x1, y1, x2, y2) in 0..1 relative coordinates.
    Returns a view into frame_bgr (no copy) when possible.
    """
    h, w = frame_bgr.shape[:2]
    x1 = int(rel_roi[0] * w)
    y1 = int(rel_roi[1] * h)
    x2 = int(rel_roi[2] * w)
    y2 = int(rel_roi[3] * h)

    x1 = max(0, min(x1, w))
    x2 = max(0, min(x2, w))
    y1 = max(0, min(y1, h))
    y2 = max(0, min(y2, h))

    if x2 <= x1 or y2 <= y1:
        return frame_bgr[0:0, 0:0]

    return frame_bgr[y1:y2, x1:x2]


def draw_relative_roi(
    frame_bgr: np.ndarray,
    rel_roi: Tuple[float, float, float, float],
    label: Optional[str] = None,
    *,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2,
    copy: bool = True,
) -> np.ndarray:
    """
    Draw a relative ROI on the frame. Returns the drawn image.
    If copy=False, draws in-place and returns the same array.
    """
    vis = frame_bgr.copy() if copy else frame_bgr
    h, w = vis.shape[:2]
    x1 = int(rel_roi[0] * w)
    y1 = int(rel_roi[1] * h)
    x2 = int(rel_roi[2] * w)
    y2 = int(rel_roi[3] * h)

    cv2.rectangle(vis, (x1, y1), (x2, y2), color, thickness)
    if label:
        cv2.putText(
            vis,
            label,
            (x1, max(0, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2,
        )
    return vis
