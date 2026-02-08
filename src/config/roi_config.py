from dataclasses import dataclass
from typing import Dict, Tuple, Optional

from state.initiative import RingProfile
from state.participants import ParticipantBoxProfile, ParticipantLayout, PlayerHUDProfile


@dataclass(frozen=True)
class ButtonROIProfile:
    pass_rel_roi: Tuple[float, float, float, float]
    flee_rel_roi: Tuple[float, float, float, float]
    crowns_shop_rel_roi: Tuple[float, float, float, float]
    upgrade_now_rel_roi: Tuple[float, float, float, float]
    friends_rel_roi: Tuple[float, float, float, float]
    social_rel_roi: Tuple[float, float, float, float]
    spell_book_rel_roi: Tuple[float, float, float, float]
    concede_rel_roi: Optional[Tuple[float, float, float, float]] = None


@dataclass(frozen=True)
class ButtonROIConfig:
    profiles: Dict[str, ButtonROIProfile]
    templates_base_dir: str = "src/assets/buttons"
    threshold: float = 0.78

BUTTON_ROI_CFG = ButtonROIConfig(
    profiles={
        "4:3": ButtonROIProfile(
            pass_rel_roi=(0.197, 0.615, 0.335, 0.683),
            flee_rel_roi=(0.665, 0.615, 0.802, 0.683),
            crowns_shop_rel_roi=(0.019, 0.042, 0.07, 0.10),
            upgrade_now_rel_roi=(0.107, 0.03, 0.162, 0.095),
            friends_rel_roi=(0.938, 0.025, 0.985, 0.08),
            social_rel_roi=(0.942, 0.13, 0.982, 0.185),
            spell_book_rel_roi=(0.89, 0.83, 0.95, 0.96),
            concede_rel_roi=(0.665, 0.615, 0.802, 0.683),
        ),
        "16:9": ButtonROIProfile(
            pass_rel_roi=(0.28, 0.61, 0.38, 0.675),
            flee_rel_roi=(0.62, 0.61, 0.72, 0.675),
            crowns_shop_rel_roi=(0.015, 0.04, 0.052, 0.10),
            upgrade_now_rel_roi=(0.078, 0.035, 0.117, 0.09),
            friends_rel_roi=(0.96, 0.025, 0.985, 0.08),
            social_rel_roi=(0.96, 0.125, 0.985, 0.185),
            spell_book_rel_roi=(0.917, 0.83, 0.96, 0.96),
            concede_rel_roi=(0.62, 0.61, 0.72, 0.675),
        ),
        "43:18": ButtonROIProfile(
            pass_rel_roi=(0.335, 0.61, 0.413, 0.68),
            flee_rel_roi=(0.588, 0.61, 0.665, 0.68),
            crowns_shop_rel_roi=(0.011, 0.04, 0.038, 0.10),
            upgrade_now_rel_roi=(0.058, 0.035, 0.089, 0.09),
            friends_rel_roi=(0.967, 0.025, 0.992, 0.08),
            social_rel_roi=(0.969, 0.127, 0.99, 0.184),
            spell_book_rel_roi=(0.94, 0.83, 0.975, 0.96),
            concede_rel_roi=(0.588, 0.61, 0.665, 0.68),
        ),
    }
)


@dataclass(frozen=True)
class TurnOrderROIConfig:
    rel_roi: Tuple[float, float, float, float] = (0.25, 0.03, 0.75, 0.15)


TURN_ORDER_ROI_CFG = TurnOrderROIConfig()


