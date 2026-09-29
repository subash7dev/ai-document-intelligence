import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Document Intelligence Dashboard")
st.caption("Overview of processed documents and validation performance")

try:
    response = requests.get(
        f"{API_URL}/api/analytics",
        timeout=10
    )

    if response.status_code != 200:
        st.error("Could not load analytics.")
        st.stop()

    data = response.json()

except requests.exceptions.ConnectionError:
    st.error("FastAPI backend is not running.")
    st.stop()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Documents Processed",
        data["documents_processed"]
    )

with col2:
    st.metric(
        "Validation Success",
        f'{data["validation_success_rate"]}%'
    )

with col3:
    st.metric(
        "Validation Errors",
        data["validation_errors"]
    )

with col4:
    st.metric(
        "Avg Processing Time",
        f'{data["average_processing_time"]} sec'
    )

st.divider()

st.subheader("📁 Document Types")

for document_type, count in data["document_types"].items():
    st.write(f"**{document_type.title()}** — {count}")

st.divider()

st.subheader("🕘 Recent Documents")

if data["recent_documents"]:
    st.dataframe(
        data["recent_documents"],
        use_container_width=True
    )
else:
    st.info("No documents processed yet.")