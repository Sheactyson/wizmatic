import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Dict, Sequence
import shutil
import cv2
import numpy as np

from utils.button_detect import detect_button
from utils.roi import crop_relative, draw_status_list
from config.roi_config import BUTTON_ROI_CFG
from state.game_state import GameState, BattleState
from state.initiative import InitiativeConfig, extract_initiative, render_initiative_overlay
from state.participants import ParticipantsConfig, extract_participants, render_participants_overlay
from config.wizmatic_config import (
    PARTICIPANT_OCCUPANCY_REFRESH_S,
    PARTICIPANT_DETAILS_REFRESH_S,
    INITIATIVE_CAPTURE_WINDOW_S,
    INITIATIVE_STABLE_HOLD_S,
)


@dataclass
class AnalysisResult:
    game_state: GameState
    in_card_select: bool
    pass_found: bool
    flee_found: bool
    initiative_overlay: Optional[np.ndarray] = None
    participants_overlay: Optional[np.ndarray] = None
    button_overlay: Optional[np.ndarray] = None
    button_states: Optional[Dict[str, bool]] = None


def _clear_ocr_dump_dir() -> None:
    dump_dir = Path("debug/ocr")
    if not dump_dir.exists():
        return
    for path in dump_dir.iterdir():
        try:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink()
        except Exception:
            pass


TURN_ORDER_ALLIES_FIRST = ["sun", "eye", "star", "moon", "dagger", "key", "ruby", "spiral"]
TURN_ORDER_ENEMIES_FIRST = ["dagger", "key", "ruby", "spiral", "sun", "eye", "star", "moon"]

STATE_LOADING = "loading"
STATE_IDLE = "idle"
STATE_BATTLE = "battle"
STATE_CARD_SELECT = "card_select"
STATE_ROUND_ANIMATION = "round_animation"
BATTLE_STATES = {STATE_BATTLE, STATE_CARD_SELECT, STATE_ROUND_ANIMATION}

BUTTON_ORDER = ["crownsShop", "upgradeNow", "friends", "social", "spellBook", "pass", "flee"]
BUTTON_ALL = ["pass", "flee", "crownsShop", "upgradeNow", "friends", "social", "spellBook"]
BUTTON_IDLE_TRUE = ["crownsShop", "upgradeNow", "friends", "social", "spellBook"]
BUTTON_BATTLE_TRUE = ["crownsShop", "friends"]
BUTTON_BATTLE_FALSE = ["upgradeNow", "social", "spellBook"]
BUTTON_CARD_TRUE = ["crownsShop", "friends", "pass", "flee"]
BUTTON_CARD_FALSE = ["upgradeNow", "social", "spellBook"]
BUTTON_ROUND_FALSE = ["crownsShop", "upgradeNow", "social", "spellBook", "pass", "flee"]


def _aspect_bucket(aspect: float) -> str:
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


def _count_hits(button_states: Dict[str, bool], keys: Sequence[str]) -> int:
    return sum(1 for key in keys if button_states.get(key, False))


def _all_false(button_states: Dict[str, bool], keys: Sequence[str]) -> bool:
    return all(not button_states.get(key, False) for key in keys)


def _resolve_game_state(prev_state: str, button_states: Optional[Dict[str, bool]]) -> str:
    if not button_states:
        return prev_state or STATE_IDLE

    prev_state = prev_state or STATE_IDLE
    prev_in_battle = prev_state in BATTLE_STATES

    idle_hit = _count_hits(button_states, BUTTON_IDLE_TRUE) >= 4
    loading_hit = _all_false(button_states, BUTTON_ALL)

    battle_base_hit = _count_hits(button_states, BUTTON_BATTLE_TRUE) >= 1 and _all_false(button_states, BUTTON_BATTLE_FALSE)
    battle_context = prev_in_battle or battle_base_hit

    pass_hit = button_states.get("pass", False)
    flee_hit = button_states.get("flee", False)
    pass_flee_both_false = (not pass_hit) and (not flee_hit)

    card_select_hit = (
        battle_context
        and _all_false(button_states, BUTTON_CARD_FALSE)
        and (
            _count_hits(button_states, BUTTON_CARD_TRUE) >= 3
            or (prev_state == STATE_CARD_SELECT and not pass_flee_both_false)
        )
    )
    round_animation_hit = battle_context and _all_false(button_states, BUTTON_ROUND_FALSE)

    if idle_hit:
        return STATE_IDLE
    if loading_hit and prev_state in (STATE_IDLE, STATE_LOADING):
        return STATE_LOADING
    if battle_context:
        if card_select_hit:
            return STATE_CARD_SELECT
        if round_animation_hit:
            return STATE_ROUND_ANIMATION
        return STATE_BATTLE

    return prev_state


