from __future__ import annotations

from dataclasses import dataclass, replace, field
from datetime import datetime
from pathlib import Path
import time
import threading
from typing import Dict, Optional, Tuple, List, Set
import re

import cv2
import numpy as np

from utils.roi import crop_relative, draw_relative_roi
from state.game_state import ParticipantsState, ParticipantState, PipInventory, PlayerWizardState

try:
    import pytesseract
except Exception:  # pragma: no cover - allow import failure in minimal envs
    pytesseract = None

_OCR_DUMP_DIR = Path("debug/ocr")
_OCR_DUMP_DIR.mkdir(parents=True, exist_ok=True)
_PARTICIPANT_DUMP_DIR = Path("debug/participants")
_PARTICIPANT_DUMP_DIR.mkdir(parents=True, exist_ok=True)
_PIP_DUMP_DIR = Path("debug/pips")
_PIP_DUMP_DIR.mkdir(parents=True, exist_ok=True)
_OCR_DUMP_COUNTS: Dict[str, int] = {}
_WORDLIST_CACHE: Dict[str, List[str]] = {}
_WORDLIST_NORM_CACHE: Dict[str, List[str]] = {}
_WORDLIST_NORM_NS_CACHE: Dict[str, List[str]] = {}
_WORDLIST_PREFIX_CACHE: Dict[str, Dict[int, Dict[str, List[int]]]] = {}
_WORDLIST_TOKEN_INDEX_CACHE: Dict[str, Dict[str, List[int]]] = {}
_WORDLIST_NORM_MAP_CACHE: Dict[str, Dict[str, str]] = {}
_EASYOCR_WARNED = False
_HEALTH_OCR_LOG_QUEUE: List[str] = []
_HEALTH_OCR_LOG_LOCK = threading.Lock()

_WORDLIST_PREFIX_MAX_LEN = 4
_WORDLIST_MULTI_SEP = "|"


def pop_health_ocr_logs() -> List[str]:
    with _HEALTH_OCR_LOG_LOCK:
        if not _HEALTH_OCR_LOG_QUEUE:
            return []
        logs = list(_HEALTH_OCR_LOG_QUEUE)
        _HEALTH_OCR_LOG_QUEUE.clear()
    return logs


def _push_health_ocr_log(line: str) -> None:
    with _HEALTH_OCR_LOG_LOCK:
        _HEALTH_OCR_LOG_QUEUE.append(line)


@dataclass(frozen=True)
class ParticipantBoxProfile:
    enemy_first_box: Tuple[float, float, float, float]
    ally_first_box: Tuple[float, float, float, float]
    enemy_spacing_x: float
    ally_spacing_x: float
    slots: int = 4
    ally_anchor: str = "left"  # "left" or "right"


@dataclass(frozen=True)
class ParticipantLayout:
    sigil_roi_enemy: Tuple[float, float, float, float]
    sigil_roi_ally: Tuple[float, float, float, float]
    school_roi_enemy: Tuple[float, float, float, float]
    school_roi_ally: Tuple[float, float, float, float]
    name_roi_enemy: Tuple[float, float, float, float]
    health_roi_enemy: Tuple[float, float, float, float]
    name_roi_ally: Tuple[float, float, float, float]
    health_roi_ally: Tuple[float, float, float, float]
    pips_roi_enemy: Tuple[float, float, float, float]
    pips_roi_ally: Tuple[float, float, float, float]


@dataclass(frozen=True)
class PlayerHUDProfile:
    health_roi: Tuple[float, float, float, float]
    mana_roi: Tuple[float, float, float, float]
    energy_roi: Tuple[float, float, float, float]


@dataclass(frozen=True)
class PipDetectConfig:
    white_sat_max: int = 60
    white_val_min: int = 200
    school_sat_min: int = 80
    school_val_min: int = 140
    min_area_frac: float = 0.002
    max_area_frac: float = 0.05
    templates_base_dir: str = "src/assets/pips"
    template_threshold: float = 0.7
    slot_debug_upscale: int = 3
    slot_width_px: int = 15
    slot_width_px_by_aspect: Dict[str, int] = field(default_factory=dict)
    slot_gap_px: int = 0
    slot_gap_px_by_aspect: Dict[str, int] = field(default_factory=dict)
    slot_start_px: int = 0
    slot_start_px_by_aspect: Dict[str, Dict[str, int]] = field(default_factory=dict)
    slot_top_cut_px: int = 0
    slot_top_cut_px_by_aspect: Dict[str, int] = field(default_factory=dict)
    slot_bottom_cut_px: int = 0
    slot_bottom_cut_px_by_aspect: Dict[str, int] = field(default_factory=dict)
    slot_presence_confidence_threshold: float = 0.7
    slot_count: int = 7


@dataclass(frozen=True)
class SigilDetectConfig:
    templates_base_dir: str = "src/assets/participants/sigils"
    template_threshold: float = 0.7


@dataclass(frozen=True)
class SchoolDetectConfig:
    templates_base_dir: str = "src/assets/participants/schools"
    template_threshold: float = 0.7


@dataclass(frozen=True)
class OCRConfig:
    scale: int = 3
    psm: int = 7
    oem: int = 1
    lang: str = "eng"
    name_whitelist: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '-."
    health_whitelist: str = "0123456789/,"
    player_resource_whitelist: str = "0123456789"
    invert: bool = False
    tesseract_cmd: Optional[str] = None
    user_words_path: Optional[str] = None
    name_resolution_mode: str = "pve"  # "pve" or "pvp"
    wordlist_wizards_path: Optional[str] = None
    wordlist_monsters_path: Optional[str] = None
    wordlist_minions_path: Optional[str] = None
    wordlist_max_distance: int = 2
    wordlist_min_ratio: float = 0.75
    name_blacklist: str = "$§/\\|_`~=+?><,!@#%^&*(}{][)"
    wordlist_prefix_min_ratio: float = 0.6
    wordlist_prefix_min_chars: int = 4
    backend: str = "tesseract"  # "tesseract" or "easyocr"
    easyocr_langs: Tuple[str, ...] = ("en",)
    easyocr_gpu: bool = True
    easyocr_model_dir: Optional[str] = "src/ocr_easy/models"


@dataclass(frozen=True)
class ParticipantsConfig:
    profiles: Dict[str, ParticipantBoxProfile]
    layout: ParticipantLayout
    pip: PipDetectConfig
    ocr: OCRConfig
    sigil: SigilDetectConfig
    school: SchoolDetectConfig


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


def _shift_roi(roi: Tuple[float, float, float, float], dx: float) -> Tuple[float, float, float, float]:
    x1, y1, x2, y2 = roi
    return (x1 + dx, y1, x2 + dx, y2)


def _sub_roi(
    parent: Tuple[float, float, float, float],
    sub: Tuple[float, float, float, float],
) -> Tuple[float, float, float, float]:
    px1, py1, px2, py2 = parent
    sw = px2 - px1
    sh = py2 - py1
    sx1, sy1, sx2, sy2 = sub
    return (px1 + sx1 * sw, py1 + sy1 * sh, px1 + sx2 * sw, py1 + sy2 * sh)


def _prep_ocr(gray: np.ndarray, scale: int, invert: bool) -> np.ndarray:
    if scale > 1:
        gray = cv2.resize(gray, (gray.shape[1] * scale, gray.shape[0] * scale), interpolation=cv2.INTER_CUBIC)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if invert:
        th = cv2.bitwise_not(th)
    return th


def _binary_ink_ratio(bin_img: np.ndarray) -> float:
    if bin_img.size == 0:
        return 0.0
    return float((bin_img < 128).mean())


def _name_roi_hash(img_bgr: np.ndarray) -> Optional[int]:
    if img_bgr.size == 0:
        return None
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (32, 8), interpolation=cv2.INTER_AREA)
    mean = small.mean()
    bits = (small > mean).astype(np.uint8)
    packed = np.packbits(bits.reshape(-1))
    return int.from_bytes(packed.tobytes(), "big")


def _ensure_black_text_on_white(bin_img: np.ndarray) -> np.ndarray:
    if bin_img.size == 0:
        return bin_img
    return cv2.bitwise_not(bin_img) if bin_img.mean() < 127 else bin_img


def _prep_name_option_a(img_bgr: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    # Dark-text mask using Otsu on Value channel.
    _, dark_mask = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    mask_kernel = np.ones((3, 3), np.uint8)
    dark_mask = cv2.morphologyEx(dark_mask, cv2.MORPH_OPEN, mask_kernel, iterations=1)
    dark_mask = cv2.morphologyEx(dark_mask, cv2.MORPH_CLOSE, mask_kernel, iterations=1)

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        7,
    )
    # Keep only the dark-text regions from the adaptive result.
    th = np.where(dark_mask > 0, th, 255).astype(np.uint8)
    return th


def _prep_name_option_dark(img_bgr: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    # Keep very dark pixels as text; assumes black name text on lighter background.
    _, mask = cv2.threshold(v, 70, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    return np.where(mask > 0, 0, 255).astype(np.uint8)


def _prep_name_option_b(img_bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    blackhat = cv2.normalize(blackhat, None, 0, 255, cv2.NORM_MINMAX)
    _, th = cv2.threshold(blackhat, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th


def _prep_ocr_name(img_bgr: np.ndarray, scale: int, invert: bool) -> np.ndarray:
    if scale > 1:
        img_bgr = cv2.resize(
            img_bgr,
            (img_bgr.shape[1] * scale, img_bgr.shape[0] * scale),
            interpolation=cv2.INTER_CUBIC,
        )
    th_dark = _prep_name_option_dark(img_bgr)
    th_dark = _ensure_black_text_on_white(th_dark)
    th_dark = _filter_small_components(th_dark, min_area_frac=0.0006)
    ink = _binary_ink_ratio(th_dark)
    if 0.003 <= ink <= 0.5:
        th = th_dark
    else:
        th = _prep_name_option_a(img_bgr)
        th = _ensure_black_text_on_white(th)
        th = _filter_small_components(th, min_area_frac=0.0006)

        ink = _binary_ink_ratio(th)
        if ink < 0.004 or ink > 0.5:
            th_b = _prep_name_option_b(img_bgr)
            th_b = _ensure_black_text_on_white(th_b)
            th_b = _filter_small_components(th_b, min_area_frac=0.0006)
            th = th_b

    if invert:
        th = cv2.bitwise_not(th)
    return th


def _prep_easyocr_image(
    img_bgr: np.ndarray,
    cfg: OCRConfig,
    *,
    invert: bool,
    prefer_red: bool,
    clahe: bool,
    binarize: bool = False,
) -> np.ndarray:
    if img_bgr.size == 0:
        return img_bgr
    if prefer_red:
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        lower1 = np.array([0, 120, 80])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 80])
        upper2 = np.array([179, 255, 255])
        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)
        gray = hsv[:, :, 2].copy()
        gray[mask == 0] = 255
    else:
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    if clahe:
        clahe_op = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe_op.apply(gray)

    if cfg.scale > 1:
        gray = cv2.resize(gray, (gray.shape[1] * cfg.scale, gray.shape[0] * cfg.scale), interpolation=cv2.INTER_CUBIC)

    if binarize:
        _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if invert:
        gray = cv2.bitwise_not(gray)
    return gray


def _prep_tesseract_health(
    img_bgr: np.ndarray,
    cfg: OCRConfig,
    *,
    invert: bool,
) -> np.ndarray:
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lower1 = np.array([0, 120, 80])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 120, 80])
    upper2 = np.array([179, 255, 255])
    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)
    mask = cv2.bitwise_or(mask1, mask2)
    gray = cv2.bitwise_and(hsv[:, :, 2], hsv[:, :, 2], mask=mask)
    return _prep_ocr(gray, cfg.scale, invert)


def _prep_plain_health(
    img_bgr: np.ndarray,
    cfg: OCRConfig,
    *,
    invert: bool,
) -> np.ndarray:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    return _prep_ocr(gray, cfg.scale, invert)


def _prep_tesseract_yellow_numeric(
    img_bgr: np.ndarray,
    cfg: OCRConfig,
    *,
    invert: bool,
    strict: bool = False,
) -> np.ndarray:
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    if strict:
        # Near-exact yellow text (#FFFF00 with tight tolerance). Use for energy.
        hsv_lower = np.array([25, 220, 220], dtype=np.uint8)
        hsv_upper = np.array([35, 255, 255], dtype=np.uint8)
        hsv_mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

        tol = 24
        b = img_bgr[:, :, 0].astype(np.int16)
        g = img_bgr[:, :, 1].astype(np.int16)
        r = img_bgr[:, :, 2].astype(np.int16)
        near_exact_yellow = (
            (r >= (255 - tol))
            & (g >= (255 - tol))
            & (b <= tol)
            & (np.abs(r - g) <= tol)
        )
        bgr_mask = (near_exact_yellow.astype(np.uint8) * 255)
        mask = cv2.bitwise_and(hsv_mask, bgr_mask)
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    else:
        # Looser yellow mask for health/mana where background is less problematic.
        hsv_lower = np.array([18, 145, 150], dtype=np.uint8)
        hsv_upper = np.array([40, 255, 255], dtype=np.uint8)
        hsv_mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
        b = img_bgr[:, :, 0].astype(np.int16)
        g = img_bgr[:, :, 1].astype(np.int16)
        r = img_bgr[:, :, 2].astype(np.int16)
        near_yellow = (
            (r >= 120)
            & (g >= 120)
            & (b <= 170)
            & (np.abs(r - g) <= 95)
        )
        bgr_mask = (near_yellow.astype(np.uint8) * 255)
        mask = cv2.bitwise_and(hsv_mask, bgr_mask)
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)

    # OCR target: black digits on white background.
    bin_img = np.full(mask.shape, 255, dtype=np.uint8)
    bin_img[mask > 0] = 0
    if cfg.scale > 1:
        bin_img = cv2.resize(
            bin_img,
            (bin_img.shape[1] * cfg.scale, bin_img.shape[0] * cfg.scale),
            interpolation=cv2.INTER_NEAREST,
        )
    if invert:
        bin_img = cv2.bitwise_not(bin_img)
    return bin_img


def _filter_small_components(mask: np.ndarray, min_area_frac: float) -> np.ndarray:
    if mask.size == 0:
        return mask
    h, w = mask.shape[:2]
    min_area = max(1, int(h * w * min_area_frac))
    num, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    keep = np.zeros_like(mask)
    for i in range(1, num):
        area = stats[i, cv2.CC_STAT_AREA]
        if area >= min_area:
            keep[labels == i] = 255
    return keep


def _crop_to_foreground(bin_img: np.ndarray, pad: int = 4) -> np.ndarray:
    if bin_img.size == 0:
        return bin_img
    # Expect black text (0) on white background (255).
    mask = bin_img < 128
    if not np.any(mask):
        return bin_img
    ys, xs = np.where(mask)
    y1 = max(0, int(ys.min()) - pad)
    y2 = min(bin_img.shape[0], int(ys.max()) + pad + 1)
    x1 = max(0, int(xs.min()) - pad)
    x2 = min(bin_img.shape[1], int(xs.max()) + pad + 1)
    cropped = bin_img[y1:y2, x1:x2]
    # Add white border to help Tesseract with segmentation.
    return cv2.copyMakeBorder(cropped, 4, 4, 6, 6, cv2.BORDER_CONSTANT, value=255)


def _ocr_name_per_char(img_bgr: np.ndarray, cfg: OCRConfig) -> Optional[str]:
    if cfg.backend != "tesseract":
        return None
    if pytesseract is None or img_bgr.size == 0:
        return None
    bin_img = _prep_ocr_name(img_bgr, cfg.scale, invert=False)
    bin_img = _crop_to_foreground(bin_img, pad=2)
    if bin_img.size == 0:
        return None
    mask = (bin_img < 128).astype(np.uint8)
    if mask.size == 0:
        return None

    h, w = mask.shape[:2]
    col_sum = mask.sum(axis=0)
    ink_thresh = max(1, int(h * 0.08))
    runs: List[Tuple[int, int]] = []
    in_run = False
    start = 0
    for x in range(w):
        if col_sum[x] >= ink_thresh:
            if not in_run:
                start = x
                in_run = True
        else:
            if in_run:
                runs.append((start, x - 1))
                in_run = False
    if in_run:
        runs.append((start, w - 1))

    if not runs:
        # Fallback to previous preprocessing if projection fails.
        bin_img = _prep_ocr_name(img_bgr, cfg.scale, invert=False)
        bin_img = _crop_to_foreground(bin_img, pad=2)
        mask = (bin_img < 128).astype(np.uint8)
        if mask.size == 0:
            return None
        h, w = mask.shape[:2]
        col_sum = mask.sum(axis=0)
        runs = []
        in_run = False
        start = 0
        for x in range(bin_img.shape[1]):
            if col_sum[x] >= max(1, int(bin_img.shape[0] * 0.08)):
                if not in_run:
                    start = x
                    in_run = True
            else:
                if in_run:
                    runs.append((start, x - 1))
                    in_run = False
        if in_run:
            runs.append((start, bin_img.shape[1] - 1))
        if not runs:
            return None

    widths = [r[1] - r[0] + 1 for r in runs]
    avg_w = float(sum(widths)) / max(1, len(widths))
    min_run_w = max(2, int(avg_w * 0.3))

    chars: List[str] = []
    last_x2 = None
    for x1, x2 in runs:
        if (x2 - x1 + 1) < min_run_w:
            continue
        if last_x2 is not None and (x1 - last_x2) > avg_w * 0.8:
            chars.append(" ")
        last_x2 = x2

        pad = max(2, int((x2 - x1 + 1) * 0.15))
        cx1 = max(0, x1 - pad)
        cx2 = min(w, x2 + pad + 1)
        crop = bin_img[:, cx1:cx2]
        crop = cv2.copyMakeBorder(crop, 4, 4, 6, 6, cv2.BORDER_CONSTANT, value=255)
        config = f"--oem {cfg.oem} --psm 10"
        if cfg.name_whitelist:
            config += f" -c tessedit_char_whitelist={cfg.name_whitelist}"
        try:
            ch = pytesseract.image_to_string(crop, lang=cfg.lang, config=config)
        except Exception:
            ch = ""
        ch = ch.strip()
        if not ch:
            continue
        ch = ch[0]
        if ch.isalnum() or ch in "'-":
            chars.append(ch)

    text = "".join(chars).strip()
    return text or None


