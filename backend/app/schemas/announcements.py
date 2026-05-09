from datetime import datetime
from typing import Optional

from app.schemas.base import SchemaModel


class AnnouncementBase(SchemaModel):
    title: Optional[str] = None
    content: str
    is_active: bool = True


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementResponse(AnnouncementBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

