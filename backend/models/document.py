from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, JSON, String, Text

from backend.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)

    document_type = Column(
        String(50),
        nullable=False,
        index=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="processed"
    )

    extracted_text = Column(Text, nullable=True)

    extracted_data = Column(JSON, nullable=True)

    validation_errors = Column(JSON, nullable=True)

    confidence_score = Column(Float, nullable=True)

    processing_time = Column(Float, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
