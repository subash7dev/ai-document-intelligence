from backend.services.ocr_service import OCRService


IMAGE_PATH = "data/uploads/test_invoice.jpg"


def main():
    print("\nStarting OCR...\n")

    ocr = OCRService()

    text = ocr.extract_text(IMAGE_PATH)

    print("=" * 60)
    print("EXTRACTED TEXT")
    print("=" * 60)

    print(text)

    print("=" * 60)


if __name__ == "__main__":
    main()