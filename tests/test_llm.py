from backend.services.llm_service import LLMService


def main():

    text = """
    SUBASH CHANDRA BOSE G
    JAVA FULL STACK DEVELOPER
    Avadi, Chennai
    subashdev070@gmail.com

    SKILLS
    Java
    Python
    PostgreSQL
    SQL
    Git
    GitHub
    React

    EDUCATION
    B.Tech Information Technology
    St. Lourdes Engineering College
    """

    service = LLMService()

    result = service.extract(
        text=text,
        document_type="resume"
    )

    print("\n")
    print("=" * 60)
    print("STRUCTURED RESULT")
    print("=" * 60)

    print(result)

    print("=" * 60)


if __name__ == "__main__":
    main()