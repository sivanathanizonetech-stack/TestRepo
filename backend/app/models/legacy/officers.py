from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import LegacyBase


class Officer(LegacyBase):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    designation = Column(String(200), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    email = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)
    status = Column(String(20), default="Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    department_rel = relationship("Department", back_populates="officers")