def _update_turn_order_from_initiative(game_state: GameState) -> None:
    side = game_state.battle.initiative.side
    if side == "allies":
        game_state.battle.turn_order.order = list(TURN_ORDER_ALLIES_FIRST)
        game_state.battle.turn_order.source = "initiative"
    elif side == "enemies":
        game_state.battle.turn_order.order = list(TURN_ORDER_ENEMIES_FIRST)
        game_state.battle.turn_order.source = "initiative"
    else:
        game_state.battle.turn_order.order = []
        game_state.battle.turn_order.source = None


def analyze_game_state(
    analysis: np.ndarray,
    game_state: GameState,
    *,
    initiative_cfg: InitiativeConfig,
    participants_cfg: Optional[ParticipantsConfig] = None,
    render_initiative: bool = False,
    render_participants: bool = False,
    render_pip_detection: bool = False,
    render_button_overlay: bool = False,
    debug_dump_button_rois: bool = False,
    collect_button_state: bool = False,
    debug_dump_initiative_roi: bool = False,
    debug_dump_ocr: bool = False,
    debug_dump_health_roi: bool = False,
    debug_dump_empty_names: bool = False,
    debug_dump_sigil_roi: bool = False,
    debug_dump_school_roi: bool = False,
    debug_dump_ocr_id: Optional[str] = None,
    debug_dump_ocr_limit: int = 0,
) -> AnalysisResult:
    was_in_card_select = game_state.battle.in_card_select
    game_state.updated_at = time.time()
    if analysis is None:
        aspect_key = "16:9"
        button_profile = None
    else:
        h, w = analysis.shape[:2]
        if h > 0 and w > 0:
            aspect_key = _aspect_bucket(w / h)
        else:
            aspect_key = "16:9"
        button_profile = BUTTON_ROI_CFG.profiles.get(aspect_key) or BUTTON_ROI_CFG.profiles.get("16:9")
        if button_profile is None and BUTTON_ROI_CFG.profiles:
            button_profile = next(iter(BUTTON_ROI_CFG.profiles.values()))
        if button_profile is None:
            button_profile = None

    button_states: Optional[Dict[str, bool]] = None
    pass_found = False
    flee_found = False
    if analysis is not None and button_profile is not None:
        button_states = {}
        base_dir = BUTTON_ROI_CFG.templates_base_dir
        threshold = BUTTON_ROI_CFG.threshold
        button_rois = {
            "pass": button_profile.pass_rel_roi,
            "flee": button_profile.flee_rel_roi,
            "crownsShop": button_profile.crowns_shop_rel_roi,
            "upgradeNow": button_profile.upgrade_now_rel_roi,
            "friends": button_profile.friends_rel_roi,
            "social": button_profile.social_rel_roi,
            "spellBook": button_profile.spell_book_rel_roi,
        }
        for name, rel_roi in button_rois.items():
            try:
                hit = detect_button(
                    analysis,
                    name,
                    templates_base_dir=Path(base_dir),
                    rel_roi=rel_roi,
                    threshold=threshold,
                )
            except Exception:
                hit = False
            button_states[name] = hit
        pass_found = button_states.get("pass", False)
        flee_found = button_states.get("flee", False)

    resolved_state = _resolve_game_state(game_state.state, button_states)
    game_state.state = resolved_state
    in_battle = resolved_state in BATTLE_STATES
    in_card_select = resolved_state == STATE_CARD_SELECT
    game_state.battle.active = in_battle
    game_state.battle.in_card_select = in_card_select
    entered_card_select = in_card_select and (not was_in_card_select)

    initiative_overlay = None
    participants_overlay = None
    button_overlay = None

    if (render_button_overlay or debug_dump_button_rois) and button_profile is not None and analysis is not None and button_states is not None:
        button_overlay = analysis.copy() if render_button_overlay else None
        dump_dir = Path("debug/buttons")
        if debug_dump_button_rois:
            dump_dir.mkdir(parents=True, exist_ok=True)
        dump_every_s = 5.0
        now = time.time()

        def _draw_button_roi(
            name: str,
            rel_roi: Tuple[float, float, float, float],
            *,
            label_pos: str,
            hit: bool,
        ) -> None:
            if debug_dump_button_rois:
                last_key = f"button_dump::{name}"
                last_at = getattr(analyze_game_state, "_last_dump", {}).get(last_key, 0.0)
                allow_dump = (now - last_at) >= dump_every_s
                if allow_dump:
                    if not hasattr(analyze_game_state, "_last_dump"):
                        analyze_game_state._last_dump = {}  # type: ignore[attr-defined]
                    analyze_game_state._last_dump[last_key] = now  # type: ignore[attr-defined]
                    roi_bgr = crop_relative(analysis, rel_roi)
                    if roi_bgr.size > 0:
                        try:
                            cv2.imwrite(str(dump_dir / f"{name}_roi.png"), roi_bgr)
                        except Exception:
                            pass
            color = (0, 255, 0) if hit else (128, 128, 128)
            if button_overlay is None:
                return
            h, w = button_overlay.shape[:2]
            x1 = int(rel_roi[0] * w)
            y1 = int(rel_roi[1] * h)
            x2 = int(rel_roi[2] * w)
            y2 = int(rel_roi[3] * h)
            x1 = max(0, min(x1, w))
            x2 = max(0, min(x2, w))
            y1 = max(0, min(y1, h))
            y2 = max(0, min(y2, h))
            if x2 <= x1 or y2 <= y1:
                return
            cv2.rectangle(button_overlay, (x1, y1), (x2 - 1, y2 - 1), color, 2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.55
            thickness = 2
            (tw, th), _ = cv2.getTextSize(name, font, scale, thickness)
            margin = 4
            if label_pos == "below":
                tx = x1
                ty = y2 + margin + th
            elif label_pos == "right":
                tx = x2 + margin
                ty = y1 + th
            elif label_pos == "left":
                tx = x1 - margin - tw
                ty = y1 + th
            else:
                tx = x1
                ty = y1 - margin

            tx = max(0, min(tx, w - tw))
            ty = max(th, min(ty, h - 1))
            cv2.putText(button_overlay, name, (tx, ty), font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
            cv2.putText(button_overlay, name, (tx, ty), font, scale, color, thickness, cv2.LINE_AA)

        _draw_button_roi("pass", button_profile.pass_rel_roi, label_pos="below", hit=button_states.get("pass", False))
        _draw_button_roi("flee", button_profile.flee_rel_roi, label_pos="below", hit=button_states.get("flee", False))
        _draw_button_roi("crownsShop", button_profile.crowns_shop_rel_roi, label_pos="below", hit=button_states.get("crownsShop", False))
        _draw_button_roi("upgradeNow", button_profile.upgrade_now_rel_roi, label_pos="right", hit=button_states.get("upgradeNow", False))
        _draw_button_roi("friends", button_profile.friends_rel_roi, label_pos="left", hit=button_states.get("friends", False))
        _draw_button_roi("social", button_profile.social_rel_roi, label_pos="left", hit=button_states.get("social", False))
        _draw_button_roi("spellBook", button_profile.spell_book_rel_roi, label_pos="top", hit=button_states.get("spellBook", False))
        if button_overlay is not None:
            h, w = button_overlay.shape[:2]
            items = []
            for key in BUTTON_ORDER:
                hit = button_states.get(key, False)
                if hit:
                    items.append((key, (0, 255, 0)))
            if items:
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.45
                thickness = 1
                pad = 6
                line_h = 16
                max_width = 0
                for label, _ in items:
                    (tw, _), _ = cv2.getTextSize(label, font, font_scale, thickness)
                    if tw > max_width:
                        max_width = tw
                box_w = max_width + pad * 2
                box_h = line_h * len(items) + pad
                x = max(8, w - box_w - 8)
                y = int((h - box_h) * 0.5) + line_h - 2
                y = max(line_h, min(h - 2, y))
                draw_status_list(
                    button_overlay,
                    items,
                    x=x,
                    y=y,
                    line_h=line_h,
                    font_scale=font_scale,
                    thickness=thickness,
                    pad=pad,
                    copy=False,
                )

    if in_card_select:
        if (not was_in_card_select) and (debug_dump_ocr or debug_dump_health_roi):
            _clear_ocr_dump_dir()
        if not was_in_card_select:
            game_state.battle.card_select_started_at = game_state.updated_at

        card_select_started_at = game_state.battle.card_select_started_at or game_state.updated_at

        if not game_state.battle.initial_card_select_done:
            should_check_initiative = True
            if game_state.battle.initiative.side:
                stable_since = game_state.battle.initiative.stable_since
                stable_ok = stable_since is not None and (game_state.updated_at - stable_since) >= INITIATIVE_STABLE_HOLD_S
                within_window = (game_state.updated_at - card_select_started_at) <= INITIATIVE_CAPTURE_WINDOW_S
                should_check_initiative = (not stable_ok) or within_window

            if should_check_initiative:
                init = extract_initiative(
                    analysis,
                    initiative_cfg,
                    timestamp=game_state.updated_at,
                    debug_dump_rois=debug_dump_initiative_roi,
                )
                if init.side:
                    if init.side == game_state.battle.initiative.stable_side:
                        init.stable_side = game_state.battle.initiative.stable_side or init.side
                        init.stable_since = game_state.battle.initiative.stable_since
                    else:
                        init.stable_side = init.side
                        init.stable_since = game_state.updated_at
                else:
                    init.stable_side = None
                    init.stable_since = None
                init.last_checked_at = game_state.updated_at
                game_state.battle.initiative = init
                _update_turn_order_from_initiative(game_state)

        if render_initiative:
            initiative_overlay = render_initiative_overlay(
                analysis,
                initiative_cfg,
                game_state.battle.initiative,
            )

        if participants_cfg is not None:
            previous_participants = game_state.battle.participants if game_state.battle.participants.detected else None
            game_state.battle.participants = extract_participants(
                analysis,
                participants_cfg,
                previous=previous_participants,
                skip_name_ocr=False,
                skip_health_ocr=False,
                occupancy_refresh_s=PARTICIPANT_OCCUPANCY_REFRESH_S,
                details_refresh_s=PARTICIPANT_DETAILS_REFRESH_S,
                lock_name=True,
                lock_school=True,
                lock_health_max=True,
                force_health_refresh=entered_card_select,
                force_pips_refresh=entered_card_select,
                force_school_refresh=entered_card_select,
                refresh_health_on_force_only=True,
                refresh_pips_on_force_only=True,
                timestamp=game_state.updated_at,
                debug_dump=debug_dump_ocr,
                debug_dump_health=debug_dump_health_roi,
                debug_dump_empty_names=debug_dump_empty_names,
                debug_dump_sigil_roi=debug_dump_sigil_roi,
                debug_dump_school_roi=debug_dump_school_roi,
                debug_dump_id=debug_dump_ocr_id,
                debug_dump_limit=debug_dump_ocr_limit,
            )
            if render_participants:
                participants_overlay = render_participants_overlay(
                    analysis,
                    game_state.battle.participants,
                    show_pip_detection=render_pip_detection,
                    initiative_side=game_state.battle.initiative.side,
                )
    else:
        game_state.battle.card_select_started_at = None
        if was_in_card_select and (not game_state.battle.initial_card_select_done):
            game_state.battle.initial_card_select_done = True
        if not in_battle:
            game_state.battle = BattleState()

    return AnalysisResult(
        game_state=game_state,
        in_card_select=in_card_select,
        pass_found=pass_found,
        flee_found=flee_found,
        initiative_overlay=initiative_overlay,
        participants_overlay=participants_overlay,
        button_overlay=button_overlay,
        button_states=button_states,
    )
