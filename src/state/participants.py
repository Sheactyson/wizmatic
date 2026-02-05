from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time
from typing import Dict, Optional, Tuple, List, Set
import re

import cv2
import numpy as np

from utils.roi import crop_relative, draw_relative_roi
from state.game_state import ParticipantsState, ParticipantState, PipInventory

try:
    import pytesseract
except Exception:  # pragma: no cover - allow import failure in minimal envs
    pytesseract = None

_OCR_DUMP_DIR = Path("debug/ocr")
_OCR_DUMP_DIR.mkdir(parents=True, exist_ok=True)
_PARTICIPANT_DUMP_DIR = Path("debug/participants")
_PARTICIPANT_DUMP_DIR.mkdir(parents=True, exist_ok=True)
_OCR_DUMP_COUNTS: Dict[str, int] = {}
_WORDLIST_CACHE: Dict[str, List[str]] = {}
_WORDLIST_NORM_CACHE: Dict[str, List[str]] = {}
_EASYOCR_WARNED = False
_HEALTH_ROI_DUMPS: Set[str] = set()


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
class PipDetectConfig:
    white_sat_max: int = 60
    white_val_min: int = 200
    school_sat_min: int = 80
    school_val_min: int = 140
    min_area_frac: float = 0.002
    max_area_frac: float = 0.05
    templates_base_dir: str = "src/assets/pips"
    template_threshold: float = 0.7


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
    health_whitelist: str = "0123456789/"
    invert: bool = False
    tesseract_cmd: Optional[str] = None
    user_words_path: Optional[str] = None
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
    if not debug_dump_id or health_crop.size == 0:
        return
    dump_key = f"{debug_dump_id}_{side}_{index}"
    if dump_key in _HEALTH_ROI_DUMPS:
        return
    _HEALTH_ROI_DUMPS.add(dump_key)
    try:
        stamp = f"{int(time.time() * 1000)}"
        path = _OCR_DUMP_DIR / f"health_roi_{side}_{index}_{stamp}.png"
        cv2.imwrite(str(path), health_crop)
        if prepped:
            for suffix, img in prepped:
                if img is None or getattr(img, "size", 0) == 0:
                    continue
                prep_path = _OCR_DUMP_DIR / f"health_roi_{side}_{index}_{stamp}_{suffix}.png"
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
    words, norms = _load_wordlist(cfg.user_words_path)
    if not words:
        return None
    prefix_ns = prefix.replace(" ", "")
    best_i = -1
    best_ratio = 0.0
    best_len = 0
    for i, norm_word in enumerate(norms):
        if not norm_word:
            continue
        norm_ns = norm_word.replace(" ", "")
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
    words, norms = _load_wordlist(cfg.user_words_path)
    if not words:
        return None
    best_i = -1
    best_ratio = 0.0
    best_len = 0
    min_ratio = max(cfg.wordlist_prefix_min_ratio, 0.75)
    max_len = 5
    for i, norm_word in enumerate(norms):
        if not norm_word:
            continue
        norm_ns = norm_word.replace(" ", "")
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
    words, norms = _load_wordlist(cfg.user_words_path)
    if not words:
        return None
    has_any_exact_first = any(first_token in norm.split() for norm in norms)

    best_i = -1
    best_score = 0.0
    best_exact = 0
    best_matched = 0
    best_len = 0

    for i, norm_word in enumerate(norms):
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


def _load_wordlist(path: Optional[str]) -> Tuple[List[str], List[str]]:
    if not path:
        return ([], [])
    p = Path(path)
    key = str(p.resolve())
    if key in _WORDLIST_CACHE and key in _WORDLIST_NORM_CACHE:
        return (_WORDLIST_CACHE[key], _WORDLIST_NORM_CACHE[key])
    if not p.exists():
        _WORDLIST_CACHE[key] = []
        _WORDLIST_NORM_CACHE[key] = []
        return ([], [])
    words: List[str] = []
    norms: List[str] = []
    try:
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
    return (words, norms)


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


def _apply_wordlist_correction(text: Optional[str], cfg: OCRConfig) -> Optional[str]:
    if not text:
        return text
    truncated = _is_truncated_text(text)
    base = _normalize_ocr_input(text.replace("â€¦", "...").replace(".", " "))
    if not base:
        return text
    base_norm = _normalize_word(base)
    words, norms = _load_wordlist(cfg.user_words_path)
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


