"""
Formatting Utilities
"""


class Formatter:

    @staticmethod
    def compact(value):

        if not isinstance(value, (int, float)):

            return value

        if value >= 1_000_000_000:

            return f"{value/1_000_000_000:.2f}B"

        if value >= 1_000_000:

            return f"{value/1_000_000:.2f}M"

        if value >= 1_000:

            return f"{value/1_000:.2f}K"

        if float(value).is_integer():

            return str(int(value))

        return f"{value:.2f}"