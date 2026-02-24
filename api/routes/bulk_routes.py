from fastapi import APIRouter, HTTPException
from datetime import datetime
from api.db import supabase

# router = APIRouter(prefix="/bulk", tags=["Bulk Orders"])
router = APIRouter(tags=["Bulk Orders"])



@router.post("/create")
def create_bulk_order(payload: dict):

    required_fields = ["name", "email", "phone", "dataset_groups"]

    for field in required_fields:
        if field not in payload or not payload[field]:
            raise HTTPException(status_code=400, detail=f"{field} is required")

    supabase.table("bulk_orders").insert({
        "name": payload["name"],
        "email": payload["email"],
        "phone": payload["phone"],
        "company": payload.get("company"),
        "use_case": payload.get("use_case"),
        "description": payload.get("description"),
        "dataset_groups": payload["dataset_groups"],
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }).execute()

    return {"message": "Bulk order submitted successfully"}

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel, EmailStr
# from typing import List, Dict, Optional
# from api.db import supabase

# router = APIRouter(prefix="/bulk", tags=["Bulk Orders"])


# # ---------- Request Schema ----------
# class DatasetGroup(BaseModel):
#     gender: str
#     age: str
#     count: int


# class BulkOrderRequest(BaseModel):
#     name: str
#     email: EmailStr
#     phone: str
#     company: Optional[str] = None
#     use_case: Optional[str] = None
#     description: Optional[str] = None
#     dataset_groups: List[DatasetGroup]


# # ---------- Endpoint ----------
# @router.post("/create")
# def create_bulk_order(order: BulkOrderRequest):

#     try:
#         supabase.table("bulk_orders").insert({
#             "name": order.name,
#             "email": order.email,
#             "phone": order.phone,
#             "company": order.company,
#             "use_case": order.use_case,
#             "description": order.description,
#             "dataset_groups": [g.dict() for g in order.dataset_groups],
#             "status": "pending"
#         }).execute()

#         return {"message": "Bulk order submitted successfully"}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
