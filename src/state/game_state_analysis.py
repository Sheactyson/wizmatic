import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import shutil
import cv2
import numpy as np

from utils.button_detect import detect_button
from utils.roi import draw_relative_roi
from config.roi_config import BUTTON_ROI_CFG
from state.game_state import GameState, TurnOrderState, InitiativeState, ParticipantsState
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
    if analysis is None:
        pass_found = False
        flee_found = False
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
            pass_found = False
            flee_found = False
        else:
            pass_found = detect_button(
                analysis,
                "pass",
                rel_roi=button_profile.pass_rel_roi,
                threshold=BUTTON_ROI_CFG.pass_threshold,
            )
            flee_found = detect_button(
                analysis,
                "flee",
                rel_roi=button_profile.flee_rel_roi,
                threshold=BUTTON_ROI_CFG.flee_threshold,
            )

    in_card_select = pass_found or flee_found
    game_state.updated_at = time.time()
    game_state.battle.in_card_select = in_card_select

    initiative_overlay = None
    participants_overlay = None
    button_overlay = None

    if render_button_overlay and button_profile is not None and analysis is not None:
        button_overlay = analysis.copy()
        pass_color = (0, 255, 0) if pass_found else (0, 0, 255)
        flee_color = (0, 255, 0) if flee_found else (0, 0, 255)
        pass_label = f"pass {'DETECTED' if pass_found else 'not detected'}"
        flee_label = f"flee {'DETECTED' if flee_found else 'not detected'}"
        aspect_label = f"button profile: {aspect_key}"
        (tw, th), _ = cv2.getTextSize(aspect_label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        pad = 6
        x, y = 10, 10
        cv2.rectangle(
            button_overlay,
            (x - pad, y - pad),
            (x + tw + pad, y + th + pad),
            (0, 0, 0),
            -1,
        )
        cv2.putText(
            button_overlay,
            aspect_label,
            (x, y + th),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )
        draw_relative_roi(
            button_overlay,
            button_profile.pass_rel_roi,
            pass_label,
            color=pass_color,
            copy=False,
            avoid_rois=[button_profile.flee_rel_roi],
        )
        draw_relative_roi(
            button_overlay,
            button_profile.flee_rel_roi,
            flee_label,
            color=flee_color,
            copy=False,
            avoid_rois=[button_profile.pass_rel_roi],
        )

    if in_card_select:
        if (not was_in_card_select) and (debug_dump_ocr or debug_dump_health_roi):
            _clear_ocr_dump_dir()
        if not was_in_card_select:
            game_state.battle.card_select_started_at = game_state.updated_at

        card_select_started_at = game_state.battle.card_select_started_at or game_state.updated_at

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
        game_state.battle.turn_order = TurnOrderState()
        game_state.battle.initiative = InitiativeState()
        game_state.battle.participants = ParticipantsState()
        game_state.battle.card_select_started_at = None

    return AnalysisResult(
        game_state=game_state,
        in_card_select=in_card_select,
        pass_found=pass_found,
        flee_found=flee_found,
        initiative_overlay=initiative_overlay,
        participants_overlay=participants_overlay,
        button_overlay=button_overlay,
    )
