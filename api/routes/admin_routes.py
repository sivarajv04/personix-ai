from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from api.db import supabase
from fastapi import Body
from api.monitoring.metrics_cache import metrics_cache
from api.monitoring.health_rules import evaluate_health
from api.monitoring.metrics_cache import metrics_cache

router = APIRouter(prefix="/admin", tags=["admin"])

ADMIN_PASSWORD = "admin"


# ---------------- LOGIN ----------------
@router.post("/login")
def admin_login(payload: dict):
    if payload.get("password") != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"success": True}


# ---------------- METRICS ----------------
@router.get("/metrics")
def get_metrics():

    total = supabase.table("dataset_requests") \
        .select("*", count="exact") \
        .execute().count

    pending = supabase.table("dataset_requests") \
        .select("*", count="exact") \
        .neq("status", "completed") \
        .execute().count

    completed = supabase.table("dataset_requests") \
        .select("*", count="exact") \
        .eq("status", "completed") \
        .execute().count

    today_date = datetime.now(timezone.utc).date().isoformat()

    today = supabase.table("dataset_requests") \
        .select("*", count="exact") \
        .gte("created_at", today_date) \
        .execute().count

    return {
        "total_orders": total or 0,
        "pending_orders": pending or 0,
        "completed_orders": completed or 0,
        "today_orders": today or 0
    }
@router.get("/system-health")
def system_health():
    return metrics_cache.get()

@router.get("/system-status")
def system_status():
    snapshot = metrics_cache.get()
    return {
        "health": evaluate_health(snapshot),
        "metrics": snapshot
    }


# # ---------------- INSTANT ORDERS ----------------
# @router.get("/dataset-orders")
# def get_dataset_orders():

#     res = supabase.table("dataset_requests") \
#         .select("*") \
#         .order("created_at", desc=True) \
#         .limit(200) \
#         .execute()

#     return res.data


# # ---------------- BULK ORDERS ----------------
# @router.get("/bulk-orders")
# def get_bulk_orders():

#     res = supabase.table("bulk_orders") \
#         .select("*") \
#         .order("created_at", desc=True) \
#         .limit(200) \
#         .execute()

#     return res.data


# # ---------------- INVENTORY ----------------
# @router.get("/inventory")
# def get_inventory():

#     # gender distribution
#     male = supabase.table("dataset_requests") \
#         .select("*", count="exact") \
#         .eq("gender", "male") \
#         .execute().count

#     female = supabase.table("dataset_requests") \
#         .select("*", count="exact") \
#         .eq("gender", "female") \
#         .execute().count

#     # total images generated
#     total_images = supabase.table("dataset_requests") \
#         .select("count") \
#         .execute().data

#     total_images = sum(row["count"] for row in total_images)

#     return {
#         "male_images": male or 0,
#         "female_images": female or 0,
#         "total_images": total_images or 0
#     }
#...........................................................................................
@router.get("/dataset-orders")
def get_dataset_orders():

    res = supabase.table("dataset_requests") \
        .select("request_id, gender, age_bucket, count, status, created_at") \
        .order("created_at", desc=True) \
        .execute()

    return res.data


@router.get("/bulk-orders")
def get_bulk_orders():

    res = supabase.table("bulk_orders") \
        .select("*") \
        .order("created_at", desc=True) \
        .execute()

    return res.data



@router.get("/inventory")
def get_inventory():

    completed = supabase.table("dataset_requests") \
        .select("gender, age_bucket, count") \
        .eq("status", "completed") \
        .execute().data

    inventory = {}

    for row in completed:
        key = f"{row['gender']} | {row['age_bucket']}"
        inventory[key] = inventory.get(key, 0) + row["count"]

    return [
        {"category": k, "images": v}
        for k, v in inventory.items()
    ]

@router.get("/bulk-orders")
def get_bulk_orders():

    res = supabase.table("bulk_orders") \
        .select("*") \
        .order("created_at", desc=True) \
        .execute()

    return res.data or []
