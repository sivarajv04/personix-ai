import os
import sys
import time
import subprocess
from pathlib import Path
from api.db import supabase

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

CHECK_INTERVAL = 15  # seconds


def get_pending_requests():
    res = (
        supabase.table("dataset_requests")
        .select("*")
        .eq("status", "pending")
        .limit(1)
        .execute()
    )
    return res.data


def mark_processing(request_id):
    supabase.table("dataset_requests") \
        .update({"status": "processing"}) \
        .eq("request_id", request_id) \
        .execute()


def mark_waiting(request_id):
    supabase.table("dataset_requests") \
        .update({"status": "waiting_generation"}) \
        .eq("request_id", request_id) \
        .execute()


def check_stock(gender, age_bucket, count):

    res = (
        supabase.table("stock_levels")
        .select("available_count")
        .eq("gender", gender)
        .eq("age_bucket", age_bucket)
        .execute()
    )

    if not res.data:
        print(f"No inventory bucket yet for {gender}_{age_bucket}", flush=True)
        return False

    return res.data[0]["available_count"] >= count


def start_worker():

    print("🚀 Dataset Request Worker Started", flush=True)

    while True:

        jobs = get_pending_requests()

        if not jobs:
            print("No pending dataset requests", flush=True)
            time.sleep(CHECK_INTERVAL)
            continue

        job = jobs[0]

        request_id = job["request_id"]
        gender = job["gender"]
        age_bucket = job["age_bucket"]
        count = job["count"]

        print(
            f"Processing request {request_id} → {gender}_{age_bucket} x{count}",
            flush=True
        )

        if not check_stock(gender, age_bucket, count):

            print("Not enough inventory — waiting for generator", flush=True)

            mark_waiting(request_id)

            time.sleep(CHECK_INTERVAL)

            continue

        # mark processing
        mark_processing(request_id)

        env = dict(os.environ)
        env["PYTHONPATH"] = str(PROJECT_ROOT)

        result = subprocess.run(
            [
                sys.executable,
                str(PROJECT_ROOT / "scripts" / "package_dataset.py"),
                request_id,
                gender,
                age_bucket,
                str(count),
            ],
            capture_output=True,
            text=True,
            env=env,
        )

        print(result.stdout, flush=True)
        print(result.stderr, flush=True)

        if result.returncode != 0:

            print("Packaging failed — reverting to pending", flush=True)

            supabase.table("dataset_requests") \
                .update({"status": "pending"}) \
                .eq("request_id", request_id) \
                .execute()

        time.sleep(CHECK_INTERVAL)
# import os
# import sys
# from pathlib import Path
# import random

# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# sys.path.append(str(PROJECT_ROOT))

# import time
# from pathlib import Path
# from api.db import supabase
# import subprocess
# import sys
# from datetime import datetime, timedelta
# # import random

# CHECK_INTERVAL = 15  # seconds
# PROJECT_ROOT = Path(__file__).resolve().parents[1]

# print(" Dataset Request Worker Started")
# # import sys
# # from pathlib import Path

# # PROJECT_ROOT = Path(__file__).resolve().parents[1]
# # sys.path.append(str(PROJECT_ROOT))

# # import time
# # from api.db import supabase
# # import subprocess
# # from datetime import datetime


# # CHECK_INTERVAL = 15

# # print("Dataset Request Worker Started")

# def get_pending_requests():
#     res = supabase.table("dataset_requests") \
#         .select("*") \
#         .eq("status", "pending") \
#         .limit(1) \
#         .execute()
#     return res.data

# def mark_processing(request_id):
#     supabase.table("dataset_requests") \
#         .update({"status": "processing"}) \
#         .eq("request_id", request_id) \
#         .execute()

# def mark_waiting(request_id):
#     supabase.table("dataset_requests") \
#         .update({"status": "waiting_generation"}) \
#         .eq("request_id", request_id) \
#         .execute()

# def check_stock(gender, age_bucket, count):
#     res = supabase.table("stock_levels") \
#         .select("available_count") \
#         .eq("gender", gender) \
#         .eq("age_bucket", age_bucket) \
#         .execute()

#     if not res.data:
#         print(f"No inventory bucket yet for {gender}_{age_bucket}")
#         return False

#     return res.data[0]["available_count"] >= count

# while True:

#     jobs = get_pending_requests()

#     if not jobs:
#         print("No pending dataset requests", flush=True)
#         time.sleep(CHECK_INTERVAL)
#         continue

#     job = jobs[0]
#     request_id = job["request_id"]
#     gender = job["gender"]
#     age_bucket = job["age_bucket"]
#     count = job["count"]

#     print(f"\nProcessing request {request_id} → {gender}_{age_bucket} x{count}")

#     if not check_stock(gender, age_bucket, count):
#         print("Not enough inventory — waiting for generator")
#         mark_waiting(request_id)
#         time.sleep(CHECK_INTERVAL)
#         continue

#     # reserve job
#     mark_processing(request_id)

