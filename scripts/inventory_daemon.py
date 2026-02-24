# import sys
# from pathlib import Path

# # allow scripts to import project modules
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# sys.path.append(str(PROJECT_ROOT))

# # import sys
# # from pathlib import Path
# from googleapiclient.http import MediaFileUpload
# from auth.drive_auth import get_drive_service

# # --------------------------------------------------
# # FIX MODULE IMPORT PATH
# # --------------------------------------------------
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# sys.path.append(str(PROJECT_ROOT))

# REQUEST_FILE = PROJECT_ROOT / "refill_request.json"

# # 🔴 THIS IS THE REAL CONTROL FOLDER (QUEUE LOCATION)
# CONTROL_FOLDER_ID = "1i54l5t6BhF44e61e98VPko7Chk5WwFbr"

# service = get_drive_service()

# print("☁ Uploading refill request to Drive...")

# file_metadata = {
#     "name": "refill_request.json",
#     "parents": [CONTROL_FOLDER_ID]
# }

# media = MediaFileUpload(REQUEST_FILE, mimetype="application/json")

# service.files().create(
#     body=file_metadata,
#     media_body=media,
#     fields="id"
# ).execute()

# print("✅ Refill request uploaded to CONTROL folder")

import sys
from pathlib import Path

# --------------------------------------------------
# FIX PROJECT IMPORT PATH (CRITICAL)
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


import time
import subprocess
import sys
from pathlib import Path
from auth.drive_auth import get_drive_service

CONTROL_FOLDER_ID = "1S0d7ccdhgfAxqIB2Rs8JhjlOh9Jxw_-N"

def refill_job_exists():
    service = get_drive_service()
    results = service.files().list(
        q=f"'{CONTROL_FOLDER_ID}' in parents and name='refill_request.json' and trashed=false",
        fields="files(id, name)"
    ).execute()
    return len(results.get("files", [])) > 0


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CHECK_SCRIPT = PROJECT_ROOT / "scripts" / "check_refill_needed.py"
UPLOAD_SCRIPT = PROJECT_ROOT / "scripts" / "upload_refill_request.py"
REQUEST_FILE = PROJECT_ROOT / "refill_request.json"

INTERVAL = 60  # seconds
PYTHON_EXEC = sys.executable

print("🧠 Personix Inventory Daemon started")
print(f"Using interpreter: {PYTHON_EXEC}")

while True:
    print("\n🔍 Checking stock...")

    # 1️⃣ run stock checker
    # run stock checker
    subprocess.run([PYTHON_EXEC, str(CHECK_SCRIPT)], check=False)

    # wait a moment for file write
    time.sleep(1)

    # upload ONLY if file exists
    # if REQUEST_FILE.is_file():
    #     print("☁ Uploading refill request to Drive...")
    #     subprocess.run([PYTHON_EXEC, str(UPLOAD_SCRIPT)], check=False)

    #     if REQUEST_FILE.exists():
    #         REQUEST_FILE.unlink()
    #         print("🧹 Local refill_request.json removed")
    # else:
    #     print("✔ No refill needed")

    if REQUEST_FILE.is_file():

        if refill_job_exists():
            print("⏳ Refill already requested — waiting for generation")
            REQUEST_FILE.unlink(missing_ok=True)

        else:
            print("☁ Uploading refill request to Drive...")
            subprocess.run([PYTHON_EXEC, str(UPLOAD_SCRIPT)], check=False)

            if REQUEST_FILE.exists():
                REQUEST_FILE.unlink()
                print("🧹 Local refill_request.json removed")

    else:
        print("✔ No refill needed")


# import time
# import subprocess
# from pathlib import Path

# PROJECT_ROOT = Path(__file__).resolve().parents[1]

# CHECK_SCRIPT = PROJECT_ROOT / "scripts" / "check_refill_needed.py"

# INTERVAL = 60  # seconds (later 15 min in production)

# print("🧠 Personix Inventory Daemon started")

# while True:
#     print("\n🔍 Checking stock...")
#     subprocess.run(["python", str(CHECK_SCRIPT)])

#     print("💤 Sleeping...\n")
#     time.sleep(INTERVAL)