def _allow_ocr_dump(debug_dump_id: Optional[str], debug_dump_limit: int) -> bool:
    if not debug_dump_id or debug_dump_limit <= 0:
        return False
    count = _OCR_DUMP_COUNTS.get(debug_dump_id, 0)
    if count >= debug_dump_limit:
        return False
    _OCR_DUMP_COUNTS[debug_dump_id] = count + 1
    return True


def _remove_ocr_dumps_with_prefix(prefix: str, *, dump_id: Optional[str] = None) -> None:
    if not prefix:
        return
    try:
        for path in _OCR_DUMP_DIR.glob(f"{prefix}_*.png"):
            try:
                path.unlink()
            except Exception:
                pass
    except Exception:
        pass
    if dump_id:
        _OCR_DUMP_COUNTS.pop(dump_id, None)


def _dump_health_roi(
    health_crop: np.ndarray,
    *,
    side: str,
    index: int,
    debug_dump_id: Optional[str],
    prepped: Optional[Tuple[Tuple[str, np.ndarray], ...]] = None,
) -> None:
    if health_crop.size == 0:
        return
    try:
        base = f"health_roi_{side}_{index}"
        path = _OCR_DUMP_DIR / f"{base}.png"
        cv2.imwrite(str(path), health_crop)
        if prepped:
            for suffix, img in prepped:
                if img is None or getattr(img, "size", 0) == 0:
                    continue
                prep_path = _OCR_DUMP_DIR / f"{base}_{suffix}.png"
                cv2.imwrite(str(prep_path), img)
    except Exception:
        pass


def _dump_participant_roi(
    crop: np.ndarray,
    *,
    kind: str,
    side: str,
    index: int,
    enabled: bool,
) -> None:
    if not enabled or crop.size == 0:
        return
    try:
        path = _PARTICIPANT_DUMP_DIR / f"{kind}_{side}_{index}.png"
        cv2.imwrite(str(path), crop)
    except Exception:
        pass


def _pip_slot_name(side: str, index: int) -> str:
    enemy_sigils = ("dagger", "key", "ruby", "spiral")
    ally_sigils = ("sun", "eye", "star", "moon")
    names = enemy_sigils if side == "enemy" else ally_sigils
    if 0 <= index < len(names):
        return names[index]
    return f"{side}_{index}"


def _pip_slot_start_px(cfg: PipDetectConfig, aspect_key: str, slot_name: str) -> int:
    by_aspect = cfg.slot_start_px_by_aspect or {}
    aspect_map = by_aspect.get(aspect_key) or by_aspect.get("16:9") or {}
    try:
        start = aspect_map.get(slot_name)
        if start is None:
            start = cfg.slot_start_px
        return max(0, int(round(float(start))))
    except Exception:
        return max(0, int(round(float(cfg.slot_start_px))))


def _pip_aspect_dir_name(aspect_key: str) -> str:
    # Windows-safe aspect directory names.
    known = {
        "4:3": "4x3",
        "16:9": "16x9",
        "43:18": "43x18",
    }
    if aspect_key in known:
        return known[aspect_key]
    safe = []
    for ch in str(aspect_key):
        if ch.isalnum() or ch in ("-", "_"):
            safe.append(ch)
        else:
            safe.append("_")
    out = "".join(safe).strip("_")
    return out or "unknown"


def _pip_slot_width_px(cfg: PipDetectConfig, aspect_key: str) -> int:
    by_aspect = cfg.slot_width_px_by_aspect or {}
    try:
        width = by_aspect.get(aspect_key)
        if width is None:
            width = by_aspect.get("16:9")
        if width is None:
            width = cfg.slot_width_px
        return max(1, int(round(float(width))))
    except Exception:
        return max(1, int(round(float(cfg.slot_width_px))))


def _pip_slot_gap_px(cfg: PipDetectConfig, aspect_key: str) -> int:
    by_aspect = cfg.slot_gap_px_by_aspect or {}
    try:
        gap = by_aspect.get(aspect_key)
        if gap is None:
            gap = by_aspect.get("16:9")
        if gap is None:
            gap = cfg.slot_gap_px
        return max(0, int(round(float(gap))))
    except Exception:
        return max(0, int(round(float(cfg.slot_gap_px))))


def _pip_slot_top_cut_px(cfg: PipDetectConfig, aspect_key: str) -> int:
    by_aspect = cfg.slot_top_cut_px_by_aspect or {}
    try:
        top = by_aspect.get(aspect_key)
        if top is None:
            top = by_aspect.get("16:9")
        if top is None:
            top = cfg.slot_top_cut_px
        return max(0, int(round(float(top))))
    except Exception:
        return max(0, int(round(float(cfg.slot_top_cut_px))))


def _pip_slot_bottom_cut_px(cfg: PipDetectConfig, aspect_key: str) -> int:
    by_aspect = cfg.slot_bottom_cut_px_by_aspect or {}
    try:
        bot = by_aspect.get(aspect_key)
        if bot is None:
            bot = by_aspect.get("16:9")
        if bot is None:
            bot = cfg.slot_bottom_cut_px
        return max(0, int(round(float(bot))))
    except Exception:
        return max(0, int(round(float(cfg.slot_bottom_cut_px))))


def _dump_pips_roi_debug(
    pips_crop: np.ndarray,
    *,
    side: str,
    index: int,
    aspect_key: str,
    cfg: PipDetectConfig,
) -> None:
    if pips_crop is None or pips_crop.size == 0:
        return
    try:
        slot_name = _pip_slot_name(side, index)
        slot_dir = _PIP_DUMP_DIR / slot_name
        slot_dir.mkdir(parents=True, exist_ok=True)

        upscale = max(1, int(cfg.slot_debug_upscale))
        if upscale > 1:
            pips_debug = cv2.resize(
                pips_crop,
                (pips_crop.shape[1] * upscale, pips_crop.shape[0] * upscale),
                interpolation=cv2.INTER_CUBIC,
            )
        else:
            pips_debug = pips_crop

        raw_path = slot_dir / "pips_roi.png"
        cv2.imwrite(str(raw_path), pips_debug)

        h, w = pips_debug.shape[:2]
        if h <= 0 or w <= 0:
            return
        slot_count = max(1, int(cfg.slot_count))
        start_x = _pip_slot_start_px(cfg, aspect_key, slot_name)
        slot_w = _pip_slot_width_px(cfg, aspect_key)
        slot_gap = _pip_slot_gap_px(cfg, aspect_key)
        slot_step = slot_w + slot_gap
        top_cut = _pip_slot_top_cut_px(cfg, aspect_key)
        bottom_cut = _pip_slot_bottom_cut_px(cfg, aspect_key)
        y1 = max(0, min(h - 1, top_cut))
        y2 = max(y1 + 1, min(h, h - bottom_cut))

        # Guide image: only the kept slot crops are shown; excluded gap regions are black.
        guide = np.zeros_like(pips_debug)
        for n in range(slot_count):
            x1 = start_x + (n * slot_step)
            x2 = x1 + slot_w
            cx1 = max(0, min(w, x1))
            cx2 = max(0, min(w, x2))
            if cx2 <= cx1:
                continue
            guide[y1:y2, cx1:cx2] = pips_debug[y1:y2, cx1:cx2]

        guide_path = slot_dir / "pips_roi_guides.png"
        cv2.imwrite(str(guide_path), guide)

        # Dump each pip-slot crop (1..7) based on start + slot width.
        for n in range(slot_count):
            x1 = start_x + (n * slot_step)
            x2 = x1 + slot_w
            cx1 = max(0, min(w, x1))
            cx2 = max(0, min(w, x2))
            if cx2 > cx1:
                slot_crop = pips_debug[y1:y2, cx1:cx2]
            else:
                # Keep deterministic output even if bounds are invalid.
                slot_crop = np.zeros((max(1, y2 - y1), 1, 3), dtype=np.uint8)
            slot_path = slot_dir / f"pip_slot_{n + 1}.png"
            cv2.imwrite(str(slot_path), slot_crop)
    except Exception:
        pass


def _normalize_word(text: str) -> str:
    filtered = []
    for ch in text.upper():
        if ch.isalpha() or ch == " ":
            filtered.append(ch)
    return " ".join("".join(filtered).split())


def _normalize_ocr_compare(text: Optional[str]) -> str:
    if text is None:
        return ""
    return str(text).strip().upper()


def _normalize_ocr_input(text: str) -> str:
    cleaned = re.sub(r"[.,;:]+", " ", str(text))
    cleaned = re.sub(r"[^A-Za-z0-9 \-_`'|/]+", " ", cleaned)
    return " ".join(cleaned.upper().split())


def _is_truncated_text(text: str) -> bool:
    t = text.strip()
    if "..." in t or "…" in t:
        return True
    if t.endswith("..") or t.endswith("."):
        return True
    return False


def _match_wordlist_prefix(prefix: str, cfg: OCRConfig) -> Optional[str]:
    if not prefix or len(prefix) < cfg.wordlist_prefix_min_chars:
        return None
    prefix = _normalize_ocr_compare(prefix)
    words, norms, norms_ns, prefix_maps, _ = _load_wordlist_index(cfg.user_words_path)
    if not words:
        return None
    prefix_ns = prefix.replace(" ", "")
    candidates = _prefix_candidates(prefix_ns, prefix_maps)
    if candidates is not None and not candidates:
        return None
    best_i = -1
    best_ratio = 0.0
    best_len = 0
    indices = candidates if candidates is not None else range(len(norms))
    for i in indices:
        norm_word = norms[i]
        if not norm_word:
            continue
        norm_ns = norms_ns[i] if i < len(norms_ns) else norm_word.replace(" ", "")
        if not (norm_word.startswith(prefix) or norm_ns.startswith(prefix_ns)):
            continue
        ratio = len(prefix_ns) / max(1, len(norm_ns))
        if ratio < cfg.wordlist_prefix_min_ratio:
            continue
        if ratio > best_ratio or (ratio == best_ratio and len(norm_word) < best_len):
            best_ratio = ratio
            best_len = len(norm_word)
            best_i = i
    if best_i >= 0:
        return words[best_i]
    return None


def _match_wordlist_short_prefix(prefix: str, cfg: OCRConfig) -> Optional[str]:
    prefix = _normalize_ocr_compare(prefix)
    if not prefix:
        return None
    prefix_ns = prefix.replace(" ", "")
    if len(prefix_ns) < 3:
        return None
    words, norms, norms_ns, prefix_maps, _ = _load_wordlist_index(cfg.user_words_path)
    if not words:
        return None
    candidates = _prefix_candidates(prefix_ns, prefix_maps)
    if candidates is not None and not candidates:
        return None
    best_i = -1
    best_ratio = 0.0
    best_len = 0
    min_ratio = max(cfg.wordlist_prefix_min_ratio, 0.75)
    max_len = 5
    indices = candidates if candidates is not None else range(len(norms))
    for i in indices:
        norm_word = norms[i]
        if not norm_word:
            continue
        norm_ns = norms_ns[i] if i < len(norms_ns) else norm_word.replace(" ", "")
        if len(norm_ns) > max_len:
            continue
        if not (norm_word.startswith(prefix) or norm_ns.startswith(prefix_ns)):
            continue
        ratio = len(prefix_ns) / max(1, len(norm_ns))
        if ratio < min_ratio:
            continue
        if ratio > best_ratio or (ratio == best_ratio and len(norm_word) < best_len):
            best_ratio = ratio
            best_len = len(norm_word)
            best_i = i
    if best_i >= 0:
        return words[best_i]
    return None


def _match_wordlist_substring(substring: str, cfg: OCRConfig) -> Optional[str]:
    if not substring or len(substring) < cfg.wordlist_prefix_min_chars:
        return None
    substring = _normalize_ocr_compare(substring)
    words, norms = _load_wordlist(cfg.user_words_path)
    if not words:
        return None
    sub_ns = substring.replace(" ", "")
    for i, norm_word in enumerate(norms):
        if not norm_word:
            continue
        norm_ns = norm_word.replace(" ", "")
        if sub_ns in norm_ns:
            return words[i]
    return None


def _match_wordlist_close(norm_text: str, cfg: OCRConfig) -> Optional[str]:
    if not norm_text or len(norm_text) < 4:
        return None
    norm_text = _normalize_ocr_compare(norm_text)
    words, norms = _load_wordlist(cfg.user_words_path)
    if not words:
        return None
    best_i = -1
    best_score = 0.0
    best_len = 0
    text_tokens = norm_text.split()
    for i, norm_word in enumerate(norms):
        if not norm_word:
            continue
        max_len = max(len(norm_text), len(norm_word))
        if max_len < 4:
            continue
        max_dist = max(2, int(max_len * 0.3))
        dist = _levenshtein(norm_text, norm_word, max_dist)
        if dist > max_dist:
            continue
        score = 1.0 - (dist / max_len)
        if score < 0.7:
            continue
        if len(text_tokens) > 1:
            cand_tokens = norm_word.split()
            if not any(token in cand_tokens for token in text_tokens):
                continue
        if score > best_score or (score == best_score and len(norm_word) < best_len):
            best_score = score
            best_len = len(norm_word)
            best_i = i
    if best_i >= 0:
        return words[best_i]
    return None


def _match_wordlist_prefix_distance(norm_text: str, cfg: OCRConfig) -> Optional[str]:
    if not norm_text or len(norm_text) < 4:
        return None
    norm_text = _normalize_ocr_compare(norm_text)
    text_ns = norm_text.replace(" ", "")
    if len(text_ns) < 4:
        return None
    words, norms = _load_wordlist(cfg.user_words_path)
    if not words:
        return None
    best_i = -1
    best_dist = 2
    best_len = 0
    max_dist = 1
    for i, norm_word in enumerate(norms):
        if not norm_word:
            continue
        norm_ns = norm_word.replace(" ", "")
        if len(norm_ns) < len(text_ns):
            continue
        candidate = norm_ns[: len(text_ns)]
        dist = _levenshtein(text_ns, candidate, max_dist)
        if dist > max_dist:
            continue
        if dist < best_dist or (dist == best_dist and len(norm_word) < best_len):
            best_dist = dist
            best_len = len(norm_word)
            best_i = i
    if best_i >= 0:
        return words[best_i]
    return None


def _match_wordlist_token_remainder(norm_text: str, cfg: OCRConfig) -> Optional[str]:
    if not norm_text or len(norm_text) < 4:
        return None
    norm_text = _normalize_ocr_compare(norm_text)
    raw_tokens = [token for token in norm_text.split() if token]
    if not raw_tokens:
        return None
    first_token = raw_tokens[0]
    words, norms, _, _, token_index = _load_wordlist_index(cfg.user_words_path)
    if not words:
        return None
    candidate_indices = token_index.get(first_token) if token_index else None
    has_any_exact_first = bool(candidate_indices)

    best_i = -1
    best_score = 0.0
    best_exact = 0
    best_matched = 0
    best_len = 0

    indices = candidate_indices if has_any_exact_first else range(len(norms))
    for i in indices:
        norm_word = norms[i]
        if not norm_word:
            continue
        cand_tokens = [token for token in norm_word.split() if token]
        if not cand_tokens:
            continue
        has_exact_first = first_token in cand_tokens
        if has_any_exact_first and not has_exact_first:
            continue

        cand_counts: Dict[str, int] = {}
        for tok in cand_tokens:
            cand_counts[tok] = cand_counts.get(tok, 0) + 1

        matched_tokens: List[Tuple[str, int]] = []
        raw_remaining: List[str] = []
        for tok in raw_tokens:
            if cand_counts.get(tok, 0) > 0:
                matched_tokens.append((tok, 0))
                cand_counts[tok] -= 1
            else:
                raw_remaining.append(tok)

        def _token_close_prefix_score(raw_tok: str, cand_tok: str, max_dist: int = 2) -> Optional[Tuple[int, float]]:
            if not raw_tok or not cand_tok:
                return None
            raw_ns = raw_tok.replace(" ", "")
            cand_ns = cand_tok.replace(" ", "")
            if not raw_ns or not cand_ns:
                return None
            options: List[str] = []
            if len(cand_ns) >= len(raw_ns):
                options.append(cand_ns[: len(raw_ns)])
                if len(cand_ns) >= len(raw_ns) + 1:
                    options.append(cand_ns[: len(raw_ns) + 1])
            else:
                options.append(cand_ns)
            best_dist = max_dist + 1
            best_len = 0
            for opt in options:
                dist = _levenshtein(raw_ns, opt, max_dist)
                if dist < best_dist:
                    best_dist = dist
                    best_len = max(len(raw_ns), len(opt))
            if best_dist > max_dist:
                return None
            score = 1.0 - (best_dist / max(1, best_len))
            return (best_dist, score)

        close_matches: List[Tuple[str, str, int, float]] = []
        cand_remaining_for_close = [tok for tok, count in cand_counts.items() for _ in range(count)]
        raw_remaining_after_exact: List[str] = []
        first_token_matched = False
        for raw_tok in raw_remaining:
            best = None
            best_idx = -1
            for idx, cand_tok in enumerate(cand_remaining_for_close):
                res = _token_close_prefix_score(raw_tok, cand_tok)
                if res is None:
                    continue
                dist, score = res
                if best is None or dist < best[2] or (dist == best[2] and score > best[3]):
                    best = (raw_tok, cand_tok, dist, score)
                    best_idx = idx
            if best is None:
                raw_remaining_after_exact.append(raw_tok)
                continue
            close_matches.append(best)
            cand_remaining_for_close.pop(best_idx)
            if raw_tok == first_token:
                first_token_matched = True

        if not matched_tokens and not close_matches:
            continue
        if (not has_exact_first) and (not has_any_exact_first) and (not first_token_matched):
            continue

        cand_remaining = cand_remaining_for_close
        raw_remaining = raw_remaining_after_exact

        raw_remain_ns = "".join(raw_remaining)
        cand_remain_ns = "".join(cand_remaining)
        exact_count = len(matched_tokens)
        close_count = len(close_matches)
        matched_count = exact_count + close_count

        if not raw_remain_ns:
            score_sum = sum(1.0 for _ in matched_tokens) + sum(cm[3] for cm in close_matches)
            score = score_sum / max(1, matched_count)
            if score < 0.7:
                continue
        else:
            if len(cand_remain_ns) < len(raw_remain_ns):
                continue
            cand_comp = cand_remain_ns[: len(raw_remain_ns)]
            max_len = max(len(raw_remain_ns), len(cand_comp))
            max_dist = max(1, int(max_len * 0.3))
            dist = _levenshtein(raw_remain_ns, cand_comp, max_dist)
            score = 1.0 - (dist / max_len)
            if score < 0.7 and close_count > 0:
                def _generate_insdel_candidates(raw: str, target: str, cap: int = 64) -> List[str]:
                    candidates: Set[str] = set()
                    for idx in range(len(raw)):
                        candidates.add(raw[:idx] + raw[idx + 1 :])
                        if len(candidates) >= cap:
                            return list(candidates)
                    if target:
                        for idx in range(len(raw) + 1):
                            ch = target[idx] if idx < len(target) else target[-1]
                            candidates.add(raw[:idx] + ch + raw[idx:])
                            if len(candidates) >= cap:
                                break
                    return list(candidates)

                best_alt = score
                for cand_raw in _generate_insdel_candidates(raw_remain_ns, cand_comp):
                    if len(cand_comp) < len(cand_raw):
                        continue
                    comp = cand_comp[: len(cand_raw)]
                    max_len_alt = max(len(cand_raw), len(comp))
                    max_dist_alt = max(1, int(max_len_alt * 0.3))
                    dist_alt = _levenshtein(cand_raw, comp, max_dist_alt)
                    alt_score = 1.0 - (dist_alt / max_len_alt)
                    if alt_score > best_alt:
                        best_alt = alt_score
                    if best_alt >= 0.7:
                        break
                score = best_alt
            if score < 0.7:
                continue

        if (
            score > best_score
            or (score == best_score and exact_count > best_exact)
            or (score == best_score and exact_count == best_exact and matched_count > best_matched)
            or (score == best_score and exact_count == best_exact and matched_count == best_matched and len(norm_word) < best_len)
        ):
            best_score = score
            best_exact = exact_count
            best_matched = matched_count
            best_len = len(norm_word)
            best_i = i

    if best_i >= 0:
        return words[best_i]
    return None


