class ValidationService:

    def validate(self, data: dict, document_type: str) -> list[str]:
        errors = []

        if document_type == "resume":
            if not data.get("name"):
                errors.append("Missing candidate name")

            if not data.get("email"):
                errors.append("Missing email")

            if not data.get("skills"):
                errors.append("No skills detected")

        elif document_type == "invoice":
            required_fields = [
                "invoice_number",
                "vendor_name",
                "invoice_date",
                "total"
            ]

            for field in required_fields:
                if not data.get(field):
                    errors.append(f"Missing {field}")

        elif document_type == "purchase_order":
            if not data.get("po_number"):
                errors.append("Missing purchase order number")

            if not data.get("vendor_name"):
                errors.append("Missing vendor name")

        elif document_type == "receipt":
            if not data.get("total"):
                errors.append("Missing receipt total")

        elif document_type == "contract":
            if not data.get("parties"):
                errors.append("Missing contract parties")

        return errors