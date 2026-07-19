"""
frontend/components/download_panel.py

Enterprise Download Center

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd
import plotly.io as pio
import streamlit as st


class DownloadPanel:

    @staticmethod
    def render():

        st.subheader("📥 Download Center")

        sql = st.session_state.get("generated_sql", "")
        result = st.session_state.get("query_result", [])
        explanation = st.session_state.get("explanation", {})
        chart = st.session_state.get("chart", None)

        col1, col2 = st.columns(2)

        # ==================================================
        # Download SQL
        # ==================================================

        with col1:

            st.download_button(
                label="⬇ Download SQL",
                data=sql,
                file_name="generated_query.sql",
                mime="text/plain",
                disabled=(sql == ""),
                width="stretch",
                key="download_sql",
            )

        # ==================================================
        # Download CSV
        # ==================================================

        with col2:

            if result:

                df = pd.DataFrame(result)

                st.download_button(
                    label="⬇ Download CSV",
                    data=df.to_csv(index=False),
                    file_name="query_results.csv",
                    mime="text/csv",
                    width="stretch",
                    key="download_csv",
                )

            else:

                st.button(
                    "⬇ Download CSV",
                    disabled=True,
                    width="stretch",
                    key="download_csv_disabled",
                )

        st.divider()

        col3, col4 = st.columns(2)

        # ==================================================
        # Download Report
        # ==================================================

        with col3:

            report = ""

            if explanation:

                report = "\n\n".join(
                    [
                        explanation.get("overview", ""),
                        explanation.get("trends", ""),
                        explanation.get("risks", ""),
                        explanation.get("opportunities", ""),
                        explanation.get("recommendations", ""),
                        explanation.get("conclusion", ""),
                    ]
                )

            st.download_button(
                label="⬇ Download Report",
                data=report,
                file_name="executive_report.txt",
                mime="text/plain",
                disabled=(report == ""),
                width="stretch",
                key="download_report",
            )

        # ==================================================
        # Download Chart
        # ==================================================

        with col4:

            if chart is not None:

                try:

                    html = pio.to_html(
                        chart,
                        full_html=True,
                    )

                    st.download_button(
                        label="⬇ Download Chart",
                        data=html,
                        file_name="chart.html",
                        mime="text/html",
                        width="stretch",
                        key="download_chart",
                    )

                except Exception:

                    st.button(
                        "⬇ Download Chart",
                        disabled=True,
                        width="stretch",
                        key="download_chart_error",
                    )

            else:

                st.button(
                    "⬇ Download Chart",
                    disabled=True,
                    width="stretch",
                    key="download_chart_disabled",
                )