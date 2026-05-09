from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Announcement
from app.schemas import AnnouncementCreate, AnnouncementResponse
from routes.auth import get_current_user

router = APIRouter(prefix="/api/announcements", tags=["announcements"])

@router.post("/", response_model=AnnouncementResponse)
def create_announcement(
    announcement: AnnouncementCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_announcement = Announcement(
        title=announcement.title,
        content=announcement.content,
        is_active=announcement.is_active
    )
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

@router.get("/", response_model=List[AnnouncementResponse])
def list_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).filter(Announcement.is_active == True).order_by(Announcement.created_at.desc()).all()

@router.delete("/{announcement_id}")
def delete_announcement(
    announcement_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    db.delete(db_announcement)
    db.commit()
    return {"message": "Announcement deleted"}
