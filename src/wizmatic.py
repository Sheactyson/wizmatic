import time
import cv2
from pathlib import Path
from utils.capture_wiz import Wizard101Capture
from utils.capture_thread import FrameSource
import utils.button_detect as bDetect

SHOW_CAPTURE = False
TARGET_HZ = 15
DT = 1.0 / TARGET_HZ

def main():
    cap = Wizard101Capture(fps=60)
    frames = FrameSource(cap, hz=60)
    frames.start()

    state_cardSelect_last = None

    try:
        while True:
            t0 = time.perf_counter()

            bundle = frames.get_latest()
            if bundle is not None: # All actions regarding latest frames will go within this statement
                native = bundle.native  # native image captured
                analysis = bundle.normalized(1280, 720, allow_upscale=True) # normalized image captured

                pass_found = bDetect.detect_button(analysis,"pass",rel_roi=(0.25, 0.57, 0.45, 0.63),threshold=0.78)
                flee_found = bDetect.detect_button(analysis,"flee",rel_roi=(0.55, 0.57, 0.74, 0.63),threshold=0.78)

                # If either button is found, we are in Card Select
                state_cardSelect_current = pass_found or flee_found
                if(state_cardSelect_last != state_cardSelect_current):
                    state_cardSelect_last = state_cardSelect_current
                    if pass_found or flee_found:
                        # Card Selection logic
                        print("Card Select Mode")
                    else:
                        # Idle logic
                        print("Idle Mode")

                # If debug windows are open, keep this in your loop:
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