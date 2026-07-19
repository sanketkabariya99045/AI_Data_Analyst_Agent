"""
frontend/components/dataset_info.py

Enterprise Dataset Health Dashboard

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st


class DatasetInfo:
    """
    Enterprise Dataset Health Panel.
    """

    @staticmethod
    def _quality(profile: dict):

        rows = max(profile.get("rows", 1), 1)

        missing = profile.get("missing_values", 0)

        duplicates = profile.get("duplicate_rows", 0)

        score = int(
            max(
                0,
                100 - ((missing + duplicates) / rows) * 100
            )
        )

        if score >= 95:

            return score, "🟢 Excellent"

        if score >= 85:

            return score, "🟡 Good"

        return score, "🔴 Needs Attention"

    # ----------------------------------------------------

    @staticmethod
    def render():

        st.subheader("📊 Dataset Health")

        if not st.session_state.get(
            "upload_success",
            False,
        ):

            st.info(
                "Upload a dataset to begin."
            )

            return

        profile = st.session_state.get(
            "profile",
            {},
        )

        score, status = DatasetInfo._quality(
            profile
        )

        # ==================================================
        # Quality
        # ==================================================

        col1, col2 = st.columns([1, 1])

        with col1:

            st.metric(
                "Quality Score",
                f"{score}%"
            )

        with col2:

            st.success(status)

        st.divider()

        # ==================================================
        # Dataset
        # ==================================================

        st.markdown("### 📄 Dataset")

        st.write(
            f"**File** : {st.session_state.get('file_name','Unknown')}"
        )

        st.write(
            f"**Table** : {st.session_state.get('table_name','Unknown')}"
        )

        st.divider()

        # ==================================================
        # Statistics
        # ==================================================

        stats1, stats2 = st.columns(2)

        with stats1:

            st.metric(
                "Rows",
                f"{profile.get('rows', st.session_state.get('rows',0)):,}"
            )

            st.metric(
                "Missing",
                profile.get(
                    "missing_values",
                    0,
                ),
            )

            st.metric(
                "Memory",
                f"{profile.get('memory_mb',0)} MB"
            )

        with stats2:

            st.metric(
                "Columns",
                profile.get(
                    "columns",
                    st.session_state.get(
                        "columns",
                        0,
                    ),
                ),
            )

            st.metric(
                "Duplicates",
                profile.get(
                    "duplicate_rows",
                    0,
                ),
            )

            st.metric(
                "Business Columns",
                len(
                    profile.get(
                        "business_columns",
                        [],
                    )
                ),
            )

        st.divider()

        # ==================================================
        # Business Columns
        # ==================================================

        st.markdown(
            "### 💼 Business Columns"
        )

        business_columns = profile.get(
            "business_columns",
            [],
        )

        if business_columns:

            cols = st.columns(2)

            for i, column in enumerate(
                business_columns
            ):

                with cols[i % 2]:

                    st.success(column)

        else:

            st.info(
                "No business columns detected."
            )

        st.divider()

        st.success(
            "✅ Dataset Ready for AI Analysis"
        )