from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models.document import Document

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


@router.get("")
def get_analytics(db: Session = Depends(get_db)):

    total_documents = db.query(Document).count()

    validated_documents = (
        db.query(Document)
        .filter(Document.status == "validated")
        .count()
    )

    validation_errors = (
        db.query(Document)
        .filter(Document.status == "validation_failed")
        .count()
    )

    average_processing_time = (
        db.query(func.avg(Document.processing_time))
        .scalar()
    )

    document_type_rows = (
        db.query(
            Document.document_type,
            func.count(Document.id)
        )
        .group_by(Document.document_type)
        .all()
    )

    document_types = {
        document_type: count
        for document_type, count in document_type_rows
    }

    recent_documents = (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .limit(10)
        .all()
    )

    success_rate = (
        (validated_documents / total_documents) * 100
        if total_documents > 0
        else 0
    )

    return {
        "documents_processed": total_documents,
        "validation_success_rate": round(success_rate, 2),
        "validation_errors": validation_errors,
        "average_processing_time": round(
            average_processing_time or 0,
            2
        ),
        "document_types": document_types,
        "recent_documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "document_type": document.document_type,
                "status": document.status,
                "processing_time": document.processing_time,
                "created_at": document.created_at
            }
            for document in recent_documents
        ]
    }