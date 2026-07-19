"""
frontend/components/upload_panel.py

Enterprise Upload Panel

Responsible for:

• Uploading datasets
• Calling FastAPI Upload API
• Storing dataset metadata in session

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from services.api_client import APIClient


class UploadPanel:
    """
    Upload dataset component.
    """

    def __init__(self):

        self.api = APIClient()

    # --------------------------------------------------

    def render(self):

        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=["csv", "xlsx", "xls"],
        )

        if uploaded_file is None:
            return

        if st.button(
            "📤 Upload Dataset",
            width="stretch",
        ):

            with st.spinner("Uploading dataset..."):

                try:

                    response = self.api.upload_file(
                        uploaded_file,
                    )

                    # -----------------------------
                    # Success
                    # -----------------------------

                    if response["success"]:

                        info = response["files"][0]

                        st.session_state["upload_success"] = True

                        st.session_state["file_name"] = uploaded_file.name

                        st.session_state["table_name"] = info["table_name"]

                        st.session_state["rows"] = info["rows"]

                        st.session_state["columns"] = len(
                            info["columns"]
                        )

                        st.session_state["profile"] = response.get(
                            "profile",
                            {},
                        )

                        st.session_state["suggestions"] = response.get(
                            "suggestions",
                            [],
                        )

                        st.success(
                            "Dataset uploaded successfully."
                        )

                    else:

                        st.error(
                            "Upload failed."
                        )

                except Exception as error:

                    st.error(str(error))