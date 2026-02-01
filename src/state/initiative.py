from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import cv2
import numpy as np

from utils.roi import crop_relative, draw_relative_roi
from state.game_state import InitiativeState


@dataclass
class RingProfile:
    sun_center: Tuple[float, float]
    dagger_center: Tuple[float, float]
    sun_box_size: Tuple[float, float]
    dagger_box_size: Tuple[float, float]


@dataclass
class InitiativeConfig:
    # Profiles keyed by aspect ratio bucket.
    profiles: Dict[str, RingProfile]
    min_score: float = 0.02
    min_delta: float = 0.01
    white_sat_max: int = 60
    white_val_min: int = 200


def _roi_from_center(center: Tuple[float, float], size: Tuple[float, float]) -> Tuple[float, float, float, float]:
    cx, cy = center
    w, h = size
    x1 = max(0.0, cx - w / 2.0)
    y1 = max(0.0, cy - h / 2.0)
    x2 = min(1.0, cx + w / 2.0)
    y2 = min(1.0, cy + h / 2.0)
    return (x1, y1, x2, y2)


def _aspect_bucket(aspect: float) -> str:
    # Buckets: 4:3, 16:10, 16:9, 43:18 (ultrawide)
    targets = {
        "4:3": 4.0 / 3.0,
        "16:10": 16.0 / 10.0,
        "16:9": 16.0 / 9.0,
        "43:18": 43.0 / 18.0,
    }
    best_key = "16:9"
    best_diff = 999.0
    for key, val in targets.items():
        diff = abs(aspect - val)
        if diff < best_diff:
            best_diff = diff
            best_key = key
    return best_key


def _white_ratio(bgr: np.ndarray, sat_max: int, val_min: int) -> float:
    if bgr.size == 0:
        return 0.0
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]
    mask = (sat <= sat_max) & (val >= val_min)
    return float(mask.mean())


def extract_initiative(
    frame_bgr: np.ndarray,
    cfg: InitiativeConfig,
    *,
    timestamp: Optional[float] = None,
) -> InitiativeState:
    state = InitiativeState()
    if frame_bgr is None:
        return state

    h, w = frame_bgr.shape[:2]
    if h == 0 or w == 0:
        return state

    aspect = w / h
    bucket = _aspect_bucket(aspect)
    profile = cfg.profiles.get(bucket)
    if profile is None:
        return state

    sun_roi = _roi_from_center(profile.sun_center, profile.sun_box_size)
    dagger_roi = _roi_from_center(profile.dagger_center, profile.dagger_box_size)

    sun_crop = crop_relative(frame_bgr, sun_roi)
    dagger_crop = crop_relative(frame_bgr, dagger_roi)

    sun_score = _white_ratio(sun_crop, cfg.white_sat_max, cfg.white_val_min)
    dagger_score = _white_ratio(dagger_crop, cfg.white_sat_max, cfg.white_val_min)

    state.sun_score = sun_score
    state.dagger_score = dagger_score
    state.profile = bucket

    delta = abs(sun_score - dagger_score)
    if delta >= cfg.min_delta and max(sun_score, dagger_score) >= cfg.min_score:
        state.side = "allies" if sun_score > dagger_score else "enemies"

    return state


def render_initiative_overlay(
    frame_bgr: np.ndarray,
    cfg: InitiativeConfig,
    state: InitiativeState,
) -> np.ndarray:
    vis = frame_bgr.copy()
    h, w = vis.shape[:2]
    if h == 0 or w == 0:
        return vis

    aspect = w / h
    bucket = _aspect_bucket(aspect)
    profile = cfg.profiles.get(bucket)
    if profile is None:
        return vis

    sun_roi = _roi_from_center(profile.sun_center, profile.sun_box_size)
    dagger_roi = _roi_from_center(profile.dagger_center, profile.dagger_box_size)

    draw_relative_roi(
        vis,
        sun_roi,
        f"sun {state.sun_score:.3f}",
        color=(0, 255, 255),
        copy=False,
    )
    draw_relative_roi(
        vis,
        dagger_roi,
        f"dagger {state.dagger_score:.3f}",
        color=(255, 255, 0),
        copy=False,
    )

    label = (
        f"initiative: {state.side or 'unknown'} | "
        f"sun={state.sun_score:.3f} "
        f"dagger={state.dagger_score:.3f} "
        f"profile={state.profile or 'n/a'}"
    )
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    pad = 6
    x, y = 10, 10
    cv2.rectangle(vis, (x - pad, y - pad), (x + tw + pad, y + th + pad), (0, 0, 0), -1)
    cv2.putText(
        vis,
        label,
        (x, y + th),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    return vis
