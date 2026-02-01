from dataclasses import dataclass
from typing import Dict, Tuple

from state.initiative import RingProfile


@dataclass(frozen=True)
class ButtonROIConfig:
    pass_rel_roi: Tuple[float, float, float, float] = (0.25, 0.57, 0.45, 0.63)
    flee_rel_roi: Tuple[float, float, float, float] = (0.55, 0.57, 0.74, 0.63)
    pass_threshold: float = 0.78
    flee_threshold: float = 0.78


BUTTON_ROI_CFG = ButtonROIConfig()


@dataclass(frozen=True)
class TurnOrderROIConfig:
    rel_roi: Tuple[float, float, float, float] = (0.25, 0.03, 0.75, 0.15)


TURN_ORDER_ROI_CFG = TurnOrderROIConfig()


@dataclass(frozen=True)
class InitiativeRingThresholds:
    min_score: float = 0.02
    min_delta: float = 0.01
    white_sat_max: int = 60
    white_val_min: int = 200


INITIATIVE_RING_THRESHOLDS = InitiativeRingThresholds()


# Central place for initiative ring ROIs per aspect ratio.
INITIATIVE_RING_PROFILES: Dict[str, RingProfile] = {
    "4:3": RingProfile(
        sun_center=(0.755, 0.605),
        dagger_center=(0.32, 0.39),
        sun_box_size=(0.1, 0.1),
        dagger_box_size=(0.08, 0.07),
    ),
    "16:10": RingProfile(
        sun_center=(0.705, 0.605),
        dagger_center=(0.36, 0.39),
        sun_box_size=(0.08, 0.1),
        dagger_box_size=(0.06, 0.08),
    ),
    "16:9": RingProfile(
        sun_center=(0.69, 0.605),
        dagger_center=(0.365, 0.39),
        sun_box_size=(0.08, 0.1),
        dagger_box_size=(0.055, 0.075),
    ),
    "43:18": RingProfile(
        sun_center=(0.64, 0.605),
        dagger_center=(0.40, 0.39),
        sun_box_size=(0.065, 0.1),
        dagger_box_size=(0.05, 0.08),
    ),
}
