import os
import shutil
import uuid
import logging
from pathlib import Path
from deepface import DeepFace
from supabase import create_client
from dotenv import load_dotenv

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TMP_DIR = PROJECT_ROOT / "faces" / "tmp"
FACES_DIR = PROJECT_ROOT / "faces"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "classification.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

AGE_BUCKETS = [
    (0, 5, "0_5"),
    (6, 12, "6_12"),
    (13, 17, "13_17"),
    (18, 25, "18_25"),
    (26, 40, "26_40"),
    (41, 60, "41_60"),
    (61, 80, "61_80"),
]

# --------------------------------------------------
def get_age_bucket(age):
    for low, high, label in AGE_BUCKETS:
        if low <= age <= high:
            return label
    return None
# --------------------------------------------------

for img_path in TMP_DIR.glob("*.png"):
    try:
        result = DeepFace.analyze(
            img_path=str(img_path),
            actions=["age", "gender"],
            enforce_detection=False
        )[0]

        gender = result["dominant_gender"].lower()

        # Normalize DeepFace outputs
        if gender in ["man"]:
            gender = "male"
        elif gender in ["woman"]:
            gender = "female"
        elif gender not in ["male", "female"]:
            # fallback using probabilities
            probs = result.get("gender", {})
            male_p = probs.get("Man", 0)
            female_p = probs.get("Woman", 0)
            gender = "male" if male_p >= female_p else "female"

        age = int(result["age"])


        age_bucket = get_age_bucket(age)
        if not age_bucket:
            logging.warning(f"Skipped {img_path.name} (age out of range)")
            continue

        image_id = f"img_{uuid.uuid4().hex[:8]}"
        dest_dir = FACES_DIR / f"{gender}_{age_bucket}"
        dest_dir.mkdir(exist_ok=True)

        dest_path = dest_dir / f"{image_id}.png"
        shutil.move(img_path, dest_path)

        storage_path = f"{gender}_{age_bucket}/{image_id}.png"


        # INSERT INTO active_images
        supabase.table("active_images").insert({
            "image_id": image_id,
            "gender": gender,
            "age_bucket": age_bucket,
            "storage_path": storage_path
        }).execute()

        # UPDATE stock_levels
        supabase.rpc("increment_stock", {
            "p_gender": gender,
            "p_age_bucket": age_bucket,
            "p_increment": 1
        }).execute()

        logging.info(f"Added {image_id} → {gender}_{age_bucket}")

    except Exception as e:
        logging.error(f"Failed {img_path.name}: {str(e)}")



# import os
# import shutil
# from datetime import datetime
# from pathlib import Path


# import cv2
# from deepface import DeepFace
# from supabase import create_client
# from dotenv import load_dotenv

# # --------------------------------------------------
# # LOAD ENV
# # --------------------------------------------------
# load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# print("SUPABASE_URL:", SUPABASE_URL)
# print("SUPABASE_KEY loaded:", bool(SUPABASE_KEY))


# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# # --------------------------------------------------
# # PATHS
# # --------------------------------------------------
# INCOMING_DIR = "faces/_incoming"
# FACES_DIR = "faces"

# # --------------------------------------------------
# # AGE BUCKET LOGIC
# # --------------------------------------------------
# def get_age_bucket(age: int) -> str:
#     if age <= 5:
#         return "0_5"
#     elif age <= 12:
#         return "6_12"
#     elif age <= 17:
#         return "13_17"
#     elif age <= 25:
#         return "18_25"
#     elif age <= 40:
#         return "26_40"
#     elif age <= 60:
#         return "41_60"
#     else:
#         return "61_80"

# # --------------------------------------------------
# # MAIN PIPELINE
# # --------------------------------------------------
# def process_images():
#     images = os.listdir(INCOMING_DIR)

#     for img_name in images:
#         img_path = os.path.join(INCOMING_DIR, img_name)

#         if not img_name.lower().endswith(".png"):
#             continue

#         print(f"Processing {img_name}...")

#         try:
#             # -------------------------------
#             # CLASSIFY IMAGE
#             # -------------------------------
#             result = DeepFace.analyze(
#                 img_path=img_path,
#                 actions=["age", "gender"],
#                 enforce_detection=False
#             )[0]

#             # age = int(result["age"])
#             # gender = result["dominant_gender"].lower()

#             # if gender not in ["male", "female"]:
#             #     print("Skipping unknown gender")
#             #     continue

#             # age_bucket = get_age_bucket(age)

#             age = int(result["age"])
#             raw_gender = result["dominant_gender"].lower()

#             # Normalize DeepFace labels
#             if raw_gender == "man":
#                 gender = "male"
#             elif raw_gender == "woman":
#                 gender = "female"
#             else:
#                 gender = "unknown"   # fallback, but DO NOT skip

#             age_bucket = get_age_bucket(age)


#             # -------------------------------
#             # MOVE IMAGE
#             # -------------------------------
#             target_dir = os.path.join(FACES_DIR, f"{gender}_{age_bucket}")
#             os.makedirs(target_dir, exist_ok=True)

#             image_id = os.path.splitext(img_name)[0]
#             new_path = os.path.join(target_dir, img_name)

#             shutil.move(img_path, new_path)

#             storage_path = f"faces/{gender}_{age_bucket}/{img_name}"

#             # -------------------------------
#             # INSERT INTO images TABLE
#             # -------------------------------
#             supabase.table("images").insert({
#                 "image_id": image_id,
#                 "gender": gender,
#                 "age_bucket": age_bucket,
#                 "storage_path": storage_path,
#                 "is_available": True,
#                 "created_at": datetime.utcnow().isoformat()
#             }).execute()

#             # -------------------------------
#             # UPDATE STOCK LEVELS
#             # -------------------------------
#             supabase.rpc(
#                 "increment_stock",
#                 {
#                     "p_gender": gender,
#                     "p_age_bucket": age_bucket
#                 }
#             ).execute()

#             print(f"✔ Stored {img_name} → {gender}_{age_bucket}")

#         except Exception as e:
#             print(f"❌ Error processing {img_name}: {e}")

# # --------------------------------------------------
# if __name__ == "__main__":
#     process_images()
