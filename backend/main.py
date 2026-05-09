import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from app.db.bootstrap import bootstrap_legacy_schema
from database import SessionLocal
from models import AdminUser
from routes import announcements, auth, complaints, departments, feedback, officers


bootstrap_legacy_schema()

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="TN Grievance Redressal Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(complaints.router)
app.include_router(departments.router)
app.include_router(officers.router)
app.include_router(feedback.router)
app.include_router(announcements.router)


@app.on_event("startup")
def create_startup_admin() -> None:
    admin_username = os.getenv("ADMIN_USERNAME", "").strip()
    admin_password = os.getenv("ADMIN_PASSWORD", "").strip()

    if not admin_username or not admin_password:
        logger.warning(
            "ADMIN_USERNAME or ADMIN_PASSWORD is not set; skipping automatic admin creation."
        )
        return

    db = SessionLocal()
    try:
        existing_admin = (
            db.query(AdminUser)
            .filter(AdminUser.username == admin_username)
            .first()
        )
        if existing_admin:
            logger.info(
                "Admin user '%s' already exists; skipping automatic admin creation.",
                admin_username,
            )
            return

        db.add(
            AdminUser(
                username=admin_username,
                hashed_password=pwd_context.hash(admin_password),
                role="admin",
            )
        )
        db.commit()
        logger.info(
            "Automatic admin user '%s' created successfully.",
            admin_username,
        )
    except Exception:
        db.rollback()
        logger.exception("Failed to create automatic admin user during startup.")
        raise
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the TN Grievance Redressal Portal API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
