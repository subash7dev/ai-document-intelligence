from fastapi import FastAPI

from backend.database import Base, engine
from backend.models.document import Document
from backend.api.documents import router as documents_router
from backend.api.analytics import router as analytics_router
from backend.api.search import router as search_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Document Intelligence API",
    version="1.0.0"
)

app.include_router(documents_router)
app.include_router(analytics_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {
        "application": "AI Document Intelligence",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}