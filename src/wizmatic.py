import time
import threading
from copy import deepcopy
from typing import Optional
import cv2
from utils.capture_wiz import Wizard101Capture
from utils.capture_thread import FrameSource
from state.game_state import GameState
from state.game_state_analysis import analyze_game_state
from config.initiative_config import INITIATIVE_CFG
from config.wizmatic_config import (
    DT,
    SHOW_CAPTURE,
    SHOW_INITIATIVE_OVERLAY,
    SHOW_PARTICIPANTS_OVERLAY,
    SHOW_PIPDETECTION_OVERLAY,
    SHOW_BUTTON_OVERLAY,
    SHOW_PLAYER_WIZARD_OVERLAY,
    SHOW_MASTER_DEBUG_OVERLAY,
    DEBUG_DUMP_OCR,
    DEBUG_DUMP_OCR_MAX,
    DEBUG_DUMP_HEALTH_ROI,
    DEBUG_DUMP_EMPTY_NAME_ROI,
    DEBUG_DUMP_INITIATIVE_ROI,
    DEBUG_DUMP_SIGIL_ROI,
    DEBUG_DUMP_SCHOOL_ROI,
    DEBUG_DUMP_BUTTON_ROI,
    DEBUG_DUMP_PLAYER_WIZARD_ROI,
    DEBUG_DUMP_PIP_ROI,
    DEBUG_PRINT_HEALTH_OCR,
    DEBUG_PRINT_NAME_OCR,
    DEBUG_PRINT_STATE_CHANGES,
    OCR_BACKEND,
    COMBAT_MODE,
    MASTER_OVERLAY_SHOW_PARTICIPANTS,
    MASTER_OVERLAY_SHOW_PARTICIPANT_LEGEND,
    MASTER_OVERLAY_SHOW_PARTICIPANT_DETAILS,
    MASTER_OVERLAY_HIDE_EMPTY_SLOTS,
    MASTER_OVERLAY_SHOW_INITIATIVE,
    MASTER_OVERLAY_SHOW_PIPS,
    MASTER_OVERLAY_SHOW_BUTTON_LIST,
)
from config.participants_config import PARTICIPANTS_CFG
from state.initiative import render_initiative_boxes, render_initiative_overlay
from state.participants import render_participants_overlay, render_player_wizard_overlay, pop_health_ocr_logs
_PVP_MODE = str(COMBAT_MODE).strip().lower() == "pvp"
_RETREAT_STATE_KEY = "concede" if _PVP_MODE else "flee"
_RETREAT_BUTTON_LABEL = "concede" if _PVP_MODE else "flee"

