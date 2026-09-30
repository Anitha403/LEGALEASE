import os
from datetime import datetime

import requests
import streamlit as st

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
from services.document_formatter import (
    format_docx,
    format_pdf,
    format_txt
)

from utils.text import html_preview


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 1.5rem;
    }

    .preview-card {
        background: #171717;
        color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 14px;
        max-height: 650px;
        overflow-y: auto;
        line-height: 1.65;
    }

    .preview-card h3 {
        color: #ffffff;
        margin-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


logo_col1, logo_col2, logo_col3 = st.columns(
    [1, 2, 1]
)


with logo_col2:

    if os.path.exists(
        "assets/logo.png"
    ):

        st.image(
            "assets/logo.png",
            width=110
        )


st.markdown(
    '<div class="main-title">LegalEase</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)


if "document" not in st.session_state:

    st.session_state.document = ""


if "editing" not in st.session_state:

    st.session_state.editing = False


with st.form(
    "document_form"
):

    col1, col2 = st.columns(2)


    with col1:

        document_type = st.selectbox(
            "Document Type",
            [
                "Employment Contract",
                "Non-Disclosure Agreement (NDA)",
                "Lease Agreement",
                "Freelance Work Contract",
                "Employment Offer Letter",
                "Service Agreement",
                "General Agreement",
            ]
        )


        dates = st.text_input(
            "Effective Date",
            value=datetime.now().strftime(
                "%d/%m/%Y"
            )
        )


    with col2:

        parties = st.text_area(
            "Parties Involved",
            placeholder=(
                "Example: Jane Doe "
                "(Service Provider), "
                "TechNova Inc. (Client)"
            ),
            height=120
        )


        terms = st.text_area(
            "Terms & Conditions",
            placeholder=(
                "Separate clauses with semicolons;\n"
                "Payment within 30 days; "
                "confidentiality must be maintained; "
                "either party may terminate with "
                "15 days notice"
            ),
            height=120
        )


    submitted = st.form_submit_button(
        "Generate Document",
        type="primary",
        use_container_width=True
    )


if submitted:

    if (
        not parties.strip()
        or not terms.strip()
    ):

        st.error(
            "Please enter the parties and terms "
            "before generating."
        )

    else:

        payload = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "dates":
                dates
        }


        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=120
                )


                response.raise_for_status()


                st.session_state.document = (
                    response.json()["content"]
                )


                st.session_state.editing = False


                st.success(
                    "Document generated successfully."
                )


            except requests.RequestException as exc:

                st.error(
                    "Could not connect to the "
                    "FastAPI backend. Make sure "
                    "it is running and BACKEND_URL "
                    "is correct."
                )

                st.code(
                    str(exc)
                )


if st.session_state.document:

    st.divider()


    left, right = st.columns(
        [2, 1]
    )


    with left:

        st.subheader(
            "Document Preview"
        )


        if st.session_state.editing:

            edited = st.text_area(
                "Edit Document",
                value=st.session_state.document,
                height=600
            )


            if st.button(
                "Save Edits",
                type="primary"
            ):

                st.session_state.document = edited

                st.session_state.editing = False

                st.rerun()


        else:

            st.markdown(
                f"""
                <div class="preview-card">
                    {html_preview(
                        st.session_state.document
                    )}
                </div>
                """,
                unsafe_allow_html=True
            )


    with right:

        st.subheader(
            "Actions"
        )


        if not st.session_state.editing:

            if st.button(
                "Click to Edit Document",
                use_container_width=True
            ):

                st.session_state.editing = True

                st.rerun()

        else:

            if st.button(
                "Cancel Editing",
                use_container_width=True
            ):

                st.session_state.editing = False

                st.rerun()


        current = (
            st.session_state.document
        )


        safe_name = "".join(

            c
            if c.isalnum() or c in "-_"
            else "_"

            for c in document_type.lower()
        )


        st.download_button(

            "Download TXT",

            data=format_txt(
                current
            ),

            file_name=f"{safe_name}.txt",

            mime="text/plain",

            use_container_width=True
        )


        st.download_button(

            "Download DOCX",

            data=format_docx(
                current,
                document_type
            ),

            file_name=f"{safe_name}.docx",

            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),

            use_container_width=True
        )


        st.download_button(

            "Download PDF",

            data=format_pdf(
                current,
                document_type
            ),

            file_name=f"{safe_name}.pdf",

            mime="application/pdf",

            use_container_width=True
        )


        st.info(
            "LegalEase creates editable drafts. "
            "Review the final document with a "
            "qualified legal professional before "
            "relying on it."
        )