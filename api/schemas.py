from pydantic import BaseModel, Field
from pydantic import BaseModel

class DatasetRequest(BaseModel):
    gender: str = Field(example="male")
    age_bucket: str = Field(example="26_40")
    count: int = Field(example=50, gt=0, le=1000)


class DatasetResponse(BaseModel):
    request_id: str
    status: str
    message: str


class DatasetStatus(BaseModel):
    request_id: str
    status: str
    message: str
    download_url: str | None = None
