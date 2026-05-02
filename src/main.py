from fastapi import FastAPI
from .database import Base, engine

from .routers import auth, batches, sessions, attendance, monitoring

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(batches.router, prefix="/batches")
app.include_router(sessions.router, prefix="/sessions")
app.include_router(attendance.router, prefix="/attendance")
app.include_router(monitoring.router, prefix="/monitoring")

@app.get("/")
def root():
    return {"message": "API Running"}