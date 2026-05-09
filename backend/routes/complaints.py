import random
import string
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.complaint_extensions import sync_complaint_extensions
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Complaint, Department, Officer
from app.schemas import (
    ComplaintCreate,
    ComplaintResponse,
    ComplaintTrackResponse,
    ComplaintUpdate,
)

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])


def generate_token() -> str:
    letters = "".join(random.choices(string.ascii_uppercase, k=5))
    digits = "".join(random.choices(string.digits, k=5))
    return f"{letters}{digits}"


@router.post("/", response_model=ComplaintResponse)
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    token = generate_token()

    # Ensure uniqueness
    while db.query(Complaint).filter(Complaint.token == token).first():
        token = generate_token()

    db_complaint = Complaint(
        token=token,
        name=complaint.name,
        email=complaint.email,
        phone=complaint.phone,
        department_name=complaint.department_name,
        constituency=complaint.constituency,
        taluka=complaint.taluka,
        ondiyam=complaint.ondiyam,
        address=complaint.address,
        pincode=complaint.pincode,
        subject=complaint.subject,
        message=complaint.message,
        attachments=complaint.attachments,
        status="Pending",
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    sync_complaint_extensions(
        db=db,
        complaint=db_complaint,
        event_type="complaint.created",
        actor="citizen",
        remarks="Complaint submitted through the citizen flow.",
        event_payload={"status": db_complaint.status},
    )
    return db_complaint


@router.get("/", response_model=List[ComplaintResponse])
def get_all_complaints(
    status: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(Complaint)
    if status:
        query = query.filter(Complaint.status == status)
    if department:
        query = query.filter(Complaint.department_name == department)
    return query.order_by(Complaint.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/track/{token}", response_model=ComplaintTrackResponse)
def track_complaint(token: str, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.token == token).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found with this token")
    return complaint


@router.get("/stats")
def get_complaint_stats(db: Session = Depends(get_db)):
    total = db.query(Complaint).count()
    pending = db.query(Complaint).filter(Complaint.status == "Pending").count()
    in_progress = db.query(Complaint).filter(Complaint.status == "In Progress").count()
    resolved = db.query(Complaint).filter(Complaint.status == "Resolved").count()
    
    depts_count = db.query(Department).count()
    officers_count = db.query(Officer).count()
    
    return {
        "total_complaints": total,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "departments_count": depts_count,
        "officers_count": officers_count
    }


@router.get("/stats/by-department")
def get_complaints_by_department(db: Session = Depends(get_db)):
    """Return complaint counts grouped by department_name."""
    from sqlalchemy import func
    results = (
        db.query(Complaint.department_name, func.count(Complaint.id).label("count"))
        .filter(Complaint.department_name != None)
        .group_by(Complaint.department_name)
        .all()
    )
    return [{"department": r.department_name, "complaints": r.count} for r in results]


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(complaint_id: int, update: ComplaintUpdate, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    previous_status = complaint.status
    if update.status is not None:
        complaint.status = update.status
    if update.remarks is not None:
        complaint.remarks = update.remarks
    if update.assigned_officer_id is not None:
        complaint.assigned_officer_id = update.assigned_officer_id
    if update.department_id is not None:
        complaint.department_id = update.department_id

    db.commit()
    db.refresh(complaint)
    sync_complaint_extensions(
        db=db,
        complaint=complaint,
        event_type="complaint.updated",
        previous_status=previous_status,
        actor="admin",
        remarks=complaint.remarks,
        event_payload={
            "assigned_officer_id": complaint.assigned_officer_id,
            "department_id": complaint.department_id,
        },
    )
    return complaint


@router.delete("/{complaint_id}")
def delete_complaint(complaint_id: int, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    db.delete(complaint)
    db.commit()
    return {"message": "Complaint deleted successfully"}
