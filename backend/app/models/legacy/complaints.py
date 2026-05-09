from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import LegacyBase


class Complaint(LegacyBase):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department_name = Column(String(200), nullable=True)
    constituency = Column(String(200), nullable=True)
    taluka = Column(String(200), nullable=True)
    ondiyam = Column(String(200), nullable=True)
    address = Column(Text, nullable=True)
    pincode = Column(String(10), nullable=True)
    subject = Column(String(500), nullable=True)
    message = Column(Text, nullable=False)
    status = Column(String(30), default="Pending")
    remarks = Column(Text, nullable=True)
    attachments = Column(Text, nullable=True)
    assigned_officer_id = Column(Integer, ForeignKey("officers.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    department_rel = relationship("Department", back_populates="complaints")
    assigned_officer = relationship("Officer")
