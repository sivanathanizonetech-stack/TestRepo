from datetime import datetime
from typing import Optional

from app.schemas.base import SchemaModel


class FeedbackCreate(SchemaModel):
    complaint_token: str
    citizen_name: Optional[str] = None
    rating: int
    comment: Optional[str] = None


class FeedbackResponse(SchemaModel):
    id: int
    complaint_token: str
    rating: Optional[int]
    comment: Optional[str]
    citizen_name: Optional[str] = "Anonymous"
    created_at: datetime
