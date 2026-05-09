import re

from sqlalchemy import text

from app.core.config import settings
from app.db.base import ExtensionBase, LegacyBase
from app.db.session import engine


def _normalized_schema_name(schema_name: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", schema_name):
        raise ValueError(f"Unsupported schema name: {schema_name!r}")
    return schema_name


def bootstrap_database() -> None:
    if not settings.auto_create_legacy_tables:
        return

    with engine.begin() as connection:
        if connection.dialect.name == "postgresql" and settings.extension_schema:
            schema_name = _normalized_schema_name(settings.extension_schema)
            connection.execute(
                text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
            )

        LegacyBase.metadata.create_all(bind=connection)
        ExtensionBase.metadata.create_all(bind=connection)


def bootstrap_legacy_schema() -> None:
    bootstrap_database()
