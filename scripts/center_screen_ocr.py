import argparse
import time
from datetime import datetime
from pathlib import Path
import sys

import cv2
import numpy as np
import easyocr

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from config.participants_config import OCR_CFG
from utils.capture_wiz import Wizard101Capture
from utils.capture_thread import FrameSource


def _build_reader() -> easyocr.Reader:
    return easyocr.Reader(
        list(OCR_CFG.easyocr_langs),
        gpu=OCR_CFG.easyocr_gpu,
        model_storage_directory=OCR_CFG.easyocr_model_dir,
        download_enabled=True,
    )


def _read_text(reader: easyocr.Reader, img_bgr: np.ndarray, allowlist: str | None) -> str:
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    results = reader.readtext(img_rgb, detail=0, allowlist=allowlist or None)
    return " ".join(r.strip() for r in results if r and str(r).strip()).strip()


def _normalize_bgr(
    img_bgr: np.ndarray,
    ref_w: int,
    ref_h: int,
    *,
    allow_upscale: bool,
) -> np.ndarray:
    h, w = img_bgr.shape[:2]
    scale = min(ref_w / w, ref_h / h)
    if not allow_upscale:
        scale = min(scale, 1.0)
    if scale == 1.0:
        return img_bgr
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    return cv2.resize(img_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)


def _apply_crop(
    img_bgr: np.ndarray,
    crop: tuple[int, int, int, int] | None,
) -> tuple[np.ndarray, tuple[int, int, int, int] | None]:
    if not crop:
        return img_bgr, None
    h, w = img_bgr.shape[:2]
    x1, y1, x2, y2 = crop
    x1 = max(0, min(x1, w - 1))
    x2 = max(0, min(x2, w))
    y1 = max(0, min(y1, h - 1))
    y2 = max(0, min(y2, h))
    if x2 <= x1 or y2 <= y1:
        return img_bgr, None
    return img_bgr[y1:y2, x1:x2], (x1, y1, x2, y2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Read text from the Wizard101 client frame.")
    parser.add_argument("--width", type=int, default=1280, help="Normalize width for analysis.")
    parser.add_argument("--height", type=int, default=720, help="Normalize height for analysis.")
    parser.add_argument("--allow-upscale", action="store_true", help="Allow upscaling during normalization.")
    parser.add_argument("--interval", type=float, default=0.5, help="Seconds between OCR reads.")
    parser.add_argument("--once", action="store_true", help="Capture once and exit.")
    parser.add_argument("--only-changes", action="store_true", help="Print only when text changes.")
    parser.add_argument("--allowlist", type=str, default="", help="Allowlist for OCR (empty = none).")
    parser.add_argument(
        "--crop",
        type=int,
        nargs=4,
        metavar=("X1", "Y1", "X2", "Y2"),
        help="Crop region in Wizard101 client pixels (native coordinates).",
    )
    parser.add_argument("--no-preview", action="store_true", help="Disable capture preview overlay window.")
    args = parser.parse_args()

    reader = _build_reader()
    prev = None
    preview = not args.no_preview
    window_ready = False

    cap = Wizard101Capture(fps=60)
    frames = FrameSource(cap, hz=60)
    frames.start()

    allowlist = args.allowlist or None

    try:
        while True:
            bundle = frames.get_latest()
            if bundle is None:
                time.sleep(0.01)
                continue
            native = bundle.native
            crop_img, crop_rect = _apply_crop(native, tuple(args.crop) if args.crop else None)
            frame = _normalize_bgr(
                crop_img,
                args.width,
                args.height,
                allow_upscale=args.allow_upscale,
            )
            text = _read_text(reader, frame, allowlist)
            if (not args.only_changes) or (text != prev):
                stamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{stamp}] {text}")
                prev = text
            if preview:
                vis = native.copy()
                h, w = vis.shape[:2]
                if crop_rect:
                    x1, y1, x2, y2 = crop_rect
                    cv2.rectangle(vis, (x1, y1), (x2 - 1, y2 - 1), (0, 255, 255), 2)
                overlay = text or ""
                if overlay:
                    cv2.putText(
                        vis,
                        overlay[:120],
                        (10, max(24, h - 12)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )
                cv2.putText(
                    vis,
                    f"{w}x{h}",
                    (10, 24),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                if not window_ready:
                    cv2.namedWindow("Wizard101 Capture OCR", cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("Wizard101 Capture OCR", w, h)
                    window_ready = True
                cv2.imshow("Wizard101 Capture OCR", vis)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            if args.once:
                break
            time.sleep(max(0.0, args.interval))
    finally:
        frames.stop()
        cap.close()
        if preview:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
