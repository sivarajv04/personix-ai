import threading
import time
from workers import request_worker
from workers.request_worker import start_worker
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pathlib import Path
import uuid
from datetime import datetime
from api.routes.bulk_routes import router as bulk_router
from api.routes.admin_routes import router as admin_router
from api.monitoring.metrics_collector import monitoring_loop
import asyncio
from fastapi.responses import RedirectResponse
from api.schemas import DatasetRequest, DatasetResponse, DatasetStatus
from api.db import supabase

app = FastAPI(title="Personix AI Dataset API")

# -------------------------------------------------
# START BACKGROUND WORKER
# -------------------------------------------------
# def start_worker():
#     print("Starting dataset request worker...")
#     request_worker.main()

# @app.on_event("startup")
# def launch_worker():
#     thread = threading.Thread(target=start_worker)
#     thread.daemon = True
#     thread.start()
from workers.request_worker import start_worker
import threading
import asyncio

@app.on_event("startup")
def start_background_services():

    print("Starting background services...")

    # Start worker thread
    worker_thread = threading.Thread(
        target=start_worker,
        daemon=True
    )
    worker_thread.start()

    # Start monitoring loop
    loop = asyncio.get_event_loop()
    loop.create_task(monitoring_loop())
# -------------------------------------------------
# CORS FIX
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# ROOT
# -------------------------------------------------
@app.get("/")
def root():
    return {"message": "Personix Dataset API running"}

