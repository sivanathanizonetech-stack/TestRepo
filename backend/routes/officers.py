from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Officer
from app.schemas import OfficerCreate, OfficerResponse

router = APIRouter(prefix="/api/officers", tags=["Officers"])


@router.post("/", response_model=OfficerResponse)
def create_officer(officer: OfficerCreate, db: Session = Depends(get_db)):
    db_officer = Officer(**officer.dict())
    db.add(db_officer)
    db.commit()
    db.refresh(db_officer)
    return db_officer


@router.get("/", response_model=List[OfficerResponse])
def get_all_officers(db: Session = Depends(get_db)):
    return db.query(Officer).order_by(Officer.name).all()


@router.get("/{officer_id}", response_model=OfficerResponse)
def get_officer(officer_id: int, db: Session = Depends(get_db)):
    officer = db.query(Officer).filter(Officer.id == officer_id).first()
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")
    return officer


@router.put("/{officer_id}", response_model=OfficerResponse)
def update_officer(officer_id: int, update: OfficerCreate, db: Session = Depends(get_db)):
    officer = db.query(Officer).filter(Officer.id == officer_id).first()
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")

    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(officer, key, value)

    db.commit()
    db.refresh(officer)
    return officer


@router.delete("/{officer_id}")
def delete_officer(officer_id: int, db: Session = Depends(get_db)):
    officer = db.query(Officer).filter(Officer.id == officer_id).first()
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")
    db.delete(officer)
    db.commit()
    return {"message": "Officer deleted successfully"}
