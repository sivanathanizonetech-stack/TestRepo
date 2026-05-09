from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from database import get_db
from models import Feedback

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


class FeedbackCreate(BaseModel):
    complaint_token: str
    citizen_name: Optional[str] = None
    rating: int
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: int
    complaint_token: str
    citizen_name: Optional[str] = None
    rating: int
    comment: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


@router.post("/", response_model=FeedbackResponse)
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    if not 1 <= feedback.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    db_feedback = Feedback(
        complaint_token=feedback.complaint_token,
        citizen_name=feedback.citizen_name,
        rating=feedback.rating,
        comment=feedback.comment,
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@router.get("/", response_model=List[FeedbackResponse])
def get_all_feedback(db: Session = Depends(get_db)):
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()
