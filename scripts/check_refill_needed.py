import os
import json
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
LOW_STOCK_THRESHOLD = 5
REFILL_TARGET = 10
OUTPUT_FILE = "refill_request.json"

# --------------------------------------------------
# LOAD ENV
# --------------------------------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ SUPABASE env vars missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("\n🔎 CHECKING INVENTORY FOR REFILL NEEDS\n")

# --------------------------------------------------
# FETCH STOCK LEVELS
# --------------------------------------------------
stock_rows = (
    supabase
    .table("stock_levels")
    .select("gender, age_bucket, available_count")
    .execute()
    .data
)

if not stock_rows:
    print("⚠️ No stock rows found — nothing to check")
    exit(0)

refill_categories = []

for row in stock_rows:
    gender = row["gender"]
    age_bucket = row["age_bucket"]
    current = row["available_count"]

    if current < LOW_STOCK_THRESHOLD:
        required = REFILL_TARGET - current
        refill_categories.append({
            "gender": gender,
            "age_bucket": age_bucket,
            "current_stock": current,
            "required": required
        })

# --------------------------------------------------
# DECISION
# --------------------------------------------------
if not refill_categories:
    print("✅ All stock levels healthy — no refill needed\n")

    # Remove stale refill request if exists
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print("🧹 Removed stale refill_request.json")

    exit(0)

# --------------------------------------------------
# WRITE REFILL REQUEST
# --------------------------------------------------
refill_request = {
    "created_at": datetime.utcnow().isoformat() + "Z",
    "threshold": LOW_STOCK_THRESHOLD,
    "refill_target": REFILL_TARGET,
    "needs_refill": True,
    "categories": refill_categories
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(refill_request, f, indent=2)

print("❌ REFILL REQUIRED\n")

for c in refill_categories:
    print(
        f"  - {c['gender']}_{c['age_bucket']}: "
        f"current={c['current_stock']} → need={c['required']}"
    )

print(f"\n📄 refill_request.json CREATED\n")
