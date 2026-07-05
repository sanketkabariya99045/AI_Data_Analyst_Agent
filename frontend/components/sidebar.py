import streamlit as st

from services.api_client import APIClient
from utils.session import clear_analysis


class SidebarComponent:
    """
    Sidebar responsible for dataset upload.
    """

    @staticmethod
    def render():

        with st.sidebar:

            st.title("📊 AI Data Analyst")

            st.markdown("---")

            st.subheader("Upload Dataset")

            uploaded_file = st.file_uploader(
                label="Choose CSV or Excel",
                type=["csv", "xlsx", "xls"],
                accept_multiple_files=False,
            )

            if uploaded_file is not None:

                if st.button(
                    "Upload Dataset",
                    width="stretch",
                ):

                    try:

                        with st.spinner("Uploading dataset..."):

                            response = APIClient.upload_file(uploaded_file)

                        st.session_state.uploaded = True

                        st.session_state.table_name = response.get("table_name")
                        st.session_state.rows = response.get("rows")
                        st.session_state.columns = response.get("columns")

                        clear_analysis()

                        st.success("Dataset uploaded successfully.")

                    except Exception as e:

                        st.error(f"Upload failed.\n\n{e}")

            st.markdown("---")

            if st.session_state.uploaded:

                st.success("Dataset Ready")

                st.write(
                    f"**Table:** {st.session_state.table_name}"
                )

                rows = st.session_state.get("rows")
                columns = st.session_state.get("columns")

                if rows is not None:
                    st.write(f"Rows : {rows:,}")

                if columns is not None:

                    if isinstance(columns, list):
                        st.write(f"Columns : {len(columns)}")
                    else:
                        st.write(f"Columns : {columns}")