from dataclasses import dataclass


@dataclass(slots=True)
class BusinessReport:
    """
    Executive business report produced
    by the Business Intelligence Engine.
    """

    summary: str

    overview: str

    trends: str

    risks: str

    opportunities: str

    recommendations: str

    conclusion: str