_ORDERED_OCR_CONFUSIONS: Tuple[Tuple[str, Tuple[Tuple[str, str], ...]], ...] = (
    ("I_L_1", (("I", "L"), ("I", "1"), ("L", "1"))),
    ("O_0", (("O", "0"),)),
    ("RN_M", (("RN", "M"),)),
    ("CL_D", (("CL", "D"),)),
    ("LL_U", (("LL", "U"),)),
    ("VV_W", (("VV", "W"),)),
    ("8_B", (("8", "B"),)),
    ("5_S", (("5", "S"),)),
    ("2_Z", (("2", "Z"),)),
    ("6_G", (("6", "G"),)),
    ("9_G", (("9", "G"),)),
    ("C_G", (("C", "G"),)),
    ("O_D", (("O", "D"),)),
    ("B_D", (("B", "D"),)),
    ("P_Q", (("P", "Q"),)),
    ("V_U", (("V", "U"),)),
    ("V_Y", (("V", "Y"),)),
    ("F_E", (("F", "E"),)),
    ("F_P", (("F", "P"),)),
    ("K_R", (("K", "R"),)),
    ("R_P", (("R", "P"),)),
    ("W_VV", (("W", "VV"),)),
    ("M_NN", (("M", "NN"),)),
    ("RI_N", (("RI", "N"),)),
    ("IL_U", (("IL", "U"),)),
    ("DASH_UNDERSCORE", (("-", "_"),)),
    ("APOSTROPHE_BACKTICK", (("'", "`"),)),
    ("PIPE_I", (("|", "I"),)),
    ("SLASH_L", (("/", "L"),)),
)


def _generate_candidates_for_rule(text: str, pairs: Tuple[Tuple[str, str], ...]) -> List[str]:
    if not text:
        return []
    candidates: Set[str] = set()
    for left, right in pairs:
        for src, dst in ((left, right), (right, left)):
            if not src:
                continue
            start = 0
            while start < len(text):
                idx = text.find(src, start)
                if idx < 0:
                    break
                cand = f"{text[:idx]}{dst}{text[idx + len(src):]}"
                if cand != text:
                    candidates.add(cand)
                start = idx + 1
            if src in text:
                cand = text.replace(src, dst)
                if cand != text:
                    candidates.add(cand)
    return list(candidates)


def _best_wordlist_match_from_candidates(
    base: str,
    candidates: List[str],
    cfg: OCRConfig,
    *,
    truncated: bool,
) -> Optional[str]:
    best_word = None
    best_score = 0.0
    best_penalty = 999
    for cand in candidates:
        norm_text = _normalize_word(cand)
        if not norm_text:
            continue
        match = _match_wordlist_for_text(norm_text, cfg, truncated=truncated)
        if not match:
            continue
        score = _score_wordlist_match(norm_text, match)
        penalty = _levenshtein(base, cand, max(len(base), len(cand)))
        if score > best_score or (score == best_score and penalty < best_penalty):
            best_score = score
            best_penalty = penalty
            best_word = match
    return best_word


def _score_wordlist_match(norm_text: str, match_word: str) -> float:
    norm_word = _normalize_word(match_word)
    left = norm_text.replace(" ", "")
    right = norm_word.replace(" ", "")
    if not left or not right:
        return 0.0
    max_len = max(len(left), len(right))
    dist = _levenshtein(left, right, max_len)
    return 1.0 - (dist / max_len)


def _match_wordlist_for_text(norm_text: str, cfg: OCRConfig, *, truncated: bool) -> Optional[str]:
    if not norm_text:
        return None
    if truncated:
        substring_match = _match_wordlist_substring(norm_text, cfg)
        if substring_match:
            return substring_match
        prefix_match = _match_wordlist_prefix(norm_text, cfg)
        if prefix_match:
            return prefix_match
        if len(norm_text) < cfg.wordlist_prefix_min_chars:
            short_prefix_match = _match_wordlist_short_prefix(norm_text, cfg)
            if short_prefix_match:
                return short_prefix_match
        prefix_dist_match = _match_wordlist_prefix_distance(norm_text, cfg)
        if prefix_dist_match:
            return prefix_dist_match
        token_match = _match_wordlist_token_remainder(norm_text, cfg)
        if token_match:
            return token_match
    else:
        prefix_match = _match_wordlist_prefix(norm_text, cfg)
        if prefix_match:
            return prefix_match
        if len(norm_text) < cfg.wordlist_prefix_min_chars:
            short_prefix_match = _match_wordlist_short_prefix(norm_text, cfg)
            if short_prefix_match:
                return short_prefix_match
        prefix_dist_match = _match_wordlist_prefix_distance(norm_text, cfg)
        if prefix_dist_match:
            return prefix_dist_match
        token_match = _match_wordlist_token_remainder(norm_text, cfg)
        if token_match:
            return token_match
    words, norms = _load_wordlist(cfg.user_words_path)
    if not words:
        return None
    best_i = -1
    best_dist = cfg.wordlist_max_distance + 1
    best_ratio = 0.0
    for i, norm_word in enumerate(norms):
        if not norm_word:
            continue
        max_len = max(len(norm_text), len(norm_word))
        dist = _levenshtein(norm_text, norm_word, cfg.wordlist_max_distance)
        if dist > cfg.wordlist_max_distance:
            continue
        ratio = 1.0 - (dist / max_len)
        if dist < best_dist or (dist == best_dist and ratio > best_ratio):
            best_dist = dist
            best_ratio = ratio
            best_i = i
    if best_i >= 0 and best_ratio >= cfg.wordlist_min_ratio:
        return words[best_i]
    if len(norm_text) < cfg.wordlist_prefix_min_chars:
        short_prefix_match = _match_wordlist_short_prefix(norm_text, cfg)
        if short_prefix_match:
            return short_prefix_match
    # If no close edit-distance match, try prefix match even without ellipsis.
    prefix_match = _match_wordlist_prefix(norm_text, cfg)
    if prefix_match:
        return prefix_match
    close_match = _match_wordlist_close(norm_text, cfg)
    if close_match:
        return close_match
    return None


def _best_wordlist_fallback(norm_text: str, cfg: OCRConfig) -> Optional[str]:
    words, norms = _load_wordlist(cfg.user_words_path)
    if not words:
        return None
    text_ns = norm_text.replace(" ", "")
    if not text_ns:
        return None
    tokens = [token for token in norm_text.split() if token]
    first_token = tokens[0] if tokens else ""

    def _best_from_indices(indices: List[int]) -> Optional[str]:
        best_i = -1
        best_score = -1.0
        best_len = 0
        for i in indices:
            norm_word = norms[i]
            if not norm_word:
                continue
            word_ns = norm_word.replace(" ", "")
            max_len = max(len(text_ns), len(word_ns))
            dist = _levenshtein(text_ns, word_ns, max_len)
            score = 1.0 - (dist / max_len)
            if score > best_score or (score == best_score and len(norm_word) < best_len):
                best_score = score
                best_len = len(norm_word)
                best_i = i
        return words[best_i] if best_i >= 0 else None

    if first_token:
        exact_indices = [i for i, norm in enumerate(norms) if first_token in norm.split()]
        if exact_indices:
            return _best_from_indices(exact_indices)
        close_indices: List[int] = []
        for i, norm in enumerate(norms):
            for tok in norm.split():
                if _levenshtein(first_token, tok[: len(first_token)], 2) <= 2:
                    close_indices.append(i)
                    break
        if close_indices:
            return _best_from_indices(close_indices)

    return _best_from_indices(list(range(len(norms))))


def _build_prefix_maps(norms_ns: List[str], max_len: int) -> Dict[int, Dict[str, List[int]]]:
    maps: Dict[int, Dict[str, List[int]]] = {length: {} for length in range(1, max_len + 1)}
    for i, norm_ns in enumerate(norms_ns):
        if not norm_ns:
            continue
        for length in range(1, max_len + 1):
            if len(norm_ns) < length:
                break
            key = norm_ns[:length]
            bucket = maps[length].get(key)
            if bucket is None:
                maps[length][key] = [i]
            else:
                bucket.append(i)
    return maps


def _split_wordlist_paths(path: Optional[str]) -> List[str]:
    if not path:
        return []
    return [part.strip() for part in str(path).split(_WORDLIST_MULTI_SEP) if part.strip()]


def _wordlist_cache_key(path: Optional[str]) -> str:
    parts = _split_wordlist_paths(path)
    if not parts:
        return ""
    resolved_parts: List[str] = []
    for part in parts:
        try:
            resolved_parts.append(str(Path(part).resolve()))
        except Exception:
            resolved_parts.append(str(part))
    return _WORDLIST_MULTI_SEP.join(resolved_parts)


def _combine_wordlist_paths(primary: Optional[str], secondary: Optional[str]) -> Optional[str]:
    combined: List[str] = []
    seen: Set[str] = set()
    for part in _split_wordlist_paths(primary) + _split_wordlist_paths(secondary):
        if part in seen:
            continue
        seen.add(part)
        combined.append(part)
    if not combined:
        return None
    return _WORDLIST_MULTI_SEP.join(combined)


def _load_wordlist_index(
    path: Optional[str],
) -> Tuple[List[str], List[str], List[str], Dict[int, Dict[str, List[int]]], Dict[str, List[int]]]:
    words, norms = _load_wordlist(path)
    if not path:
        return (words, norms, [], {}, {})
    key = _wordlist_cache_key(path)
    norms_ns = _WORDLIST_NORM_NS_CACHE.get(key, [])
    prefix_maps = _WORDLIST_PREFIX_CACHE.get(key, {})
    token_index = _WORDLIST_TOKEN_INDEX_CACHE.get(key, {})
    return (words, norms, norms_ns, prefix_maps, token_index)


def _prefix_candidates(prefix_ns: str, prefix_maps: Dict[int, Dict[str, List[int]]]) -> Optional[List[int]]:
    if not prefix_ns or not prefix_maps:
        return None
    plen = min(len(prefix_ns), _WORDLIST_PREFIX_MAX_LEN)
    table = prefix_maps.get(plen)
    if table is None:
        return None
    return table.get(prefix_ns[:plen], [])


def _load_wordlist(path: Optional[str]) -> Tuple[List[str], List[str]]:
    if not path:
        return ([], [])
    parts = _split_wordlist_paths(path)
    if not parts:
        return ([], [])
    key = _wordlist_cache_key(path)
    if (
        key in _WORDLIST_CACHE
        and key in _WORDLIST_NORM_CACHE
        and key in _WORDLIST_NORM_NS_CACHE
        and key in _WORDLIST_TOKEN_INDEX_CACHE
        and key in _WORDLIST_NORM_MAP_CACHE
    ):
        return (_WORDLIST_CACHE[key], _WORDLIST_NORM_CACHE[key])
    if not any(Path(raw_path).exists() for raw_path in parts):
        _WORDLIST_CACHE[key] = []
        _WORDLIST_NORM_CACHE[key] = []
        _WORDLIST_NORM_NS_CACHE[key] = []
        _WORDLIST_PREFIX_CACHE[key] = {}
        _WORDLIST_TOKEN_INDEX_CACHE[key] = {}
        _WORDLIST_NORM_MAP_CACHE[key] = {}
        return ([], [])
    words: List[str] = []
    norms: List[str] = []
    try:
        for raw_path in parts:
            p = Path(raw_path)
            if not p.exists():
                continue
            paths: List[Path]
            if p.is_dir():
                paths = sorted(p.glob("*.txt"))
            else:
                paths = [p]
            for file_path in paths:
                for line in file_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    words.append(line)
                    norms.append(_normalize_word(line))
    except Exception:
        words = []
        norms = []
    _WORDLIST_CACHE[key] = words
    _WORDLIST_NORM_CACHE[key] = norms
    norms_ns = [norm.replace(" ", "") for norm in norms]
    _WORDLIST_NORM_NS_CACHE[key] = norms_ns
    _WORDLIST_PREFIX_CACHE[key] = _build_prefix_maps(norms_ns, _WORDLIST_PREFIX_MAX_LEN)
    token_index: Dict[str, List[int]] = {}
    norm_map: Dict[str, str] = {}
    for i, norm in enumerate(norms):
        if not norm:
            continue
        if norm not in norm_map:
            norm_map[norm] = words[i]
        for tok in set(norm.split()):
            if not tok:
                continue
            bucket = token_index.get(tok)
            if bucket is None:
                token_index[tok] = [i]
            else:
                bucket.append(i)
    _WORDLIST_TOKEN_INDEX_CACHE[key] = token_index
    _WORDLIST_NORM_MAP_CACHE[key] = norm_map
    return (words, norms)


def _wordlist_path_for_side(cfg: OCRConfig, side: Optional[str]) -> Optional[str]:
    mode = (cfg.name_resolution_mode or "pve").strip().lower()
    if mode == "pvp":
        return cfg.wordlist_wizards_path or cfg.user_words_path
    if mode == "pve":
        if side == "enemy":
            return cfg.wordlist_monsters_path or cfg.user_words_path
        if side == "ally":
            return cfg.wordlist_wizards_path or cfg.user_words_path
    return cfg.user_words_path


def _wordlist_cfg_for_side(cfg: OCRConfig, side: Optional[str]) -> OCRConfig:
    path = _wordlist_path_for_side(cfg, side)
    if path == cfg.user_words_path:
        return cfg
    return replace(cfg, user_words_path=path)


def _should_use_wizard_wordlist(cfg: OCRConfig, side: Optional[str]) -> bool:
    mode = (cfg.name_resolution_mode or "pve").strip().lower()
    if mode == "pvp":
        return True
    if mode == "pve":
        return side == "ally"
    return False


def _levenshtein(a: str, b: str, max_dist: int) -> int:
    if a == b:
        return 0
    if not a or not b:
        return max(len(a), len(b))
    if abs(len(a) - len(b)) > max_dist:
        return max_dist + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i]
        row_min = cur[0]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            val = min(
                prev[j] + 1,
                cur[j - 1] + 1,
                prev[j - 1] + cost,
            )
            cur.append(val)
            if val < row_min:
                row_min = val
        if row_min > max_dist:
            return max_dist + 1
        prev = cur
    return prev[-1]


def _apply_wordlist_correction_for_cfg(text: Optional[str], cfg: OCRConfig) -> Optional[str]:
    if not text:
        return text
    truncated = _is_truncated_text(text)
    base = _normalize_ocr_input(text.replace("â€¦", "...").replace(".", " "))
    if not base:
        return text
    base_norm = _normalize_word(base)
    words, norms = _load_wordlist(cfg.user_words_path)
    if cfg.user_words_path:
        key = _wordlist_cache_key(cfg.user_words_path)
        norm_map = _WORDLIST_NORM_MAP_CACHE.get(key, {})
        direct = norm_map.get(base_norm)
        if direct:
            return direct
    base_tokens = base_norm.split() if base_norm else []
    base_first_token = base_tokens[0] if base_tokens else ""
    has_any_exact_first = False
    if base_first_token and norms:
        has_any_exact_first = any(base_first_token in norm.split() for norm in norms)

    def _accept_match(match_word: Optional[str]) -> bool:
        if not match_word:
            return False
        if not has_any_exact_first:
            return True
        return base_first_token in _normalize_word(match_word).split()

    direct_match = _match_wordlist_for_text(base_norm, cfg, truncated=truncated)
    if direct_match and _accept_match(direct_match):
        return direct_match
    for _, pairs in _ORDERED_OCR_CONFUSIONS:
        candidates = _generate_candidates_for_rule(base, pairs)
        if not candidates:
            continue
        match = _best_wordlist_match_from_candidates(base, candidates, cfg, truncated=truncated)
        if match and _accept_match(match):
            return match
    fallback = _best_wordlist_fallback(base_norm, cfg)
    return fallback if fallback else text


def _is_confident_wordlist_match(base_norm: str, corrected: Optional[str], cfg: OCRConfig) -> bool:
    if not corrected or not base_norm:
        return False
    norm_corrected = _normalize_word(corrected)
    if not norm_corrected:
        return False
    _, norms = _load_wordlist(cfg.user_words_path)
    if norm_corrected not in norms:
        return False
    return _score_wordlist_match(base_norm, corrected) >= cfg.wordlist_min_ratio


