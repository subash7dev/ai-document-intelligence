import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Document Intelligence",
    page_icon="📄",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("📄 DocIntel")
    st.caption("AI Document Intelligence")

    st.divider()

    st.markdown("""
    **Capabilities**

    🔍 OCR Extraction  
    🤖 AI Structuring  
    ✅ Validation  
    🗄️ Document Storage  
    📊 Analytics  
    🔎 Search
    """)

    st.divider()

    st.caption("Powered by")
    st.caption("PaddleOCR • Ollama • FastAPI • PostgreSQL")


st.title("AI Document Intelligence")
st.write(
    "Transform unstructured documents into validated, "
    "structured information using AI."
)

st.divider()

# Upload section
st.subheader("📤 Process a Document")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "Upload PDF or Image",
        type=["pdf", "jpg", "jpeg", "png"]
    )

with col2:
    document_type = st.selectbox(
        "Document Type",
        [
            "resume",
            "invoice",
            "purchase_order",
            "receipt",
            "contract"
        ]
    )

if uploaded_file:

    st.info(
        f"Selected: **{uploaded_file.name}** "
        f"({uploaded_file.size / 1024:.1f} KB)"
    )

    if st.button(
        "🚀 Process Document",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Running OCR → AI extraction → validation..."
        ):

            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{API_URL}/api/documents/upload",
                    params={
                        "document_type": document_type
                    },
                    files=files,
                    timeout=300
                )

                if response.status_code != 200:
                    st.error(
                        f"API Error: {response.status_code}"
                    )
                    st.code(response.text)
                    st.stop()

                result = response.json()

            except requests.exceptions.ConnectionError:
                st.error(
                    "FastAPI is not running. "
                    "Start the backend first."
                )
                st.stop()

            except requests.exceptions.Timeout:
                st.error(
                    "Document processing timed out."
                )
                st.stop()

        st.success("Document processed successfully!")

        st.divider()

        # Metrics
        col1, col2, col3 = st.columns(3)

        errors = result.get("validation_errors") or []

        with col1:
            st.metric(
                "Status",
                result["status"]
            )

        with col2:
            st.metric(
                "Processing Time",
                f'{result["processing_time"]} sec'
            )

        with col3:
            st.metric(
                "Validation Errors",
                len(errors)
            )

        st.divider()

        # Results
        st.subheader("🔍 Extracted Information")

        extracted_data = result.get(
            "extracted_data",
            {}
        )

        if extracted_data:
            st.json(extracted_data)
        else:
            st.warning(
                "No structured information was extracted."
            )

        st.subheader("✅ Validation")

        if errors:
            for error in errors:
                st.error(error)
        else:
            st.success(
                "Document passed all validation checks."
            )

        with st.expander("📋 Document Details"):
            st.write(f'**Document ID:** {result["id"]}')
            st.write(f'**Filename:** {result["filename"]}')
            st.write(f'**Type:** {result["document_type"]}')