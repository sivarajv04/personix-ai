from api.db import supabase
from pathlib import Path
import time

BUCKET = "datasets"


# ---------------------------------------------------
# Upload dataset ZIP to Supabase Storage
# ---------------------------------------------------
def upload_zip(local_path: str, object_key: str):
    """
    Upload a dataset zip file to Supabase storage.

    local_path: path of zip file on server
    object_key: filename inside storage
    example -> req_xxxx_male_26_40.zip
    """

    try:
        with open(local_path, "rb") as f:
            response = supabase.storage.from_(BUCKET).upload(
                path=object_key,
                file=f,
                file_options={
                    "content-type": "application/zip",
                    "upsert": "true"
                }
            )

        print(f"[STORAGE] Uploaded dataset -> {object_key}")
        return response

    except Exception as e:
        print("[STORAGE ERROR] Upload failed:", e)
        raise


# ---------------------------------------------------
# Generate signed download URL
# ---------------------------------------------------
def generate_signed_url(object_key: str, expires: int = 300):
    """
    Create a temporary download link.

    expires = seconds before link expires
    """

    try:
        res = supabase.storage.from_(BUCKET).create_signed_url(
            path=object_key,
            expires_in=expires
        )

        # Supabase SDK sometimes wraps response inside 'data'
        if isinstance(res, dict):

            if "signedURL" in res:
                signed_url = res["signedURL"]

            elif "data" in res and "signedURL" in res["data"]:
                signed_url = res["data"]["signedURL"]

            else:
                raise RuntimeError(f"Unexpected Supabase response: {res}")

        else:
            raise RuntimeError(f"Invalid signed URL response: {res}")

        if not signed_url:
            raise RuntimeError("Signed URL generation failed")

        print(f"[STORAGE] Generated signed URL for {object_key}")

        return signed_url

    except Exception as e:
        print("[STORAGE ERROR] Signed URL generation failed:", e)
        raise
# from api.db import supabase
# from pathlib import Path
# import time

# BUCKET = "datasets"

# # -------------------------
# # Upload ZIP
# # -------------------------
# def upload_zip(local_path: str, object_key: str):
#     """
#     Upload dataset zip to Supabase Storage
#     object_key example: req_xxxx_male_26_40.zip
#     """

#     with open(local_path, "rb") as f:
#         supabase.storage.from_(BUCKET).upload(
#             path=object_key,
#             file=f,
#             file_options={"content-type": "application/zip", "upsert": "true"}
#         )

#     print(f"[SUPABASE STORAGE] Uploaded -> {object_key}")


# # -------------------------
# # Generate temporary link
# # -------------------------
# def generate_signed_url(object_key: str, expires: int = 30):
#     """
#     Create short lived download URL
#     """
#     res = supabase.storage.from_(BUCKET).create_signed_url(
#         path=object_key,
#         expires_in=expires
#     )

#     return res["signedURL"]