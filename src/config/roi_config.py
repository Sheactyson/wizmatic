from dataclasses import dataclass
from typing import Dict, Tuple

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
        ),
        "16:9": ButtonROIProfile(
            pass_rel_roi=(0.28, 0.61, 0.38, 0.675),
            flee_rel_roi=(0.62, 0.61, 0.72, 0.675),
            crowns_shop_rel_roi=(0.015, 0.04, 0.052, 0.10),
            upgrade_now_rel_roi=(0.078, 0.035, 0.117, 0.09),
            friends_rel_roi=(0.96, 0.025, 0.985, 0.08),
            social_rel_roi=(0.96, 0.125, 0.985, 0.185),
            spell_book_rel_roi=(0.917, 0.83, 0.96, 0.96),
        ),
        "43:18": ButtonROIProfile(
            pass_rel_roi=(0.335, 0.61, 0.413, 0.68),
            flee_rel_roi=(0.588, 0.61, 0.665, 0.68),
            crowns_shop_rel_roi=(0.011, 0.04, 0.038, 0.10),
            upgrade_now_rel_roi=(0.058, 0.035, 0.089, 0.09),
            friends_rel_roi=(0.967, 0.025, 0.992, 0.08),
            social_rel_roi=(0.969, 0.127, 0.99, 0.184),
            spell_book_rel_roi=(0.94, 0.83, 0.975, 0.96),
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
