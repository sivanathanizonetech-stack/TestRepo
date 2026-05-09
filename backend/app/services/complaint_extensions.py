import json
import logging
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.extensions import ComplaintLifecycleEvent, ComplaintReceipt
from app.models.legacy import Complaint


logger = logging.getLogger(__name__)


def _receipt_number(token: str) -> str:
    return f"RCP-{token}"


def sync_complaint_extensions(
    db: Session,
    complaint: Complaint,
    event_type: str,
    previous_status: Optional[str] = None,
    actor: Optional[str] = "system",
    remarks: Optional[str] = None,
    event_payload: Optional[dict] = None,
) -> None:
    try:
        receipt = (
            db.query(ComplaintReceipt)
            .filter(ComplaintReceipt.complaint_token == complaint.token)
            .first()
        )
        if receipt is None:
            receipt = ComplaintReceipt(
                complaint_id=complaint.id,
                complaint_token=complaint.token,
                receipt_number=_receipt_number(complaint.token),
                citizen_name=complaint.name,
                phone=complaint.phone,
                department_name=complaint.department_name,
                constituency=complaint.constituency,
                taluka=complaint.taluka,
                ondiyam=complaint.ondiyam,
                address=complaint.address,
                status=complaint.status,
                subject=complaint.subject,
                source=actor or "system",
            )
            db.add(receipt)
        else:
            receipt.complaint_id = complaint.id
            receipt.citizen_name = complaint.name
            receipt.phone = complaint.phone
            receipt.department_name = complaint.department_name
            receipt.constituency = complaint.constituency
            receipt.taluka = complaint.taluka
            receipt.ondiyam = complaint.ondiyam
            receipt.address = complaint.address
            receipt.status = complaint.status
            receipt.subject = complaint.subject
            receipt.source = actor or receipt.source

        db.add(
            ComplaintLifecycleEvent(
                complaint_id=complaint.id,
                complaint_token=complaint.token,
                event_type=event_type,
                previous_status=previous_status,
                current_status=complaint.status,
                remarks=remarks,
                actor=actor,
                event_payload=json.dumps(event_payload) if event_payload else None,
            )
        )
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception(
            "Unable to sync complaint extension records for token %s",
            complaint.token,
        )
