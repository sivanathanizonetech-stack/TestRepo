from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.bootstrap import bootstrap_database
from routes import announcements, auth, complaints, departments, feedback, officers

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
def on_startup() -> None:
    bootstrap_database()


@app.get("/")
def read_root():
    return {"message": "Welcome to the TN Grievance Redressal Portal API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
