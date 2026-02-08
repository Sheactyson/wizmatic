from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np
import threading

from state.game_state import PlayerHandState
from utils.roi import crop_relative, draw_relative_roi


@dataclass(frozen=True)
class CardCountProfile:
    slot_rel_roi: Tuple[float, float, float, float]
    centers_by_count: Dict[int, Tuple[int, int]]


@dataclass(frozen=True)
class CardCountConfig:
    profiles: Dict[str, CardCountProfile]
    templates_base_dir: str = "src/assets/player_hand/card_count_slot"
    template_threshold: float = 0.72
    center_match_max_dist_px: float = 90.0


_TEMPLATE_CACHE: Dict[str, List[Tuple[str, np.ndarray]]] = {}
_CARD_COUNT_LOG_QUEUE: List[str] = []
_CARD_COUNT_LOG_LOCK = threading.Lock()
_KNOWN_ASPECT_TAGS = ("4x3", "16x9", "43x18")


def pop_card_count_logs() -> List[str]:
    with _CARD_COUNT_LOG_LOCK:
        if not _CARD_COUNT_LOG_QUEUE:
            return []
        logs = list(_CARD_COUNT_LOG_QUEUE)
        _CARD_COUNT_LOG_QUEUE.clear()
    return logs


def _push_card_count_log(line: str) -> None:
    with _CARD_COUNT_LOG_LOCK:
        _CARD_COUNT_LOG_QUEUE.append(line)


def _template_key(base_dir: Path, aspect_key: str) -> str:
    return f"{str(base_dir).lower()}::{aspect_key}"


def _stem_aspect_tag(stem: str) -> Optional[str]:
    s = stem.lower()
    for tag in _KNOWN_ASPECT_TAGS:
        if tag in s:
            return tag
    return None


def _load_templates(base_dir: Path, aspect_key: str) -> List[Tuple[str, np.ndarray]]:
    key = _template_key(base_dir, aspect_key)
    if key in _TEMPLATE_CACHE:
        return _TEMPLATE_CACHE[key]

    tag = aspect_key.replace(":", "x").lower()
    candidates: List[Path] = []

    aspect_dir = base_dir / tag
    if aspect_dir.exists():
        candidates.extend(sorted(aspect_dir.glob("*.png")))

    # Flat layout support, strict by aspect:
    # only include files explicitly tagged for the active aspect.
    for path in sorted(base_dir.glob("*.png")):
        stem_tag = _stem_aspect_tag(path.stem)
        if stem_tag == tag:
            candidates.append(path)

    candidates.extend(
        [
            base_dir / f"card_count_slot_{tag}.png",
        ]
    )

    bank: List[Tuple[str, np.ndarray]] = []
    seen: set[str] = set()
    for path in candidates:
        if not path.exists():
            continue
        key_path = str(path.resolve()).lower()
        if key_path in seen:
            continue
        seen.add(key_path)
        img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if img is None or img.size == 0:
            continue
        bank.append((path.stem, img))

    _TEMPLATE_CACHE[key] = bank
    return bank


def _nearest_count_from_center(
    center_px: Tuple[int, int],
    centers_by_count: Dict[int, Tuple[int, int]],
    *,
    max_dist_px: float,
) -> Optional[int]:
    if not centers_by_count:
        return None
    best_count = None
    best_dist = 1e9
    cx, cy = center_px
    for count, ref in centers_by_count.items():
        rx, ry = ref
        dist = float(((cx - rx) ** 2 + (cy - ry) ** 2) ** 0.5)
        if dist < best_dist:
            best_dist = dist
            best_count = count
    if best_count is None:
        return None
    if max_dist_px > 0 and best_dist > max_dist_px:
        # Card-count slot movement is primarily horizontal; allow a strict x-only
        # fallback so tiny vertical drift does not force "unknown".
        x_best_count = None
        x_best_dist = 1e9
        for count, ref in centers_by_count.items():
            rx, _ = ref
            dx = float(abs(cx - rx))
            if dx < x_best_dist:
                x_best_dist = dx
                x_best_count = count
        if x_best_count is None:
            return None
        if x_best_dist > max_dist_px:
            return None
        return int(x_best_count)
    return int(best_count)


