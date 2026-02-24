import os
from pathlib import Path
from collections import defaultdict
from supabase import create_client
from dotenv import load_dotenv
from postgrest.exceptions import APIError
from pathlib import Path
from collections import defaultdict
# --------------------------------------------------
# LOAD ENV
# --------------------------------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ SUPABASE env vars missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --------------------------------------------------
# PATHS
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FACES_DIR = PROJECT_ROOT / "faces"
DELIVERED_DIR = PROJECT_ROOT / "delivered_datasets"
LOG_DIR = PROJECT_ROOT / "logs"

print("\n🧪 PERSONIX.AI — SYSTEM AUDIT REPORT\n")



# --------------------------------------------------
# 1️⃣ FILESYSTEM CHECK
# --------------------------------------------------
print("📁 FILESYSTEM CHECK")

required_dirs = {
    "faces": FACES_DIR,
    "delivered_datasets": DELIVERED_DIR,
    "logs": LOG_DIR,
}

for name, d in required_dirs.items():
    print(f"  {'✅' if d.exists() else '❌'} {name} → {d}")

# --------------------------------------------------
# 2️⃣ DATABASE TABLE CHECK (SUPABASE-SAFE)
# --------------------------------------------------
print("\n🗄️ DATABASE TABLE CHECK")

tables = [
    "active_images",
    "stock_levels",
    "consumption_ledger",
]

for table in tables:
    try:
        supabase.table(table).select("*").limit(1).execute()
        print(f"  ✅ {table}")
    except APIError:
        print(f"  ❌ {table}")

# --------------------------------------------------
# 3️⃣ ACTIVE INVENTORY CONSISTENCY
# --------------------------------------------------
print("\n📦 ACTIVE INVENTORY CONSISTENCY")

rows = supabase.table("active_images") \
    .select("image_id, gender, age_bucket, storage_path") \
    .execute().data

db_paths = set(r["storage_path"] for r in rows)
fs_paths = set(
    p.relative_to(PROJECT_ROOT).as_posix()
    for p in FACES_DIR.rglob("*.png")
    if "_orphaned" not in p.parts
)



print(f"  DB active_images rows: {len(rows)}")
print(f"  FS image files:        {len(fs_paths)}")

missing_files = db_paths - fs_paths
extra_files = fs_paths - db_paths

print(f"  {'⚠️' if missing_files else '✅'} Missing files: {len(missing_files)}")
print(f"  {'⚠️' if extra_files else '✅'} Extra files:   {len(extra_files)}")

# --------------------------------------------------
# 4️⃣ STOCK LEVELS VALIDATION
# --------------------------------------------------
print("\n📊 STOCK LEVELS VALIDATION")

stock = supabase.table("stock_levels") \
    .select("gender, age_bucket, available_count") \
    .execute().data

counts = defaultdict(int)
for r in rows:
    counts[(r["gender"], r["age_bucket"])] += 1

for s in stock:
    key = (s["gender"], s["age_bucket"])
    expected = counts.get(key, 0)
    actual = s["available_count"]

    status = "✅" if expected == actual else "❌"
    print(f"  {status} {key[0]}_{key[1]} → stock={actual}, actual={expected}")

# --------------------------------------------------
# 5️⃣ LEDGER SANITY
# --------------------------------------------------
print("\n📜 CONSUMPTION LEDGER CHECK")

ledger = supabase.table("consumption_ledger") \
    .select("id, consumed_count, before_count, after_count") \
    .execute().data

invalid = 0
for l in ledger:
    if l["before_count"] - l["consumed_count"] != l["after_count"]:
        invalid += 1

print(f"  Ledger entries: {len(ledger)}")
print(f"  {'❌' if invalid else '✅'} Invalid rows: {invalid}")

# --------------------------------------------------
# 6️⃣ SCALABILITY WARNINGS
# --------------------------------------------------
print("\n⚙️ SCALABILITY WARNINGS")

if len(rows) > 10000:
    print("  ⚠️ active_images > 10k (consider pagination / batching)")
else:
    print("  ✅ active_images size OK")

if len(fs_paths) > 20000:
    print("  ⚠️ filesystem large (cloud storage recommended)")
else:
    print("  ✅ filesystem size OK")

print("\n✅ AUDIT COMPLETE\n")

# --------------------------------------------------
# PATHS
# --------------------------------------------------


IGNORED_DIRS = {"_orphaned", "tmp"}

print("\n📂 LOCAL FILESYSTEM INVENTORY\n")

counts = defaultdict(int)
# --------------------------------------------------
# SCAN FILESYSTEM
# --------------------------------------------------
for category_dir in FACES_DIR.iterdir():
    if not category_dir.is_dir():
        continue

    if category_dir.name in IGNORED_DIRS:
        continue

    # Expect folder like male_18_25
    category = category_dir.name

    images = list(category_dir.glob("*.png"))
    counts[category] = len(images)

# --------------------------------------------------
# PRINT RESULTS
# --------------------------------------------------
if not counts:
    print("⚠️ No inventory folders found")
else:
    for category in sorted(counts.keys()):
        print(f"  {category:<15} → {counts[category]} images")

print("\n✅ LOCAL INVENTORY CHECK COMPLETE\n")