_HEALTH_RE = re.compile(r"(\d+)\s*[/\\|Iil]\s*(\d+)")
_HEALTH_NUM_RE = re.compile(r"\d+")


def _parse_health(text: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    if not text:
        return (None, None)
    m = _HEALTH_RE.search(text)
    if m:
        try:
            cur = int(m.group(1))
            maxv = int(m.group(2))
            return (cur, maxv)
        except Exception:
            return (None, None)
    nums = _HEALTH_NUM_RE.findall(text)
    if len(nums) >= 2:
        try:
            return (int(nums[0]), int(nums[1]))
        except Exception:
            return (None, None)
    if len(nums) == 1:
        try:
            return (int(nums[0]), None)
        except Exception:
            return (None, None)
    return (None, None)


def _first_number(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    m = _HEALTH_NUM_RE.search(text)
    if not m:
        return None
    try:
        return int(m.group(0))
    except Exception:
        return None


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


def _ocr_health_split(img_bgr: np.ndarray, cfg: OCRConfig) -> Tuple[Optional[int], Optional[int]]:
    if img_bgr.size == 0:
        return (None, None)
    h, w = img_bgr.shape[:2]
    if w == 0:
        return (None, None)
    left_end = max(1, int(w * 0.60))
    right_start = min(w - 1, int(w * 0.40))
    left_crop = img_bgr[:, :left_end]
    right_crop = img_bgr[:, right_start:]
    digits_only = "0123456789"
    left_text = _ocr_text(left_crop, cfg, digits_only, prefer_red=False, clahe=True, backend_override="tesseract")
    right_text = _ocr_text(right_crop, cfg, digits_only, prefer_red=False, clahe=True, backend_override="tesseract")
    return (_first_number(left_text), _first_number(right_text))


def _easyocr_health(img_bgr: np.ndarray, cfg: OCRConfig) -> Tuple[Optional[int], Optional[int]]:
    if img_bgr.size == 0:
        return (None, None)
    try:
        from ocr_easy.adapter import read_text, read_text_with_boxes
    except Exception:
        return (None, None)

    def _read_combined(prepped: np.ndarray) -> str:
        results = read_text_with_boxes(prepped, cfg, allowlist="0123456789/")
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
        return read_text(prepped, cfg, allowlist="0123456789/") or ""

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

    for invert in (False, True):
        prepped = _prep_tesseract_health(img_bgr, cfg, invert=invert)
        text = _read_combined(prepped)
        cur, maxv = _parse_text(text)
        if cur is not None:
            best_cur = cur
        if maxv is not None:
            best_max = maxv
        if cur is not None and maxv is not None:
            return (cur, maxv)

    if best_cur is not None and best_max is not None:
        return (best_cur, best_max)

    for invert in (False, True):
        prepped = _prep_plain_health(img_bgr, cfg, invert=invert)
        text = _read_combined(prepped)
        cur, maxv = _parse_text(text)
        if cur is not None and best_cur is None:
            best_cur = cur
        if maxv is not None and best_max is None:
            best_max = maxv
        if best_cur is not None and best_max is not None:
            return (best_cur, best_max)
    return (None, None)


def _ocr_health(img_bgr: np.ndarray, cfg: OCRConfig) -> Tuple[Optional[int], Optional[int]]:
    candidates: List[Tuple[int, Optional[int], Optional[int]]] = []

    def _try(text: Optional[str]) -> None:
        if not text:
            return
        cur, maxv = _parse_health(text)
        cur, maxv = _normalize_health_pair(cur, maxv)
        if cur is None and maxv is None:
            return
        candidates.append((_health_score(cur, maxv), cur, maxv))

    _try(_ocr_text(img_bgr, cfg, cfg.health_whitelist, prefer_red=True, backend_override="tesseract"))
    _try(
        _ocr_text(
            img_bgr,
            cfg,
            cfg.health_whitelist,
            prefer_red=True,
            invert_override=True,
            backend_override="tesseract",
        )
    )
    _try(_ocr_text(img_bgr, cfg, cfg.health_whitelist, prefer_red=False, backend_override="tesseract"))
    _try(
        _ocr_text(
            img_bgr,
            cfg,
            cfg.health_whitelist,
            prefer_red=False,
            invert_override=True,
            backend_override="tesseract",
        )
    )

    best = max(candidates, key=lambda item: item[0], default=None)
    if best is not None and best[2] is not None:
        return (best[1], best[2])

    split_cur, split_max = _ocr_health_split(img_bgr, cfg)
    split_cur, split_max = _normalize_health_pair(split_cur, split_max)
    if split_cur is not None or split_max is not None:
        candidates.append((_health_score(split_cur, split_max), split_cur, split_max))

    best = max(candidates, key=lambda item: item[0], default=None)
    if best is None:
        return (None, None)
    return (best[1], best[2])


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


_PIP_TEMPLATE_CACHE: Dict[str, List[Tuple[str, np.ndarray]]] = {}
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
) -> Tuple[Optional[str], float]:
    if crop_bgr.size == 0 or not templates:
        return None, 0.0
    crop_gray = _ensure_gray(crop_bgr)
    best_name = None
    best_score = -1.0
    for name, templ in templates:
        try:
            resized = cv2.resize(crop_gray, (templ.shape[1], templ.shape[0]), interpolation=cv2.INTER_AREA)
        except Exception:
            continue
        res = cv2.matchTemplate(resized, templ, cv2.TM_CCOEFF_NORMED)
        score = float(res[0][0])
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
    return _match_named_template(school_bgr, templates, cfg.template_threshold)


def _load_pip_templates(cfg: PipDetectConfig, aspect_key: str) -> List[Tuple[str, np.ndarray]]:
    base = Path(cfg.templates_base_dir)
    cache_key = f"{base.resolve()}::{aspect_key}"
    if cache_key in _PIP_TEMPLATE_CACHE:
        return _PIP_TEMPLATE_CACHE[cache_key]

    if not base.exists():
        _PIP_TEMPLATE_CACHE[cache_key] = []
        return []

    suffixes = _template_suffixes_for_aspect(aspect_key)
    templates: List[Tuple[str, np.ndarray]] = []
    for folder in sorted(p for p in base.iterdir() if p.is_dir()):
        token = folder.name.lower()
        for png in sorted(folder.glob("*.png")):
            stem = png.stem.strip().lower()
            if not any(stem.endswith(suf) for suf in suffixes):
                continue
            img = cv2.imread(str(png), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            templates.append((token, img))

    _PIP_TEMPLATE_CACHE[cache_key] = templates
    return templates


def _match_pip_template(
    crop_gray: np.ndarray,
    templates: List[Tuple[str, np.ndarray]],
    threshold: float,
) -> Optional[str]:
    if crop_gray.size == 0 or not templates:
        return None
    best_name = None
    best_score = -1.0
    for name, templ in templates:
        try:
            resized = cv2.resize(crop_gray, (templ.shape[1], templ.shape[0]), interpolation=cv2.INTER_AREA)
        except Exception:
            continue
        res = cv2.matchTemplate(resized, templ, cv2.TM_CCOEFF_NORMED)
        score = float(res[0][0])
        if score > best_score:
            best_score = score
            best_name = name
    if best_score >= threshold:
        return best_name
    return None


def _pip_counts(pips_bgr: np.ndarray, cfg: PipDetectConfig, aspect_key: str) -> PipInventory:
    counts = PipInventory()
    if pips_bgr.size == 0:
        return counts

    hsv = cv2.cvtColor(pips_bgr, cv2.COLOR_BGR2HSV)
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    white = (s <= cfg.white_sat_max) & (v >= cfg.white_val_min)
    colored = (s >= cfg.school_sat_min) & (v >= cfg.school_val_min)
    candidate = white | colored

    kernel = np.ones((3, 3), np.uint8)
    candidate_mask = cv2.morphologyEx(candidate.astype(np.uint8) * 255, cv2.MORPH_OPEN, kernel)

    area = pips_bgr.shape[0] * pips_bgr.shape[1]
    min_area = max(1, int(area * cfg.min_area_frac))
    max_area = max(1, int(area * cfg.max_area_frac))

    tokens: List[str] = []
    templates = _load_pip_templates(cfg, aspect_key)
    if templates:
        num, _, stats, _ = cv2.connectedComponentsWithStats(candidate_mask, connectivity=8)
        for i in range(1, num):
            blob_area = stats[i, cv2.CC_STAT_AREA]
            if blob_area < min_area or blob_area > max_area:
                continue
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            pad = max(1, int(min(w, h) * 0.15))
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(pips_bgr.shape[1], x + w + pad)
            y2 = min(pips_bgr.shape[0], y + h + pad)
            crop = pips_bgr[y1:y2, x1:x2]
            crop_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            match = _match_pip_template(crop_gray, templates, cfg.template_threshold)
            if match == "regular":
                tokens.append("pip")
            elif match:
                tokens.append(match)
            else:
                tokens.append("unknown")
    else:
        num = _count_blobs(candidate_mask, min_area, max_area)
        tokens.extend(["unknown"] * num)

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
    skip_health_ocr: bool = False,
    health_override: Optional[Tuple[Optional[int], Optional[int]]] = None,
    occupied_override: Optional[bool] = None,
    debug_dump: bool = False,
    debug_dump_health: bool = False,
    debug_dump_empty_names: bool = False,
    debug_dump_sigil_roi: bool = False,
    debug_dump_school_roi: bool = False,
    debug_dump_id: Optional[str] = None,
    debug_dump_limit: int = 0,
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

    name_crop = crop_relative(frame_bgr, name_roi)
    health_crop = crop_relative(frame_bgr, health_roi)
    pips_crop = crop_relative(frame_bgr, pips_roi)
    school_crop = crop_relative(frame_bgr, school_roi)
    _dump_participant_roi(school_crop, kind="school", side=side, index=index, enabled=debug_dump_school_roi)
    school_match, school_score = _detect_school(school_crop, cfg.school, aspect_key, side)

    if debug_dump_health and index == 0 and side in ("enemy", "ally"):
        prepped = None
        if cfg.ocr.backend == "easyocr":
            prepped = (
                ("prepped", _prep_plain_health(health_crop, cfg.ocr, invert=False)),
                ("prepped_inv", _prep_plain_health(health_crop, cfg.ocr, invert=True)),
            )
        _dump_health_roi(
            health_crop,
            side=side,
            index=index,
            debug_dump_id=debug_dump_id,
            prepped=prepped,
        )

    tag = f"{side}_{index}_name"
    name_text = None
    if skip_name_ocr:
        name_text = name_override
        name_raw = name_raw_override
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
        name_text = _apply_wordlist_correction(name_text, cfg.ocr)

    if (not skip_name_ocr) and (not name_text) and debug_dump and (not debug_dump_empty_names) and debug_dump_id:
        _remove_ocr_dumps_with_prefix(tag, dump_id=slot_dump_id)

    if skip_health_ocr:
        if health_override is None:
            health_current, health_max = (None, None)
        else:
            health_current, health_max = health_override
    else:
        health_current, health_max = _ocr_health(health_crop, cfg.ocr)
    pips = _pip_counts(pips_crop, cfg.pip, aspect_key)

    return ParticipantState(
        side=side,
        index=index,
        rel_roi=box_roi,
        sigil=sigil_match,
        sigil_score=sigil_score,
        name=name_text,
        name_raw=name_raw,
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
    timestamp: Optional[float] = None,
    debug_dump: bool = False,
    debug_dump_health: bool = False,
    debug_dump_empty_names: bool = False,
    debug_dump_sigil_roi: bool = False,
    debug_dump_school_roi: bool = False,
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

    prev_enemies = previous.enemies if previous else []
    prev_allies = previous.allies if previous else []

    def _prev_for(side: str, idx: int) -> Optional[ParticipantState]:
        arr = prev_enemies if side == "enemy" else prev_allies
        if idx < len(arr):
            return arr[idx]
        return None

    for i in range(profile.slots):
        enemy_roi = _shift_roi(profile.enemy_first_box, profile.enemy_spacing_x * i)
        if profile.ally_anchor == "right":
            ally_roi = _shift_roi(profile.ally_first_box, -profile.ally_spacing_x * i)
        else:
            ally_roi = _shift_roi(profile.ally_first_box, profile.ally_spacing_x * i)
        prev_enemy = _prev_for("enemy", i) if (skip_health_ocr or skip_name_ocr) else None
        prev_ally = _prev_for("ally", i) if (skip_health_ocr or skip_name_ocr) else None
        enemies.append(
            _extract_participant(
                frame_bgr,
                "enemy",
                i,
                enemy_roi,
                cfg,
                skip_name_ocr=skip_name_ocr,
                name_override=(prev_enemy.name if prev_enemy is not None else None),
                name_raw_override=(prev_enemy.name_raw if prev_enemy is not None else None),
                skip_health_ocr=skip_health_ocr,
                health_override=(
                    (prev_enemy.health_current, prev_enemy.health_max) if prev_enemy is not None else None
                ),
                occupied_override=(prev_enemy.occupied if prev_enemy is not None else None),
                debug_dump=debug_dump,
                debug_dump_health=debug_dump_health,
                debug_dump_empty_names=debug_dump_empty_names,
                debug_dump_sigil_roi=debug_dump_sigil_roi,
                debug_dump_school_roi=debug_dump_school_roi,
                debug_dump_id=debug_dump_id,
                debug_dump_limit=debug_dump_limit,
            )
        )
        allies.append(
            _extract_participant(
                frame_bgr,
                "ally",
                i,
                ally_roi,
                cfg,
                skip_name_ocr=skip_name_ocr,
                name_override=(prev_ally.name if prev_ally is not None else None),
                name_raw_override=(prev_ally.name_raw if prev_ally is not None else None),
                skip_health_ocr=skip_health_ocr,
                health_override=((prev_ally.health_current, prev_ally.health_max) if prev_ally is not None else None),
                occupied_override=(prev_ally.occupied if prev_ally is not None else None),
                debug_dump=debug_dump,
                debug_dump_health=debug_dump_health,
                debug_dump_empty_names=debug_dump_empty_names,
                debug_dump_sigil_roi=debug_dump_sigil_roi,
                debug_dump_school_roi=debug_dump_school_roi,
                debug_dump_id=debug_dump_id,
                debug_dump_limit=debug_dump_limit,
            )
        )

    state.enemies = enemies
    state.allies = allies
    state.profile = bucket
    state.detected = True
    return state


def render_participants_overlay(
    frame_bgr: np.ndarray,
    state: ParticipantsState,
    *,
    draw_sub_rois: bool = True,
    show_pip_detection: bool = False,
    initiative_side: Optional[str] = None,
) -> np.ndarray:
    vis = frame_bgr.copy()
    aspect_key = _aspect_bucket(frame_bgr.shape[1] / frame_bgr.shape[0]) if frame_bgr.size else "unknown"
    _draw_participants_legend(vis, initiative_side, aspect_key)
    for p in state.enemies + state.allies:
        box_color = (0, 255, 255) if p.occupied else (128, 128, 128)
        draw_relative_roi(vis, p.rel_roi, None, color=box_color, copy=False)
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


_ALLY_SIGILS = ["sun", "eye", "star", "moon"]
_ENEMY_SIGILS = ["dagger", "key", "ruby", "spiral"]


def _draw_participants_legend(vis: np.ndarray, initiative_side: Optional[str], aspect_key: str) -> None:
    h, w = vis.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.45
    thickness = 1
    line_h = 16
    pad = 6
    init_label = f"initiative: {initiative_side or 'unknown'}"
    aspect_label = f"aspect: {aspect_key}"

    lines = [
        ("box", (0, 255, 255)),
        ("sigil", (255, 0, 255)),
        ("school", (0, 165, 255)),
        ("name", (255, 0, 0)),
        ("hp", (0, 255, 0)),
        ("pips", (255, 255, 0)),
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
        token_color = _token_color(token)
        (tw, _), _ = cv2.getTextSize(token_label, font, scale, thickness)
        cv2.putText(vis, token_label, (cursor, y), font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
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
    "balance": (0, 170, 255),
    "death": (80, 0, 80),
    "fire": (0, 0, 255),
    "ice": (255, 200, 80),
    "life": (0, 200, 0),
    "myth": (0, 215, 255),
    "storm": (255, 0, 255),
}

_TOKEN_COLORS: Dict[str, Tuple[int, int, int]] = {
    "pip": (255, 255, 255),
    "power": (0, 215, 255),
    "unknown": (180, 180, 180),
}


def _token_label(token: str) -> str:
    if token == "pip":
        return "p"
    if token == "power":
        return "P"
    if token in _SCHOOL_COLORS:
        return token[0].upper()
    return "?"


def _token_color(token: str) -> Tuple[int, int, int]:
    if token in _SCHOOL_COLORS:
        return _SCHOOL_COLORS[token]
    return _TOKEN_COLORS.get(token, (180, 180, 180))


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
        color = _token_color(token)
        (tw, th), _ = cv2.getTextSize(label, font, scale, thickness)
        cv2.putText(vis, label, (x, y), font, scale, color, thickness, cv2.LINE_AA)
        x += tw + 6
        total += _pip_token_value(token)

    total_label = f"= {total}"
    cv2.putText(vis, total_label, (x + 2, y), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)
