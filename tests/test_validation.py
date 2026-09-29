from backend.services.validation_service import ValidationService


def main():
    service = ValidationService()

    data = {
        "name": "SUBASH CHANDRA BOSE",
        "email": "subashdev070@gmail.com",
        "skills": ["Java", "Python", "React"]
    }

    errors = service.validate(
        data=data,
        document_type="resume"
    )

    print("\n")
    print("=" * 60)
    print("VALIDATION RESULT")
    print("=" * 60)

    if errors:
        for error in errors:
            print("❌", error)
    else:
        print("✅ Document passed validation")

    print("=" * 60)


if __name__ == "__main__":
    main()