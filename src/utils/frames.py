# utils/frames.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
import cv2
import numpy as np

@dataclass
class FrameBundle:
    native: np.ndarray
    _norm_cache: Optional[np.ndarray] = None
    _norm_key: Optional[Tuple[int, int, int]] = None  # (ref_w, ref_h, allow_upscale)

    def normalized(
        self,
        ref_w: int = 1280,
        ref_h: int = 720,
        allow_upscale: bool = False,
    ) -> np.ndarray:
        """
        Aspect-preserving resize to fit within (ref_w, ref_h).
        - No letterboxing (output size may be smaller than ref_w/ref_h).
        - If allow_upscale=False: never enlarge small frames.
        - If allow_upscale=True: enlarge frames up to the ref bounds.
        Cached after first call per (ref_w, ref_h, allow_upscale).
        """
        key = (ref_w, ref_h, int(allow_upscale))
        if self._norm_cache is not None and self._norm_key == key:
            return self._norm_cache

        h, w = self.native.shape[:2]
        scale = min(ref_w / w, ref_h / h)

        if not allow_upscale:
            scale = min(scale, 1.0)

        if scale == 1.0:
            out = self.native
        else:
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            out = cv2.resize(self.native, (new_w, new_h), interpolation=cv2.INTER_AREA)

        self._norm_cache = out
        self._norm_key = key
        return out

    def invalidate_cache(self):
        self._norm_cache = None
        self._norm_key = None
