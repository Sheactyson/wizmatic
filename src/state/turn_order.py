from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import cv2
import numpy as np

from utils.roi import crop_relative, draw_relative_roi
from state.game_state import TurnOrderSlot, TurnOrderState


@dataclass
class TurnOrderConfig:
    # Tune rel_roi for your resolution (x1, y1, x2, y2) in relative coords.
    rel_roi: Tuple[float, float, float, float] = (0.25, 0.03, 0.75, 0.15)
    slots: int = 8
    slot_gap_rel: float = 0.01
    active_border_frac: float = 0.18
    min_active_delta: float = 6.0


def _slot_rel_rois(cfg: TurnOrderConfig) -> List[Tuple[float, float, float, float]]:
    x1, y1, x2, y2 = cfg.rel_roi
    if cfg.slots <= 0:
        return []
    roi_w = x2 - x1
    gap = cfg.slot_gap_rel
    total_gap = gap * (cfg.slots - 1)
    if roi_w <= total_gap:
        return []

    slot_w = (roi_w - total_gap) / cfg.slots
    rois = []
    for i in range(cfg.slots):
        sx1 = x1 + i * (slot_w + gap)
        sx2 = sx1 + slot_w
        rois.append((sx1, y1, sx2, y2))
    return rois


def _active_score(slot_bgr: np.ndarray, border_frac: float) -> float:
    gray = cv2.cvtColor(slot_bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]
    border = max(1, int(min(h, w) * border_frac))
    if h <= 2 * border or w <= 2 * border:
        return float(gray.mean())

    inner = gray[border:-border, border:-border]
    outer_mean = float(gray.mean())
    inner_mean = float(inner.mean())
    return outer_mean - inner_mean


def extract_turn_order(
    frame_bgr: np.ndarray,
    cfg: TurnOrderConfig,
    *,
    timestamp: Optional[float] = None,
) -> TurnOrderState:
    state = TurnOrderState(detected=False, rel_roi=cfg.rel_roi, timestamp=timestamp)
    if frame_bgr is None:
        return state

    roi_bgr = crop_relative(frame_bgr, cfg.rel_roi)
    if roi_bgr.size == 0:
        return state

    slot_rois = _slot_rel_rois(cfg)
    if not slot_rois:
        return state

    slots: List[TurnOrderSlot] = []
    scores: List[Optional[float]] = []

    for i, slot_rel in enumerate(slot_rois):
        slot_bgr = crop_relative(frame_bgr, slot_rel)
        if slot_bgr.size == 0:
            slots.append(TurnOrderSlot(index=i, rel_roi=slot_rel))
            scores.append(None)
            continue

        score = _active_score(slot_bgr, cfg.active_border_frac)
        slots.append(TurnOrderSlot(index=i, rel_roi=slot_rel, active_score=score))
        scores.append(score)

    valid_scores = [(i, s) for i, s in enumerate(scores) if s is not None]
    if valid_scores:
        sorted_scores = sorted(valid_scores, key=lambda x: x[1], reverse=True)
        best_i, best_s = sorted_scores[0]
        second_s = sorted_scores[1][1] if len(sorted_scores) > 1 else None
        delta = best_s - second_s if second_s is not None else best_s

        if delta >= cfg.min_active_delta:
            for i, _ in valid_scores:
                slots[i].is_active = (i == best_i)
            state.active_index = best_i
            state.active_confidence = float(delta)

    state.slots = slots
    state.detected = True
    return state


def render_turn_order_overlay(
    frame_bgr: np.ndarray,
    state: TurnOrderState,
    cfg: TurnOrderConfig,
) -> np.ndarray:
    vis = frame_bgr.copy()
    if state.rel_roi:
        draw_relative_roi(vis, state.rel_roi, "turn_order", color=(0, 255, 255), copy=False)

    for slot in state.slots:
        label = f"{slot.index}"
        color = (255, 0, 0)
        if slot.is_active:
            label = f"{label}*"
            color = (0, 255, 0)
        draw_relative_roi(vis, slot.rel_roi, label, color=color, copy=False)

    return vis
