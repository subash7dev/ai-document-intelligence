import os
import time

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database import get_db
from backend.models.document import Document
from backend.services.ocr_service import OCRService
from backend.services.llm_service import LLMService
from backend.services.validation_service import ValidationService


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

ocr_service = OCRService()
llm_service = LLMService()
validation_service = ValidationService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "resume",
    db: Session = Depends(get_db)
):
    start_time = time.time()

    os.makedirs(settings.upload_dir, exist_ok=True)

    file_path = os.path.join(
        settings.upload_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # OCR
    extracted_text = ocr_service.extract_text(file_path)

    # AI extraction
    extracted_data = llm_service.extract(
        text=extracted_text,
        document_type=document_type
    )

    # Validation
    validation_errors = validation_service.validate(
        data=extracted_data,
        document_type=document_type
    )

    processing_time = round(
        time.time() - start_time,
        2
    )

    status = (
        "validated"
        if not validation_errors
        else "validation_failed"
    )

    document = Document(
        filename=file.filename,
        document_type=document_type,
        status=status,
        extracted_text=extracted_text,
        extracted_data=extracted_data,
        validation_errors=validation_errors,
        confidence_score=None,
        processing_time=processing_time
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "id": document.id,
        "filename": document.filename,
        "document_type": document.document_type,
        "status": document.status,
        "extracted_data": document.extracted_data,
        "validation_errors": document.validation_errors,
        "processing_time": document.processing_time
    }