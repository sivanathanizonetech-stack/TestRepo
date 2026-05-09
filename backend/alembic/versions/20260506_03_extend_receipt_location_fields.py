"""Extend complaint receipt schema with location fields.

Revision ID: 20260506_03
Revises: 20260506_02
Create Date: 2026-05-06 00:35:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260506_03"
down_revision = "20260506_02"
branch_labels = None
depends_on = None

EXTENSION_SCHEMA = "grievance_extensions"


def upgrade() -> None:
    op.add_column(
        "complaint_receipts",
        sa.Column("constituency", sa.String(length=200), nullable=True),
        schema=EXTENSION_SCHEMA,
    )
    op.add_column(
        "complaint_receipts",
        sa.Column("taluka", sa.String(length=200), nullable=True),
        schema=EXTENSION_SCHEMA,
    )
    op.add_column(
        "complaint_receipts",
        sa.Column("ondiyam", sa.String(length=200), nullable=True),
        schema=EXTENSION_SCHEMA,
    )
    op.add_column(
        "complaint_receipts",
        sa.Column("address", sa.String(length=500), nullable=True),
        schema=EXTENSION_SCHEMA,
    )

    op.execute(
        f"""
        UPDATE "{EXTENSION_SCHEMA}".complaint_receipts AS cr
        SET
            constituency = c.constituency,
            taluka = c.taluka,
            ondiyam = c.ondiyam,
            address = c.address
        FROM complaints AS c
        WHERE cr.complaint_id = c.id
        """
    )


def downgrade() -> None:
    op.drop_column("complaint_receipts", "address", schema=EXTENSION_SCHEMA)
    op.drop_column("complaint_receipts", "ondiyam", schema=EXTENSION_SCHEMA)
    op.drop_column("complaint_receipts", "taluka", schema=EXTENSION_SCHEMA)
    op.drop_column("complaint_receipts", "constituency", schema=EXTENSION_SCHEMA)
