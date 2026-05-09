from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.db.base import ExtensionBase


class ComplaintLifecycleEvent(ExtensionBase):
    __tablename__ = "complaint_lifecycle_events"

    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, nullable=False, index=True)
    complaint_token = Column(String(20), nullable=False, index=True)
    event_type = Column(String(60), nullable=False)
    previous_status = Column(String(30), nullable=True)
    current_status = Column(String(30), nullable=False)
    remarks = Column(Text, nullable=True)
    actor = Column(String(100), nullable=True)
    event_payload = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
