from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

legacy_metadata = MetaData(naming_convention=NAMING_CONVENTION)
extension_metadata = MetaData(
    schema=settings.extension_schema,
    naming_convention=NAMING_CONVENTION,
)

LegacyBase = declarative_base(metadata=legacy_metadata)
ExtensionBase = declarative_base(metadata=extension_metadata)


def get_target_metadata():
    return [LegacyBase.metadata, ExtensionBase.metadata]

