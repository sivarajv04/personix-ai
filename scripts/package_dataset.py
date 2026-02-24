import os
import sys
import zipfile
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv
from api.storage.r2 import upload_zip

# --------------------------------------------------
# CLI ARGUMENTS
# python package_dataset.py <request_id> <gender> <age_bucket> <count>
# --------------------------------------------------
if len(sys.argv) == 5:
    REQUEST_ID = sys.argv[1]
    GENDER = sys.argv[2]
    AGE_BUCKET = sys.argv[3]
    COUNT = int(sys.argv[4])
else:
    print("Usage: package_dataset.py <request_id> <gender> <age_bucket> <count>")
    sys.exit(1)

# --------------------------------------------------
# LOAD ENV
# --------------------------------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE env vars missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FACES_DIR = PROJECT_ROOT / "faces"
DELIVERED_DIR = PROJECT_ROOT / "delivered_datasets"
DELIVERED_DIR.mkdir(exist_ok=True)

print(f"\nPackaging dataset {REQUEST_ID} -> {GENDER}_{AGE_BUCKET} (x{COUNT})")

# --------------------------------------------------
# FETCH AVAILABLE IMAGES
# --------------------------------------------------
rows = (
    supabase.table("active_images")
    .select("*")
    .eq("gender", GENDER)
    .eq("age_bucket", AGE_BUCKET)
    .limit(COUNT)
    .execute()
    .data
)

if not rows:
    print("Not enough stock available")
    sys.exit()

# --------------------------------------------------
# CREATE ZIP
# --------------------------------------------------
zip_name = f"{REQUEST_ID}_{GENDER}_{AGE_BUCKET}.zip"
zip_path = DELIVERED_DIR / zip_name

with zipfile.ZipFile(zip_path, "w") as zipf:
    for row in rows:
        img_path = PROJECT_ROOT / "faces" / row["storage_path"]

        if img_path.exists():
            zipf.write(img_path, arcname=img_path.name)
        else:
            print(f"Missing file: {img_path}")

print(f"[OK] ZIP created: {zip_name}")

# --------------------------------------------------
# UPLOAD TO R2 (IMPORTANT CHANGE)
# --------------------------------------------------
object_key = zip_name
upload_zip(str(zip_path), object_key)

# Save OBJECT KEY (not URL)
supabase.table("dataset_requests").update({
    "status": "completed",
    "download_file": object_key
}).eq("request_id", REQUEST_ID).execute()

print("[OK] Uploaded to storage & DB updated")

# --------------------------------------------------
# UPDATE INVENTORY
# --------------------------------------------------
consumed_count = len(rows)

for row in rows:
    img_path = PROJECT_ROOT / "faces" / row["storage_path"]
    if img_path.exists():
        img_path.unlink()

    supabase.table("active_images").delete().eq(
        "image_id", row["image_id"]
    ).execute()

supabase.rpc("increment_stock", {
    "p_gender": GENDER,
    "p_age_bucket": AGE_BUCKET,
    "p_increment": -consumed_count
}).execute()

print("Dataset delivered & inventory updated")
# import os
# import sys
# import shutil
# import zipfile
# from pathlib import Path
# from supabase import create_client
# from dotenv import load_dotenv
# import uuid
# from api.storage.r2 import upload_zip

# # --------------------------------------------------
# # CONFIG (simulate customer request)
# # --------------------------------------------------
# # GENDER = "male"
# # AGE_BUCKET = "26_40"
# # COUNT = 2


# # ---- CLI ARGUMENTS ----
# if len(sys.argv) == 4:
#     GENDER = sys.argv[1]
#     AGE_BUCKET = sys.argv[2]
#     COUNT = int(sys.argv[3])
# else:
#     print(" Usage: package_dataset.py <gender> <age_bucket> <count>")
#     sys.exit(1)

# # --------------------------------------------------
# # LOAD ENV
# # --------------------------------------------------
# load_dotenv()

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# if not SUPABASE_URL or not SUPABASE_KEY:
#     raise RuntimeError(" SUPABASE env vars missing")

# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# FACES_DIR = PROJECT_ROOT / "faces"
# DELIVERED_DIR = PROJECT_ROOT / "delivered_datasets"
# DELIVERED_DIR.mkdir(exist_ok=True)

# print(f"\n Packaging dataset {GENDER}_{AGE_BUCKET} (x{COUNT})")

# # --------------------------------------------------
# # FETCH AVAILABLE IMAGES
# # --------------------------------------------------
# rows = (
#     supabase.table("active_images")
#     .select("*")
#     .eq("gender", GENDER)
#     .eq("age_bucket", AGE_BUCKET)
#     .limit(COUNT)
#     .execute()
#     .data
# )

# if not rows:
#     print(" Not enough stock available")
#     exit()

# # --------------------------------------------------
# # CREATE ZIP
# # --------------------------------------------------
# delivery_id = f"del_{uuid.uuid4().hex[:6]}"
# zip_path = DELIVERED_DIR / f"{delivery_id}_{GENDER}_{AGE_BUCKET}.zip"

# with zipfile.ZipFile(zip_path, "w") as zipf:
#     for row in rows:
#         img_path = PROJECT_ROOT / "faces" / row["storage_path"]

#         if img_path.exists():
#             zipf.write(img_path, arcname=img_path.name)
#         else:
#             print(f"Missing file: {img_path}")

# print(f"[OK] ZIP created: {zip_path.name}")


# remote_name = f"datasets/{zip_path.name}"
# download_url = upload_zip(str(zip_path), remote_name)

# supabase.table("dataset_requests").update({
#     "status": "completed",
#     "download_file": download_url
# }).eq("request_id", delivery_id).execute()

# print(f"ZIP_OUTPUT::{zip_path.name}")

# # --------------------------------------------------
# # UPDATE DATABASE + DELETE FILES
# # --------------------------------------------------
# before_count = (
#     supabase.table("stock_levels")
#     .select("available_count")
#     .eq("gender", GENDER)
#     .eq("age_bucket", AGE_BUCKET)
#     .single()
#     .execute()
#     .data["available_count"]
# )

# consumed_count = len(rows)
# after_count = before_count - consumed_count

# # ledger
# supabase.table("consumption_ledger").insert({
#     "delivery_id": delivery_id,
#     "gender": GENDER,
#     "age_bucket": AGE_BUCKET,
#     "before_count": before_count,
#     "consumed_count": consumed_count,
#     "after_count": after_count
# }).execute()

# # delete images + rows
# for row in rows:
#     img_path = PROJECT_ROOT / "faces" / row["storage_path"]
#     if img_path.exists():
#         img_path.unlink()

#     supabase.table("active_images").delete().eq(
#         "image_id", row["image_id"]
#     ).execute()

# # decrement stock
# supabase.rpc("increment_stock", {
#     "p_gender": GENDER,
#     "p_age_bucket": AGE_BUCKET,
#     "p_increment": -consumed_count
# }).execute()

# print(" Dataset delivered & inventory updated")