PARTICIPANT_BOX_PROFILES: Dict[str, ParticipantBoxProfile] = {
    "4:3": ParticipantBoxProfile(
        enemy_first_box=(0.078, 0.000, 0.28, 0.115),
        ally_first_box=(0.763, 0.855, 0.96, 1.000),
        enemy_spacing_x=0.201,
        ally_spacing_x=0.1935,
        ally_anchor="right",
    ),
    "16:9": ParticipantBoxProfile(
        enemy_first_box=(0.057, 0.000, 0.21, 0.115),
        ally_first_box=(0.76, 0.855, 0.910, 1.000),
        enemy_spacing_x=0.2138,
        ally_spacing_x=0.2088,
        ally_anchor="right",
    ),
    "43:18": ParticipantBoxProfile(
        enemy_first_box=(0.042, 0.000, 0.157, 0.115),
        ally_first_box=(0.7555, 0.855, 0.868, 1.000),
        enemy_spacing_x=0.223,
        ally_spacing_x=0.2185,
        ally_anchor="right",
    ),
}


PARTICIPANT_LAYOUT = ParticipantLayout(
    sigil_roi_enemy=(0.07, 0.45, 0.28, 0.75),
    sigil_roi_ally=(0.07, 0.25, 0.28, 0.55),
    school_roi_enemy=(0.00, 0.05, 0.15, 0.35),
    school_roi_ally=(0.00, 0.60, 0.15, 0.85),
    name_roi_enemy=(0.31, 0.25, 0.985, 0.52),
    health_roi_enemy=(0.31, 0.50, 0.985, 0.79),
    name_roi_ally=(0.32, 0.25, 0.90, 0.50),
    health_roi_ally=(0.32, 0.475, 0.92, 0.67),
    pips_roi_enemy=(0.25, 0.00, 0.985, 0.25),
    pips_roi_ally=(0.25, 0.67, 0.99, 0.95),
)


PLAYER_HUD_PROFILES: Dict[str, PlayerHUDProfile] = {
    # Bottom-left HUD numeric overlays: health (red orb), mana (blue orb), energy (green orb).
    "4:3": PlayerHUDProfile(
        health_roi=(0.0217, 0.82, 0.12, 0.872),
        mana_roi=(0.11, 0.878, 0.18, 0.92),
        energy_roi=(0.058, 0.908, 0.108, 0.94),
    ),
    "16:9": PlayerHUDProfile(
        health_roi=(0.018, 0.83, 0.09, 0.873),
        mana_roi=(0.08, 0.88, 0.13, 0.923),
        energy_roi=(0.042, 0.908, 0.078, 0.942),
    ),
    "43:18": PlayerHUDProfile(
        health_roi=(0.014, 0.825, 0.067, 0.875),
        mana_roi=(0.06, 0.88, 0.098, 0.923),
        energy_roi=(0.03, 0.908, 0.058, 0.942),
    ),
}


# Pip-slot slicing debug tuning.
# Debug dump upscale factor applied before pip-slot guideline/crop slicing.
PIP_SLOT_DEBUG_UPSCALE: int = 4

