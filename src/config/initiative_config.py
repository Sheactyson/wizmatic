from state.initiative import InitiativeConfig
from config.roi_config import INITIATIVE_RING_PROFILES, INITIATIVE_RING_THRESHOLDS

INITIATIVE_CFG = InitiativeConfig(
    profiles=INITIATIVE_RING_PROFILES,
    min_score=INITIATIVE_RING_THRESHOLDS.min_score,
    min_delta=INITIATIVE_RING_THRESHOLDS.min_delta,
    white_sat_max=INITIATIVE_RING_THRESHOLDS.white_sat_max,
    white_val_min=INITIATIVE_RING_THRESHOLDS.white_val_min,
)
