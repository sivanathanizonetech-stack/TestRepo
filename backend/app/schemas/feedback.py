from datetime import datetime
from typing import Optional

from app.schemas.base import SchemaModel


class FeedbackResponse(SchemaModel):
    id: int
    complaint_token: str
    rating: Optional[int]
    comment: Optional[str]
    citizen_name: Optional[str] = "Anonymous"
    created_at: datetime

    class Config:
        orm_mode = True

