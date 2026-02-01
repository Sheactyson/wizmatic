from state.initiative import InitiativeConfig
from config.roi_config import INITIATIVE_RING_PROFILES, INITIATIVE_RING_THRESHOLDS

INITIATIVE_CFG = InitiativeConfig(
    profiles=INITIATIVE_RING_PROFILES,
    templates_base_dir=INITIATIVE_RING_THRESHOLDS.templates_base_dir,
    template_min_score=INITIATIVE_RING_THRESHOLDS.template_min_score,
    template_min_delta=INITIATIVE_RING_THRESHOLDS.template_min_delta,
)