@router.get("/inventory")
def get_inventory():

    res = supabase.table("dataset_requests") \
        .select("*") \
        .eq("status", "completed") \
        .order("created_at", desc=True) \
        .execute()

    return res.data or []


@router.patch("/order-status/{request_id}")
def update_status(request_id: str, payload: dict = Body(...)):

    status = payload.get("status")

    if status not in ["pending", "processing", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    supabase.table("dataset_requests") \
        .update({"status": status}) \
        .eq("request_id", request_id) \
        .execute()

    return {"success": True}
@router.get("/usage-daily")
def usage_daily():

    from collections import defaultdict

    res = supabase.table("dataset_requests") \
        .select("created_at") \
        .execute()

    days = defaultdict(int)

    for row in res.data:
        if not row.get("created_at"):
            continue

        day = row["created_at"][:10]  # YYYY-MM-DD
        days[day] += 1

    return [
        {"date": k, "orders": v}
        for k, v in sorted(days.items())
    ]



# from fastapi import APIRouter, HTTPException, Header
# from datetime import datetime, timezone
# from api.db import supabase
# import uuid

# router = APIRouter(prefix="/admin", tags=["admin"])

# ADMIN_PASSWORD = "admin"
# ADMIN_TOKEN = None   # memory token (simple mode)

# # ---------------- LOGIN ----------------
# @router.post("/login")
# def admin_login(payload: dict):
#     global ADMIN_TOKEN

#     if payload.get("password") != ADMIN_PASSWORD:
#         raise HTTPException(status_code=401, detail="Invalid password")

#     ADMIN_TOKEN = str(uuid.uuid4())  # generate session token
#     return {"token": ADMIN_TOKEN}


# # ---------------- AUTH CHECK ----------------
# def verify_admin(x_admin_token: str = Header(None)):
#     if not ADMIN_TOKEN or x_admin_token != ADMIN_TOKEN:
#         raise HTTPException(status_code=401, detail="Unauthorized")


# # ---------------- METRICS ----------------
# @router.get("/metrics")
# def get_metrics(x_admin_token: str = Header(None)):
#     verify_admin(x_admin_token)

#     total = supabase.table("dataset_requests").select("*", count="exact").execute().count
#     pending = supabase.table("dataset_requests").select("*", count="exact").neq("status", "completed").execute().count
#     completed = supabase.table("dataset_requests").select("*", count="exact").eq("status", "completed").execute().count

#     today_date = datetime.now(timezone.utc).date().isoformat()
#     today = supabase.table("dataset_requests").select("*", count="exact").gte("created_at", today_date).execute().count

#     return {
#         "total_orders": total or 0,
#         "pending_orders": pending or 0,
#         "completed_orders": completed or 0,
#         "today_orders": today or 0
#     }


# from fastapi import APIRouter
# from datetime import datetime, timezone
# from api.db import supabase

# router = APIRouter(prefix="/admin", tags=["admin"])


# ADMIN_PASSWORD = "admin"

# @router.post("/login")
# def admin_login(payload: dict):

#     if payload.get("password") != ADMIN_PASSWORD:
#         raise HTTPException(status_code=401, detail="Invalid password")

#     return {"success": True}
# @router.get("/metrics")
# def get_metrics():

#     # total orders
#     total = supabase.table("dataset_requests") \
#         .select("*", count="exact") \
#         .execute().count

#     # pending orders (anything not completed)
#     pending = supabase.table("dataset_requests") \
#         .select("*", count="exact") \
#         .neq("status", "completed") \
#         .execute().count

#     # completed orders
#     completed = supabase.table("dataset_requests") \
#         .select("*", count="exact") \
#         .eq("status", "completed") \
#         .execute().count

#     # today orders
#     today_date = datetime.now(timezone.utc).date().isoformat()

#     today = supabase.table("dataset_requests") \
#         .select("*", count="exact") \
#         .gte("created_at", today_date) \
#         .execute().count

#     return {
#         "total_orders": total or 0,
#         "pending_orders": pending or 0,
#         "completed_orders": completed or 0,
#         "today_orders": today or 0
#     }

