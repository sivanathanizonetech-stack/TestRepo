"""Create isolated grievance extension schema tables.

Revision ID: 20260506_01
Revises:
Create Date: 2026-05-06 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260506_01"
down_revision = None
branch_labels = None
depends_on = None

EXTENSION_SCHEMA = "grievance_extensions"


def upgrade() -> None:
    op.execute(f'CREATE SCHEMA IF NOT EXISTS "{EXTENSION_SCHEMA}"')

    op.create_table(
        "complaint_receipts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("complaint_id", sa.Integer(), nullable=False),
        sa.Column("complaint_token", sa.String(length=20), nullable=False),
        sa.Column("receipt_number", sa.String(length=40), nullable=False),
        sa.Column("citizen_name", sa.String(length=200), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("department_name", sa.String(length=200), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("subject", sa.String(length=500), nullable=True),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "last_synced_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_complaint_receipts")),
        schema=EXTENSION_SCHEMA,
    )
    op.create_index(
        op.f("ix_complaint_receipts_complaint_id"),
        "complaint_receipts",
        ["complaint_id"],
        unique=False,
        schema=EXTENSION_SCHEMA,
    )
    op.create_index(
        op.f("ix_complaint_receipts_complaint_token"),
        "complaint_receipts",
        ["complaint_token"],
        unique=True,
        schema=EXTENSION_SCHEMA,
    )
    op.create_index(
        op.f("ix_complaint_receipts_receipt_number"),
        "complaint_receipts",
        ["receipt_number"],
        unique=True,
        schema=EXTENSION_SCHEMA,
    )

    op.create_table(
        "complaint_lifecycle_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("complaint_id", sa.Integer(), nullable=False),
        sa.Column("complaint_token", sa.String(length=20), nullable=False),
        sa.Column("event_type", sa.String(length=60), nullable=False),
        sa.Column("previous_status", sa.String(length=30), nullable=True),
        sa.Column("current_status", sa.String(length=30), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("actor", sa.String(length=100), nullable=True),
        sa.Column("event_payload", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_complaint_lifecycle_events"),
        ),
        schema=EXTENSION_SCHEMA,
    )
    op.create_index(
        op.f("ix_complaint_lifecycle_events_complaint_id"),
        "complaint_lifecycle_events",
        ["complaint_id"],
        unique=False,
        schema=EXTENSION_SCHEMA,
    )
    op.create_index(
        op.f("ix_complaint_lifecycle_events_complaint_token"),
        "complaint_lifecycle_events",
        ["complaint_token"],
        unique=False,
        schema=EXTENSION_SCHEMA,
    )

    op.execute(
        f"""
        INSERT INTO "{EXTENSION_SCHEMA}".complaint_receipts (
            complaint_id,
            complaint_token,
            receipt_number,
            citizen_name,
            phone,
            department_name,
            status,
            subject,
            source,
            created_at,
            last_synced_at
        )
        SELECT
            c.id,
            c.token,
            'RCP-' || c.token,
            c.name,
            c.phone,
            c.department_name,
            COALESCE(c.status, 'Pending'),
            c.subject,
            'migration-backfill',
            COALESCE(c.created_at, NOW()),
            COALESCE(c.updated_at, c.created_at, NOW())
        FROM complaints c
        ON CONFLICT (complaint_token) DO NOTHING
        """
    )
    op.execute(
        f"""
        INSERT INTO "{EXTENSION_SCHEMA}".complaint_lifecycle_events (
            complaint_id,
            complaint_token,
            event_type,
            previous_status,
            current_status,
            remarks,
            actor,
            event_payload,
            created_at
        )
        SELECT
            c.id,
            c.token,
            'complaint.backfilled',
            NULL,
            COALESCE(c.status, 'Pending'),
            c.remarks,
            'migration-backfill',
            '{{"source":"legacy_complaints"}}',
            COALESCE(c.created_at, NOW())
        FROM complaints c
        """
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_complaint_lifecycle_events_complaint_token"),
        table_name="complaint_lifecycle_events",
        schema=EXTENSION_SCHEMA,
    )
    op.drop_index(
        op.f("ix_complaint_lifecycle_events_complaint_id"),
        table_name="complaint_lifecycle_events",
        schema=EXTENSION_SCHEMA,
    )
    op.drop_table("complaint_lifecycle_events", schema=EXTENSION_SCHEMA)

    op.drop_index(
        op.f("ix_complaint_receipts_receipt_number"),
        table_name="complaint_receipts",
        schema=EXTENSION_SCHEMA,
    )
    op.drop_index(
        op.f("ix_complaint_receipts_complaint_token"),
        table_name="complaint_receipts",
        schema=EXTENSION_SCHEMA,
    )
    op.drop_index(
        op.f("ix_complaint_receipts_complaint_id"),
        table_name="complaint_receipts",
        schema=EXTENSION_SCHEMA,
    )
    op.drop_table("complaint_receipts", schema=EXTENSION_SCHEMA)
    op.execute(f'DROP SCHEMA IF EXISTS "{EXTENSION_SCHEMA}"')
