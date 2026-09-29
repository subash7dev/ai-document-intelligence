import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Search Documents",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Search Documents")
st.caption("Search processed documents and extracted information")

col1, col2 = st.columns([2, 1])

with col1:
    query = st.text_input(
        "Search",
        placeholder="Search name, skill, company, filename..."
    )

with col2:
    document_type = st.selectbox(
        "Document Type",
        [
            "All",
            "resume",
            "invoice",
            "purchase_order",
            "receipt",
            "contract"
        ]
    )

params = {}

if query:
    params["query"] = query

if document_type != "All":
    params["document_type"] = document_type

try:
    response = requests.get(
        f"{API_URL}/api/search",
        params=params,
        timeout=10
    )

    response.raise_for_status()
    data = response.json()

except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to backend: {e}")
    st.stop()

st.divider()

st.write(f"**{data['count']} document(s) found**")

for document in data["results"]:

    with st.container(border=True):

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.subheader(document["filename"])
            st.write(
                f"Type: **{document['document_type'].title()}**"
            )

        with col2:
            st.write(
                f"Status: **{document['status']}**"
            )

        with col3:
            st.write(
                f"Time: **{document['processing_time']}s**"
            )

        with st.expander("View extracted data"):
            st.json(document["extracted_data"])