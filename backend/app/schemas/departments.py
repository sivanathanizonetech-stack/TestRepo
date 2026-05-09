from datetime import datetime
from typing import Optional

from app.schemas.base import SchemaModel


class DepartmentCreate(SchemaModel):
    name: str
    name_ta: Optional[str] = None
    description: Optional[str] = None
    head_officer: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None


class DepartmentResponse(SchemaModel):
    id: int
    name: str
    name_ta: Optional[str] = None
    description: Optional[str] = None
    head_officer: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

