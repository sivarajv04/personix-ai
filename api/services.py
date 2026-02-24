import os
import uuid
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DELIVERED_DIR = PROJECT_ROOT / "delivered_datasets"


def check_stock(gender, age_bucket):
    row = supabase.table("stock_levels") \
        .select("available_count") \
        .eq("gender", gender) \
        .eq("age_bucket", age_bucket) \
        .single() \
        .execute().data

    return row["available_count"]


def create_delivery_record(gender, age_bucket, count):
    request_id = f"req_{uuid.uuid4().hex[:8]}"

    supabase.table("dataset_requests").insert({
        "request_id": request_id,
        "gender": gender,
        "age_bucket": age_bucket,
        "count": count,
        "status": "processing"
    }).execute()

    return request_id


def mark_ready(request_id, zip_name):
    supabase.table("dataset_requests").update({
        "status": "ready",
        "file": zip_name
    }).eq("request_id", request_id).execute()


def mark_waiting(request_id):
    supabase.table("dataset_requests").update({
        "status": "waiting_generation"
    }).eq("request_id", request_id).execute()