def main():
    if OCR_BACKEND == "easyocr":
        try:
            from ocr_easy.adapter import warmup
            warmup(PARTICIPANTS_CFG.ocr)
        except Exception as exc:
            print(f"[ocr] easyocr warmup failed: {exc}")
    cap = Wizard101Capture(fps=60)
    frames = FrameSource(cap, hz=60)
    frames.start()

    state_last = None
    game_state = GameState()
    analysis_seq = 0
    last_logged_seq = -1
    latest_capture_frame = None
    last_bundle_obj_id = None
    pending_task = None
    latest_packet = None
    latest_button_states = None
    latest_button_overlay = None
    task_lock = threading.Lock()
    result_lock = threading.Lock()
    task_event = threading.Event()
    stop_event = threading.Event()
    gui_ok = True
    gui_warned = False

    def _disable_gui(err: Exception) -> None:
        nonlocal gui_ok, gui_warned
        gui_ok = False
        if not gui_warned:
            print(f"[ui] OpenCV GUI disabled (headless build?): {err}")
            gui_warned = True

    def _safe_imshow(name: str, frame) -> None:
        if not gui_ok:
            return
        try:
            cv2.imshow(name, frame)
        except cv2.error as exc:
            _disable_gui(exc)

    def _safe_wait_key() -> bool:
        if not gui_ok:
            return False
        try:
            return (cv2.waitKey(1) & 0xFF) == ord("q")
        except cv2.error as exc:
            _disable_gui(exc)
            return False

    def _format_state_label(state: str) -> str:
        labels = {
            "loading": "Loading Screen",
            "idle": "Idle",
            "battle": "Battle",
            "card_select": "Card Select",
            "round_animation": "Round Animation",
        }
        return labels.get(state, state.title())

    def _draw_state_and_buttons(
        vis,
        label: str,
        button_states: Optional[dict],
        *,
        show_buttons: bool,
    ) -> None:
        h, w = vis.shape[:2]
        if h == 0 or w == 0:
            return
        font = cv2.FONT_HERSHEY_SIMPLEX
        state_scale = 0.7
        state_thickness = 2
        item_scale = 0.45
        item_thickness = 1
        pad = 6
        margin = 8
        alpha = 0.35
        gold = (0, 215, 255)
        green = (0, 255, 0)

        order = ["crownsShop", "upgradeNow", "friends", "social", "spellBook", "pass", _RETREAT_STATE_KEY]
        items = []
        if show_buttons and button_states:
            for key in order:
                if button_states.get(key, False):
                    items.append(_RETREAT_BUTTON_LABEL if key == _RETREAT_STATE_KEY else key)

        (state_w, state_h), _ = cv2.getTextSize(label, font, state_scale, state_thickness)
        max_width = state_w
        for item in items:
            (tw, _), _ = cv2.getTextSize(item, font, item_scale, item_thickness)
            if tw > max_width:
                max_width = tw

        state_line_h = state_h + 6
        if items:
            (_, item_h), _ = cv2.getTextSize("X", font, item_scale, item_thickness)
            item_line_h = item_h + 4
        else:
            item_line_h = 0

        box_w = max_width + pad * 2
        box_h = pad * 2 + state_line_h + (item_line_h * len(items))

        x1 = max(2, w - box_w - margin)
        y1 = int((h - box_h) * 0.5)
        y1 = max(2, min(h - box_h - 2, y1))
        x2 = min(w - 2, x1 + box_w)
        y2 = min(h - 2, y1 + box_h)

        overlay = vis.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 0), -1)
        cv2.addWeighted(overlay, alpha, vis, 1 - alpha, 0, vis)

        text_x = x1 + pad
        cy = y1 + pad + state_h
        cv2.putText(vis, label, (text_x, cy), font, state_scale, gold, state_thickness, cv2.LINE_AA)
        cy += state_line_h
        for item in items:
            cv2.putText(vis, item, (text_x, cy), font, item_scale, green, item_thickness, cv2.LINE_AA)
            cy += item_line_h

    def _participants_legend_bottom(h: int, w: int) -> int:
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.45
        thickness = 1
        line_h = 16
        pad = 6
        init_label = "Initiative: Unknown"
        aspect_label = "Aspect: Unknown"
        lines = [
            "Box",
            "Sigil",
            "School",
            "Name",
            "Hp",
            "Pips",
            init_label,
            aspect_label,
        ]
        x = max(8, int(w * 0.03))
        y = int(h * 0.45)
        max_width = 0
        for label in lines:
            (tw, _), _ = cv2.getTextSize(label, font, scale, thickness)
            if tw > max_width:
                max_width = tw
        box_w = max_width + pad * 2
        box_h = line_h * len(lines) + pad
        _ = box_w
        top = y - line_h + 2
        bottom = top + box_h
        return bottom

    def _analysis_worker() -> None:
        nonlocal pending_task, latest_packet
        worker_game_state = GameState()
        worker_state_last = worker_game_state.state
        worker_debug_ocr_session_id = 0

        while not stop_event.is_set():
            task_event.wait(timeout=0.05)
            if stop_event.is_set():
                break

            task = None
            with task_lock:
                if pending_task is not None:
                    task = pending_task
                    pending_task = None
                task_event.clear()
            if task is None:
                continue

            seq, analysis = task
            render_initiative = (not SHOW_MASTER_DEBUG_OVERLAY) and SHOW_INITIATIVE_OVERLAY
            render_participants = (not SHOW_MASTER_DEBUG_OVERLAY) and SHOW_PARTICIPANTS_OVERLAY
            render_player_wizard = SHOW_PLAYER_WIZARD_OVERLAY
            render_buttons = (not SHOW_MASTER_DEBUG_OVERLAY) and SHOW_BUTTON_OVERLAY
            render_pips = (not SHOW_MASTER_DEBUG_OVERLAY) and SHOW_PIPDETECTION_OVERLAY
            collect_buttons = MASTER_OVERLAY_SHOW_BUTTON_LIST
            try:
                result = analyze_game_state(
                    analysis,
                    worker_game_state,
                    initiative_cfg=INITIATIVE_CFG,
                    participants_cfg=PARTICIPANTS_CFG,
                    render_initiative=render_initiative,
                    render_participants=render_participants,
                    render_player_wizard=render_player_wizard,
                    render_pip_detection=render_pips,
                    render_button_overlay=render_buttons,
                    debug_dump_button_rois=DEBUG_DUMP_BUTTON_ROI,
                    collect_button_state=collect_buttons,
                    debug_dump_initiative_roi=DEBUG_DUMP_INITIATIVE_ROI,
                    debug_dump_ocr=DEBUG_DUMP_OCR,
                    debug_dump_health_roi=DEBUG_DUMP_HEALTH_ROI,
                    debug_dump_empty_names=DEBUG_DUMP_EMPTY_NAME_ROI,
                    debug_dump_sigil_roi=DEBUG_DUMP_SIGIL_ROI,
                    debug_dump_school_roi=DEBUG_DUMP_SCHOOL_ROI,
                    debug_dump_player_wizard_roi=DEBUG_DUMP_PLAYER_WIZARD_ROI,
                    debug_dump_pip_roi=DEBUG_DUMP_PIP_ROI,
                    debug_print_health_ocr=DEBUG_PRINT_HEALTH_OCR,
                    debug_dump_ocr_id=str(worker_debug_ocr_session_id),
                    debug_dump_ocr_limit=DEBUG_DUMP_OCR_MAX,
                )
            except Exception as exc:
                print(f"[analysis] failed: {exc}")
                continue

            state_current = result.game_state.state
            if worker_state_last != state_current and state_current == "card_select":
                worker_debug_ocr_session_id += 1
            worker_state_last = state_current

            # Keep worker-owned state separate from published snapshots.
            worker_game_state = deepcopy(result.game_state)

            with result_lock:
                latest_packet = (seq, analysis, result)

    analysis_thread = threading.Thread(target=_analysis_worker, daemon=True)
    analysis_thread.start()

    try:
        while True:
            t0 = time.perf_counter()

            bundle = frames.get_latest()
            if bundle is not None and id(bundle) != last_bundle_obj_id:
                last_bundle_obj_id = id(bundle)
                latest_capture_frame = bundle.normalized(1280, 720, allow_upscale=True)
                with task_lock:
                    analysis_seq += 1
                    pending_task = (analysis_seq, latest_capture_frame)
                task_event.set()

            packet = None
            with result_lock:
                packet = latest_packet

            packet_analysis = None
            state_current = game_state.state
            in_card_select = game_state.battle.in_card_select
            if packet is not None:
                result_seq, analysis, result = packet
                packet_analysis = analysis
                game_state = result.game_state
                if result.button_states is not None:
                    latest_button_states = result.button_states
                if result.button_overlay is not None:
                    latest_button_overlay = result.button_overlay
                state_current = game_state.state
                in_card_select = game_state.battle.in_card_select

                if result_seq != last_logged_seq:
                    last_logged_seq = result_seq
                    if state_last != state_current:
                        state_last = state_current
                        if state_current == "card_select":
                            if DEBUG_PRINT_STATE_CHANGES:
                                print("Card Select Mode")
                            if DEBUG_PRINT_NAME_OCR and game_state.battle.participants:
                                enemies = game_state.battle.participants.enemies
                                allies = game_state.battle.participants.allies
                                for p in enemies + allies:
                                    if p is None:
                                        continue
                                    if not p.name_ocr:
                                        continue
                                    raw = p.name_raw if p.name_raw else "unknown"
                                    final = p.name if p.name else "unknown"
                                    sigil_label = ((p.sigil or "unknown").strip() or "unknown").title()
                                    if p.name_time_ms is not None:
                                        if p.name_time_parts:
                                            cap_ms, prep_ms, ocr_ms, res_ms = p.name_time_parts
                                            print(
                                                f"[ocr:name] {sigil_label}: {raw} -> {final} "
                                                f"({p.name_time_ms:.1f}ms | capture {cap_ms:.1f}ms "
                                                f"prep {prep_ms:.1f}ms ocr {ocr_ms:.1f}ms "
                                                f"resolve {res_ms:.1f}ms)"
                                            )
                                        else:
                                            print(f"[ocr:name] {sigil_label}: {raw} -> {final} ({p.name_time_ms:.1f}ms)")
                                    else:
                                        print(f"[ocr:name] {sigil_label}: {raw} -> {final}")
                        else:
                            if DEBUG_PRINT_STATE_CHANGES:
                                print(f"{_format_state_label(state_current)} Mode")

            render_base = latest_capture_frame if latest_capture_frame is not None else packet_analysis
            if render_base is not None:
                if SHOW_MASTER_DEBUG_OVERLAY:
                    master = render_base.copy()
                    state_label = _format_state_label(state_current)
                    _draw_state_and_buttons(
                        master,
                        state_label,
                        latest_button_states,
                        show_buttons=MASTER_OVERLAY_SHOW_BUTTON_LIST,
                    )
                    if in_card_select:
                        if MASTER_OVERLAY_SHOW_PARTICIPANTS:
                            master = render_participants_overlay(
                                master,
                                game_state.battle.participants,
                                draw_sub_rois=MASTER_OVERLAY_SHOW_PARTICIPANT_DETAILS,
                                show_slot_labels=MASTER_OVERLAY_SHOW_PARTICIPANTS,
                                show_pip_detection=(MASTER_OVERLAY_SHOW_PIPS and MASTER_OVERLAY_SHOW_PARTICIPANT_DETAILS),
                                initiative_side=game_state.battle.initiative.side,
                                show_empty=not MASTER_OVERLAY_HIDE_EMPTY_SLOTS,
                                show_legend=MASTER_OVERLAY_SHOW_PARTICIPANT_LEGEND,
                                legend_detailed=MASTER_OVERLAY_SHOW_PARTICIPANT_DETAILS,
                                use_role_colors=True,
                                player_slot_index=game_state.battle.player_wizard.slot_index,
                                player_slot_side=game_state.battle.player_wizard.side,
                                player_slot_locked=game_state.battle.player_wizard.slot_locked,
                                player_slot_sigil=game_state.battle.player_wizard.slot_sigil,
                            )
                        if MASTER_OVERLAY_SHOW_INITIATIVE:
                            master = render_initiative_boxes(master, INITIATIVE_CFG, game_state.battle.initiative)
                    _safe_imshow("wizmatic:master", master)
                else:
                    if SHOW_INITIATIVE_OVERLAY:
                        _safe_imshow(
                            "wizmatic:initiative",
                            render_initiative_overlay(render_base, INITIATIVE_CFG, game_state.battle.initiative),
                        )
                    if SHOW_PARTICIPANTS_OVERLAY:
                        _safe_imshow(
                            "wizmatic:participants",
                            render_participants_overlay(
                                render_base,
                                game_state.battle.participants,
                                show_pip_detection=SHOW_PIPDETECTION_OVERLAY,
                                initiative_side=game_state.battle.initiative.side,
                                show_empty=True,
                                show_legend=True,
                                player_slot_sigil=game_state.battle.player_wizard.slot_sigil,
                            ),
                        )
                    if SHOW_BUTTON_OVERLAY:
                        if latest_button_overlay is not None:
                            button_vis = latest_button_overlay.copy()
                        else:
                            button_vis = render_base.copy()
                        _draw_state_and_buttons(
                            button_vis,
                            _format_state_label(state_current),
                            latest_button_states,
                            show_buttons=True,
                        )
                        _safe_imshow("wizmatic:buttons", button_vis)

                if SHOW_PLAYER_WIZARD_OVERLAY:
                    in_battle = state_current in {"battle", "card_select", "round_animation"}
                    _safe_imshow(
                        "wizmatic:player_wizard",
                        render_player_wizard_overlay(
                            render_base,
                            game_state.battle.player_wizard,
                            in_battle=in_battle,
                        ),
                    )

            if DEBUG_PRINT_HEALTH_OCR:
                for line in pop_health_ocr_logs():
                    print(line)

            if SHOW_CAPTURE and (not SHOW_MASTER_DEBUG_OVERLAY) and latest_capture_frame is not None:
                _safe_imshow("W101 Capture", latest_capture_frame)

            if _safe_wait_key():
                break

            elapsed = time.perf_counter() - t0
            sleep_for = DT - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)

    finally:
        stop_event.set()
        task_event.set()
        analysis_thread.join(timeout=1.0)
        frames.stop()
        cap.close()

        # Break references so destructors run now, not at interpreter teardown
        frames = None
        cap = None

        # Force garbage collection while Python is still fully alive
        import gc
        gc.collect()
        gc.collect()
        try:
            cv2.destroyAllWindows()
        except cv2.error as exc:
            _disable_gui(exc)

if __name__ == "__main__":
    main()
