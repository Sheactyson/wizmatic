import time
import cv2
from utils.capture_wiz import Wizard101Capture
from utils.capture_thread import FrameSource
from state.game_state import GameState
from state.game_state_analysis import analyze_game_state
from config.initiative_config import INITIATIVE_CFG
from config.wizmatic_config import (DT,SHOW_CAPTURE,SHOW_INITIATIVE_OVERLAY)

def main():
    cap = Wizard101Capture(fps=60)
    frames = FrameSource(cap, hz=60)
    frames.start()

    state_cardSelect_last = None
    game_state = GameState()

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
                    render_initiative=SHOW_INITIATIVE_OVERLAY,
                )
                game_state = result.game_state
                state_cardSelect_current = result.in_card_select

                if SHOW_INITIATIVE_OVERLAY and result.initiative_overlay is not None:
                    cv2.imshow("wizmatic:initiative", result.initiative_overlay)

                if(state_cardSelect_last != state_cardSelect_current):
                    state_cardSelect_last = state_cardSelect_current
                    if result.pass_found or result.flee_found:
                        # Card Selection logic
                        print("Card Select Mode")
                    else:
                        # Idle logic
                        print("Idle Mode")

                # If debug windows are open, close them:
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

                if SHOW_CAPTURE:
                    # Only compute normalized when needed
                    analysis = bundle.normalized(1280, 720)
                    cv2.imshow("W101 Capture", analysis)

            if SHOW_CAPTURE:
                # Required for OpenCV window updates
                if cv2.waitKey(1) & 0xFF == ord("q"):
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
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
