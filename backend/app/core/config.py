import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv


load_dotenv()


def _as_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    ssl_mode = os.getenv("DATABASE_SSLMODE", "").strip()
    if not ssl_mode:
        return database_url

    parts = urlsplit(database_url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.setdefault("sslmode", ssl_mode)
    return urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment)
    )


class Settings:
    def __init__(self) -> None:
        self.database_url = _normalize_database_url(
            os.getenv(
                "DATABASE_URL",
                "postgresql://postgres:1234@localhost:5432/tn_db",
            )
        )
        self.secret_key = os.getenv("SECRET_KEY", "tn_grievance_secret_key_2026")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
        )
        self.auto_create_legacy_tables = _as_bool(
            os.getenv("AUTO_CREATE_LEGACY_TABLES", "true"),
            default=True,
        )
        self.extension_schema = os.getenv(
            "GRIEVANCE_EXTENSION_SCHEMA",
            "grievance_extensions",
        )


settings = Settings()
