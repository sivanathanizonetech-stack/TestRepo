from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.db.base import LegacyBase


class Feedback(LegacyBase):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    complaint_token = Column(String(20), nullable=False, index=True)
    citizen_name = Column(String(200), nullable=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

