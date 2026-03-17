from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine
from app.models import user, notification
from app.api.v1.router import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}