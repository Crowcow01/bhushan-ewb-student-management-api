

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine
from app.routes.students import router as students_router
from app.routes.ai_query import router as ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A REST API for managing student records.",
    lifespan=lifespan,
)

app.include_router(students_router)
app.include_router(ai_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Student Management API is running.",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
