import time
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
    SHOW_MASTER_DEBUG_OVERLAY,
    DEBUG_DUMP_OCR,
    DEBUG_DUMP_OCR_MAX,
    DEBUG_DUMP_HEALTH_ROI,
    DEBUG_DUMP_EMPTY_NAME_ROI,
    DEBUG_DUMP_INITIATIVE_ROI,
    DEBUG_DUMP_SIGIL_ROI,
    DEBUG_DUMP_SCHOOL_ROI,
    OCR_BACKEND,
    MASTER_OVERLAY_SHOW_PARTICIPANTS,
    MASTER_OVERLAY_SHOW_PARTICIPANT_LEGEND,
    MASTER_OVERLAY_HIDE_EMPTY_SLOTS,
    MASTER_OVERLAY_SHOW_INITIATIVE,
    MASTER_OVERLAY_SHOW_PIPS,
)
from config.participants_config import PARTICIPANTS_CFG
from state.initiative import render_initiative_boxes
from state.participants import render_participants_overlay

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

    state_cardSelect_last = None
    debug_ocr_session_id = 0
    game_state = GameState()
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

    def _draw_state_indicator(vis, label: str) -> None:
        h, w = vis.shape[:2]
        if h == 0 or w == 0:
            return
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.8
        thickness = 2
        (tw, th), _ = cv2.getTextSize(label, font, scale, thickness)
        pad = 8
        x = max(2, w - tw - pad - 2)
        y = int(h * 0.5)
        y = max(th + pad, min(h - 2, y))
        cv2.rectangle(vis, (x - pad, y - th - pad), (x + tw + pad, y + pad), (0, 0, 0), -1)
        cv2.putText(vis, label, (x, y), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)

    try:
        while True:
            t0 = time.perf_counter()

            bundle = frames.get_latest()
            if bundle is not None: # All actions regarding latest frames will go within this statement
                #native = bundle.native # native image captured
                analysis = bundle.normalized(1280, 720, allow_upscale=True) # normalized image captured

                render_initiative = (not SHOW_MASTER_DEBUG_OVERLAY) and SHOW_INITIATIVE_OVERLAY
                render_participants = (not SHOW_MASTER_DEBUG_OVERLAY) and SHOW_PARTICIPANTS_OVERLAY
                render_buttons = (not SHOW_MASTER_DEBUG_OVERLAY) and SHOW_BUTTON_OVERLAY
                render_pips = (not SHOW_MASTER_DEBUG_OVERLAY) and SHOW_PIPDETECTION_OVERLAY
                result = analyze_game_state(
                    analysis,
                    game_state,
                    initiative_cfg=INITIATIVE_CFG,
                    participants_cfg=PARTICIPANTS_CFG,
                    render_initiative=render_initiative,
                    render_participants=render_participants,
                    render_pip_detection=render_pips,
                    render_button_overlay=render_buttons,
                    debug_dump_initiative_roi=DEBUG_DUMP_INITIATIVE_ROI,
                    debug_dump_ocr=DEBUG_DUMP_OCR,
                    debug_dump_health_roi=DEBUG_DUMP_HEALTH_ROI,
                    debug_dump_empty_names=DEBUG_DUMP_EMPTY_NAME_ROI,
                    debug_dump_sigil_roi=DEBUG_DUMP_SIGIL_ROI,
                    debug_dump_school_roi=DEBUG_DUMP_SCHOOL_ROI,
                    debug_dump_ocr_id=str(debug_ocr_session_id),
                    debug_dump_ocr_limit=DEBUG_DUMP_OCR_MAX,
                )
                game_state = result.game_state
                state_cardSelect_current = result.in_card_select

                if SHOW_MASTER_DEBUG_OVERLAY:
                    master = analysis.copy()
                    state_label = "Card Select" if state_cardSelect_current else "Idle"
                    _draw_state_indicator(master, state_label)
                    if state_cardSelect_current:
                        if MASTER_OVERLAY_SHOW_PARTICIPANTS:
                            master = render_participants_overlay(
                                master,
                                game_state.battle.participants,
                                show_pip_detection=MASTER_OVERLAY_SHOW_PIPS,
                                initiative_side=game_state.battle.initiative.side,
                                show_empty=not MASTER_OVERLAY_HIDE_EMPTY_SLOTS,
                                show_legend=MASTER_OVERLAY_SHOW_PARTICIPANT_LEGEND,
                            )
                        if MASTER_OVERLAY_SHOW_INITIATIVE:
                            master = render_initiative_boxes(master, INITIATIVE_CFG, game_state.battle.initiative)
                    _safe_imshow("wizmatic:master", master)
                else:
                    if SHOW_INITIATIVE_OVERLAY and result.initiative_overlay is not None:
                        _safe_imshow("wizmatic:initiative", result.initiative_overlay)
                    if SHOW_PARTICIPANTS_OVERLAY and result.participants_overlay is not None:
                        _safe_imshow("wizmatic:participants", result.participants_overlay)
                    if SHOW_BUTTON_OVERLAY and result.button_overlay is not None:
                        _safe_imshow("wizmatic:buttons", result.button_overlay)

                if(state_cardSelect_last != state_cardSelect_current):
                    state_cardSelect_last = state_cardSelect_current
                    if result.pass_found or result.flee_found:
                        # Card Selection logic
                        print("Card Select Mode")
                        debug_ocr_session_id += 1
                        if game_state.battle.participants:
                            enemies = game_state.battle.participants.enemies
                            allies = game_state.battle.participants.allies
                            for p in enemies + allies:
                                if p is None:
                                    continue
                                raw = p.name_raw if p.name_raw else "unknown"
                                final = p.name if p.name else "unknown"
                                if p.name_time_ms is not None:
                                    if p.name_time_parts:
                                        cap_ms, prep_ms, ocr_ms, res_ms = p.name_time_parts
                                        print(
                                            f"[ocr:name] {p.side} {p.index}: {raw} -> {final} "
                                            f"({p.name_time_ms:.1f}ms | capture {cap_ms:.1f}ms "
                                            f"prep {prep_ms:.1f}ms ocr {ocr_ms:.1f}ms "
                                            f"resolve {res_ms:.1f}ms)"
                                        )
                                    else:
                                        print(f"[ocr:name] {p.side} {p.index}: {raw} -> {final} ({p.name_time_ms:.1f}ms)")
                                else:
                                    print(f"[ocr:name] {p.side} {p.index}: {raw} -> {final}")
                    else:
                        # Idle logic
                        print("Idle Mode")

                # If debug windows are open, close them:
                if _safe_wait_key():
                    break

                if SHOW_CAPTURE and (not SHOW_MASTER_DEBUG_OVERLAY):
                    # Only compute normalized when needed
                    analysis = bundle.normalized(1280, 720)
                    _safe_imshow("W101 Capture", analysis)

            if SHOW_CAPTURE:
                # Required for OpenCV window updates
                if _safe_wait_key():
                    break

            elapsed = time.perf_counter() - t0
            sleep_for = DT - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)

    finally:
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
