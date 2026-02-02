from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple, List
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
    templates_base_dir: str = "src/assets/initiative"
    template_min_score: float = 0.05
    template_min_delta: float = 0.02


def _roi_from_center(center: Tuple[float, float], size: Tuple[float, float]) -> Tuple[float, float, float, float]:
    cx, cy = center
    w, h = size
    x1 = max(0.0, cx - w / 2.0)
    y1 = max(0.0, cy - h / 2.0)
    x2 = min(1.0, cx + w / 2.0)
    y2 = min(1.0, cy + h / 2.0)
    return (x1, y1, x2, y2)


def _aspect_bucket(aspect: float) -> str:
    # Buckets: 4:3, 16:9, 43:18 (ultrawide)
    targets = {
        "4:3": 4.0 / 3.0,
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


_INITIATIVE_TEMPLATE_CACHE: Dict[str, List[np.ndarray]] = {}


def _template_suffixes_for_aspect(aspect_key: str) -> Tuple[str, ...]:
    if aspect_key == "4:3":
        return ("_4x3",)
    if aspect_key == "16:9":
        return ("_16x9",)
    if aspect_key == "43:18":
        return ("_43x18",)
    return ("_16x9",)


def _load_templates(base_dir: Path, side: str, state: str, aspect_key: str) -> List[np.ndarray]:
    candidates: List[Path] = []
    side_dir = base_dir / side / state
    if side_dir.exists():
        candidates.extend(sorted(side_dir.glob("*.png")))
    if not candidates:
        generic_dir = base_dir / state
        if generic_dir.exists():
            candidates.extend(sorted(generic_dir.glob("*.png")))
    key = f"{base_dir.resolve()}::{side}::{state}::{aspect_key}"
    if key in _INITIATIVE_TEMPLATE_CACHE:
        return _INITIATIVE_TEMPLATE_CACHE[key]
    templates: List[np.ndarray] = []
    suffixes = _template_suffixes_for_aspect(aspect_key)
    for p in candidates:
        stem = p.stem.strip().lower()
        if suffixes and not any(stem.endswith(suf) for suf in suffixes):
            continue
        img = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        templates.append(img)
    if not templates:
        # Fall back to any templates if none matched the aspect suffix.
        for p in candidates:
            img = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            templates.append(img)
    _INITIATIVE_TEMPLATE_CACHE[key] = templates
    return templates


def _best_template_score(roi_gray: np.ndarray, templates: List[np.ndarray]) -> float:
    if roi_gray.size == 0 or not templates:
        return 0.0
    best = -1.0
    rh, rw = roi_gray.shape[:2]
    for templ in templates:
        th, tw = templ.shape[:2]
        if tw > rw or th > rh:
            continue
        res = cv2.matchTemplate(roi_gray, templ, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        if max_val > best:
            best = float(max_val)
    return max(best, 0.0)


def _template_ring_score(
    frame_bgr: np.ndarray,
    roi: Tuple[float, float, float, float],
    *,
    base_dir: Path,
    side: str,
    aspect_key: str,
) -> Tuple[float, float]:
    roi_bgr = crop_relative(frame_bgr, roi)
    if roi_bgr.size == 0:
        return (0.0, 0.0)
    roi_gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
    on_templates = _load_templates(base_dir, side, "on", aspect_key)
    off_templates = _load_templates(base_dir, side, "off", aspect_key)
    on_score = _best_template_score(roi_gray, on_templates)
    off_score = _best_template_score(roi_gray, off_templates)
    return (on_score, off_score)


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

    base_dir = Path(cfg.templates_base_dir)
    sun_on, sun_off = _template_ring_score(
        frame_bgr,
        sun_roi,
        base_dir=base_dir,
        side="sun",
        aspect_key=bucket,
    )
    dagger_on, dagger_off = _template_ring_score(
        frame_bgr,
        dagger_roi,
        base_dir=base_dir,
        side="dagger",
        aspect_key=bucket,
    )
    sun_score = sun_on - sun_off
    dagger_score = dagger_on - dagger_off
    state.method = "template"
    state.sun_off_score = sun_off
    state.dagger_off_score = dagger_off
    min_score = cfg.template_min_score
    min_delta = cfg.template_min_delta

    state.sun_score = sun_score
    state.dagger_score = dagger_score
    state.profile = bucket

    delta = abs(sun_score - dagger_score)
    if delta >= min_delta and max(sun_score, dagger_score) >= min_score:
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

    method_tag = state.method or "white"
    label = (
        f"initiative: {state.side or 'unknown'} | "
        f"sun={state.sun_score:.3f} "
        f"dagger={state.dagger_score:.3f} "
        f"profile={state.profile or 'n/a'} "
        f"{method_tag}"
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
