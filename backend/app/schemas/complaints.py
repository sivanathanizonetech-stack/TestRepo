from datetime import datetime
from typing import Optional

from app.schemas.base import SchemaModel


class ComplaintCreate(SchemaModel):
    name: str
    email: Optional[str] = None
    phone: str
    department_name: Optional[str] = None
    constituency: Optional[str] = None
    taluka: Optional[str] = None
    ondiyam: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    subject: Optional[str] = None
    message: str
    attachments: Optional[str] = None


class ComplaintUpdate(SchemaModel):
    status: Optional[str] = None
    remarks: Optional[str] = None
    assigned_officer_id: Optional[int] = None
    department_id: Optional[int] = None


class ComplaintResponse(SchemaModel):
    id: int
    token: str
    name: str
    email: Optional[str] = None
    phone: str
    department_name: Optional[str] = None
    constituency: Optional[str] = None
    taluka: Optional[str] = None
    ondiyam: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    subject: Optional[str] = None
    message: str
    status: str
    remarks: Optional[str] = None
    attachments: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ComplaintTrackResponse(SchemaModel):
    id: Optional[int] = None
    token: str
    name: str
    phone: str
    email: Optional[str] = None
    department_name: Optional[str] = None
    constituency: Optional[str] = None
    taluka: Optional[str] = None
    ondiyam: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    subject: Optional[str] = None
    message: str
    status: str
    remarks: Optional[str] = None
    attachments: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class DashboardStats(SchemaModel):
    total_complaints: int
    pending: int
    in_progress: int
    resolved: int
    departments_count: int
    officers_count: int
