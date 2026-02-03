from __future__ import annotations
from typing import List, Optional, Tuple
import cv2
import numpy as np


def _rects_intersect(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> bool:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return (ax1 < bx2) and (ax2 > bx1) and (ay1 < by2) and (ay2 > by1)


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
    avoid_rois: Optional[List[Tuple[float, float, float, float]]] = None,
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

    x1 = max(0, min(x1, w))
    x2 = max(0, min(x2, w))
    y1 = max(0, min(y1, h))
    y2 = max(0, min(y2, h))

    if x2 <= x1 or y2 <= y1:
        return vis

    restore_boxes: List[Tuple[int, int, int, int]] = [(x1, y1, x2, y2)]
    if avoid_rois:
        for aroi in avoid_rois:
            ax1 = int(aroi[0] * w)
            ay1 = int(aroi[1] * h)
            ax2 = int(aroi[2] * w)
            ay2 = int(aroi[3] * h)
            ax1 = max(0, min(ax1, w))
            ax2 = max(0, min(ax2, w))
            ay1 = max(0, min(ay1, h))
            ay2 = max(0, min(ay2, h))
            if ax2 <= ax1 or ay2 <= ay1:
                continue
            box = (ax1, ay1, ax2, ay2)
            if box not in restore_boxes:
                restore_boxes.append(box)

    restore_copies = None
    if not copy:
        restore_copies = [vis[ry1:ry2, rx1:rx2].copy() for rx1, ry1, rx2, ry2 in restore_boxes]

    x2_in = max(x1, x2 - 1)
    y2_in = max(y1, y2 - 1)
    x1_draw = max(0, x1 - thickness)
    y1_draw = max(0, y1 - thickness)
    x2_draw = min(w - 1, x2_in + thickness)
    y2_draw = min(h - 1, y2_in + thickness)

    cv2.rectangle(vis, (x1_draw, y1_draw), (x2_draw, y2_draw), color, thickness)
    if label:
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
        margin = 4
        avoid_rects = list(restore_boxes)

        candidates = [
            (x1, y1 - th - margin),
            (x2 - tw, y1 - th - margin),
            (x1, y2 + margin),
            (x2 - tw, y2 + margin),
            (x2 + margin, y1),
            (x2 + margin, y2 - th),
            (x1 - tw - margin, y1),
            (x1 - tw - margin, y2 - th),
        ]

        def _pick_label_pos(rects: List[Tuple[int, int, int, int]]) -> Optional[Tuple[int, int]]:
            for tx, ty in candidates:
                if tx < 0 or ty < 0:
                    continue
                if (tx + tw) > w or (ty + th) > h:
                    continue
                label_rect = (tx, ty, tx + tw, ty + th)
                if any(_rects_intersect(label_rect, r) for r in rects):
                    continue
                return (tx, ty)
            return None

        pos = _pick_label_pos(avoid_rects)
        if pos is None:
            pos = _pick_label_pos(avoid_rects[:1])
        if pos is not None:
            tx, ty = pos
            cv2.putText(
                vis,
                label,
                (tx, ty + th),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                color,
                2,
            )

    if copy:
        for rx1, ry1, rx2, ry2 in restore_boxes:
            vis[ry1:ry2, rx1:rx2] = frame_bgr[ry1:ry2, rx1:rx2]
    elif restore_copies is not None:
        for (rx1, ry1, rx2, ry2), patch in zip(restore_boxes, restore_copies):
            vis[ry1:ry2, rx1:rx2] = patch
    return vis
