from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.document import Document

router = APIRouter(
    prefix="/api/search",
    tags=["Search"]
)


@router.get("")
def search_documents(
    query: str | None = Query(default=None),
    document_type: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    documents = db.query(Document)

    if document_type:
        documents = documents.filter(
            Document.document_type == document_type
        )

    results = documents.order_by(
        Document.created_at.desc()
    ).all()

    if query:
        query_lower = query.lower()

        results = [
            document
            for document in results
            if (
                query_lower in document.filename.lower()
                or query_lower in (
                    document.extracted_text or ""
                ).lower()
                or query_lower in str(
                    document.extracted_data or {}
                ).lower()
            )
        ]

    return {
        "count": len(results),
        "results": [
            {
                "id": document.id,
                "filename": document.filename,
                "document_type": document.document_type,
                "status": document.status,
                "extracted_data": document.extracted_data,
                "processing_time": document.processing_time,
                "created_at": document.created_at
            }
            for document in results
        ]
    }