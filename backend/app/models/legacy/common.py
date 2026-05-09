import enum


class ComplaintStatus(str, enum.Enum):
    PENDING = "Pending"
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

