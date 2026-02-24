from api.db import supabase
from pathlib import Path
import time

BUCKET = "datasets"

# -------------------------
# Upload ZIP
# -------------------------
def upload_zip(local_path: str, object_key: str):
    """
    Upload dataset zip to Supabase Storage
    object_key example: req_xxxx_male_26_40.zip
    """

    with open(local_path, "rb") as f:
        supabase.storage.from_(BUCKET).upload(
            path=object_key,
            file=f,
            file_options={"content-type": "application/zip", "upsert": "true"}
        )

    print(f"[SUPABASE STORAGE] Uploaded -> {object_key}")


# -------------------------
# Generate temporary link
# -------------------------
def generate_signed_url(object_key: str, expires: int = 30):
    """
    Create short lived download URL
    """
    res = supabase.storage.from_(BUCKET).create_signed_url(
        path=object_key,
        expires_in=expires
    )

    return res["signedURL"]