#     # NEW: pass request_id to packager
#     env = dict(os.environ)
#     env["PYTHONPATH"] = str(PROJECT_ROOT)

#     result = subprocess.run(
#         [
#             sys.executable,
#             str(PROJECT_ROOT / "scripts" / "package_dataset.py"),
#             request_id,
#             gender,
#             age_bucket,
#             str(count)
#         ],
#         capture_output=True,
#         text=True,
#         env=env
#     )

#     print(result.stdout)
#     print(result.stderr)

#     # If packager crashes → revert job
#     if result.returncode != 0:
#         print("Packaging failed — reverting to pending")

#         supabase.table("dataset_requests") \
#             .update({"status": "pending"}) \
#             .eq("request_id", request_id) \
#             .execute()

#     time.sleep(CHECK_INTERVAL)

# import sys
# from pathlib import Path
# import random

# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# sys.path.append(str(PROJECT_ROOT))

# import time
# from pathlib import Path
# from api.db import supabase
# import subprocess
# import sys
# from datetime import datetime, timedelta
# # import random

# CHECK_INTERVAL = 15  # seconds
# PROJECT_ROOT = Path(__file__).resolve().parents[1]

# print(" Dataset Request Worker Started")

# def get_pending_requests():
#     res = supabase.table("dataset_requests") \
#         .select("*") \
#         .eq("status", "pending") \
#         .limit(1) \
#         .execute()
#     return res.data

# def mark_processing(request_id):
#     supabase.table("dataset_requests") \
#         .update({"status": "processing"}) \
#         .eq("request_id", request_id) \
#         .execute()

# def mark_waiting(request_id):
#     supabase.table("dataset_requests") \
#         .update({"status": "waiting_generation"}) \
#         .eq("request_id", request_id) \
#         .execute()


# # def mark_completed(request_id, zip_name):

# #     auth_code = str(random.randint(100000, 999999))
# #     expires_at = datetime.utcnow() + timedelta(hours=24)

# #     supabase.table("dataset_requests") \
# #         .update({
# #             "status": "completed",
# #             "download_file": zip_name,
# #             "auth_code": auth_code,
# #             "download_limit": 3,
# #             "download_count": 0,
# #             "expires_at": expires_at.isoformat(),
# #             "completed_at": datetime.utcnow().isoformat()
# #         }) \
# #         .eq("request_id", request_id) \
# #         .execute()

# #     print(f" Auth code for {request_id}: {auth_code}")

# def mark_completed(request_id, zip_name):

#     supabase.table("dataset_requests") \
#         .update({
#             "status": "completed",
#             "download_file": zip_name,
#             "completed_at": datetime.utcnow().isoformat()
#         }) \
#         .eq("request_id", request_id) \
#         .execute()

#     print(f" Request {request_id} completed (auth code preserved)")


# def check_stock(gender, age_bucket, count):
#     res = supabase.table("stock_levels") \
#         .select("available_count") \
#         .eq("gender", gender) \
#         .eq("age_bucket", age_bucket) \
#         .single() \
#         .execute()
#     return res.data["available_count"] >= count

# while True:
#     jobs = get_pending_requests()

#     if not jobs:
#         print(" No pending dataset requests")
#         time.sleep(CHECK_INTERVAL)
#         continue

#     job = jobs[0]
#     request_id = job["request_id"]
#     gender = job["gender"]
#     age_bucket = job["age_bucket"]
#     count = job["count"]

#     print(f"\n Processing request {request_id} → {gender}_{age_bucket} x{count}")

#     if not check_stock(gender, age_bucket, count):
#         print(" Not enough inventory — waiting for generator")
#         mark_waiting(request_id)
#         time.sleep(CHECK_INTERVAL)
#         continue

#     mark_processing(request_id)

#     # call your existing packager
#     result = subprocess.run(
#         [
#             sys.executable,
#             str(PROJECT_ROOT / "scripts" / "package_dataset.py"),
#             gender,
#             age_bucket,
#             str(count)
#         ],
#         capture_output=True,
#         text=True
#     )

#     print(result.stdout)
#     print(result.stderr)


#     # # find newest zip
#     # delivered = PROJECT_ROOT / "delivered_datasets"
#     # latest_zip = sorted(delivered.glob("*.zip"), key=lambda p: p.stat().st_mtime)[-1]

#     # mark_completed(request_id, latest_zip.name)

#     # print(f" Request {request_id} completed")

#     # time.sleep(CHECK_INTERVAL)
#     zip_name = None

#     for line in result.stdout.splitlines():
#         if line.startswith("ZIP_OUTPUT::"):
#             zip_name = line.split("::")[1].strip()

#     if not zip_name:
#         print(" Packaging failed — no zip produced")
#         supabase.table("dataset_requests") \
#             .update({"status": "failed"}) \
#             .eq("request_id", request_id) \
#             .execute()
#         continue

#     mark_completed(request_id, zip_name)
