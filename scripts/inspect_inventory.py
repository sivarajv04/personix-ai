import os
from pathlib import Path
from collections import defaultdict
from supabase import create_client
from dotenv import load_dotenv

# --------------------------------------------------
# LOAD ENV
# --------------------------------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --------------------------------------------------
# PATHS
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FACES_DIR = PROJECT_ROOT / "faces"

# --------------------------------------------------
# FETCH DB INVENTORY
# --------------------------------------------------
rows = supabase.table("active_images").select(
    "gender, age_bucket, storage_path"
).execute().data

# db_stats = defaultdict(lambda: {
#     "total": 0,
#     "available": 0,
#     "consumed": 0,
#     "paths": set()
# })

# for row in rows:
#     key = (row["gender"], row["age_bucket"])
#     db_stats[key]["total"] += 1
#     if row["is_available"]:
#         db_stats[key]["available"] += 1
#     else:
#         db_stats[key]["consumed"] += 1
#     db_stats[key]["paths"].add(row["storage_path"])
db_stats = defaultdict(lambda: {
    "total": 0,
    "paths": set()
})

for row in rows:
    key = (row["gender"], row["age_bucket"])
    db_stats[key]["total"] += 1
    # db_stats[key]["paths"].add("faces/" + row["storage_path"])
    db_stats[key]["paths"].add(("faces/" + row["storage_path"]).replace("\\", "/"))


# --------------------------------------------------
# FETCH FILESYSTEM INVENTORY
# --------------------------------------------------
fs_stats = defaultdict(set)

if FACES_DIR.exists():
    for img in FACES_DIR.rglob("*.png"):
        # faces/male_26_40/img_x.png
        rel = img.relative_to(PROJECT_ROOT)
        parts = rel.parts
        if len(parts) >= 2:
            category = parts[1]  # male_26_40
            fs_stats[category].add(str(rel).replace("\\", "/"))


# --------------------------------------------------
# PRINT REPORT
# --------------------------------------------------
print("\n📦 PERSONIX.AI INVENTORY INSPECTION\n")

for (gender, age_bucket), stats in sorted(db_stats.items()):
    category = f"{gender}_{age_bucket}"
    fs_count = len(fs_stats.get(category, []))

    print(f"🔹 {category}")
    # print(f"   DB → total: {stats['total']}, available: {stats['available']}, consumed: {stats['consumed']}")
    print(f"   DB → total available: {stats['total']}")

    print(f"   FS → files present: {fs_count}")

    # Warnings
    missing_in_fs = stats["paths"] - fs_stats.get(category, set())
    extra_in_fs = fs_stats.get(category, set()) - stats["paths"]

    if missing_in_fs:
        print(f"   ⚠️ Missing in FS ({len(missing_in_fs)})")

    if extra_in_fs:
        print(f"   ⚠️ Extra in FS ({len(extra_in_fs)})")

    if not missing_in_fs and not extra_in_fs:
        print(f"   ✅ Inventory consistent")

    print("-" * 50)

print("✅ Inspection complete\n")
