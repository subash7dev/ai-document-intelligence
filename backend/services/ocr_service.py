import json

from paddleocr import PaddleOCR


class OCRService:

    def __init__(self):
        self.ocr = PaddleOCR(
            lang="en",
            enable_mkldnn=False
        )

    def extract_text(self, image_path: str) -> str:
        results = self.ocr.predict(image_path)

        texts = []

        for result in results:

            data = result.json

            # PaddleOCR returns JSON as a string
            if isinstance(data, str):
                data = json.loads(data)

            # Result JSON has:
            # {"res": {..., "rec_texts": [...]}}
            if isinstance(data, dict):
                data = data.get("res", data)

            rec_texts = data.get("rec_texts", [])

            for text in rec_texts:
                if text and text.strip():
                    texts.append(text.strip())

        return "\n".join(texts)