def extract_player_hand_state(
    frame_bgr: np.ndarray,
    cfg: CardCountConfig,
    *,
    aspect_key: str,
    timestamp: Optional[float] = None,
    debug_dump_roi: bool = False,
) -> PlayerHandState:
    profile = cfg.profiles.get(aspect_key) or cfg.profiles.get("16:9")
    if frame_bgr is None or frame_bgr.size == 0 or profile is None:
        return PlayerHandState(profile=aspect_key, slot_roi=(profile.slot_rel_roi if profile is not None else None), timestamp=timestamp)

    h, w = frame_bgr.shape[:2]
    roi = profile.slot_rel_roi
    roi_crop = crop_relative(frame_bgr, roi)
    roi_gray = cv2.cvtColor(roi_crop, cv2.COLOR_BGR2GRAY) if roi_crop.size > 0 else None

    best_score = -1.0
    best_loc: Optional[Tuple[int, int]] = None
    best_size: Optional[Tuple[int, int]] = None

    templates = _load_templates(Path(cfg.templates_base_dir), aspect_key)
    if roi_gray is not None and roi_gray.size > 0:
        rh, rw = roi_gray.shape[:2]
        for _name, templ in templates:
            th, tw = templ.shape[:2]
            if tw > rw or th > rh:
                continue
            res = cv2.matchTemplate(roi_gray, templ, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            score = float(max_val)
            if score > best_score:
                best_score = score
                best_loc = max_loc
                best_size = (tw, th)

    detected = bool(best_loc is not None and best_size is not None and best_score >= cfg.template_threshold)
    center_px: Optional[Tuple[int, int]] = None
    center_rel: Optional[Tuple[float, float]] = None
    cards_in_hand: Optional[int] = None

    x1_px = int(roi[0] * w)
    y1_px = int(roi[1] * h)

    if detected and best_loc is not None and best_size is not None:
        tw, th = best_size
        mx, my = best_loc
        cx = x1_px + mx + (tw // 2)
        cy = y1_px + my + (th // 2)
        cx = max(0, min(cx, w - 1))
        cy = max(0, min(cy, h - 1))
        center_px = (cx, cy)
        center_rel = (cx / float(w), cy / float(h))
        cards_in_hand = _nearest_count_from_center(
            center_px,
            profile.centers_by_count,
            max_dist_px=cfg.center_match_max_dist_px,
        )
        cards_text = "unknown" if cards_in_hand is None else str(cards_in_hand)
        _push_card_count_log(
            f"[card count slot detected] Center: ({cx}, {cy}) Cards: {cards_text}"
        )

    if debug_dump_roi and roi_crop is not None and roi_crop.size > 0:
        try:
            dump_dir = Path("debug/player_hand")
            dump_dir.mkdir(parents=True, exist_ok=True)
            tag = aspect_key.replace(":", "x")
            raw_path = dump_dir / f"card_count_slot_roi_{tag}.png"
            vis_path = dump_dir / f"card_count_slot_roi_{tag}_vis.png"
            cv2.imwrite(str(raw_path), roi_crop)
            vis = roi_crop.copy()
            if detected and center_px is not None:
                local_cx = center_px[0] - x1_px
                local_cy = center_px[1] - y1_px
                cv2.circle(vis, (local_cx, local_cy), 4, (0, 255, 255), -1)
            cv2.imwrite(str(vis_path), vis)
        except Exception:
            pass

    return PlayerHandState(
        detected=detected,
        cards_in_hand=cards_in_hand,
        slot_score=max(0.0, best_score),
        slot_center_px=center_px,
        slot_center_rel=center_rel,
        slot_roi=roi,
        profile=aspect_key,
        timestamp=timestamp,
    )


def render_player_hand_overlay(
    frame_bgr: np.ndarray,
    hand: Optional[PlayerHandState],
) -> np.ndarray:
    vis = frame_bgr.copy()
    if vis.size == 0:
        return vis

    h, w = vis.shape[:2]
    roi = hand.slot_roi if hand is not None else None
    if roi is not None:
        draw_relative_roi(vis, roi, None, color=(0, 255, 255), thickness=2, copy=False)

    if hand is not None and hand.slot_center_px is not None:
        cx, cy = hand.slot_center_px
        cx = max(0, min(cx, w - 1))
        cy = max(0, min(cy, h - 1))
        cv2.circle(vis, (cx, cy), 4, (0, 255, 255), -1)
        roi_bottom_px = cy
        if roi is not None:
            roi_bottom_px = int(roi[3] * h)
        line_bottom = min(h - 2, max(cy + 40, roi_bottom_px + 36, int(h * 0.74)))
        cv2.line(vis, (cx, cy), (cx, line_bottom), (0, 255, 255), 1, cv2.LINE_AA)
        coord_text = f"Center (x1,y1): ({cx},{cy})"
        coord_y = min(h - 6, max(line_bottom + 20, int(h * 0.80)))
        cv2.putText(vis, coord_text, (max(4, cx - 70), coord_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(vis, coord_text, (max(4, cx - 70), coord_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1, cv2.LINE_AA)

    count_text = "Cards In Hand: Unknown"
    if hand is not None and hand.cards_in_hand is not None:
        count_text = f"Cards In Hand: {hand.cards_in_hand}"
    label_y = max(18, min(h - 8, int(h * 0.5)))
    cv2.putText(vis, count_text, (8, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(vis, count_text, (8, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 255, 255), 1, cv2.LINE_AA)

    aspect_text = f"Aspect Ratio: {(hand.profile if (hand is not None and hand.profile) else 'Unknown')}"
    aspect_y = min(h - 8, label_y + 22)
    cv2.putText(vis, aspect_text, (8, aspect_y), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(vis, aspect_text, (8, aspect_y), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 255), 1, cv2.LINE_AA)

    return vis
