from __future__ import annotations

from typing import Optional, Any, List, Tuple
from pathlib import Path
import threading

import numpy as np

_READER = None
_READER_LOCK = threading.Lock()
_INIT_ERROR: Optional[Exception] = None


def _build_reader(cfg: Any):
    import easyocr

    if cfg.easyocr_model_dir:
        Path(cfg.easyocr_model_dir).mkdir(parents=True, exist_ok=True)

    return easyocr.Reader(
        list(cfg.easyocr_langs),
        gpu=cfg.easyocr_gpu,
        model_storage_directory=cfg.easyocr_model_dir,
        download_enabled=True,
    )


def _get_reader(cfg: Any):
    global _READER
    global _INIT_ERROR
    if _READER is not None:
        return _READER
    if _INIT_ERROR is not None:
        raise _INIT_ERROR
    with _READER_LOCK:
        if _READER is not None:
            return _READER
        try:
            _READER = _build_reader(cfg)
        except Exception as exc:  # pragma: no cover - depends on optional dep
            _INIT_ERROR = exc
            raise
    return _READER


def read_text(img: np.ndarray, cfg: Any, *, allowlist: Optional[str] = None) -> Optional[str]:
    reader = _get_reader(cfg)
    if allowlist == "":
        allowlist = None
    results = reader.readtext(img, detail=0, allowlist=allowlist)
    if not results:
        return None
    text = " ".join(r.strip() for r in results if r and r.strip())
    return text or None


def read_text_with_boxes(
    img: np.ndarray,
    cfg: Any,
    *,
    allowlist: Optional[str] = None,
) -> List[Tuple[List[Tuple[float, float]], str, float]]:
    reader = _get_reader(cfg)
    if allowlist == "":
        allowlist = None
    results = reader.readtext(img, detail=1, allowlist=allowlist)
    cleaned: List[Tuple[List[Tuple[float, float]], str, float]] = []
    for item in results:
        if not item or len(item) < 3:
            continue
        bbox, text, conf = item[0], item[1], item[2]
        if not text:
            continue
        try:
            conf_val = float(conf)
        except Exception:
            conf_val = 0.0
        cleaned.append((bbox, str(text), conf_val))
    return cleaned
