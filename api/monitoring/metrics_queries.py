from datetime import datetime, timezone
from api.db import supabase
from datetime import datetime, timezone
import re

# -------------------------
# SAFE DATETIME PARSER
# -------------------------
from datetime import datetime, timezone
from dateutil import parser

def to_utc(value):
    if not value:
        return None
    try:
        dt = parser.parse(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None

# def to_utc(dt_str):
#     if not dt_str:
#         return None

#     # remove Z → +00:00
#     dt_str = dt_str.replace("Z", "+00:00")

#     # fix variable microseconds (.123, .1234, .12345 → .123000 etc)
#     match = re.match(r"(.*\.\d+)(\+.*|$)", dt_str)

#     if match:
#         base, suffix = match.groups()

#         # split seconds + fraction
#         sec, frac = base.split(".")
#         frac = (frac + "000000")[:6]   # force 6 digits

#         dt_str = f"{sec}.{frac}{suffix}"

#     try:
#         dt = datetime.fromisoformat(dt_str)
#     except Exception:
#         return None

#     # make timezone aware
#     if dt.tzinfo is None:
#         dt = dt.replace(tzinfo=timezone.utc)

#     return dt


# -------------------------
# FETCH DATA
# -------------------------
def fetch_all_requests():
    res = supabase.table("dataset_requests").select("*").execute()
    return res.data or []


# -------------------------
# QUEUE METRICS
# -------------------------
def compute_queue_metrics(rows):
    now = datetime.now(timezone.utc)

    pending = []
    processing = 0
    completed = 0

    for r in rows:
        status = r.get("status")

        if status == "pending":
            created = to_utc(r.get("created_at"))
            if created:
                pending.append(created)

        elif status == "processing":
            processing += 1

        elif status == "completed":
            completed += 1

    oldest_age = 0
    if pending:
        oldest_age = max((now - min(pending)).total_seconds(), 0)

    return {
        "pending_jobs": len(pending),
        "active_jobs": processing,
        "completed_jobs": completed,
        "oldest_pending_seconds": int(oldest_age)
    }

# def compute_queue_metrics(rows):
#     now = datetime.now(timezone.utc)

#     pending = [r for r in rows if r["status"] == "pending"]
#     processing = [r for r in rows if r["status"] == "processing"]
#     completed = [r for r in rows if r["status"] == "completed"]

#     oldest_age = 0

#     if pending:
#         oldest = min(pending, key=lambda r: r["created_at"])
#         created = to_utc(oldest["created_at"])
#         if created:
#             oldest_age = (now - created).total_seconds()

#     return {
#         "pending_jobs": len(pending),
#         "active_jobs": len(processing),
#         "completed_jobs": len(completed),
#         "oldest_pending_seconds": int(oldest_age)
#     }


# -------------------------
# PERFORMANCE METRICS
# -------------------------
def compute_performance_metrics(rows):
    durations = []

    for r in rows:
        if r.get("status") != "completed":
            continue

        start = to_utc(r.get("created_at"))
        end = to_utc(r.get("completed_at"))

        if start and end and end >= start:
            durations.append((end - start).total_seconds())

    avg_time = sum(durations) / len(durations) if durations else 0

    return {
        "avg_completion_seconds": round(avg_time, 2),
        "total_completed": len(durations)
    }

# def compute_performance_metrics(rows):
#     durations = []

#     for r in rows:
#         if r["status"] == "completed" and r.get("completed_at"):
#             start = to_utc(r["created_at"])
#             end = to_utc(r["completed_at"])

#             if start and end:
#                 durations.append((end - start).total_seconds())

#     avg_time = sum(durations) / len(durations) if durations else 0

#     return {
#         "avg_completion_seconds": round(avg_time, 2),
#         "total_completed": len(durations)
#     }


# -------------------------
# DOWNLOAD METRICS
# -------------------------
def compute_download_metrics(rows):
    total_downloads = sum(r.get("download_count", 0) or 0 for r in rows)

    unused = sum(
        1 for r in rows
        if r.get("status") == "completed" and (r.get("download_count", 0) == 0)
    )

    return {
        "total_downloads": total_downloads,
        "unused_completed_orders": unused
    }