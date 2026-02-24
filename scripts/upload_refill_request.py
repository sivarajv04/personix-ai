import sys
from pathlib import Path

# --------------------------------------------------
# ADD PROJECT ROOT FIRST (VERY IMPORTANT)
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

# now project imports work
from googleapiclient.http import MediaFileUpload
from auth.drive_auth import get_drive_service

# --------------------------------------------------
REQUEST_FILE = PROJECT_ROOT / "refill_request.json"

# 🔴 HARD-BOUND CONTROL QUEUE FOLDER
CONTROL_FOLDER_ID = "1S0d7ccdhgfAxqIB2Rs8JhjlOh9Jxw_-N"

service = get_drive_service()

print("☁ Uploading refill request to Drive...")

file_metadata = {
    "name": "refill_request.json",
    "parents": [CONTROL_FOLDER_ID]
}

media = MediaFileUpload(REQUEST_FILE, mimetype="application/json")

service.files().create(
    body=file_metadata,
    media_body=media,
    fields="id"
).execute()

print("✅ Refill request uploaded to CONTROL folder")

# import sys
# import os
# from pathlib import Path

# # --------------------------------------------------
# # FIX MODULE IMPORT PATH
# # --------------------------------------------------
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# sys.path.append(str(PROJECT_ROOT))

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# # ==================================================
# # CONFIG - UPDATED PATHS
# # ==================================================
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# REQUEST_FILE = PROJECT_ROOT / "refill_request.json"

# # Changed from PROJECT_ROOT / "credentials" / "client_secrets.json" 
# # to match your actual file location:
# CLIENT_SECRETS = PROJECT_ROOT / "credentials.json" 
# TOKEN_FILE = PROJECT_ROOT / "token.json" 

# SCOPES = ["https://www.googleapis.com/auth/drive"]
# ROOT_FOLDER_ID = "1S0d7ccdhgfAxqIB2Rs8JhjlOh9Jxw_-N"

# # # ==================================================
# # # CONFIG
# # # ==================================================
# # REQUEST_FILE = PROJECT_ROOT / "refill_request.json"
# # CLIENT_SECRETS = PROJECT_ROOT / "credentials" / "client_secrets.json"
# # TOKEN_FILE = PROJECT_ROOT / "credentials" / "token.json"

# # # Use FULL scope to ensure we can see the manually created ROOT_FOLDER_ID
# # SCOPES = ["https://www.googleapis.com/auth/drive"]
# # ROOT_FOLDER_ID = "1S0d7ccdhgfAxqIB2Rs8JhjlOh9Jxw_-N"

# # ==================================================
# # OAUTH AUTHENTICATION
# # ==================================================
# def get_authenticated_service():
#     creds = None
#     if TOKEN_FILE.exists():
#         creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             if not CLIENT_SECRETS.exists():
#                 raise FileNotFoundError(f"Missing {CLIENT_SECRETS}. Download it from Google Cloud Console.")
            
#             flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), SCOPES)
#             creds = flow.run_local_server(port=0)
        
#         # Save the token for next time
#         with open(TOKEN_FILE, "w") as token:
#             token.write(creds.to_json())
    
#     return build("drive", "v3", credentials=creds)

# def find_folder(name, parent_id):
#     query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{parent_id}' in parents"
#     res = service.files().list(
#         q=query, 
#         fields="files(id,name)",
#         supportsAllDrives=True,
#         includeItemsFromAllDrives=True
#     ).execute()
#     files = res.get("files", [])
#     return files[0]["id"] if files else None

# # ==================================================
# # MAIN EXECUTION
# # ==================================================
# try:
#     service = get_authenticated_service()
#     print("☁ Finding 'control' folder...")
    
#     control_id = find_folder("control", ROOT_FOLDER_ID)
    
#     if not control_id:
#         # Fallback: check if the ROOT_FOLDER_ID is actually the control folder itself
#         print("⚠️ 'control' not found inside parent. Checking if ID is direct...")
#         control_id = ROOT_FOLDER_ID 

#     print(f"☁ Uploading {REQUEST_FILE.name}...")
#     file_metadata = {
#         "name": REQUEST_FILE.name,
#         "parents": [control_id]
#     }
    
#     media = MediaFileUpload(str(REQUEST_FILE), mimetype="application/json")
    
#     uploaded_file = service.files().create(
#         body=file_metadata,
#         media_body=media,
#         fields="id",
#         supportsAllDrives=True
#     ).execute()

#     print(f"✅ Success! File ID: {uploaded_file.get('id')}")

# except Exception as e:
#     print(f"❌ UPLOAD ERROR: {e}")
#     sys.exit(1) # Tell the daemon that we failed


# import sys
# from pathlib import Path

# # --------------------------------------------------
# # FIX MODULE IMPORT PATH (CRITICAL)
# # --------------------------------------------------
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# sys.path.append(str(PROJECT_ROOT))

# # now imports will work
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from auth.drive_auth import get_drive_service


# # import sys
# # from pathlib import Path
# # # from google.oauth2 import service_account
# # from googleapiclient.discovery import build
# # from googleapiclient.http import MediaFileUpload
# # from auth.drive_auth import get_drive_service
# # ==================================================
# # CONFIG
# # ==================================================
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# REQUEST_FILE = PROJECT_ROOT / "refill_request.json"
# # SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "credentials" / "drive_service_account.json"

# SCOPES = ["https://www.googleapis.com/auth/drive"]
# CONTROL_FOLDER = "control"
# # ROOT_FOLDER = "personix_generation"
# ROOT_FOLDER_ID = "1S0d7ccdhgfAxqIB2Rs8JhjlOh9Jxw_-N"
# # ==================================================
# # AUTH
# # ==================================================
# # creds = service_account.Credentials.from_service_account_file(
# #     SERVICE_ACCOUNT_FILE, scopes=SCOPES
# # )
# # service = build("drive", "v3", credentials=creds)

# service = get_drive_service()

# # --------------------------------------------------
# def find_folder(name, parent=None):
#     query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     if parent:
#         query += f" and '{parent}' in parents"

#     res = service.files().list(
#     q=query,
#     fields="files(id,name)",
#     supportsAllDrives=True,
#     includeItemsFromAllDrives=True
#     ).execute()

#     files = res.get("files", [])
#     return files[0]["id"] if files else None

# # ==================================================
# # MAIN
# # ==================================================
# print("☁ Uploading refill request to Drive...")

# # root_id = find_folder(ROOT_FOLDER)
# # control_id = find_folder(CONTROL_FOLDER, root_id)
# control_id = find_folder("control", ROOT_FOLDER_ID)
# if not control_id:
#     raise RuntimeError("control folder not found in Drive")

# file_metadata = {
#     "name": "refill_request.json",
#     "parents": [control_id]
# }

# media = MediaFileUpload(REQUEST_FILE, mimetype="application/json")

# service.files().create(
#     body=file_metadata,
#     media_body=media,
#     fields="id",
#     supportsAllDrives=True
# ).execute()


# print("✅ Refill request uploaded")
