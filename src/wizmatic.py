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
    DEBUG_DUMP_OCR,
    DEBUG_DUMP_OCR_MAX,
    DEBUG_DUMP_HEALTH_ROI,
    DEBUG_DUMP_EMPTY_NAME_ROI,
)
from config.participants_config import PARTICIPANTS_CFG

def main():
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

    try:
        while True:
            t0 = time.perf_counter()

            bundle = frames.get_latest()
            if bundle is not None: # All actions regarding latest frames will go within this statement
                #native = bundle.native # native image captured
                analysis = bundle.normalized(1280, 720, allow_upscale=True) # normalized image captured

                result = analyze_game_state(
                    analysis,
                    game_state,
                    initiative_cfg=INITIATIVE_CFG,
                    participants_cfg=PARTICIPANTS_CFG,
                    render_initiative=SHOW_INITIATIVE_OVERLAY,
                    render_participants=SHOW_PARTICIPANTS_OVERLAY,
                    render_pip_detection=SHOW_PIPDETECTION_OVERLAY,
                    debug_dump_ocr=DEBUG_DUMP_OCR,
                    debug_dump_health_roi=DEBUG_DUMP_HEALTH_ROI,
                    debug_dump_empty_names=DEBUG_DUMP_EMPTY_NAME_ROI,
                    debug_dump_ocr_id=str(debug_ocr_session_id),
                    debug_dump_ocr_limit=DEBUG_DUMP_OCR_MAX,
                )
                game_state = result.game_state
                state_cardSelect_current = result.in_card_select

                if SHOW_INITIATIVE_OVERLAY and result.initiative_overlay is not None:
                    _safe_imshow("wizmatic:initiative", result.initiative_overlay)
                if SHOW_PARTICIPANTS_OVERLAY and result.participants_overlay is not None:
                    _safe_imshow("wizmatic:participants", result.participants_overlay)

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
                                print(f"[ocr:name] {p.side} {p.index}: {raw} -> {final}")
                    else:
                        # Idle logic
                        print("Idle Mode")

                # If debug windows are open, close them:
                if _safe_wait_key():
                    break

                if SHOW_CAPTURE:
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