def _apply_wordlist_correction(text: Optional[str], cfg: OCRConfig, *, side: Optional[str] = None) -> Optional[str]:
    if not text:
        return text
    active_cfg = _wordlist_cfg_for_side(cfg, side)
    primary = _apply_wordlist_correction_for_cfg(text, active_cfg)
    if not _should_use_wizard_wordlist(cfg, side):
        return primary
    if not cfg.wordlist_minions_path:
        return primary

    base = _normalize_ocr_input(text.replace("â€¦", "...").replace(".", " "))
    base_norm = _normalize_word(base) if base else ""
    if _is_confident_wordlist_match(base_norm, primary, active_cfg):
        return primary

    expanded_path = _combine_wordlist_paths(active_cfg.user_words_path, cfg.wordlist_minions_path)
    if (not expanded_path) or expanded_path == active_cfg.user_words_path:
        return primary
    expanded_cfg = replace(active_cfg, user_words_path=expanded_path)
    expanded = _apply_wordlist_correction_for_cfg(text, expanded_cfg)
    return expanded if expanded else primary


def _easyocr_text(
    img_bgr: np.ndarray,
    cfg: OCRConfig,
    whitelist: str,
    *,
    invert_override: Optional[bool] = None,
    prefer_red: bool = False,
    clahe: bool = False,
    name_mode: bool = False,
    debug_tag: Optional[str] = None,
    debug_dump: bool = False,
    debug_dump_id: Optional[str] = None,
    debug_dump_limit: int = 0,
) -> Optional[str]:
    if img_bgr.size == 0:
        return None
    invert = cfg.invert if invert_override is None else invert_override
    if name_mode:
        prepped = _prep_ocr_name(img_bgr, cfg.scale, invert)
    else:
        prepped = _prep_easyocr_image(
            img_bgr,
            cfg,
            invert=invert,
            prefer_red=prefer_red,
            clahe=clahe,
        )
    if debug_dump and debug_tag and _allow_ocr_dump(debug_dump_id, debug_dump_limit):
        try:
            stamp = f"{int(time.time() * 1000)}"
            raw_path = _OCR_DUMP_DIR / f"{debug_tag}_{stamp}_raw.png"
            prep_path = _OCR_DUMP_DIR / f"{debug_tag}_{stamp}_prep.png"
            cv2.imwrite(str(raw_path), img_bgr)
            cv2.imwrite(str(prep_path), prepped)
        except Exception:
            pass
    try:
        from ocr_easy.adapter import read_text
    except Exception as exc:
        global _EASYOCR_WARNED
        if not _EASYOCR_WARNED:
            print(f"[ocr] easyocr unavailable: {exc}")
            _EASYOCR_WARNED = True
        return None

    allowlist = whitelist if whitelist else None
    try:
        return read_text(prepped, cfg, allowlist=allowlist)
    except Exception:
        return None


@dataclass
class _NameWorkItem:
    key: Tuple[str, int]
    crop: np.ndarray
    tag: str
    dump_id: Optional[str]
    start_time: float
    raw: Optional[str] = None
    end_time: Optional[float] = None
    capture_ms: float = 0.0
    preprocess_ms: float = 0.0
    ocr_share_ms: float = 0.0
    resolve_ms: float = 0.0


def _pad_batch_images(imgs: List[np.ndarray]) -> List[np.ndarray]:
    if not imgs:
        return imgs
    fixed: List[np.ndarray] = []
    max_h = 0
    max_w = 0
    for img in imgs:
        if not isinstance(img, np.ndarray) or img.size == 0:
            continue
        h, w = img.shape[:2]
        max_h = max(max_h, h)
        max_w = max(max_w, w)
    if max_h == 0 or max_w == 0:
        return imgs
    for img in imgs:
        if not isinstance(img, np.ndarray) or img.size == 0:
            fixed.append(np.full((max_h, max_w), 255, dtype=np.uint8))
            continue
        h, w = img.shape[:2]
        pad_h = max_h - h
        pad_w = max_w - w
        top = pad_h // 2
        bottom = pad_h - top
        left = pad_w // 2
        right = pad_w - left
        if img.ndim == 2:
            fixed.append(cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=255))
        else:
            channels = img.shape[2]
            value = tuple([255] * channels)
            fixed.append(cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=value))
    return fixed


