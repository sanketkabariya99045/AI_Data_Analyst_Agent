"""
backend/utils/metadata.py

Production-ready dataset profiling utility for the AI Data Analyst project.
"""

from __future__ import annotations

from typing import Any, Dict

import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
)


class DatasetProfiler:
    """Profiles a pandas DataFrame and returns metadata."""

    def profile(self, df: pd.DataFrame, dataset_name: str = "dataset") -> Dict[str, Any]:
        return {
            "dataset_name": dataset_name,
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_usage_mb": round(
                df.memory_usage(deep=True).sum() / (1024 * 1024), 2
            ),
            "columns_info": [self._profile_column(df[col]) for col in df.columns],
        }

    def _profile_column(self, series: pd.Series) -> Dict[str, Any]:
        total = len(series)
        missing = int(series.isna().sum())

        info: Dict[str, Any] = {
            "column_name": series.name,
            "data_type": str(series.dtype),
            "missing_values": missing,
            "missing_percentage": round((missing / total * 100), 2) if total else 0.0,
            "unique_values": int(series.nunique(dropna=True)),
            "is_numeric": bool(is_numeric_dtype(series)),
            "is_datetime": bool(is_datetime64_any_dtype(series)),
            "is_boolean": bool(is_bool_dtype(series)),
        }

        if is_numeric_dtype(series):
            clean = series.dropna()
            if not clean.empty:
                info["statistics"] = {
                    "min": float(clean.min()),
                    "max": float(clean.max()),
                    "mean": float(clean.mean()),
                    "median": float(clean.median()),
                    "std": float(clean.std()) if len(clean) > 1 else 0.0,
                }

        elif is_datetime64_any_dtype(series):
            clean = series.dropna()
            if not clean.empty:
                info["statistics"] = {
                    "min": str(clean.min()),
                    "max": str(clean.max()),
                }

        else:
            top = series.astype(str).fillna("NULL").value_counts().head(5)
            info["top_values"] = top.to_dict()

        return info


def profile_dataframe(df: pd.DataFrame, dataset_name: str = "dataset") -> Dict[str, Any]:
    """Convenience function."""
    return DatasetProfiler().profile(df, dataset_name)


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "Product": ["A", "B", "A", None],
            "Revenue": [100, 250, 300, 150],
            "Profit": [20, 50, 60, None],
            "Date": pd.to_datetime(
                ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]
            ),
        }
    )

    from pprint import pprint

    pprint(profile_dataframe(sample, "sample.csv"))
