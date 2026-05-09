from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.base import ExtensionBase


class ComplaintReceipt(ExtensionBase):
    __tablename__ = "complaint_receipts"

    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, nullable=False, index=True)
    complaint_token = Column(String(20), nullable=False, unique=True, index=True)
    receipt_number = Column(String(40), nullable=False, unique=True, index=True)
    citizen_name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    department_name = Column(String(200), nullable=True)
    constituency = Column(String(200), nullable=True)
    taluka = Column(String(200), nullable=True)
    ondiyam = Column(String(200), nullable=True)
    address = Column(String(500), nullable=True)
    status = Column(String(30), nullable=False, default="Pending")
    subject = Column(String(500), nullable=True)
    source = Column(String(50), nullable=False, default="system")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_synced_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
