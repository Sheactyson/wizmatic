from dataclasses import dataclass
from typing import Dict, Tuple

from state.initiative import RingProfile
from state.participants import ParticipantBoxProfile, ParticipantLayout


@dataclass(frozen=True)
class ButtonROIProfile:
    pass_rel_roi: Tuple[float, float, float, float]
    flee_rel_roi: Tuple[float, float, float, float]


@dataclass(frozen=True)
class ButtonROIConfig:
    profiles: Dict[str, ButtonROIProfile]
    pass_threshold: float = 0.78
    flee_threshold: float = 0.78


BUTTON_ROI_CFG = ButtonROIConfig(
    profiles={
        "4:3": ButtonROIProfile(
            pass_rel_roi=(0.197, 0.615, 0.335, 0.683),
            flee_rel_roi=(0.665, 0.615, 0.802, 0.683),
        ),
        "16:9": ButtonROIProfile(
            pass_rel_roi=(0.28, 0.61, 0.38, 0.675),
            flee_rel_roi=(0.62, 0.61, 0.72, 0.675),
        ),
        "43:18": ButtonROIProfile(
            pass_rel_roi=(0.335, 0.61, 0.413, 0.68),
            flee_rel_roi=(0.588, 0.61, 0.665, 0.68),
        ),
    }
)


@dataclass(frozen=True)
class TurnOrderROIConfig:
    rel_roi: Tuple[float, float, float, float] = (0.25, 0.03, 0.75, 0.15)


TURN_ORDER_ROI_CFG = TurnOrderROIConfig()


PARTICIPANT_BOX_PROFILES: Dict[str, ParticipantBoxProfile] = {
    "4:3": ParticipantBoxProfile(
        enemy_first_box=(0.049, 0.001, 0.170, 0.108),
        ally_first_box=(0.110, 0.839, 0.232, 0.992),
        enemy_spacing_x=0.222,
        ally_spacing_x=0.217,
        ally_anchor="right",
    ),
    "16:9": ParticipantBoxProfile(
        enemy_first_box=(0.04, 0.000, 0.160, 0.08),
        ally_first_box=(0.755, 0.895, 0.870, 1.000),
        enemy_spacing_x=0.225,
        ally_spacing_x=0.221,
        ally_anchor="right",
    ),
    "43:18": ParticipantBoxProfile(
        enemy_first_box=(0.049, 0.001, 0.170, 0.108),
        ally_first_box=(0.110, 0.839, 0.232, 0.992),
        enemy_spacing_x=0.222,
        ally_spacing_x=0.217,
        ally_anchor="right",
    ),
}


PARTICIPANT_LAYOUT = ParticipantLayout(
    name_roi_enemy=(0.29, 0.25, 0.86, 0.52),
    health_roi_enemy=(0.285, 0.50, 0.86, 0.79),
    name_roi_ally=(0.31, 0.25, 0.90, 0.50),
    health_roi_ally=(0.305, 0.475, 0.90, 0.69),
    pips_roi_enemy=(0.10, 0.00, 0.94, 0.20),
    pips_roi_ally=(0.25, 0.67, 0.945, 0.95),
)


@dataclass(frozen=True)
class InitiativeRingThresholds:
    templates_base_dir: str = "src/assets/initiative"
    template_min_score: float = 0.05
    template_min_delta: float = 0.02


INITIATIVE_RING_THRESHOLDS = InitiativeRingThresholds()


# Central place for initiative ring ROIs per aspect ratio.
INITIATIVE_RING_PROFILES: Dict[str, RingProfile] = {
    "4:3": RingProfile(
        sun_center=(0.75, 0.60),
        dagger_center=(0.321, 0.397),
        sun_box_size=(0.096, 0.045),
        dagger_box_size=(0.063, 0.045),
    ),
    "16:9": RingProfile(
        sun_center=(0.688, 0.596),
        dagger_center=(0.365, 0.395),
        sun_box_size=(0.075, 0.044),
        dagger_box_size=(0.05, 0.042),
    ),
    "43:18": RingProfile(
        sun_center=(0.64, 0.597),
        dagger_center=(0.40, 0.396),
        sun_box_size=(0.055, 0.045),
        dagger_box_size=(0.04, 0.043),
    ),
}
