import sys
from pathlib import Path

# --------------------------------------------------
# FIX MODULE IMPORT PATH (CRITICAL)
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from auth.drive_auth import get_drive_service



# import io
# from pathlib import Path
# # from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# from auth.drive_auth import get_drive_service
# ==================================================
# CONFIG
# ==================================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]
TMP_DIR = PROJECT_ROOT / "faces" / "tmp"
TMP_DIR.mkdir(parents=True, exist_ok=True)

# SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "credentials" / "drive_service_account.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

DRIVE_ROOT_FOLDER = "personix_generation"
FACES_FOLDER = "faces"
INCOMING_FOLDER = "_incoming"
PROCESSED_FOLDER = "processed"

# ==================================================
# AUTH
# ==================================================
# creds = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES
# )
# service = build("drive", "v3", credentials=creds)

service = get_drive_service()
# ==================================================
# HELPERS
# ==================================================
def find_folder(name, parent=None):
    """Find folder ID by name"""
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent:
        query += f" and '{parent}' in parents"

    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None


def download_file(file_id, filename):
    """Download file to local tmp folder"""
    local_path = TMP_DIR / filename

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(local_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    return local_path


def move_to_processed(file_id, incoming_id, processed_id):
    """Move file instead of deleting (avoids ownership issue)"""
    service.files().update(
        fileId=file_id,
        addParents=processed_id,
        removeParents=incoming_id
    ).execute()


# ==================================================
# MAIN
# ==================================================
print("\n🔎 Connecting to Google Drive...")

root_id = find_folder(DRIVE_ROOT_FOLDER)
if not root_id:
    raise RuntimeError("Root folder not found in Drive")

faces_id = find_folder(FACES_FOLDER, root_id)
if not faces_id:
    raise RuntimeError("Faces folder not found in Drive")

incoming_id = find_folder(INCOMING_FOLDER, faces_id)
processed_id = find_folder(PROCESSED_FOLDER, faces_id)

if not incoming_id:
    raise RuntimeError("Incoming folder not found in Drive")
if not processed_id:
    raise RuntimeError("Processed folder not found in Drive")

print("📥 Checking for new generated images...")

files = service.files().list(
    q=f"'{incoming_id}' in parents and mimeType='image/png'",
    fields="files(id, name)"
).execute().get("files", [])

if not files:
    print("No new images in Drive")
    exit()

downloaded = 0

for file in files:
    file_id = file["id"]
    filename = file["name"]

    try:
        # Download
        download_file(file_id, filename)
        print(f"⬇ Downloaded: {filename}")

        # Move in Drive
        move_to_processed(file_id, incoming_id, processed_id)
        print(f"📦 Moved to processed/: {filename}")

        downloaded += 1

    except Exception as e:
        print(f"⚠ Failed processing {filename}: {e}")

print(f"\n✅ Sync complete — {downloaded} image(s) ready for classification")

# ==================================================
# AUTO CLASSIFICATION TRIGGER
# ==================================================
print("\n🧠 Triggering classification pipeline...")

import subprocess
import sys

subprocess.run(
    [sys.executable, str(PROJECT_ROOT / "scripts" / "classify_faces.py")],
    check=True
)

print("✅ Classification complete — inventory updated")

# import io
# import os
# from pathlib import Path
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload

# # --------------------------------------------------
# # CONFIG
# # --------------------------------------------------
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# TMP_DIR = PROJECT_ROOT / "faces" / "tmp"
# TMP_DIR.mkdir(parents=True, exist_ok=True)

# SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "credentials" / "drive_service_account.json"

# SCOPES = ["https://www.googleapis.com/auth/drive"]

# # CHANGE THIS NAME ONLY IF YOU RENAME DRIVE FOLDER
# DRIVE_ROOT_FOLDER = "personix_generation"
# INCOMING_FOLDER = "_incoming"

# # --------------------------------------------------
# # AUTH
# # --------------------------------------------------
# creds = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES
# )

# service = build("drive", "v3", credentials=creds)

# # --------------------------------------------------
# # FIND FOLDER BY NAME
# # --------------------------------------------------
# def find_folder(name, parent=None):
#     query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     if parent:
#         query += f" and '{parent}' in parents"

#     results = service.files().list(q=query, fields="files(id, name)").execute()
#     files = results.get("files", [])
#     return files[0]["id"] if files else None


# print("\n🔎 Connecting to Google Drive...")

# root_id = find_folder(DRIVE_ROOT_FOLDER)
# faces_id = find_folder("faces", root_id)
# incoming_id = find_folder(INCOMING_FOLDER, faces_id)

# if not incoming_id:
#     raise RuntimeError("❌ Cannot find Drive incoming folder")

# print("📥 Fetching generated images...")

# files = service.files().list(
#     q=f"'{incoming_id}' in parents and mimeType='image/png'",
#     fields="files(id, name)"
# ).execute().get("files", [])

# if not files:
#     print("No new images in Drive")
#     exit()

# for file in files:
#     file_id = file["id"]
#     filename = file["name"]
#     local_path = TMP_DIR / filename

#     request = service.files().get_media(fileId=file_id)
#     fh = io.FileIO(local_path, "wb")
#     downloader = MediaIoBaseDownload(fh, request)

#     done = False
#     while not done:
#         status, done = downloader.next_chunk()

#     print(f"⬇ Downloaded {filename}")

#     # delete from drive after download
#     service.files().delete(fileId=file_id).execute()
#     print(f"🗑 Removed from Drive")

# print("\n✅ Sync complete — ready for classification")