# -------------------------------------------------
# REQUEST DATASET
# -------------------------------------------------
@app.post("/dataset/request", response_model=DatasetResponse)
def request_dataset(req: DatasetRequest):

    request_id = f"req_{uuid.uuid4().hex[:8]}"
    auth_code = str(uuid.uuid4().int)[:6]   # 6 digit passcode

    supabase.table("dataset_requests").insert({
        "request_id": request_id,
        "gender": req.gender,
        "age_bucket": req.age_bucket,
        "count": req.count,
        "status": "pending",
        "auth_code": auth_code,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

    return DatasetResponse(
        request_id=request_id,
        status="queued",
        message=f"Order created. Save your passcode: {auth_code}"
    )

# -------------------------------------------------
# CHECK STATUS
# -------------------------------------------------
@app.get("/dataset/status/{request_id}", response_model=DatasetStatus)
def dataset_status(request_id: str):

    res = supabase.table("dataset_requests") \
        .select("*") \
        .eq("request_id", request_id) \
        .execute()

    if not res.data:
        raise HTTPException(status_code=404, detail="Request not found")

    row = res.data[0]

    if row["status"] != "completed":
        return DatasetStatus(
            request_id=request_id,
            status=row["status"],
            message="Dataset not ready yet",
            download_url=None
        )

    return DatasetStatus(
        request_id=request_id,
        status="completed",
        message="Dataset ready",
        download_url=f"/dataset/download/{request_id}/{row['auth_code']}"
    )

# -------------------------------------------------
# DOWNLOAD DATASET
# -------------------------------------------------
from api.storage.r2 import generate_signed_url

@app.get("/dataset/download/{request_id}/{auth_code}")
def download_dataset(request_id: str, auth_code: str):

    res = supabase.table("dataset_requests") \
        .select("*") \
        .eq("request_id", request_id) \
        .eq("auth_code", auth_code) \
        .execute()

    if not res.data:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    row = res.data[0]

    if row["status"] != "completed":
        raise HTTPException(status_code=400, detail="Dataset not ready")

    limit = row.get("download_limit", 3)
    used = row.get("download_count", 0)

    if used >= limit:
        raise HTTPException(
            status_code=403,
            detail=f"Download limit reached ({limit} downloads used)"
        )

    object_key = row["download_file"]
    if not object_key:
        raise HTTPException(status_code=404, detail="File missing")

    signed_url = generate_signed_url(object_key)

    supabase.table("dataset_requests").update({
        "download_count": used + 1
    }).eq("request_id", request_id).execute()

    return RedirectResponse(signed_url, status_code=302)

# -------------------------------------------------
# ROUTERS
# -------------------------------------------------
app.include_router(bulk_router, prefix="/bulk", tags=["Bulk Orders"])
app.include_router(admin_router)

# -------------------------------------------------
# HEALTH
# -------------------------------------------------
# @app.get("/health")
# def health():
#     return {"status": "ok"}
@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
# -------------------------------------------------
# MONITORING
# -------------------------------------------------
# @app.on_event("startup")
# async def start_monitoring():
#     asyncio.create_task(monitoring_loop())
@app.on_event("startup")
async def start_background_services():

    asyncio.create_task(monitoring_loop())

    # START DATASET WORKER
    threading.Thread(
        target=start_worker,
        daemon=True
    ).start()

# import threading
# import time
# from workers.request_worker import get_pending_requests
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI, HTTPException
# from pathlib import Path
# import uuid
# from datetime import datetime
# from api.routes.bulk_routes import router as bulk_router
# from api.routes.admin_routes import router as admin_router
# from api.monitoring.metrics_collector import monitoring_loop
# import asyncio
# from fastapi.responses import RedirectResponse
# from api.schemas import DatasetRequest, DatasetResponse, DatasetStatus
# from api.db import supabase

# app = FastAPI(title="Personix AI Dataset API")

# # CORS FIX
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # change later to frontend URL in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------------------------------------------------
# # ROOT
# # -------------------------------------------------
# @app.get("/")
# def root():
#     return {"message": "Personix Dataset API running"}

# # -------------------------------------------------
# # REQUEST DATASET
# # -------------------------------------------------
# @app.post("/dataset/request", response_model=DatasetResponse)
# def request_dataset(req: DatasetRequest):

#     request_id = f"req_{uuid.uuid4().hex[:8]}"
#     auth_code = str(uuid.uuid4().int)[:6]   # 6 digit passcode

#     supabase.table("dataset_requests").insert({
#         "request_id": request_id,
#         "gender": req.gender,
#         "age_bucket": req.age_bucket,
#         "count": req.count,
#         "status": "pending",
#         "auth_code": auth_code,
#         "created_at": datetime.utcnow().isoformat()
#     }).execute()

#     return DatasetResponse(
#         request_id=request_id,
#         status="queued",
#         message=f"Order created. Save your passcode: {auth_code}"
#     )

# # -------------------------------------------------
# # CHECK STATUS
# # -------------------------------------------------
# @app.get("/dataset/status/{request_id}", response_model=DatasetStatus)
# def dataset_status(request_id: str):

#     res = supabase.table("dataset_requests") \
#         .select("*") \
#         .eq("request_id", request_id) \
#         .execute()

#     if not res.data:
#         raise HTTPException(status_code=404, detail="Request not found")

#     row = res.data[0]

#     if row["status"] != "completed":
#         return DatasetStatus(
#             request_id=request_id,
#             status=row["status"],
#             message="Dataset not ready yet",
#             download_url=None
#         )

#     # IMPORTANT CHANGE:
#     # Instead of internal API download route → return stored R2 URL
#     return DatasetStatus(
#         request_id=request_id,
#         status="completed",
#         message="Dataset ready",
#         download_url=f"/dataset/download/{request_id}/{row['auth_code']}"
#     )

# # -------------------------------------------------
# # DOWNLOAD DATASET
# # -------------------------------------------------
# from api.storage.r2 import generate_signed_url

# @app.get("/dataset/download/{request_id}/{auth_code}")
# def download_dataset(request_id: str, auth_code: str):

#     res = supabase.table("dataset_requests") \
#         .select("*") \
#         .eq("request_id", request_id) \
#         .eq("auth_code", auth_code) \
#         .execute()

#     if not res.data:
#         raise HTTPException(status_code=403, detail="Invalid credentials")

#     row = res.data[0]

#     if row["status"] != "completed":
#         raise HTTPException(status_code=400, detail="Dataset not ready")

#     # ---- DOWNLOAD LIMIT CHECK ----
#     limit = row.get("download_limit", 3)
#     used = row.get("download_count", 0)

#     if used >= limit:
#         raise HTTPException(
#             status_code=403,
#             detail=f"Download limit reached ({limit} downloads used)"
#         )

#     object_key = row["download_file"]
#     if not object_key:
#         raise HTTPException(status_code=404, detail="File missing")

#     # ---- GENERATE TEMP LINK ----
#     signed_url = generate_signed_url(object_key)

#     # ---- INCREMENT COUNTER ----
#     supabase.table("dataset_requests").update({
#         "download_count": used + 1
#     }).eq("request_id", request_id).execute()

#     return RedirectResponse(signed_url, status_code=302)

# # @app.get("/dataset/download/{request_id}/{auth_code}")
# # def download_dataset(request_id: str, auth_code: str):

# #     res = supabase.table("dataset_requests") \
# #         .select("*") \
# #         .eq("request_id", request_id) \
# #         .eq("auth_code", auth_code) \
# #         .execute()

# #     if not res.data:
# #         raise HTTPException(status_code=403, detail="Invalid credentials")

# #     row = res.data[0]

# #     if row["status"] != "completed":
# #         raise HTTPException(status_code=400, detail="Dataset not ready")

# #     # IMPORTANT CHANGE:
# #     # Instead of FileResponse → redirect client to storage
# #     download_url = row["download_file"]

# #     if not download_url:
# #         raise HTTPException(status_code=404, detail="File missing")

# #     return {"download_url": download_url}

# # -------------------------------------------------
# # ROUTERS
# # -------------------------------------------------
# app.include_router(bulk_router, prefix="/bulk", tags=["Bulk Orders"])
# app.include_router(admin_router)

# # -------------------------------------------------
# # HEALTH
# # -------------------------------------------------
# @app.get("/health")
# def health():
#     return {"status": "ok"}

# # -------------------------------------------------
# # MONITORING
# # -------------------------------------------------
# @app.on_event("startup")
# async def start_monitoring():
#     asyncio.create_task(monitoring_loop())