# `PIP_SLOT_WIDTH_PX_BY_ASPECT_ALLY` is the width of one pip slot in pixels,
# keyed by aspect ratio. Values are interpreted in the upscaled debug ROI space.
# `PIP_SLOT_GAP_PX_BY_ASPECT_ALLY` is the inter-slot spacing (bloom exclusion)
# in pixels, keyed by aspect ratio. Values are interpreted in the upscaled debug ROI space.
# `PIP_SLOT_START_PX_BY_ASPECT_ALLY` is the left-edge start for slot 1, per combat slot sigil,
# in pixels in the upscaled debug ROI space.
# `PIP_SLOT_TOP_CUT_PX_BY_ASPECT_ALLY` and `PIP_SLOT_BOTTOM_CUT_PX_BY_ASPECT_ALLY`
# trim each slot crop vertically in the upscaled debug ROI space.
# `PIP_SLOT_PRESENCE_CONFIDENCE_THRESHOLD_ALLY` is the minimum best-template match
# score required before an ally slot is treated as containing a pip.
PIP_SLOT_WIDTH_PX_ALLY_DEFAULT: int = 15
PIP_SLOT_WIDTH_PX_BY_ASPECT_ALLY: Dict[str, int] = {
    "4:3": 40,
    "16:9": 37, # SLOT WIDTH
    "43:18": 31,
}
PIP_SLOT_WIDTH_PX_ENEMY_DEFAULT: int = 15
PIP_SLOT_WIDTH_PX_BY_ASPECT_ENEMY: Dict[str, int] = {
    "4:3": 40,
    "16:9": 37,
    "43:18": 31,
}
PIP_SLOT_GAP_PX_ALLY_DEFAULT: int = 0
PIP_SLOT_GAP_PX_BY_ASPECT_ALLY: Dict[str, int] = {
    "4:3": 33,
    "16:9": 38, # SLOT GAP
    "43:18": 25,
}
PIP_SLOT_GAP_PX_ENEMY_DEFAULT: int = 0
PIP_SLOT_GAP_PX_BY_ASPECT_ENEMY: Dict[str, int] = {
    "4:3": 33,
    "16:9": 38,
    "43:18": 25,
}
PIP_SLOT_START_PX_ALLY_DEFAULT: int = 0
PIP_SLOT_START_PX_ENEMY_DEFAULT: int = 0
PIP_SLOT_TOP_CUT_PX_ALLY_DEFAULT: int = 0
PIP_SLOT_TOP_CUT_PX_BY_ASPECT_ALLY: Dict[str, int] = {
    "4:3": 13,
    "16:9": 12, # TOP CUT
    "43:18": 10,
}
PIP_SLOT_TOP_CUT_PX_ENEMY_DEFAULT: int = 0
PIP_SLOT_TOP_CUT_PX_BY_ASPECT_ENEMY: Dict[str, int] = {
    "4:3": 0,
    "16:9": 0,
    "43:18": 0,
}
PIP_SLOT_BOTTOM_CUT_PX_ALLY_DEFAULT: int = 0
PIP_SLOT_BOTTOM_CUT_PX_BY_ASPECT_ALLY: Dict[str, int] = {
    "4:3": 22,
    "16:9": 18, # BOTTOM CUT
    "43:18": 18,
}
PIP_SLOT_BOTTOM_CUT_PX_ENEMY_DEFAULT: int = 0
PIP_SLOT_BOTTOM_CUT_PX_BY_ASPECT_ENEMY: Dict[str, int] = {
    "4:3": 0,
    "16:9": 0,
    "43:18": 0,
}
PIP_SLOT_PRESENCE_CONFIDENCE_THRESHOLD_ALLY: float = 0.70
PIP_SLOT_PRESENCE_CONFIDENCE_THRESHOLD_ENEMY: float = 0.70
PIP_SLOT_COUNT: int = 7
PIP_SLOT_START_PX_BY_ASPECT_ALLY: Dict[str, Dict[str, int]] = {
    "4:3": {
        "dagger": 45,
        "key": 45,
        "ruby": 45,
        "spiral": 45,
        "sun": 45,
        "eye": 45,
        "star": 45,
        "moon": 45,
    },
    "16:9": {
        "dagger": 45,
        "key": 45,
        "ruby": 45,
        "spiral": 45, # START LOCATION
        "sun": 45,
        "eye": 45,
        "star": 45,
        "moon": 45,
    },
    "43:18": {
        "dagger": 37,
        "key": 37,
        "ruby": 37,
        "spiral": 37,
        "sun": 37,
        "eye": 37,
        "star": 37,
        "moon": 37,
    },
}
PIP_SLOT_START_PX_BY_ASPECT_ENEMY: Dict[str, Dict[str, int]] = {
    "4:3": {
        "dagger": 40,
        "key": 40,
        "ruby": 40,
        "spiral": 40,
        "sun": 40,
        "eye": 40,
        "star": 40,
        "moon": 40,
    },
    "16:9": {
        "dagger": 45,
        "key": 45,
        "ruby": 45,
        "spiral": 45,
        "sun": 45,
        "eye": 45,
        "star": 45,
        "moon": 45,
    },
    "43:18": {
        "dagger": 31,
        "key": 31,
        "ruby": 31,
        "spiral": 31,
        "sun": 31,
        "eye": 31,
        "star": 31,
        "moon": 31,
    },
}


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
