import os
import sys
import subprocess
from supabase import create_client
from dotenv import load_dotenv

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
LOW_STOCK_THRESHOLD = 1
REFILL_TARGET = 1


load_dotenv()
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

print("\n🔁 REFILL INVENTORY STARTED\n")

# --------------------------------------------------
# FETCH STOCK LEVELS
# --------------------------------------------------
stock_rows = supabase.table("stock_levels") \
    .select("gender, age_bucket, available_count") \
    .execute().data

refill_plan = []

for row in stock_rows:
    current = row["available_count"]
    if current < LOW_STOCK_THRESHOLD:
        needed = REFILL_TARGET - current
        refill_plan.append({
            "gender": row["gender"],
            "age_bucket": row["age_bucket"],
            "needed": needed
        })

if not refill_plan:
    print("✅ All stock levels healthy — no refill needed\n")
    exit(0)

# --------------------------------------------------
# EXECUTE REFILL
# --------------------------------------------------
for task in refill_plan:
    print(
        f"🔄 Refilling {task['gender']}_{task['age_bucket']} "
        f"(+{task['needed']})"
    )

    # 1️⃣ Generate images to faces/tmp/
    subprocess.run(
        [
            sys.executable,
            "scripts/generate_faces_gan.py",
            str(task["needed"])
        ],
        check=True
    )

    # 2️⃣ Classify + ingest
    subprocess.run(
        [
            sys.executable,
            "scripts/classify_faces.py"
        ],
        check=True
    )


print("\n✅ REFILL COMPLETE\n")
