"""
Enterprise JSON Serializer.

Converts NumPy and Pandas values into
standard Python objects.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import numpy as np


def to_python(value):

    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        return float(value)

    if isinstance(value, np.bool_):
        return bool(value)

    if isinstance(value, dict):

        return {
            k: to_python(v)
            for k, v in value.items()
        }

    if isinstance(value, list):

        return [
            to_python(v)
            for v in value
        ]

    return value