"""
frontend/components/upload_panel.py

Professional dataset upload component for the
AI Data Analyst Platform.

Responsibilities
----------------
- Upload CSV or Excel files
- Call FastAPI upload endpoint
- Display dataset metadata
- Store upload information in session state

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from services.api_client import APIClient


class UploadPanel:
    """
    Dataset Upload Component.
    """

    def __init__(self) -> None:
        self.api = APIClient()

    def render(self) -> None:
        """
        Render upload panel.
        """

        st.subheader("📂 Upload Dataset")

        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=["csv", "xlsx", "xls"],
        )

        if uploaded_file is None:
            return

        if st.button(
            "Upload Dataset",
            width="stretch",
        ):

            with st.spinner("Uploading dataset..."):

                try:

                    response = self.api.upload_file(
                        uploaded_file
                    )

                    if response["success"]:

                        st.success(
                            "Dataset uploaded successfully."
                        )

                        st.session_state["dataset"] = response

                        self._show_dataset_info(
                            response
                        )

                    else:

                        st.error(
                            "Upload failed."
                        )

                except Exception as error:

                    st.error(str(error))

        if "dataset" in st.session_state:

            self._show_dataset_info(
                st.session_state["dataset"]
            )

    # -----------------------------------------------------

    @staticmethod
    def _show_dataset_info(
        response: dict,
    ) -> None:
        """
        Display uploaded dataset metadata.
        """

        st.divider()

        st.subheader("📊 Dataset Information")

        file_info = response["files"][0]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Rows",
                file_info["rows"],
            )

        with col2:

            st.metric(
                "Columns",
                len(file_info["columns"]),
            )

        st.write(
            "**Table Name:**",
            file_info["table_name"],
        )

        with st.expander(
            "Column Names"
        ):

            st.write(
                file_info["columns"]
            )