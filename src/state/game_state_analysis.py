import time
from dataclasses import dataclass
from typing import Optional
import numpy as np

from utils.button_detect import detect_button
from config.roi_config import BUTTON_ROI_CFG
from state.game_state import GameState, TurnOrderState, InitiativeState, ParticipantsState
from state.initiative import InitiativeConfig, extract_initiative, render_initiative_overlay
from state.participants import ParticipantsConfig, extract_participants, render_participants_overlay


@dataclass
class AnalysisResult:
    game_state: GameState
    in_card_select: bool
    pass_found: bool
    flee_found: bool
    initiative_overlay: Optional[np.ndarray] = None
    participants_overlay: Optional[np.ndarray] = None


TURN_ORDER_ALLIES_FIRST = ["sun", "eye", "star", "moon", "dagger", "key", "ruby", "spiral"]
TURN_ORDER_ENEMIES_FIRST = ["dagger", "key", "ruby", "spiral", "sun", "eye", "star", "moon"]


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
    debug_dump_ocr: bool = False,
    debug_dump_health_roi: bool = False,
    debug_dump_ocr_id: Optional[str] = None,
    debug_dump_ocr_limit: int = 0,
) -> AnalysisResult:
    was_in_card_select = game_state.battle.in_card_select
    pass_found = detect_button(
        analysis,
        "pass",
        rel_roi=BUTTON_ROI_CFG.pass_rel_roi,
        threshold=BUTTON_ROI_CFG.pass_threshold,
    )
    flee_found = detect_button(
        analysis,
        "flee",
        rel_roi=BUTTON_ROI_CFG.flee_rel_roi,
        threshold=BUTTON_ROI_CFG.flee_threshold,
    )

    in_card_select = pass_found or flee_found
    game_state.updated_at = time.time()
    game_state.battle.in_card_select = in_card_select

    initiative_overlay = None
    participants_overlay = None

    if in_card_select:
        game_state.battle.initiative = extract_initiative(
            analysis,
            initiative_cfg,
            timestamp=game_state.updated_at,
        )
        _update_turn_order_from_initiative(game_state)
        if render_initiative:
            initiative_overlay = render_initiative_overlay(
                analysis,
                initiative_cfg,
                game_state.battle.initiative,
            )
        if participants_cfg is not None:
            reuse_health = was_in_card_select and game_state.battle.participants.detected
            reuse_names = was_in_card_select and game_state.battle.participants.detected
            game_state.battle.participants = extract_participants(
                analysis,
                participants_cfg,
                previous=game_state.battle.participants if (reuse_health or reuse_names) else None,
                skip_name_ocr=reuse_names,
                skip_health_ocr=reuse_health,
                timestamp=game_state.updated_at,
                debug_dump=debug_dump_ocr,
                debug_dump_health=debug_dump_health_roi,
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

    return AnalysisResult(
        game_state=game_state,
        in_card_select=in_card_select,
        pass_found=pass_found,
        flee_found=flee_found,
        initiative_overlay=initiative_overlay,
        participants_overlay=participants_overlay,
    )
