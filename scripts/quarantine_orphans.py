# scripts/quarantine_orphans.py
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
FACES = ROOT / "faces"
ORPHAN = FACES / "_orphaned"
ORPHAN.mkdir(exist_ok=True)

for folder in FACES.iterdir():
    if not folder.is_dir():
        continue
    if folder.name.startswith("_"):
        continue

    for img in folder.glob("*.png"):
        shutil.move(img, ORPHAN / img.name)
        print(f"Moved orphan → {img.name}")

print("✅ Orphan quarantine complete")
