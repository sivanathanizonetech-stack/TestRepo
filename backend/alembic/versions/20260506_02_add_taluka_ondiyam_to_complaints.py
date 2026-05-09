"""Add taluka and ondiyam columns to complaints.

Revision ID: 20260506_02
Revises: 20260506_01
Create Date: 2026-05-06 00:15:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260506_02"
down_revision = "20260506_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("complaints", sa.Column("taluka", sa.String(length=200), nullable=True))
    op.add_column("complaints", sa.Column("ondiyam", sa.String(length=200), nullable=True))


def downgrade() -> None:
    op.drop_column("complaints", "ondiyam")
    op.drop_column("complaints", "taluka")
