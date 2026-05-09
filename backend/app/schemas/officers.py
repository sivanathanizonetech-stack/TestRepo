from datetime import datetime
from typing import Optional

from app.schemas.base import SchemaModel


class OfficerCreate(SchemaModel):
    name: str
    designation: Optional[str] = None
    department_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = "Active"


class OfficerResponse(SchemaModel):
    id: int
    name: str
    designation: Optional[str] = None
    department_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

