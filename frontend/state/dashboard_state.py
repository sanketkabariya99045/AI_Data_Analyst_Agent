"""
Dashboard State Manager

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from state.session_keys import SessionKeys


class DashboardState:

    # --------------------------
    # Generic Methods
    # --------------------------

    @staticmethod
    def get(key, default=None):

        return st.session_state.get(
            key,
            default,
        )

    @staticmethod
    def set(key, value):

        st.session_state[key] = value

    # --------------------------
    # SQL
    # --------------------------

    @classmethod
    def sql(cls):

        return cls.get(
            SessionKeys.GENERATED_SQL,
            "",
        )

    @classmethod
    def set_sql(cls, sql):

        cls.set(
            SessionKeys.GENERATED_SQL,
            sql,
        )

    # --------------------------
    # Chart
    # --------------------------

    @classmethod
    def chart(cls):

        return cls.get(
            SessionKeys.CHART,
            None,
        )

    @classmethod
    def set_chart(cls, chart):

        cls.set(
            SessionKeys.CHART,
            chart,
        )

    # --------------------------
    # Results
    # --------------------------

    @classmethod
    def results(cls):

        return cls.get(
            SessionKeys.QUERY_RESULT,
            [],
        )

    @classmethod
    def set_results(cls, results):

        cls.set(
            SessionKeys.QUERY_RESULT,
            results,
        )

    # --------------------------
    # KPIs
    # --------------------------

    @classmethod
    def kpis(cls):

        return cls.get(
            SessionKeys.KPIS,
            [],
        )

    @classmethod
    def set_kpis(cls, value):

        cls.set(
            SessionKeys.KPIS,
            value,
        )

    # --------------------------
    # Summary
    # --------------------------

    @classmethod
    def summary(cls):

        return cls.get(
            SessionKeys.SUMMARY,
            {},
        )

    @classmethod
    def set_summary(cls, value):

        cls.set(
            SessionKeys.SUMMARY,
            value,
        )

    # --------------------------
    # Explanation
    # --------------------------

    @classmethod
    def explanation(cls):

        return cls.get(
            SessionKeys.EXPLANATION,
            {},
        )

    @classmethod
    def set_explanation(cls, value):

        cls.set(
            SessionKeys.EXPLANATION,
            value,
        )

    # --------------------------
    # Execution Time
    # --------------------------

    @classmethod
    def execution_time(cls):

        return cls.get(
            SessionKeys.EXECUTION_TIME,
            None,
        )

    @classmethod
    def set_execution_time(cls, value):

        cls.set(
            SessionKeys.EXECUTION_TIME,
            value,
        )