from app.core.config import settings
from app.db.base import LegacyBase
from app.db.session import engine


def bootstrap_legacy_schema() -> None:
    if settings.auto_create_legacy_tables:
        LegacyBase.metadata.create_all(bind=engine)
