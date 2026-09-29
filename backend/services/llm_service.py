import json

import ollama

from backend.config import settings


class LLMService:

    def __init__(self):
        self.model = settings.ollama_model

    def extract(self, text: str, document_type: str) -> dict:
        prompt = f"""
You are a document intelligence extraction system.

Document type:
{document_type}

Extract structured information from the OCR text below.

Rules:
1. Return ONLY valid JSON.
2. Do not add markdown.
3. Do not invent information.
4. If a field is unavailable, use null.
5. Preserve values exactly where possible.
6. Return an object appropriate for the document type.

OCR TEXT:
{text}
"""

        response = ollama.chat(
            model=self.model,
            format="json",
            options={"temperature": 0},
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response["message"]["content"].strip()
        # Some models still wrap JSON in a markdown fence or add a short preamble.
        content = content.replace("```json", "```")
        if "```" in content:
            content = content.split("```", 1)[1].split("```", 1)[0].strip()

        start = content.find("{")
        if start < 0:
            raise ValueError("Ollama returned no JSON object for document extraction")

        try:
            result, _ = json.JSONDecoder().raw_decode(content[start:])
        except json.JSONDecodeError as exc:
            raise ValueError("Ollama returned malformed JSON for document extraction") from exc

        if not isinstance(result, dict):
            raise ValueError("Ollama extraction response must be a JSON object")

        return result
