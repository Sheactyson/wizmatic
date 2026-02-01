from config.roi_config import PARTICIPANT_BOX_PROFILES, PARTICIPANT_LAYOUT
from state.participants import ParticipantsConfig, PipDetectConfig, OCRConfig


PIP_DETECT_CFG = PipDetectConfig(
    white_sat_max=60,
    white_val_min=200,
    school_sat_min=80,
    school_val_min=140,
    min_area_frac=0.002,
    max_area_frac=0.05,
    templates_base_dir="src/assets/pips",
    template_threshold=0.7,
)


OCR_CFG = OCRConfig(
    scale=3,
    psm=7,
    oem=1,
    lang="eng",
    name_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '-",
    health_whitelist="0123456789/",
    invert=False,
    tesseract_cmd="Tesseract\\tesseract.exe",
    user_words_path="src/assets/ocr/wordlist.txt",
    wordlist_max_distance=2,
    wordlist_min_ratio=0.75,
    name_blacklist="0123456789$§/\\|_",
    wordlist_prefix_min_ratio=0.6,
    wordlist_prefix_min_chars=4,
)


PARTICIPANTS_CFG = ParticipantsConfig(
    profiles=PARTICIPANT_BOX_PROFILES,
    layout=PARTICIPANT_LAYOUT,
    pip=PIP_DETECT_CFG,
    ocr=OCR_CFG,
)
