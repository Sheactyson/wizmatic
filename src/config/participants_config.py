from config.roi_config import (
    PARTICIPANT_BOX_PROFILES,
    PARTICIPANT_LAYOUT,
    PIP_SLOT_DEBUG_UPSCALE,
    PIP_SLOT_WIDTH_PX_DEFAULT,
    PIP_SLOT_WIDTH_PX_BY_ASPECT,
    PIP_SLOT_GAP_PX_DEFAULT,
    PIP_SLOT_GAP_PX_BY_ASPECT,
    PIP_SLOT_START_PX_DEFAULT,
    PIP_SLOT_TOP_CUT_PX_DEFAULT,
    PIP_SLOT_TOP_CUT_PX_BY_ASPECT,
    PIP_SLOT_BOTTOM_CUT_PX_DEFAULT,
    PIP_SLOT_BOTTOM_CUT_PX_BY_ASPECT,
    PIP_SLOT_PRESENCE_CONFIDENCE_THRESHOLD,
    PIP_SLOT_COUNT,
    PIP_SLOT_START_PX_BY_ASPECT,
)
from config.wizmatic_config import OCR_BACKEND, NAME_RESOLUTION_MODE
from state.participants import (
    ParticipantsConfig,
    PipDetectConfig,
    OCRConfig,
    SigilDetectConfig,
    SchoolDetectConfig,
)


PIP_DETECT_CFG = PipDetectConfig(
    white_sat_max=60,
    white_val_min=200,
    school_sat_min=80,
    school_val_min=140,
    min_area_frac=0.002,
    max_area_frac=0.05,
    templates_base_dir="src/assets/pips",
    template_threshold=0.7,
    slot_debug_upscale=PIP_SLOT_DEBUG_UPSCALE,
    slot_width_px=PIP_SLOT_WIDTH_PX_DEFAULT,
    slot_width_px_by_aspect=PIP_SLOT_WIDTH_PX_BY_ASPECT,
    slot_gap_px=PIP_SLOT_GAP_PX_DEFAULT,
    slot_gap_px_by_aspect=PIP_SLOT_GAP_PX_BY_ASPECT,
    slot_start_px=PIP_SLOT_START_PX_DEFAULT,
    slot_start_px_by_aspect=PIP_SLOT_START_PX_BY_ASPECT,
    slot_top_cut_px=PIP_SLOT_TOP_CUT_PX_DEFAULT,
    slot_top_cut_px_by_aspect=PIP_SLOT_TOP_CUT_PX_BY_ASPECT,
    slot_bottom_cut_px=PIP_SLOT_BOTTOM_CUT_PX_DEFAULT,
    slot_bottom_cut_px_by_aspect=PIP_SLOT_BOTTOM_CUT_PX_BY_ASPECT,
    slot_presence_confidence_threshold=PIP_SLOT_PRESENCE_CONFIDENCE_THRESHOLD,
    slot_count=PIP_SLOT_COUNT,
)


OCR_CFG = OCRConfig(
    scale=3,
    psm=7,
    oem=1,
    lang="eng",
    name_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '-",
    health_whitelist="0123456789/,",
    player_resource_whitelist="0123456789",
    invert=False,
    tesseract_cmd="Tesseract\\tesseract.exe",
    user_words_path="src/assets/ocr/wordlist.txt",
    name_resolution_mode=NAME_RESOLUTION_MODE,
    wordlist_wizards_path="src/assets/ocr/wizards.txt",
    wordlist_monsters_path="src/assets/ocr/monsters.txt",
    wordlist_minions_path="src/assets/ocr/minions.txt",
    wordlist_max_distance=2,
    wordlist_min_ratio=0.75,
    name_blacklist="0123456789$§/\\|_",
    wordlist_prefix_min_ratio=0.6,
    wordlist_prefix_min_chars=4,
    backend=OCR_BACKEND,
)


SIGIL_DETECT_CFG = SigilDetectConfig(
    templates_base_dir="src/assets/participants/sigils",
    template_threshold=0.7,
)


SCHOOL_DETECT_CFG = SchoolDetectConfig(
    templates_base_dir="src/assets/participants/schools",
    template_threshold=0.7,
)


PARTICIPANTS_CFG = ParticipantsConfig(
    profiles=PARTICIPANT_BOX_PROFILES,
    layout=PARTICIPANT_LAYOUT,
    pip=PIP_DETECT_CFG,
    ocr=OCR_CFG,
    sigil=SIGIL_DETECT_CFG,
    school=SCHOOL_DETECT_CFG,
)
