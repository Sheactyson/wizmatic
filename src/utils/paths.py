from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
TEMPLATES = SRC / "assets/templates"

print(ROOT)
