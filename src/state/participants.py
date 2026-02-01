from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time
from typing import Dict, Optional, Tuple, List
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
_OCR_DUMP_COUNTS: Dict[str, int] = {}
_WORDLIST_CACHE: Dict[str, List[str]] = {}
_WORDLIST_NORM_CACHE: Dict[str, List[str]] = {}


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


@dataclass(frozen=True)
class ParticipantsConfig:
    profiles: Dict[str, ParticipantBoxProfile]
    layout: ParticipantLayout
    pip: PipDetectConfig
    ocr: OCRConfig


def _aspect_bucket(aspect: float) -> str:
    targets = {
        "4:3": 4.0 / 3.0,
        "16:10": 16.0 / 10.0,
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


def _normalize_word(text: str) -> str:
    filtered = []
    for ch in text.upper():
        if ch.isalpha() or ch == " ":
            filtered.append(ch)
    return " ".join("".join(filtered).split())


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


def _match_wordlist_substring(substring: str, cfg: OCRConfig) -> Optional[str]:
    if not substring or len(substring) < cfg.wordlist_prefix_min_chars:
        return None
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
    words, norms = _load_wordlist(cfg.user_words_path)
    if not words:
        return text
    truncated = _is_truncated_text(text)
    norm_text = _normalize_word(text.replace(".", "").replace("…", ""))
    if not norm_text:
        return text
    if truncated:
        substring_match = _match_wordlist_substring(norm_text, cfg)
        if substring_match:
            return substring_match
        prefix_match = _match_wordlist_prefix(norm_text, cfg)
        if prefix_match:
            return prefix_match
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
    # If no close edit-distance match, try prefix match even without ellipsis.
    prefix_match = _match_wordlist_prefix(norm_text, cfg)
    if prefix_match:
        return prefix_match
    return text


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
) -> Optional[str]:
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


_HEALTH_RE = re.compile(r"(\d+)\s*/\s*(\d+)")


def _parse_health(text: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    if not text:
        return (None, None)
    m = _HEALTH_RE.search(text)
    if not m:
        return (None, None)
    try:
        cur = int(m.group(1))
        maxv = int(m.group(2))
        return (cur, maxv)
    except Exception:
        return (None, None)


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


def _template_suffixes_for_aspect(aspect_key: str) -> Tuple[str, ...]:
    if aspect_key == "4:3":
        return ("_4x3",)
    if aspect_key == "16:10":
        return ("_16x10",)
    if aspect_key == "16:9":
        return ("_16x9",)
    if aspect_key == "43:18":
        return ("_43x18",)
    return ("_16x9",)


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
    debug_dump: bool = False,
    debug_dump_id: Optional[str] = None,
    debug_dump_limit: int = 0,
) -> ParticipantState:
    slot_dump_id = f"{debug_dump_id}_{side}_{index}" if debug_dump_id else None
    layout = cfg.layout
    is_enemy = side == "enemy"

    name_rel = layout.name_roi_enemy if is_enemy else layout.name_roi_ally
    health_rel = layout.health_roi_enemy if is_enemy else layout.health_roi_ally
    pips_rel = layout.pips_roi_enemy if is_enemy else layout.pips_roi_ally

    name_roi = _sub_roi(box_roi, name_rel)
    health_roi = _sub_roi(box_roi, health_rel)
    pips_roi = _sub_roi(box_roi, pips_rel)
    name_crop = crop_relative(frame_bgr, name_roi)
    health_crop = crop_relative(frame_bgr, health_roi)
    pips_crop = crop_relative(frame_bgr, pips_roi)

    health_text = _ocr_text(health_crop, cfg.ocr, cfg.ocr.health_whitelist, prefer_red=True)
    if not health_text:
        health_text = _ocr_text(
            health_crop,
            cfg.ocr,
            cfg.ocr.health_whitelist,
            prefer_red=True,
            invert_override=True,
        )
    health_current, health_max = _parse_health(health_text)
    occupied = health_current is not None or health_max is not None
    if not occupied:
        return ParticipantState(
            side=side,
            index=index,
            rel_roi=box_roi,
            name=None,
            name_raw=None,
            health_current=None,
            health_max=None,
            pips=PipInventory(),
            occupied=False,
            name_roi=name_roi,
            health_roi=health_roi,
            pips_roi=pips_roi,
        )

    name_text = _ocr_name_per_char(name_crop, cfg.ocr)
    tag = f"{side}_{index}_name"
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

    aspect_key = _aspect_bucket(frame_bgr.shape[1] / frame_bgr.shape[0])
    pips = _pip_counts(pips_crop, cfg.pip, aspect_key)

    return ParticipantState(
        side=side,
        index=index,
        rel_roi=box_roi,
        name=name_text,
        name_raw=name_raw,
        health_current=health_current,
        health_max=health_max,
        pips=pips,
        occupied=occupied,
        name_roi=name_roi,
        health_roi=health_roi,
        pips_roi=pips_roi,
    )


def extract_participants(
    frame_bgr: np.ndarray,
    cfg: ParticipantsConfig,
    *,
    timestamp: Optional[float] = None,
    debug_dump: bool = False,
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

    for i in range(profile.slots):
        enemy_roi = _shift_roi(profile.enemy_first_box, profile.enemy_spacing_x * i)
        if profile.ally_anchor == "right":
            ally_roi = _shift_roi(profile.ally_first_box, -profile.ally_spacing_x * i)
        else:
            ally_roi = _shift_roi(profile.ally_first_box, profile.ally_spacing_x * i)
        enemies.append(
            _extract_participant(
                frame_bgr,
                "enemy",
                i,
                enemy_roi,
                cfg,
                debug_dump=debug_dump,
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
                debug_dump=debug_dump,
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
        if not p.occupied:
            draw_relative_roi(vis, p.rel_roi, None, color=(128, 128, 128), thickness=1, copy=False)
            _draw_box_label(vis, p)
            continue

        draw_relative_roi(vis, p.rel_roi, None, color=(0, 255, 255), thickness=1, copy=False)
        _draw_box_label(vis, p)
        if draw_sub_rois:
            if p.name_roi:
                draw_relative_roi(vis, p.name_roi, None, color=(255, 0, 0), thickness=1, copy=False)
            if p.health_roi:
                draw_relative_roi(vis, p.health_roi, None, color=(0, 255, 0), thickness=1, copy=False)
            if p.pips_roi:
                draw_relative_roi(vis, p.pips_roi, None, color=(255, 255, 0), thickness=1, copy=False)
        if show_pip_detection and p.pips is not None:
            _draw_pip_tokens(vis, p)
    return vis


_ALLY_SIGILS = ["moon", "star", "eye", "sun"]
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

    sigil = _sigil_name(participant)
    empty = not participant.occupied

    if empty:
        lines = ["empty slot"]
    else:
        name = participant.name or "unknown"
        cur = "?" if participant.health_current is None else str(participant.health_current)
        maxv = "?" if participant.health_max is None else str(participant.health_max)
        lines = [
            f"{sigil} | {name}",
            f"hp {cur}/{maxv}",
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
    for i, text in enumerate(lines):
        ty = y - (total_h - line_h) + i * line_h
        if i == 2 and not empty:
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