def _batch_easyocr_names(
    items: List[_NameWorkItem],
    cfg: OCRConfig,
    *,
    debug_dump: bool,
    debug_dump_limit: int,
) -> Dict[Tuple[str, int], Tuple[Optional[str], Optional[str], Optional[float], Optional[Tuple[float, float, float, float]]]]:
    if not items:
        return {}
    try:
        from ocr_easy.adapter import read_text_batch
    except Exception as exc:
        global _EASYOCR_WARNED
        if not _EASYOCR_WARNED:
            print(f"[ocr] easyocr unavailable: {exc}")
            _EASYOCR_WARNED = True
        return {}

    attempts = [
        {"name_mode": True, "invert": None, "whitelist": cfg.name_whitelist, "clahe": True, "prefer_red": False},
        {"name_mode": True, "invert": True, "whitelist": cfg.name_whitelist, "clahe": True, "prefer_red": False},
        {"name_mode": True, "invert": None, "whitelist": cfg.name_whitelist, "clahe": True, "prefer_red": False},
        {"name_mode": True, "invert": True, "whitelist": cfg.name_whitelist, "clahe": True, "prefer_red": False},
        {"name_mode": True, "invert": None, "whitelist": cfg.name_whitelist, "clahe": True, "prefer_red": False},
        {"name_mode": True, "invert": None, "whitelist": "", "clahe": True, "prefer_red": False},
        {"name_mode": False, "invert": None, "whitelist": cfg.name_whitelist, "clahe": True, "prefer_red": False},
    ]
    seen = set()
    deduped = []
    for att in attempts:
        key = (att["name_mode"], att["invert"], att["whitelist"], att["clahe"], att["prefer_red"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(att)

    variant_keys: List[Tuple[bool, Optional[bool], str, bool, bool]] = []
    for att in deduped:
        variant_keys.append((att["name_mode"], att["invert"], att["whitelist"], att["clahe"], att["prefer_red"]))

    prepped_cache: Dict[Tuple[str, int], Dict[Tuple[bool, Optional[bool], str, bool, bool], np.ndarray]] = {}

    def _prep_for_variant(
        item: _NameWorkItem,
        key: Tuple[bool, Optional[bool], str, bool, bool],
    ) -> np.ndarray:
        name_mode, invert_flag, _whitelist, clahe, prefer_red = key
        invert = cfg.invert if invert_flag is None else invert_flag
        prep_start = time.perf_counter()
        if name_mode:
            prepped = _prep_ocr_name(item.crop, cfg.scale, invert)
        else:
            prepped = _prep_easyocr_image(
                item.crop,
                cfg,
                invert=invert,
                prefer_red=prefer_red,
                clahe=clahe,
            )
        item.preprocess_ms += (time.perf_counter() - prep_start) * 1000.0
        return prepped

    for attempt_idx, (att, key) in enumerate(zip(deduped, variant_keys)):
        pending = [item for item in items if item.raw is None]
        if not pending:
            break
        prepped_imgs: List[np.ndarray] = []
        if attempt_idx == 0:
            for item in pending:
                prepped = _prep_for_variant(item, key)
                prepped_cache.setdefault(item.key, {})[key] = prepped
                prepped_imgs.append(prepped)
        else:
            for item in pending:
                prepped = prepped_cache[item.key][key]
                prepped_imgs.append(prepped)
            if debug_dump and item.tag and _allow_ocr_dump(item.dump_id, debug_dump_limit):
                try:
                    stamp = f"{int(time.time() * 1000)}"
                    raw_path = _OCR_DUMP_DIR / f"{item.tag}_{stamp}_raw.png"
                    prep_path = _OCR_DUMP_DIR / f"{item.tag}_{stamp}_prep.png"
                    cv2.imwrite(str(raw_path), item.crop)
                    cv2.imwrite(str(prep_path), prepped)
                except Exception:
                    pass
        prepped_imgs = _pad_batch_images(prepped_imgs)
        ocr_start = time.perf_counter()
        texts = read_text_batch(prepped_imgs, cfg, allowlist=att["whitelist"])
        ocr_ms = (time.perf_counter() - ocr_start) * 1000.0
        if pending:
            ocr_share = ocr_ms / len(pending)
            for item in pending:
                item.ocr_share_ms += ocr_share
        for item, text in zip(pending, texts):
            if text:
                item.raw = text
                item.end_time = time.perf_counter()

        if attempt_idx == 0:
            pending_after = [item for item in items if item.raw is None]
            if pending_after:
                for item in pending_after:
                    cache = prepped_cache.setdefault(item.key, {})
                    for later_key in variant_keys[1:]:
                        if later_key in cache:
                            continue
                        cache[later_key] = _prep_for_variant(item, later_key)

    end_all = time.perf_counter()
    results: Dict[Tuple[str, int], Tuple[Optional[str], Optional[str], Optional[float], Optional[Tuple[float, float, float, float]]]] = {}
    for item in items:
        if item.end_time is None:
            item.end_time = end_all
        resolve_start = time.perf_counter()
        final = _apply_wordlist_correction(item.raw, cfg, side=item.key[0])
        item.resolve_ms += (time.perf_counter() - resolve_start) * 1000.0
        elapsed_ms = item.capture_ms + item.preprocess_ms + item.ocr_share_ms + item.resolve_ms
        parts = (item.capture_ms, item.preprocess_ms, item.ocr_share_ms, item.resolve_ms)
        results[item.key] = (item.raw, final, elapsed_ms, parts)
    return results


def _ocr_text(
    img_bgr: np.ndarray,
    cfg: OCRConfig,
    whitelist: str,
    *,
    invert_override: Optional[bool] = None,
    prefer_red: bool = False,
    clahe: bool = False,
    psm_override: Optional[int] = None,
    name_mode: bool = False,
    debug_tag: Optional[str] = None,
    debug_dump: bool = False,
    debug_dump_id: Optional[str] = None,
    debug_dump_limit: int = 0,
    blacklist: Optional[str] = None,
    backend_override: Optional[str] = None,
) -> Optional[str]:
    backend = backend_override or cfg.backend
    if backend == "easyocr":
        return _easyocr_text(
            img_bgr,
            cfg,
            whitelist,
            invert_override=invert_override,
            prefer_red=prefer_red,
            clahe=clahe,
            name_mode=name_mode,
            debug_tag=debug_tag,
            debug_dump=debug_dump,
            debug_dump_id=debug_dump_id,
            debug_dump_limit=debug_dump_limit,
        )
    if pytesseract is None or img_bgr.size == 0:
        return None
    if cfg.tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = cfg.tesseract_cmd

    invert = cfg.invert if invert_override is None else invert_override
    if name_mode:
        prepped = _prep_ocr_name(img_bgr, cfg.scale, invert)
    else:
        if prefer_red:
            hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            lower1 = np.array([0, 120, 80])
            upper1 = np.array([10, 255, 255])
            lower2 = np.array([170, 120, 80])
            upper2 = np.array([179, 255, 255])
            mask1 = cv2.inRange(hsv, lower1, upper1)
            mask2 = cv2.inRange(hsv, lower2, upper2)
            mask = cv2.bitwise_or(mask1, mask2)
            gray = cv2.bitwise_and(hsv[:, :, 2], hsv[:, :, 2], mask=mask)
        else:
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        if clahe:
            clahe_op = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray = clahe_op.apply(gray)

        prepped = _prep_ocr(gray, cfg.scale, invert)
    if debug_dump and debug_tag and _allow_ocr_dump(debug_dump_id, debug_dump_limit):
        try:
            stamp = f"{int(time.time() * 1000)}"
            raw_path = _OCR_DUMP_DIR / f"{debug_tag}_{stamp}_raw.png"
            prep_path = _OCR_DUMP_DIR / f"{debug_tag}_{stamp}_prep.png"
            cv2.imwrite(str(raw_path), img_bgr)
            cv2.imwrite(str(prep_path), prepped)
        except Exception:
            pass
    psm = cfg.psm if psm_override is None else psm_override
    config = f"--oem {cfg.oem} --psm {psm}"
    if name_mode:
        config += " -c user_defined_dpi=300"
        if cfg.user_words_path:
            user_words_path = Path(cfg.user_words_path)
            if user_words_path.is_file():
                user_words = str(user_words_path)
                config += f" --user-words \"{user_words}\""
    if whitelist:
        config += f" -c tessedit_char_whitelist={whitelist}"
    if blacklist:
        config += f" -c tessedit_char_blacklist={blacklist}"
    try:
        ocr_img = prepped
        if name_mode:
            ocr_img = _crop_to_foreground(ocr_img, pad=6)
        text = pytesseract.image_to_string(ocr_img, lang=cfg.lang, config=config)
    except Exception:
        return None
    text = text.strip().replace("\n", " ").strip()
    return text or None


_HEALTH_NUM_RE = re.compile(r"\d+")


def _normalize_health_text(text: str) -> str:
    cleaned = str(text)
    cleaned = cleaned.translate(str.maketrans({"\\": "/", "|": "/", "I": "/", "l": "/", "i": "/"}))
    cleaned = re.sub(r"[^0-9,/\s]", "", cleaned)
    return cleaned.replace(" ", "")


def _parse_health(text: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    if not text:
        return (None, None)
    normalized = _normalize_health_text(text).replace(",", "")
    if not normalized:
        return (None, None)
    if "/" in normalized:
        left, right = normalized.split("/", 1)
        right = right.split("/", 1)[0]
        left_digits = "".join(ch for ch in left if ch.isdigit())
        right_digits = "".join(ch for ch in right if ch.isdigit())
        try:
            cur = int(left_digits) if left_digits else None
            maxv = int(right_digits) if right_digits else None
            if cur is None and maxv is None:
                return (None, None)
            return (cur, maxv)
        except Exception:
            return (None, None)
    nums = _HEALTH_NUM_RE.findall(normalized)
    if len(nums) >= 1:
        try:
            return (int(nums[0]), None)
        except Exception:
            return (None, None)
    return (None, None)


def _health_score(cur: Optional[int], maxv: Optional[int]) -> int:
    cur_len = len(str(cur)) if cur is not None else 0
    max_len = len(str(maxv)) if maxv is not None else 0
    score = (cur_len * 2) + max_len
    if cur is not None and maxv is not None:
        if maxv < cur:
            score -= 6
        if abs(max_len - cur_len) > 1:
            score -= 2
    return score


def _normalize_health_pair(cur: Optional[int], maxv: Optional[int]) -> Tuple[Optional[int], Optional[int]]:
    if cur is None or maxv is None:
        return (cur, maxv)
    cur_s = str(cur)
    max_s = str(maxv)
    if len(max_s) == len(cur_s) + 1:
        best = None
        best_delta = None
        for i in range(len(max_s)):
            cand_s = max_s[:i] + max_s[i + 1 :]
            if not cand_s:
                continue
            try:
                cand = int(cand_s)
            except Exception:
                continue
            if cand < cur:
                continue
            delta = abs(cand - cur)
            if best is None or delta < best_delta:
                best = cand
                best_delta = delta
        if best is not None:
            maxv = best
    elif len(cur_s) == len(max_s) + 1 and cur > maxv:
        best = None
        best_delta = None
        for i in range(len(cur_s)):
            cand_s = cur_s[:i] + cur_s[i + 1 :]
            if not cand_s:
                continue
            try:
                cand = int(cand_s)
            except Exception:
                continue
            if cand > maxv:
                continue
            delta = abs(cand - maxv)
            if best is None or delta < best_delta:
                best = cand
                best_delta = delta
        if best is not None:
            cur = best
    return (cur, maxv)


def _easyocr_health(img_bgr: np.ndarray, cfg: OCRConfig) -> Tuple[Optional[int], Optional[int], Optional[str]]:
    if img_bgr.size == 0:
        return (None, None, None)
    try:
        from ocr_easy.adapter import read_text, read_text_with_boxes
    except Exception:
        return (None, None, None)

    def _read_combined(prepped: np.ndarray) -> str:
        results = read_text_with_boxes(prepped, cfg, allowlist="0123456789/,")
        if results:
            def _x_min(bbox: List[Tuple[float, float]]) -> float:
                return min((pt[0] for pt in bbox), default=0.0)

            parts = []
            for bbox, text, _ in sorted(results, key=lambda item: _x_min(item[0])):
                cleaned = text.replace(" ", "").replace(",", "")
                if cleaned:
                    parts.append(cleaned)
            if parts:
                return " ".join(parts)
        return read_text(prepped, cfg, allowlist="0123456789/,") or ""

    def _parse_text(text: str) -> Tuple[Optional[int], Optional[int]]:
        cur, maxv = _parse_health(text)
        if cur is not None or maxv is not None:
            return (cur, maxv)
        nums = _HEALTH_NUM_RE.findall(text or "")
        if len(nums) >= 2:
            return (int(nums[0]), int(nums[1]))
        if len(nums) == 1:
            return (int(nums[0]), None)
        return (None, None)

    best_cur = None
    best_max = None
    best_text = None

    attempts = [
        (False, True, False),
        (True, True, False),
        (False, True, True),
        (True, True, True),
        (False, False, False),
        (True, False, False),
    ]
    for invert, clahe, binarize in attempts:
        prepped = _prep_easyocr_image(
            img_bgr,
            cfg,
            invert=invert,
            prefer_red=True,
            clahe=clahe,
            binarize=binarize,
        )
        text = _read_combined(prepped)
        cur, maxv = _parse_text(text)
        if cur is not None:
            best_cur = cur
            best_text = text
        if maxv is not None:
            best_max = maxv
            best_text = text
        if cur is not None and maxv is not None:
            return (cur, maxv, text or None)

    if best_cur is not None or best_max is not None:
        return (best_cur, best_max, best_text)
    return (None, None, None)


def _ocr_health(img_bgr: np.ndarray, cfg: OCRConfig) -> Tuple[Optional[int], Optional[int], Optional[str]]:
    candidates: List[Tuple[int, Optional[int], Optional[int], Optional[str]]] = []

    def _try(text: Optional[str]) -> None:
        if not text:
            return
        cur, maxv = _parse_health(text)
        cur, maxv = _normalize_health_pair(cur, maxv)
        if cur is None and maxv is None:
            return
        candidates.append((_health_score(cur, maxv), cur, maxv, text.strip()))

    if cfg.backend == "easyocr":
        easy_cur, easy_max, easy_text = _easyocr_health(img_bgr, cfg)
        easy_cur, easy_max = _normalize_health_pair(easy_cur, easy_max)
        if easy_cur is not None or easy_max is not None:
            candidates.append((_health_score(easy_cur, easy_max), easy_cur, easy_max, easy_text))

    _try(_ocr_text(img_bgr, cfg, cfg.health_whitelist, prefer_red=True, clahe=True, psm_override=7))
    _try(
        _ocr_text(
            img_bgr,
            cfg,
            cfg.health_whitelist,
            prefer_red=True,
            clahe=True,
            invert_override=True,
            psm_override=7,
        )
    )
    _try(
        _ocr_text(
            img_bgr,
            cfg,
            cfg.health_whitelist,
            prefer_red=True,
            invert_override=True,
            psm_override=7,
        )
    )
    _try(_ocr_text(img_bgr, cfg, cfg.health_whitelist, prefer_red=True, psm_override=7))

    best = max(candidates, key=lambda item: item[0], default=None)
    if best is None:
        return (None, None, None)
    return (best[1], best[2], best[3])


def _ocr_yellow_numeric_text(
    img_bgr: np.ndarray,
    cfg: OCRConfig,
    *,
    strict_mask: bool = False,
) -> Optional[str]:
    if pytesseract is None or img_bgr.size == 0:
        return None
    if cfg.tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = cfg.tesseract_cmd
    whitelist = cfg.player_resource_whitelist or "0123456789"
    attempts = [
        (False, 7),
        (True, 7),
        (False, 6),
        (True, 6),
    ]
    best_text = None
    best_score = -1
    for invert, psm in attempts:
        prepped = _prep_tesseract_yellow_numeric(img_bgr, cfg, invert=invert, strict=strict_mask)
        config = f"--oem {cfg.oem} --psm {psm} -c tessedit_char_whitelist={whitelist}"
        try:
            text = pytesseract.image_to_string(prepped, lang=cfg.lang, config=config)
        except Exception:
            text = ""
        text = text.strip().replace("\n", " ").strip()
        if not text:
            continue
        score = (len(_HEALTH_NUM_RE.findall(text)) * 10) + len(text)
        if score > best_score:
            best_text = text
            best_score = score
    return best_text


def _parse_resource_numbers(text: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    if not text:
        return (None, None)
    cur, maxv = _parse_health(text)
    if cur is not None or maxv is not None:
        return (cur, maxv)
    normalized = _normalize_health_text(text).replace(",", "")
    nums = _HEALTH_NUM_RE.findall(normalized)
    if not nums:
        return (None, None)
    try:
        return (int(nums[0]), int(nums[1]) if len(nums) > 1 else None)
    except Exception:
        return (None, None)


def extract_player_wizard_state(
    frame_bgr: np.ndarray,
    participants: ParticipantsState,
    ocr_cfg: OCRConfig,
    hud_profile: PlayerHUDProfile,
    *,
    previous: Optional[PlayerWizardState] = None,
    timestamp: Optional[float] = None,
    debug_dump_rois: bool = False,
    resolve_slot_lookup: bool = True,
    slot_confirm_rounds: int = 2,
    scan_health: bool = True,
    scan_mana: bool = True,
    scan_energy: bool = False,
) -> PlayerWizardState:
    carry = previous if previous is not None else PlayerWizardState()
    health_crop = crop_relative(frame_bgr, hud_profile.health_roi) if scan_health else None
    mana_crop = crop_relative(frame_bgr, hud_profile.mana_roi) if scan_mana else None
    energy_crop = crop_relative(frame_bgr, hud_profile.energy_roi) if scan_energy else None

    if debug_dump_rois:
        try:
            dump_dir = Path("debug/player_wizard")
            dump_dir.mkdir(parents=True, exist_ok=True)
            if health_crop is not None and health_crop.size > 0:
                cv2.imwrite(str(dump_dir / "player_health_roi.png"), health_crop)
            if mana_crop is not None and mana_crop.size > 0:
                cv2.imwrite(str(dump_dir / "player_mana_roi.png"), mana_crop)
            if energy_crop is not None and energy_crop.size > 0:
                cv2.imwrite(str(dump_dir / "player_energy_roi.png"), energy_crop)

            # Also dump yellow-masked prep images to aid OCR tuning.
            if health_crop is not None and health_crop.size > 0:
                cv2.imwrite(
                    str(dump_dir / "player_health_roi_prepped.png"),
                    _prep_tesseract_yellow_numeric(health_crop, ocr_cfg, invert=False, strict=False),
                )
            if mana_crop is not None and mana_crop.size > 0:
                cv2.imwrite(
                    str(dump_dir / "player_mana_roi_prepped.png"),
                    _prep_tesseract_yellow_numeric(mana_crop, ocr_cfg, invert=False, strict=False),
                )
            if energy_crop is not None and energy_crop.size > 0:
                cv2.imwrite(
                    str(dump_dir / "player_energy_roi_prepped.png"),
                    _prep_tesseract_yellow_numeric(energy_crop, ocr_cfg, invert=False, strict=True),
                )
        except Exception:
            pass

    if scan_health and health_crop is not None and health_crop.size > 0:
        health_raw = _ocr_yellow_numeric_text(health_crop, ocr_cfg, strict_mask=False)
        hud_cur, hud_max = _parse_resource_numbers(health_raw)
    else:
        health_raw = carry.health_raw
        hud_cur, hud_max = (carry.health_current, carry.health_max)

    if scan_mana and mana_crop is not None and mana_crop.size > 0:
        mana_raw = _ocr_yellow_numeric_text(mana_crop, ocr_cfg, strict_mask=False)
        mana_cur, mana_max = _parse_resource_numbers(mana_raw)
    else:
        mana_raw = carry.mana_raw
        mana_cur, mana_max = (carry.mana_current, carry.mana_max)
    if mana_cur is None and carry.mana_current is not None:
        mana_cur = carry.mana_current
    if mana_max is None and carry.mana_max is not None:
        mana_max = carry.mana_max
    if (not mana_raw) and carry.mana_raw:
        mana_raw = carry.mana_raw

    if scan_energy and energy_crop is not None and energy_crop.size > 0:
        energy_raw = _ocr_yellow_numeric_text(energy_crop, ocr_cfg, strict_mask=True)
        energy_cur, energy_max = _parse_resource_numbers(energy_raw)
    else:
        energy_raw = carry.energy_raw
        energy_cur, energy_max = (carry.energy_current, carry.energy_max)
    if energy_cur is None and carry.energy_current is not None:
        energy_cur = carry.energy_current
    if energy_max is None and carry.energy_max is not None:
        energy_max = carry.energy_max
    if (not energy_raw) and carry.energy_raw:
        energy_raw = carry.energy_raw

    matches: List[ParticipantState] = []
    if resolve_slot_lookup and participants and participants.detected and hud_cur is not None:
        for ally in participants.allies:
            if (ally is None) or (not ally.occupied):
                continue
            if ally.health_current == hud_cur:
                matches.append(ally)

    selected: Optional[ParticipantState] = None
    slot_matched_by_health = False
    defaulted_to_last_slot = False
    if matches:
        if carry.slot_index is not None:
            for cand in matches:
                if cand.index == carry.slot_index:
                    selected = cand
                    break
        if selected is None:
            selected = matches[0]
        slot_matched_by_health = selected is not None

    # If this scan cannot resolve slot by health, default to the last known slot.
    if (selected is None) and (carry.slot_index is not None) and participants and participants.detected:
        for ally in participants.allies:
            if (ally is None) or (not ally.occupied):
                continue
            if ally.index == carry.slot_index:
                selected = ally
                defaulted_to_last_slot = True
                break

    if slot_confirm_rounds < 1:
        slot_confirm_rounds = 1
    if slot_matched_by_health and selected is not None and (not defaulted_to_last_slot):
        if carry.matched and carry.slot_index == selected.index:
            base_streak = carry.slot_confirm_streak if carry.slot_confirm_streak > 0 else 1
            slot_confirm_streak = base_streak + 1
        else:
            slot_confirm_streak = 1
    else:
        slot_confirm_streak = carry.slot_confirm_streak

    slot_index: Optional[int]
    slot_sigil: Optional[str]
    name: Optional[str]
    school: Optional[str]
    pips: PipInventory
    profile_health_max: Optional[int]
    if selected is not None:
        slot_index = selected.index
        slot_sigil = (selected.sigil or "unknown").strip().title() or "Unknown"
        name = selected.name
        school = selected.school
        pips = selected.pips if selected.pips is not None else PipInventory()
        profile_health_max = selected.health_max
    else:
        slot_index = carry.slot_index
        slot_sigil = carry.slot_sigil
        name = carry.name
        school = carry.school
        pips = carry.pips if carry.pips is not None else PipInventory()
        profile_health_max = carry.health_max

    slot_locked = carry.slot_locked or (slot_confirm_streak >= slot_confirm_rounds)
    if slot_index is None:
        slot_locked = False
        slot_confirm_streak = 0

    matched = slot_matched_by_health or (slot_index is not None and (carry.matched or slot_locked))
    matched_by = "health" if slot_matched_by_health else (carry.matched_by if matched else None)

    resolved_health_cur = hud_cur
    if (not scan_health) and selected is not None and selected.health_current is not None:
        resolved_health_cur = selected.health_current
    resolved_health_max = profile_health_max if profile_health_max is not None else hud_max

    return PlayerWizardState(
        detected=(resolved_health_cur is not None) or (mana_cur is not None) or (energy_cur is not None),
        matched=matched,
        side="ally",
        slot_index=slot_index,
        slot_sigil=slot_sigil,
        slot_confirm_streak=slot_confirm_streak,
        slot_locked=slot_locked,
        name=name,
        school=school,
        pips=pips,
        health_current=resolved_health_cur,
        health_max=resolved_health_max,
        mana_current=mana_cur,
        mana_max=mana_max,
        energy_current=energy_cur,
        energy_max=energy_max,
        health_raw=health_raw,
        mana_raw=mana_raw,
        energy_raw=energy_raw,
        health_roi=hud_profile.health_roi,
        mana_roi=hud_profile.mana_roi,
        energy_roi=hud_profile.energy_roi,
        matched_by=matched_by,
        timestamp=timestamp,
    )


def _log_health_ocr(
    *,
    side: str,
    index: int,
    sigil: Optional[str],
    name: Optional[str],
    raw_text: Optional[str],
    prev_cur: Optional[int],
    prev_max: Optional[int],
    cur: Optional[int],
    maxv: Optional[int],
    allow_initial_read: bool = False,
) -> None:
    enemy_sigils = ("Dagger", "Key", "Ruby", "Spiral")
    ally_sigils = ("Sun", "Eye", "Star", "Moon")
    slot_sigil = None
    if sigil and sigil.strip():
        slot_sigil = sigil.strip().title()
    else:
        fallback = enemy_sigils if side == "enemy" else ally_sigils
        if 0 <= index < len(fallback):
            slot_sigil = fallback[index]
        else:
            slot_sigil = "Unknown"
    who = (name or "unknown").strip() or "unknown"
    raw = (raw_text or "unknown").strip() or "unknown"
    label = f"[ocr:hp] {slot_sigil} ({who})"
    if prev_cur is None:
        if (not allow_initial_read) or (cur is None and maxv is None):
            return
        cur_text = "?" if cur is None else str(cur)
        max_text = "?" if maxv is None else str(maxv)
        _push_health_ocr_log(f'{label}: "{raw}" --> ({cur_text} / {max_text})')
        return
    if cur is None:
        return
    if cur == prev_cur:
        return
    delta = cur - prev_cur
    if delta >= 0:
        _push_health_ocr_log(f'{label}: "{raw}" --> ({prev_cur} + {delta} = {cur})')
        return
    _push_health_ocr_log(f'{label}: "{raw}" --> ({prev_cur} - {abs(delta)} = {cur})')


def _count_blobs(mask: np.ndarray, min_area: int, max_area: int) -> int:
    if mask.size == 0:
        return 0
    num, _, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    count = 0
    for i in range(1, num):
        area = stats[i, cv2.CC_STAT_AREA]
        if min_area <= area <= max_area:
            count += 1
    return count


_PIP_TEMPLATE_CACHE: Dict[str, Dict[str, List[np.ndarray]]] = {}
_SIGIL_TEMPLATE_CACHE: Dict[str, List[Tuple[str, np.ndarray]]] = {}
_SCHOOL_TEMPLATE_CACHE: Dict[str, List[Tuple[str, np.ndarray]]] = {}


def _template_suffixes_for_aspect(aspect_key: str) -> Tuple[str, ...]:
    if aspect_key == "4:3":
        return ("_4x3",)
    if aspect_key == "16:9":
        return ("_16x9",)
    if aspect_key == "43:18":
        return ("_43x18",)
    return ("_16x9",)


def _load_named_templates(
    base_dir: str,
    aspect_key: str,
    cache: Dict[str, List[Tuple[str, np.ndarray]]],
    *,
    suffixes: Optional[Tuple[str, ...]] = None,
    cache_key_suffix: Optional[str] = None,
    allow_fallback: bool = True,
) -> List[Tuple[str, np.ndarray]]:
    base = Path(base_dir)
    cache_key = f"{base.resolve()}::{aspect_key}"
    if cache_key_suffix:
        cache_key = f"{cache_key}::{cache_key_suffix}"
    if cache_key in cache:
        return cache[cache_key]

    if not base.exists():
        cache[cache_key] = []
        return []

    suffixes = suffixes or _template_suffixes_for_aspect(aspect_key)
    templates: List[Tuple[str, np.ndarray]] = []
    fallback: List[Tuple[str, np.ndarray]] = []
    for folder in sorted(p for p in base.iterdir() if p.is_dir()):
        label = folder.name.lower()
        for png in sorted(folder.glob("*.png")):
            stem = png.stem.strip().lower()
            img = cv2.imread(str(png), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            if any(stem.endswith(suf) for suf in suffixes):
                templates.append((label, img))
            else:
                fallback.append((label, img))

    if allow_fallback and (not templates) and fallback:
        templates = fallback

    cache[cache_key] = templates
    return templates


def _ensure_gray(img: np.ndarray) -> np.ndarray:
    if img.size == 0:
        return img
    if len(img.shape) == 2:
        return img
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def _match_named_template(
    crop_bgr: np.ndarray,
    templates: List[Tuple[str, np.ndarray]],
    threshold: float,
    *,
    pad: int = 0,
) -> Tuple[Optional[str], float]:
    if crop_bgr.size == 0 or not templates:
        return None, 0.0
    crop_gray = _ensure_gray(crop_bgr)
    best_name = None
    best_score = -1.0
    for name, templ in templates:
        try:
            if crop_gray.shape[0] < templ.shape[0] or crop_gray.shape[1] < templ.shape[1]:
                resized = cv2.resize(crop_gray, (templ.shape[1], templ.shape[0]), interpolation=cv2.INTER_AREA)
                res = cv2.matchTemplate(resized, templ, cv2.TM_CCOEFF_NORMED)
            else:
                if pad > 0:
                    padded = cv2.copyMakeBorder(
                        crop_gray,
                        pad,
                        pad,
                        pad,
                        pad,
                        cv2.BORDER_REPLICATE,
                    )
                else:
                    padded = crop_gray
                res = cv2.matchTemplate(padded, templ, cv2.TM_CCOEFF_NORMED)
        except Exception:
            continue
        score = float(res.max()) if res.size else -1.0
        if score > best_score:
            best_score = score
            best_name = name
    if best_score >= threshold:
        return best_name, best_score
    return None, best_score


def _detect_sigil(
    sigil_bgr: np.ndarray,
    cfg: SigilDetectConfig,
    aspect_key: str,
) -> Tuple[Optional[str], float]:
    templates = _load_named_templates(cfg.templates_base_dir, aspect_key, _SIGIL_TEMPLATE_CACHE)
    return _match_named_template(sigil_bgr, templates, cfg.template_threshold)


def _school_template_suffixes(aspect_key: str, side: str) -> Tuple[str, ...]:
    side = (side or "").lower()
    if side not in ("ally", "enemy"):
        return _template_suffixes_for_aspect(aspect_key)
    suffixes = _template_suffixes_for_aspect(aspect_key)
    return tuple(f"_{side}{suf}" for suf in suffixes)


def _detect_school(
    school_bgr: np.ndarray,
    cfg: SchoolDetectConfig,
    aspect_key: str,
    side: str,
) -> Tuple[Optional[str], float]:
    templates = _load_named_templates(
        cfg.templates_base_dir,
        aspect_key,
        _SCHOOL_TEMPLATE_CACHE,
        suffixes=_school_template_suffixes(aspect_key, side),
        cache_key_suffix=side,
        allow_fallback=False,
    )
    return _match_named_template(school_bgr, templates, cfg.template_threshold, pad=4)


def _load_pip_templates(cfg: PipDetectConfig, aspect_key: str) -> Dict[str, List[np.ndarray]]:
    base = Path(cfg.templates_base_dir)
    aspect_dir = _pip_aspect_dir_name(aspect_key)
    cache_key = f"{base.resolve()}::{aspect_dir}"
    if cache_key in _PIP_TEMPLATE_CACHE:
        return _PIP_TEMPLATE_CACHE[cache_key]

    if not base.exists():
        _PIP_TEMPLATE_CACHE[cache_key] = {}
        return {}

    templates: Dict[str, List[np.ndarray]] = {}
    for folder in sorted(p for p in base.iterdir() if p.is_dir()):
        token = folder.name.lower()
        paths: List[Path] = []
        # Preferred layout: assets/pips/<token>/<aspect_dir>/*.png
        aspect_subdir = folder / aspect_dir
        if aspect_subdir.exists():
            paths.extend(sorted(aspect_subdir.glob("*.png")))
        # Fallback layout: assets/pips/<token>/*.png
        if not paths:
            paths.extend(sorted(folder.glob("*.png")))
        for png in paths:
            img = cv2.imread(str(png), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            if token not in templates:
                templates[token] = []
            templates[token].append(img)

    _PIP_TEMPLATE_CACHE[cache_key] = templates
    return templates


def _best_pip_template_match(
    crop_gray: np.ndarray,
    templates_by_token: Dict[str, List[np.ndarray]],
    *,
    allowed_tokens: Optional[Set[str]] = None,
) -> Tuple[Optional[str], float]:
    if crop_gray.size == 0 or not templates_by_token:
        return None, -1.0
    best_name: Optional[str] = None
    best_score = -1.0
    for token, templates in templates_by_token.items():
        if allowed_tokens is not None and token not in allowed_tokens:
            continue
        for templ in templates:
            try:
                resized = cv2.resize(crop_gray, (templ.shape[1], templ.shape[0]), interpolation=cv2.INTER_AREA)
            except Exception:
                continue
            res = cv2.matchTemplate(resized, templ, cv2.TM_CCOEFF_NORMED)
            score = float(res[0][0]) if res.size else -1.0
            if score > best_score:
                best_score = score
                best_name = token
    return best_name, best_score


def _pip_presence_metrics(slot_bgr: np.ndarray, cfg: PipDetectConfig) -> Tuple[float, int]:
    if slot_bgr.size == 0:
        return 0.0, 0
    hsv = cv2.cvtColor(slot_bgr, cv2.COLOR_BGR2HSV)
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    white = (s <= cfg.white_sat_max) & (v >= cfg.white_val_min)
    colored = (s >= cfg.school_sat_min) & (v >= cfg.school_val_min)
    mask = (white | colored).astype(np.uint8) * 255
    kernel = np.ones((2, 2), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    ink_ratio = float((mask > 0).mean()) if mask.size else 0.0
    num, _, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    largest = 0
    for i in range(1, num):
        largest = max(largest, int(stats[i, cv2.CC_STAT_AREA]))
    return ink_ratio, largest


def _pip_slot_is_school(slot_bgr: np.ndarray, cfg: PipDetectConfig) -> bool:
    if slot_bgr.size == 0:
        return False
    h, w = slot_bgr.shape[:2]
    if h < 3 or w < 3:
        return False
    cx1 = max(0, int(w * 0.28))
    cx2 = max(cx1 + 1, min(w, int(w * 0.72)))
    cy1 = max(0, int(h * 0.28))
    cy2 = max(cy1 + 1, min(h, int(h * 0.72)))
    center = slot_bgr[cy1:cy2, cx1:cx2]
    if center.size == 0:
        return False
    gray = cv2.cvtColor(center, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 140)
    edge_ratio = float((edges > 0).mean()) if edges.size else 0.0
    hsv = cv2.cvtColor(center, cv2.COLOR_BGR2HSV)
    sat_mean = float(hsv[:, :, 1].mean()) if hsv.size else 0.0
    return edge_ratio >= 0.06 and sat_mean >= max(35.0, cfg.school_sat_min * 0.5)


def _pip_non_school_fallback(slot_bgr: np.ndarray, cfg: PipDetectConfig) -> str:
    if slot_bgr.size == 0:
        return "unknown"
    hsv = cv2.cvtColor(slot_bgr, cv2.COLOR_BGR2HSV)
    h = hsv[:, :, 0].astype(np.float32)
    s = hsv[:, :, 1].astype(np.float32)
    v = hsv[:, :, 2].astype(np.float32)
    active = v >= float(cfg.white_val_min * 0.55)
    if not np.any(active):
        return "unknown"
    h_mean = float(h[active].mean())
    s_mean = float(s[active].mean())
    v_mean = float(v[active].mean())
    # Regular pips are bright/low-sat. Power pips skew warm/gold with higher sat.
    if s_mean <= float(cfg.white_sat_max + 25) and v_mean >= float(cfg.white_val_min * 0.75):
        return "pip"
    if 10.0 <= h_mean <= 45.0 and s_mean >= 70.0:
        return "power"
    return "pip" if s_mean < 90.0 else "power"


def _pip_counts(
    pips_bgr: np.ndarray,
    cfg: PipDetectConfig,
    aspect_key: str,
    *,
    slot_name: str = "sun",
) -> PipInventory:
    counts = PipInventory()
    if pips_bgr.size == 0:
        return counts

    upscale = max(1, int(cfg.slot_debug_upscale))
    if upscale > 1:
        pips_eval = cv2.resize(
            pips_bgr,
            (pips_bgr.shape[1] * upscale, pips_bgr.shape[0] * upscale),
            interpolation=cv2.INTER_CUBIC,
        )
    else:
        pips_eval = pips_bgr

    h, w = pips_eval.shape[:2]
    if h == 0 or w == 0:
        return counts

    slot_count = max(1, int(cfg.slot_count))
    start_x = _pip_slot_start_px(cfg, aspect_key, slot_name)
    slot_w = _pip_slot_width_px(cfg, aspect_key)
    slot_gap = _pip_slot_gap_px(cfg, aspect_key)
    slot_step = slot_w + slot_gap
    top_cut = _pip_slot_top_cut_px(cfg, aspect_key)
    bottom_cut = _pip_slot_bottom_cut_px(cfg, aspect_key)
    y1 = max(0, min(h - 1, top_cut))
    y2 = max(y1 + 1, min(h, h - bottom_cut))

    templates_by_token = _load_pip_templates(cfg, aspect_key)
    tokens: List[str] = []
    for i in range(slot_count):
        x1 = start_x + (i * slot_step)
        x2 = x1 + slot_w
        cx1 = max(0, min(w, x1))
        cx2 = max(0, min(w, x2))
        if cx2 <= cx1:
            continue
        slot = pips_eval[y1:y2, cx1:cx2]
        if slot.size == 0:
            continue

        ink_ratio, largest = _pip_presence_metrics(slot, cfg)
        slot_area = max(1, slot.shape[0] * slot.shape[1])
        if not (
            ((ink_ratio >= 0.025) and (largest >= max(1, int(slot_area * 0.015))))
            or (largest >= max(1, int(slot_area * 0.05)))
        ):
            continue

        slot_gray = cv2.cvtColor(slot, cv2.COLOR_BGR2GRAY)
        best_match, best_score = _best_pip_template_match(slot_gray, templates_by_token)
        if best_score < float(cfg.slot_presence_confidence_threshold):
            # Treat as empty when template confidence is below configured threshold.
            continue
        if best_match == "regular":
            token = "pip"
        elif best_match:
            token = best_match
        else:
            token = "unknown"
        tokens.append(token)

    counts.tokens = tokens
    counts.normal = tokens.count("pip")
    counts.power = tokens.count("power")
    counts.school = len(tokens) - counts.normal - counts.power
    return counts


def _red_ratio(bgr: np.ndarray) -> float:
    if bgr.size == 0:
        return 0.0
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    red1 = (h <= 10) & (s >= 90) & (v >= 120)
    red2 = (h >= 170) & (s >= 90) & (v >= 120)
    return float((red1 | red2).mean())


def _dark_ratio(bgr: np.ndarray) -> float:
    if bgr.size == 0:
        return 0.0
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return float((gray <= 60).mean())


def _is_slot_occupied(
    *,
    name_crop: np.ndarray,
    health_crop: np.ndarray,
    name_text: Optional[str],
    health_current: Optional[int],
    health_max: Optional[int],
    pips: PipInventory,
) -> bool:
    if name_text:
        return True
    if health_current is not None or health_max is not None:
        return True
    if any(token != "unknown" for token in pips.tokens):
        return True
    red_ratio = _red_ratio(health_crop)
    if red_ratio >= 0.01:
        return True
    dark_ratio = _dark_ratio(name_crop)
    if dark_ratio >= 0.01:
        return True
    return False


def _extract_participant(
    frame_bgr: np.ndarray,
    side: str,
    index: int,
    box_roi: Tuple[float, float, float, float],
    cfg: ParticipantsConfig,
    *,
    skip_name_ocr: bool = False,
    name_override: Optional[str] = None,
    name_raw_override: Optional[str] = None,
    name_time_override: Optional[float] = None,
    name_time_parts_override: Optional[Tuple[float, float, float, float]] = None,
    name_hash_override: Optional[int] = None,
    name_prev_hash: Optional[int] = None,
    name_ocr_override: Optional[bool] = None,
    skip_health_ocr: bool = False,
    health_override: Optional[Tuple[Optional[int], Optional[int]]] = None,
    health_max_override: Optional[int] = None,
    skip_school_detect: bool = False,
    school_override: Optional[str] = None,
    school_score_override: Optional[float] = None,
    skip_pip_detect: bool = False,
    pips_override: Optional[PipInventory] = None,
    details_checked_at_override: Optional[float] = None,
    occupied_override: Optional[bool] = None,
    debug_dump: bool = False,
    debug_dump_health: bool = False,
    debug_dump_empty_names: bool = False,
    debug_dump_sigil_roi: bool = False,
    debug_dump_school_roi: bool = False,
    debug_dump_pips: bool = False,
    debug_print_health_ocr: bool = True,
    debug_print_health_ocr_initial_read: bool = False,
    debug_dump_id: Optional[str] = None,
    debug_dump_limit: int = 0,
    sigil_override: Optional[str] = None,
    sigil_score_override: Optional[float] = None,
    sigil_checked: bool = False,
) -> ParticipantState:
    slot_dump_id = f"{debug_dump_id}_{side}_{index}" if debug_dump_id else None
    layout = cfg.layout
    is_enemy = side == "enemy"
    aspect_key = _aspect_bucket(frame_bgr.shape[1] / frame_bgr.shape[0])

    sigil_rel = layout.sigil_roi_enemy if is_enemy else layout.sigil_roi_ally
    school_rel = layout.school_roi_enemy if is_enemy else layout.school_roi_ally
    name_rel = layout.name_roi_enemy if is_enemy else layout.name_roi_ally
    health_rel = layout.health_roi_enemy if is_enemy else layout.health_roi_ally
    pips_rel = layout.pips_roi_enemy if is_enemy else layout.pips_roi_ally

    sigil_roi = _sub_roi(box_roi, sigil_rel)
    school_roi = _sub_roi(box_roi, school_rel)
    name_roi = _sub_roi(box_roi, name_rel)
    health_roi = _sub_roi(box_roi, health_rel)
    pips_roi = _sub_roi(box_roi, pips_rel)

    if sigil_checked:
        sigil_match, sigil_score = sigil_override, sigil_score_override
    else:
        sigil_crop = crop_relative(frame_bgr, sigil_roi)
        _dump_participant_roi(sigil_crop, kind="sigil", side=side, index=index, enabled=debug_dump_sigil_roi)
        sigil_match, sigil_score = _detect_sigil(sigil_crop, cfg.sigil, aspect_key)
    if sigil_match is None:
        return ParticipantState(
            side=side,
            index=index,
            rel_roi=box_roi,
            sigil=sigil_match,
            sigil_score=sigil_score,
            name=None,
            name_raw=None,
            name_time_ms=None,
            name_time_parts=None,
            name_roi_hash=None,
            name_ocr=False,
            details_checked_at=None,
            health_current=None,
            health_max=None,
            school=None,
            school_score=None,
            pips=PipInventory(),
            occupied=False,
            empty_reason="sigil missing",
            name_roi=name_roi,
            health_roi=health_roi,
            pips_roi=pips_roi,
            sigil_roi=sigil_roi,
            school_roi=school_roi,
        )

    name_timer_start = time.perf_counter()
    name_crop = crop_relative(frame_bgr, name_roi)
    name_hash = name_hash_override if name_hash_override is not None else _name_roi_hash(name_crop)
    health_crop = None
    pips_crop = None
    school_crop = None
    if not skip_health_ocr:
        health_crop = crop_relative(frame_bgr, health_roi)
    if (not skip_pip_detect) or debug_dump_pips:
        pips_crop = crop_relative(frame_bgr, pips_roi)
    if debug_dump_pips and pips_crop is not None:
        _dump_pips_roi_debug(
            pips_crop,
            side=side,
            index=index,
            aspect_key=aspect_key,
            cfg=cfg.pip,
        )
    if (not skip_school_detect) or debug_dump_school_roi:
        school_crop = crop_relative(frame_bgr, school_roi)
    if school_crop is not None:
        _dump_participant_roi(school_crop, kind="school", side=side, index=index, enabled=debug_dump_school_roi)
    if skip_school_detect:
        school_match = school_override
        school_score = school_score_override
    else:
        school_match, school_score = _detect_school(school_crop, cfg.school, aspect_key, side)

    if debug_dump_health and (health_crop is not None) and side in ("enemy", "ally"):
        prepped_list: List[Tuple[str, np.ndarray]] = [
            ("prepped_redmask", _prep_tesseract_health(health_crop, cfg.ocr, invert=False)),
            ("prepped_redmask_inv", _prep_tesseract_health(health_crop, cfg.ocr, invert=True)),
        ]
        if cfg.ocr.backend == "easyocr":
            prepped_list.extend(
                [
                    ("prepped", _prep_plain_health(health_crop, cfg.ocr, invert=False)),
                    ("prepped_inv", _prep_plain_health(health_crop, cfg.ocr, invert=True)),
                ]
            )
        _dump_health_roi(
            health_crop,
            side=side,
            index=index,
            debug_dump_id=debug_dump_id,
            prepped=tuple(prepped_list),
        )

    tag = f"{side}_{index}_name"
    name_text = None
    reuse_name = (
        (not skip_name_ocr)
        and name_prev_hash is not None
        and name_hash is not None
        and name_hash == name_prev_hash
        and (name_override or name_raw_override)
    )

    if skip_name_ocr or reuse_name:
        name_text = name_override
        name_raw = name_raw_override
        if name_text is None and name_raw is not None:
            name_text = name_raw
        if reuse_name:
            name_time_ms = (time.perf_counter() - name_timer_start) * 1000.0
            name_time_parts = None
        else:
            name_time_ms = name_time_override
            name_time_parts = name_time_parts_override
        name_ocr = False if name_ocr_override is None else name_ocr_override
    else:
        name_text = _ocr_name_per_char(name_crop, cfg.ocr)
        if not name_text:
            name_text = _ocr_text(
                name_crop,
                cfg.ocr,
                cfg.ocr.name_whitelist,
                clahe=True,
                psm_override=7,
                name_mode=True,
                debug_tag=tag,
                debug_dump=debug_dump,
                debug_dump_id=slot_dump_id,
                debug_dump_limit=debug_dump_limit,
            )
        if not name_text:
            name_text = _ocr_text(
                name_crop,
                cfg.ocr,
                cfg.ocr.name_whitelist,
                clahe=True,
                invert_override=True,
                psm_override=7,
                name_mode=True,
                debug_tag=f"{tag}_inv",
                debug_dump=debug_dump,
                debug_dump_id=slot_dump_id,
                debug_dump_limit=debug_dump_limit,
            )
        if not name_text:
            name_text = _ocr_text(
                name_crop,
                cfg.ocr,
                cfg.ocr.name_whitelist,
                clahe=True,
                psm_override=8,
                name_mode=True,
                debug_tag=f"{tag}_psm8",
                debug_dump=debug_dump,
                debug_dump_id=slot_dump_id,
                debug_dump_limit=debug_dump_limit,
            )
        if not name_text:
            name_text = _ocr_text(
                name_crop,
                cfg.ocr,
                cfg.ocr.name_whitelist,
                clahe=True,
                invert_override=True,
                psm_override=8,
                name_mode=True,
                debug_tag=f"{tag}_psm8_inv",
                debug_dump=debug_dump,
                debug_dump_id=slot_dump_id,
                debug_dump_limit=debug_dump_limit,
            )
        if not name_text:
            name_text = _ocr_text(
                name_crop,
                cfg.ocr,
                cfg.ocr.name_whitelist,
                clahe=True,
                psm_override=6,
                name_mode=True,
                debug_tag=f"{tag}_psm6",
                debug_dump=debug_dump,
                debug_dump_id=slot_dump_id,
                debug_dump_limit=debug_dump_limit,
            )
        if not name_text:
            name_text = _ocr_text(
                name_crop,
                cfg.ocr,
                "",
                clahe=True,
                psm_override=7,
                name_mode=True,
                debug_tag=f"{tag}_nowhitelist",
                debug_dump=debug_dump,
                debug_dump_id=slot_dump_id,
                debug_dump_limit=debug_dump_limit,
            )
        if not name_text:
            name_text = _ocr_text(
                name_crop,
                cfg.ocr,
                cfg.ocr.name_whitelist,
                psm_override=7,
                name_mode=False,
                blacklist=cfg.ocr.name_blacklist,
                debug_tag=f"{tag}_otsu",
                debug_dump=debug_dump,
                debug_dump_id=slot_dump_id,
                debug_dump_limit=debug_dump_limit,
            )
        name_raw = name_text
        name_text = _apply_wordlist_correction(name_text, cfg.ocr, side=side)
        name_time_ms = (time.perf_counter() - name_timer_start) * 1000.0
        name_time_parts = None
        name_ocr = True if name_ocr_override is None else name_ocr_override

    if (not skip_name_ocr) and (not name_text) and debug_dump and (not debug_dump_empty_names) and debug_dump_id:
        _remove_ocr_dumps_with_prefix(tag, dump_id=slot_dump_id)

    prev_health_current = None
    prev_health_max = None
    if health_override is not None:
        prev_health_current, prev_health_max = health_override

    if skip_health_ocr:
        if health_override is None:
            health_current, health_max = (None, None)
        else:
            health_current, health_max = health_override
        health_raw_text = None
    else:
        health_current, health_max, health_raw_text = _ocr_health(health_crop, cfg.ocr)
        # Safety: participant HP must be read as "current/max". If slash is missing,
        # keep prior values to avoid propagating a bad parse.
        normalized_health_raw = _normalize_health_text(health_raw_text) if health_raw_text else ""
        if "/" not in normalized_health_raw:
            if health_override is None:
                health_current, health_max = (None, None)
            else:
                health_current, health_max = health_override
    if health_max_override is not None:
        health_max = health_max_override
    if debug_print_health_ocr and (not skip_health_ocr):
        _log_health_ocr(
            side=side,
            index=index,
            sigil=sigil_match,
            name=name_text,
            raw_text=health_raw_text,
            prev_cur=prev_health_current,
            prev_max=prev_health_max,
            cur=health_current,
            maxv=health_max,
            allow_initial_read=debug_print_health_ocr_initial_read,
        )
    if skip_pip_detect:
        pips = pips_override if pips_override is not None else PipInventory()
    else:
        pips = _pip_counts(
            pips_crop,
            cfg.pip,
            aspect_key,
            slot_name=_pip_slot_name(side, index),
        )

    return ParticipantState(
        side=side,
        index=index,
        rel_roi=box_roi,
        sigil=sigil_match,
        sigil_score=sigil_score,
        name=name_text,
        name_raw=name_raw,
        name_time_ms=name_time_ms,
        name_time_parts=name_time_parts,
        name_roi_hash=name_hash,
        name_ocr=name_ocr,
        details_checked_at=details_checked_at_override,
        health_current=health_current,
        health_max=health_max,
        school=school_match,
        school_score=school_score,
        pips=pips,
        occupied=True,
        empty_reason=None,
        name_roi=name_roi,
        health_roi=health_roi,
        pips_roi=pips_roi,
        sigil_roi=sigil_roi,
        school_roi=school_roi,
    )


def extract_participants(
    frame_bgr: np.ndarray,
    cfg: ParticipantsConfig,
    *,
    previous: Optional[ParticipantsState] = None,
    skip_name_ocr: bool = False,
    skip_health_ocr: bool = False,
    occupancy_refresh_s: float = 5.0,
    details_refresh_s: float = 3.0,
    lock_name: bool = False,
    lock_school: bool = False,
    lock_health_max: bool = False,
    force_health_refresh: bool = False,
    force_pips_refresh: bool = False,
    force_school_refresh: bool = False,
    refresh_health_on_force_only: bool = False,
    refresh_pips_on_force_only: bool = False,
    timestamp: Optional[float] = None,
    debug_dump: bool = False,
    debug_dump_health: bool = False,
    debug_dump_empty_names: bool = False,
    debug_dump_sigil_roi: bool = False,
    debug_dump_school_roi: bool = False,
    debug_dump_pips: bool = False,
    debug_print_health_ocr: bool = True,
    debug_print_health_ocr_initial_read: bool = False,
    debug_dump_id: Optional[str] = None,
    debug_dump_limit: int = 0,
) -> ParticipantsState:
    state = ParticipantsState(detected=False, timestamp=timestamp)
    if frame_bgr is None:
        return state
    h, w = frame_bgr.shape[:2]
    if h == 0 or w == 0:
        return state

    aspect = w / h
    bucket = _aspect_bucket(aspect)
    profile = cfg.profiles.get(bucket)
    if profile is None:
        return state

    enemies: List[ParticipantState] = []
    allies: List[ParticipantState] = []
    layout = cfg.layout
    ts = timestamp if timestamp is not None else time.time()

    prev_enemies = previous.enemies if previous else []
    prev_allies = previous.allies if previous else []

    def _prev_for(side: str, idx: int) -> Optional[ParticipantState]:
        arr = prev_enemies if side == "enemy" else prev_allies
        if idx < len(arr):
            return arr[idx]
        return None

    def _refresh_due(prev: ParticipantState) -> bool:
        if details_refresh_s <= 0:
            return False
        if prev.details_checked_at is None:
            return True
        return (ts - prev.details_checked_at) >= details_refresh_s

    def _name_incomplete(prev: ParticipantState) -> bool:
        return (not prev.name) or (prev.name == "unknown")

    def _health_incomplete(prev: ParticipantState) -> bool:
        return (prev.health_current is None) or (prev.health_max is None)

    def _school_incomplete(prev: ParticipantState) -> bool:
        if not prev.school:
            return True
        if prev.school_score is None:
            return False
        return prev.school_score < cfg.school.template_threshold

    def _pips_incomplete(prev: ParticipantState) -> bool:
        if prev.pips is None:
            return True
        tokens = prev.pips.tokens or []
        if not tokens:
            return True
        return any(tok == "unknown" for tok in tokens)

    def _name_locked(prev: ParticipantState) -> bool:
        if not lock_name:
            return False
        if not prev.name:
            return False
        return prev.name != "unknown"

    def _school_locked(prev: ParticipantState) -> bool:
        if not lock_school:
            return False
        if not prev.school:
            return False
        if prev.school_score is None:
            return True
        return prev.school_score >= cfg.school.template_threshold

    def _detail_needs(prev: Optional[ParticipantState], occupied_now: bool) -> Tuple[bool, bool, bool, bool, Optional[float]]:
        if not occupied_now:
            return (False, False, False, False, None)
        if prev is None or not prev.occupied:
            # New sigil-occupied slot: resolve pips immediately on detection.
            return (not skip_name_ocr, not skip_health_ocr, True, True, ts)
        need_name = False
        need_health = False
        need_school = False
        need_pips = False

        if force_health_refresh and (not skip_health_ocr):
            need_health = True
        if force_pips_refresh:
            need_pips = True
        if force_school_refresh:
            if prev.school is None or prev.school == "unknown":
                need_school = True

        refresh_due = _refresh_due(prev)
        if refresh_due:
            if (not skip_name_ocr) and (not _name_locked(prev)) and _name_incomplete(prev):
                need_name = True
            if (not skip_health_ocr) and (not refresh_health_on_force_only) and _health_incomplete(prev):
                need_health = True
            if (not _school_locked(prev)) and _school_incomplete(prev):
                need_school = True
            if (not refresh_pips_on_force_only) and _pips_incomplete(prev):
                need_pips = True

        if not (need_name or need_health or need_school or need_pips):
            return (False, False, False, False, prev.details_checked_at)
        return (need_name, need_health, need_school, need_pips, ts)

    do_occupancy_check = True
    if previous and previous.detected and previous.occupancy_checked_at is not None and occupancy_refresh_s > 0:
        do_occupancy_check = (ts - previous.occupancy_checked_at) >= occupancy_refresh_s

    use_batch_easyocr = (not skip_name_ocr) and cfg.ocr.backend == "easyocr"
    sigil_info: Dict[Tuple[str, int], Tuple[Optional[str], Optional[float], Tuple[float, float, float, float]]] = {}
    name_overrides: Dict[
        Tuple[str, int],
        Tuple[Optional[str], Optional[str], Optional[float], Optional[Tuple[float, float, float, float]]],
    ] = {}
    name_hash_overrides: Dict[Tuple[str, int], Optional[int]] = {}
    detail_needs: Dict[Tuple[str, int], Tuple[bool, bool, bool, bool, Optional[float]]] = {}

    for i in range(profile.slots):
        enemy_roi = _shift_roi(profile.enemy_first_box, profile.enemy_spacing_x * i)
        if profile.ally_anchor == "right":
            ally_roi = _shift_roi(profile.ally_first_box, -profile.ally_spacing_x * i)
        else:
            ally_roi = _shift_roi(profile.ally_first_box, profile.ally_spacing_x * i)
        for side, box_roi in (("enemy", enemy_roi), ("ally", ally_roi)):
            is_enemy = side == "enemy"
            prev = _prev_for(side, i) if previous else None
            if do_occupancy_check:
                sigil_rel = layout.sigil_roi_enemy if is_enemy else layout.sigil_roi_ally
                sigil_roi = _sub_roi(box_roi, sigil_rel)
                sigil_crop = crop_relative(frame_bgr, sigil_roi)
                _dump_participant_roi(sigil_crop, kind="sigil", side=side, index=i, enabled=debug_dump_sigil_roi)
                sigil_match, sigil_score = _detect_sigil(sigil_crop, cfg.sigil, bucket)
            else:
                sigil_match = prev.sigil if prev else None
                sigil_score = prev.sigil_score if prev else None
            sigil_info[(side, i)] = (sigil_match, sigil_score, box_roi)

    if use_batch_easyocr:
        name_items: List[_NameWorkItem] = []
        for i in range(profile.slots):
            enemy_roi = _shift_roi(profile.enemy_first_box, profile.enemy_spacing_x * i)
            if profile.ally_anchor == "right":
                ally_roi = _shift_roi(profile.ally_first_box, -profile.ally_spacing_x * i)
            else:
                ally_roi = _shift_roi(profile.ally_first_box, profile.ally_spacing_x * i)

            for side, box_roi in (("enemy", enemy_roi), ("ally", ally_roi)):
                is_enemy = side == "enemy"
                prev = _prev_for(side, i) if previous else None
                name_rel = layout.name_roi_enemy if is_enemy else layout.name_roi_ally
                sigil_match, _, _ = sigil_info.get((side, i), (None, None, box_roi))
                occupied_now = sigil_match is not None
                needs = _detail_needs(prev, occupied_now)
                detail_needs[(side, i)] = needs
                need_name, _, _, _, _ = needs
                if (not occupied_now) or (not need_name):
                    continue
                name_roi = _sub_roi(box_roi, name_rel)
                cap_start = time.perf_counter()
                name_crop = crop_relative(frame_bgr, name_roi)
                capture_ms = (time.perf_counter() - cap_start) * 1000.0
                name_hash = _name_roi_hash(name_crop)
                name_hash_overrides[(side, i)] = name_hash
                if prev is not None and name_hash is not None and prev.name_roi_hash == name_hash and (prev.name or prev.name_raw):
                    name_time_parts = (capture_ms, 0.0, 0.0, 0.0)
                    prev_final = prev.name or prev.name_raw
                    prev_raw = prev.name_raw or prev.name
                    name_overrides[(side, i)] = (prev_final, prev_raw, capture_ms, name_time_parts)
                    detail_needs[(side, i)] = (False, needs[1], needs[2], needs[3], needs[4])
                    continue
                slot_dump_id = f"{debug_dump_id}_{side}_{i}" if debug_dump_id else None
                name_items.append(
                    _NameWorkItem(
                        key=(side, i),
                        crop=name_crop,
                        tag=f"{side}_{i}_name",
                        dump_id=slot_dump_id,
                        start_time=time.perf_counter(),
                        capture_ms=capture_ms,
                    )
                )
        batch_results = _batch_easyocr_names(
            name_items,
            cfg.ocr,
            debug_dump=debug_dump,
            debug_dump_limit=debug_dump_limit,
        )
        name_overrides.update(batch_results)

    for i in range(profile.slots):
        enemy_roi = _shift_roi(profile.enemy_first_box, profile.enemy_spacing_x * i)
        if profile.ally_anchor == "right":
            ally_roi = _shift_roi(profile.ally_first_box, -profile.ally_spacing_x * i)
        else:
            ally_roi = _shift_roi(profile.ally_first_box, profile.ally_spacing_x * i)
        prev_enemy = _prev_for("enemy", i) if previous else None
        prev_ally = _prev_for("ally", i) if previous else None

        enemy_name_raw = None
        enemy_name_final = None
        enemy_name_time = None
        enemy_name_parts = None
        enemy_name_ocr = None
        enemy_name_hash = name_hash_overrides.get(("enemy", i)) if use_batch_easyocr else None
        enemy_sigil, enemy_sigil_score, _ = sigil_info.get(("enemy", i), (None, None, enemy_roi))
        enemy_needs = detail_needs.get(("enemy", i))
        if use_batch_easyocr:
            enemy_name_raw, enemy_name_final, enemy_name_time, enemy_name_parts = name_overrides.get(
                ("enemy", i), (None, None, None, None)
            )
            if enemy_name_parts is not None:
                _, _, ocr_ms, res_ms = enemy_name_parts
                enemy_name_ocr = (ocr_ms > 0.0) or (res_ms > 0.0)
            if (enemy_name_final is None) and prev_enemy is not None:
                enemy_name_final = prev_enemy.name or prev_enemy.name_raw
                enemy_name_raw = prev_enemy.name_raw or prev_enemy.name

        ally_name_raw = None
        ally_name_final = None
        ally_name_time = None
        ally_name_parts = None
        ally_name_ocr = None
        ally_name_hash = name_hash_overrides.get(("ally", i)) if use_batch_easyocr else None
        ally_sigil, ally_sigil_score, _ = sigil_info.get(("ally", i), (None, None, ally_roi))
        ally_needs = detail_needs.get(("ally", i))
        if use_batch_easyocr:
            ally_name_raw, ally_name_final, ally_name_time, ally_name_parts = name_overrides.get(
                ("ally", i), (None, None, None, None)
            )
            if ally_name_parts is not None:
                _, _, ocr_ms, res_ms = ally_name_parts
                ally_name_ocr = (ocr_ms > 0.0) or (res_ms > 0.0)
            if (ally_name_final is None) and prev_ally is not None:
                ally_name_final = prev_ally.name or prev_ally.name_raw
                ally_name_raw = prev_ally.name_raw or prev_ally.name

        if enemy_needs is None:
            occupied_now = enemy_sigil is not None
            enemy_needs = _detail_needs(prev_enemy, occupied_now)
        if ally_needs is None:
            occupied_now = ally_sigil is not None
            ally_needs = _detail_needs(prev_ally, occupied_now)

        enemy_need_name, enemy_need_health, enemy_need_school, enemy_need_pips, enemy_details_at = enemy_needs
        ally_need_name, ally_need_health, ally_need_school, ally_need_pips, ally_details_at = ally_needs

        enemy_health_max_override = None
        if lock_health_max and prev_enemy is not None and prev_enemy.health_max is not None:
            enemy_health_max_override = prev_enemy.health_max
        ally_health_max_override = None
        if lock_health_max and prev_ally is not None and prev_ally.health_max is not None:
            ally_health_max_override = prev_ally.health_max

        enemies.append(
            _extract_participant(
                frame_bgr,
                "enemy",
                i,
                enemy_roi,
                cfg,
                skip_name_ocr=skip_name_ocr or use_batch_easyocr or (not enemy_need_name),
                name_override=(
                    enemy_name_final if use_batch_easyocr else (prev_enemy.name if prev_enemy is not None else None)
                ),
                name_raw_override=(
                    enemy_name_raw if use_batch_easyocr else (prev_enemy.name_raw if prev_enemy is not None else None)
                ),
                name_time_override=(enemy_name_time if use_batch_easyocr else None),
                name_time_parts_override=(enemy_name_parts if use_batch_easyocr else None),
                name_hash_override=enemy_name_hash,
                name_prev_hash=(prev_enemy.name_roi_hash if prev_enemy is not None else None),
                name_ocr_override=enemy_name_ocr,
                skip_health_ocr=skip_health_ocr or (not enemy_need_health),
                health_override=(
                    (prev_enemy.health_current, prev_enemy.health_max) if prev_enemy is not None else None
                ),
                health_max_override=enemy_health_max_override,
                skip_school_detect=(not enemy_need_school),
                school_override=(prev_enemy.school if prev_enemy is not None else None),
                school_score_override=(prev_enemy.school_score if prev_enemy is not None else None),
                skip_pip_detect=(not enemy_need_pips),
                pips_override=(prev_enemy.pips if prev_enemy is not None else None),
                details_checked_at_override=(enemy_details_at if prev_enemy is not None else enemy_details_at),
                occupied_override=(prev_enemy.occupied if prev_enemy is not None else None),
                debug_dump=debug_dump,
                debug_dump_health=debug_dump_health,
                debug_dump_empty_names=debug_dump_empty_names,
                debug_dump_sigil_roi=debug_dump_sigil_roi,
                debug_dump_school_roi=debug_dump_school_roi,
                debug_dump_pips=debug_dump_pips,
                debug_print_health_ocr=debug_print_health_ocr,
                debug_print_health_ocr_initial_read=debug_print_health_ocr_initial_read,
                debug_dump_id=debug_dump_id,
                debug_dump_limit=debug_dump_limit,
                sigil_override=enemy_sigil,
                sigil_score_override=enemy_sigil_score,
                sigil_checked=True,
            )
        )
        allies.append(
            _extract_participant(
                frame_bgr,
                "ally",
                i,
                ally_roi,
                cfg,
                skip_name_ocr=skip_name_ocr or use_batch_easyocr or (not ally_need_name),
                name_override=(
                    ally_name_final if use_batch_easyocr else (prev_ally.name if prev_ally is not None else None)
                ),
                name_raw_override=(
                    ally_name_raw if use_batch_easyocr else (prev_ally.name_raw if prev_ally is not None else None)
                ),
                name_time_override=(ally_name_time if use_batch_easyocr else None),
                name_time_parts_override=(ally_name_parts if use_batch_easyocr else None),
                name_hash_override=ally_name_hash,
                name_prev_hash=(prev_ally.name_roi_hash if prev_ally is not None else None),
                name_ocr_override=ally_name_ocr,
                skip_health_ocr=skip_health_ocr or (not ally_need_health),
                health_override=((prev_ally.health_current, prev_ally.health_max) if prev_ally is not None else None),
                health_max_override=ally_health_max_override,
                skip_school_detect=(not ally_need_school),
                school_override=(prev_ally.school if prev_ally is not None else None),
                school_score_override=(prev_ally.school_score if prev_ally is not None else None),
                skip_pip_detect=(not ally_need_pips),
                pips_override=(prev_ally.pips if prev_ally is not None else None),
                details_checked_at_override=(ally_details_at if prev_ally is not None else ally_details_at),
                occupied_override=(prev_ally.occupied if prev_ally is not None else None),
                debug_dump=debug_dump,
                debug_dump_health=debug_dump_health,
                debug_dump_empty_names=debug_dump_empty_names,
                debug_dump_sigil_roi=debug_dump_sigil_roi,
                debug_dump_school_roi=debug_dump_school_roi,
                debug_dump_pips=debug_dump_pips,
                debug_print_health_ocr=debug_print_health_ocr,
                debug_print_health_ocr_initial_read=debug_print_health_ocr_initial_read,
                debug_dump_id=debug_dump_id,
                debug_dump_limit=debug_dump_limit,
                sigil_override=ally_sigil,
                sigil_score_override=ally_sigil_score,
                sigil_checked=True,
            )
        )

    state.enemies = enemies
    state.allies = allies
    state.profile = bucket
    state.detected = True
    state.occupancy_checked_at = ts if do_occupancy_check else (previous.occupancy_checked_at if previous else None)
    return state


def render_participants_overlay(
    frame_bgr: np.ndarray,
    state: ParticipantsState,
    *,
    draw_sub_rois: bool = True,
    show_slot_labels: bool = True,
    show_pip_detection: bool = False,
    initiative_side: Optional[str] = None,
    show_empty: bool = True,
    show_legend: bool = True,
    legend_detailed: bool = True,
    use_role_colors: bool = False,
    player_slot_index: Optional[int] = None,
    player_slot_side: str = "ally",
    player_slot_locked: bool = False,
    player_slot_sigil: Optional[str] = None,
) -> np.ndarray:
    vis = frame_bgr.copy()
    aspect_key = _aspect_bucket(frame_bgr.shape[1] / frame_bgr.shape[0]) if frame_bgr.size else "unknown"
    if show_legend:
        _draw_participants_legend(
            vis,
            initiative_side,
            aspect_key,
            player_slot_sigil=player_slot_sigil,
            player_slot_locked=player_slot_locked,
            detailed=legend_detailed,
        )
    for p in state.enemies + state.allies:
        if (not show_empty) and (not p.occupied):
            continue
        if use_role_colors:
            is_player_slot = (
                player_slot_index is not None
                and p.side == player_slot_side
                and p.index == player_slot_index
            )
            if is_player_slot:
                box_color = (0, 215, 255) if player_slot_locked else (255, 255, 255)  # gold when locked, white while suspected
            elif p.side == "ally":
                box_color = (0, 255, 0)  # green
            elif p.side == "enemy":
                box_color = (0, 0, 255)  # red
            else:
                box_color = (128, 128, 128)
        else:
            box_color = (0, 255, 255) if p.occupied else (128, 128, 128)
        draw_relative_roi(vis, p.rel_roi, None, color=box_color, copy=False)
        if show_slot_labels:
            _draw_box_label(vis, p)
        if draw_sub_rois:
            if p.sigil_roi:
                draw_relative_roi(vis, p.sigil_roi, None, color=(255, 0, 255), copy=False)
            if p.occupied:
                if p.school_roi:
                    draw_relative_roi(vis, p.school_roi, None, color=(0, 165, 255), copy=False)
                if p.name_roi:
                    draw_relative_roi(vis, p.name_roi, None, color=(255, 0, 0), copy=False)
                if p.health_roi:
                    draw_relative_roi(vis, p.health_roi, None, color=(0, 255, 0), copy=False)
                if p.pips_roi:
                    draw_relative_roi(vis, p.pips_roi, None, color=(255, 255, 0), copy=False)
        if show_pip_detection and p.pips is not None and p.occupied:
            _draw_pip_tokens(vis, p)
    return vis


def render_player_wizard_overlay(
    frame_bgr: np.ndarray,
    player: Optional[PlayerWizardState],
    *,
    in_battle: bool = True,
) -> np.ndarray:
    vis = frame_bgr.copy()
    if vis.size == 0:
        return vis

    if player is not None:
        if player.health_roi is not None:
            draw_relative_roi(vis, player.health_roi, None, color=(0, 0, 255), copy=False)
        if player.mana_roi is not None:
            draw_relative_roi(vis, player.mana_roi, None, color=(255, 0, 0), copy=False)
        if player.energy_roi is not None:
            draw_relative_roi(vis, player.energy_roi, None, color=(0, 255, 0), copy=False)

    def _fmt_num(value: Optional[int]) -> str:
        return "Unknown" if value is None else str(value)

    def _fmt_text(value: Optional[str]) -> str:
        txt = "" if value is None else str(value).strip()
        return txt if txt else "Unknown"

    slot = _fmt_text(player.slot_sigil) if player is not None else "Unknown"
    slot_color = (255, 255, 255)
    if player is not None and player.slot_locked:
        slot_color = (0, 215, 255)

    pips = player.pips if (player is not None and player.pips is not None) else PipInventory()

    def _player_pip_label(token: str) -> str:
        if token == "pip":
            return "N"
        if token == "power":
            return "P"
        if token in _SCHOOL_COLORS:
            return token[0].upper()
        return "?"

    def _player_pip_color(token: str) -> Tuple[int, int, int]:
        return _token_fill_color(token)

    pip_items = [(_player_pip_label(tok), _player_pip_color(tok), tok) for tok in (pips.tokens or [])]
    if not pip_items:
        pip_items = [("?", (200, 200, 200), "unknown")]

    timestamp = "Unknown"
    if player is not None and player.timestamp is not None:
        try:
            timestamp = datetime.fromtimestamp(player.timestamp).strftime("%H:%M:%S")
        except Exception:
            timestamp = "Unknown"

    health_cur = _fmt_num(player.health_current) if player is not None else "Unknown"
    health_max = _fmt_num(player.health_max) if player is not None else "Unknown"
    mana_cur = _fmt_num(player.mana_current) if player is not None else "Unknown"
    mana_max = _fmt_num(player.mana_max) if player is not None else "Unknown"
    energy_cur = _fmt_num(player.energy_current) if player is not None else "Unknown"

    h, w = vis.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.45
    thickness = 1
    line_h = 18
    pad = 8

    if in_battle:
        rows: List[Tuple[str, str, Tuple[int, int, int]]] = [
            ("text", "Player Wizard", (255, 255, 255)),
            ("text", f"Player Slot: {slot}", slot_color),
            ("text", f"Slot Confirm Streak: {player.slot_confirm_streak if player is not None else 0}", (255, 255, 255)),
            ("text", f"Name: {_fmt_text(player.name) if player is not None else 'Unknown'}", (255, 255, 255)),
            ("text", f"School: {_fmt_text(player.school) if player is not None else 'Unknown'}", (255, 255, 255)),
            ("text", f"Pips: {pips.total} (N:{pips.normal} P:{pips.power} S:{pips.school})", (255, 255, 255)),
            ("tokens", "Pip Tokens:", (200, 200, 200)),
            ("text", f"Health: {health_cur}/{health_max}", (0, 0, 255)),
            ("text", f"Mana: {mana_cur}/{mana_max}", (255, 0, 0)),
            ("text", f"Timestamp (Local): {timestamp}", (200, 200, 200)),
        ]
    else:
        rows = [
            ("text", "Player Resources", (255, 255, 255)),
            ("text", f"Health: {health_cur}", (0, 0, 255)),
            ("text", f"Mana: {mana_cur}", (255, 0, 0)),
            ("text", f"Energy: {energy_cur}", (0, 255, 0)),
            ("text", f"Timestamp (Local): {timestamp}", (200, 200, 200)),
        ]

    def _text_w(text: str) -> int:
        (tw, _), _ = cv2.getTextSize(text, font, scale, thickness)
        return tw

    def _fit_text(text: str, max_w: int) -> str:
        if _text_w(text) <= max_w:
            return text
        ell = "..."
        if _text_w(ell) >= max_w:
            return ell
        trimmed = text
        while trimmed and _text_w(trimmed + ell) > max_w:
            trimmed = trimmed[:-1]
        return (trimmed + ell) if trimmed else ell

    max_text_w_cap = max(220, int(w * 0.42))
    token_prefix_w = _text_w("Pip Tokens:") + 6
    token_items_fit = list(pip_items)
    token_total_w = token_prefix_w + sum(_text_w(lbl) + 6 for lbl, _, _ in token_items_fit)
    while token_items_fit and token_total_w > max_text_w_cap:
        token_items_fit.pop()
        token_total_w = token_prefix_w + sum(_text_w(lbl) + 6 for lbl, _, _ in token_items_fit)
    if not token_items_fit:
        token_items_fit = [("?", (200, 200, 200), "unknown")]
    if len(token_items_fit) < len(pip_items):
        token_items_fit.append(("...", (255, 255, 255), "ellipsis"))

    fitted_rows: List[Tuple[str, str, Tuple[int, int, int]]] = []
    max_w_px = 0
    for kind, text, color in rows:
        if kind == "tokens":
            width_px = token_prefix_w + sum(_text_w(lbl) + 6 for lbl, _, _ in token_items_fit)
            max_w_px = max(max_w_px, min(width_px, max_text_w_cap))
            fitted_rows.append((kind, text, color))
            continue
        fit = _fit_text(text, max_text_w_cap)
        max_w_px = max(max_w_px, _text_w(fit))
        fitted_rows.append((kind, fit, color))

    box_w = max_w_px + pad * 2
    box_h = (line_h * len(fitted_rows)) + pad * 2
    x1 = max(2, w - box_w - 8)
    y1 = max(2, min(h - box_h - 2, 8))
    x2 = min(w - 2, x1 + box_w)
    y2 = min(h - 2, y1 + box_h)

    overlay = vis.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.45, vis, 0.55, 0, vis)

    ty = y1 + pad + line_h - 4
    for kind, text, color in fitted_rows:
        if kind == "tokens":
            cursor = x1 + pad
            cv2.putText(vis, text, (cursor, ty), font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
            cv2.putText(vis, text, (cursor, ty), font, scale, color, thickness, cv2.LINE_AA)
            cursor += _text_w(text) + 6
            for lbl, tok_color, token_name in token_items_fit:
                outline = _token_outline_color(token_name)
                cv2.putText(vis, lbl, (cursor, ty), font, scale, outline, thickness + 2, cv2.LINE_AA)
                cv2.putText(vis, lbl, (cursor, ty), font, scale, tok_color, thickness, cv2.LINE_AA)
                cursor += _text_w(lbl) + 6
            ty += line_h
            continue
        cv2.putText(vis, text, (x1 + pad, ty), font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
        cv2.putText(vis, text, (x1 + pad, ty), font, scale, color, thickness, cv2.LINE_AA)
        ty += line_h
    return vis


_ALLY_SIGILS = ["sun", "eye", "star", "moon"]
_ENEMY_SIGILS = ["dagger", "key", "ruby", "spiral"]


def _draw_participants_legend(
    vis: np.ndarray,
    initiative_side: Optional[str],
    aspect_key: str,
    *,
    player_slot_sigil: Optional[str] = None,
    player_slot_locked: bool = False,
    detailed: bool = True,
) -> None:
    h, w = vis.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.45
    thickness = 1
    line_h = 16
    pad = 6
    init_value = str(initiative_side).strip().title() if initiative_side else "Unknown"
    init_label = f"Initiative: {init_value}"
    aspect_label = f"Aspect: {aspect_key}"
    slot_text = "Unknown"
    if player_slot_sigil is not None:
        cleaned = str(player_slot_sigil).strip()
        if cleaned:
            slot_text = cleaned.title()
    player_label = f"Player: {slot_text}"
    player_color = (0, 215, 255) if player_slot_locked else (255, 255, 255)

    if detailed:
        lines = [
            ("Box", (0, 255, 255)),
            ("Sigil", (255, 0, 255)),
            ("School", (0, 165, 255)),
            ("Name", (255, 0, 0)),
            ("Hp", (0, 255, 0)),
            ("Pips", (255, 255, 0)),
            (player_label, player_color),
            (init_label, (255, 255, 255)),
            (aspect_label, (200, 200, 200)),
        ]
    else:
        lines = [
            (player_label, player_color),
            (init_label, (255, 255, 255)),
            (aspect_label, (200, 200, 200)),
        ]

    x = max(8, int(w * 0.03))
    y = int(h * 0.45)
    max_width = 0
    for label, _ in lines:
        (tw, _), _ = cv2.getTextSize(label, font, scale, thickness)
        if tw > max_width:
            max_width = tw
    box_w = max_width + pad * 2
    box_h = line_h * len(lines) + pad

    overlay = vis.copy()
    cv2.rectangle(overlay, (x - pad, y - line_h + 2), (x - pad + box_w, y - line_h + 2 + box_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.3, vis, 0.7, 0, vis)

    for label, color in lines:
        cv2.putText(vis, label, (x + pad, y), font, scale, color, thickness, cv2.LINE_AA)
        y += line_h


def _sigil_name(participant: ParticipantState) -> str:
    if participant.side == "enemy":
        if 0 <= participant.index < len(_ENEMY_SIGILS):
            return _ENEMY_SIGILS[participant.index]
    if participant.side == "ally":
        if 0 <= participant.index < len(_ALLY_SIGILS):
            return _ALLY_SIGILS[participant.index]
    return "unknown"


def _draw_box_label(vis: np.ndarray, participant: ParticipantState) -> None:
    h, w = vis.shape[:2]
    x1, y1, x2, y2 = participant.rel_roi
    px1 = int(x1 * w)
    py1 = int(y1 * h)
    px2 = int(x2 * w)
    py2 = int(y2 * h)

    sigil = participant.sigil or _sigil_name(participant)
    empty = not participant.occupied

    if empty:
        reason = participant.empty_reason or "unknown"
        lines = [f"empty: {reason}"]
    else:
        name = participant.name or "unknown"
        cur = "?" if participant.health_current is None else str(participant.health_current)
        maxv = "?" if participant.health_max is None else str(participant.health_max)
        school = participant.school or "unknown"
        lines = [
            f"{sigil} | {name}",
            f"hp {cur}/{maxv}",
            f"school {school}",
            "",  # placeholder for pip list line
        ]

    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.45
    thickness = 1
    line_h = 14
    total_h = line_h * len(lines)

    above = participant.side == "ally"
    if above:
        y = py1 - 6
        if y - total_h < 2:
            y = py2 + total_h + 6
    else:
        y = py2 + total_h + 6
        if y > h - 2:
            y = py1 - 6

    x = px1
    pip_line_idx = len(lines) - 1
    for i, text in enumerate(lines):
        ty = y - (total_h - line_h) + i * line_h
        if (not empty) and i == pip_line_idx:
            _draw_pip_list_line(vis, participant, x, ty, font, scale, thickness)
            continue
        cv2.putText(vis, text, (x, ty), font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
        cv2.putText(vis, text, (x, ty), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)


def _draw_pip_list_line(
    vis: np.ndarray,
    participant: ParticipantState,
    x: int,
    y: int,
    font: int,
    scale: float,
    thickness: int,
) -> None:
    tokens = participant.pips.tokens if participant.pips else []
    if not tokens:
        text = "pips: none"
        cv2.putText(vis, text, (x, y), font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
        cv2.putText(vis, text, (x, y), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)
        return

    cursor = x
    label = "pips:"
    cv2.putText(vis, label, (cursor, y), font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
    cv2.putText(vis, label, (cursor, y), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)
    (tw, _), _ = cv2.getTextSize(label, font, scale, thickness)
    cursor += tw + 6

    total = 0
    for token in tokens:
        token_label = _token_label(token)
        token_color = _token_fill_color(token)
        (tw, _), _ = cv2.getTextSize(token_label, font, scale, thickness)
        outline = _token_outline_color(token)
        cv2.putText(vis, token_label, (cursor, y), font, scale, outline, thickness + 2, cv2.LINE_AA)
        cv2.putText(vis, token_label, (cursor, y), font, scale, token_color, thickness, cv2.LINE_AA)
        cursor += tw + 6
        total += _pip_token_value(token)

    total_label = f"= {total}"
    cv2.putText(vis, total_label, (cursor + 2, y), font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
    cv2.putText(vis, total_label, (cursor + 2, y), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)

def _pip_token_value(token: str) -> int:
    if token == "pip":
        return 1
    if token == "power":
        return 2
    if token in _SCHOOL_COLORS:
        return 2
    return 0


_SCHOOL_COLORS: Dict[str, Tuple[int, int, int]] = {
    # Fill colors for school pip labels.
    "balance": (0, 0, 255),      # red
    "death": (0, 0, 0),          # black
    "fire": (0, 165, 255),       # orange
    "ice": (255, 200, 120),      # light blue
    "life": (0, 100, 0),         # dark green
    "myth": (0, 255, 255),       # yellow
    "storm": (180, 0, 180),      # purple
}

_TOKEN_COLORS: Dict[str, Tuple[int, int, int]] = {
    "pip": (255, 255, 255),
    "power": (0, 215, 255),
    "unknown": (180, 180, 180),
}

_TOKEN_OUTLINE_COLORS: Dict[str, Tuple[int, int, int]] = {
    "fire": (0, 255, 255),       # yellow
    "balance": (0, 215, 255),    # gold
    "ice": (225, 105, 65),       # royal blue
    "life": (144, 238, 144),     # light green
    "storm": (0, 255, 255),      # yellow
    "myth": (139, 0, 0),         # dark blue
    "death": (255, 255, 255),    # white
    "power": (0, 215, 255),      # gold
    "pip": (255, 255, 255),      # white
    "unknown": (0, 0, 0),
}


def _token_label(token: str) -> str:
    if token == "pip":
        return "p"
    if token == "power":
        return "P"
    if token in _SCHOOL_COLORS:
        return token[0].upper()
    return "?"


def _token_fill_color(token: str) -> Tuple[int, int, int]:
    if token in _SCHOOL_COLORS:
        return _SCHOOL_COLORS[token]
    return _TOKEN_COLORS.get(token, (180, 180, 180))


def _token_outline_color(token: str) -> Tuple[int, int, int]:
    return _TOKEN_OUTLINE_COLORS.get(token, (0, 0, 0))


def _token_color(token: str) -> Tuple[int, int, int]:
    return _token_fill_color(token)


def _draw_pip_tokens(vis: np.ndarray, participant: ParticipantState) -> None:
    h, w = vis.shape[:2]
    x1, y1, x2, y2 = participant.rel_roi
    px1 = int(x1 * w)
    py1 = int(y1 * h)
    px2 = int(x2 * w)
    py2 = int(y2 * h)

    above = participant.side == "enemy"
    y = py1 - 8 if above else py2 + 16
    if above and y < 12:
        y = py2 + 16
    if (not above) and y > h - 8:
        y = py1 - 8

    x = px1
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    thickness = 1

    total = 0
    for token in participant.pips.tokens:
        label = _token_label(token)
        color = _token_fill_color(token)
        (tw, th), _ = cv2.getTextSize(label, font, scale, thickness)
        outline = _token_outline_color(token)
        cv2.putText(vis, label, (x, y), font, scale, outline, thickness + 2, cv2.LINE_AA)
        cv2.putText(vis, label, (x, y), font, scale, color, thickness, cv2.LINE_AA)
        x += tw + 6
        total += _pip_token_value(token)

    total_label = f"= {total}"
    cv2.putText(vis, total_label, (x + 2, y), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)
