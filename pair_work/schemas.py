__author__ = "Matthew Poole"


from typing import List

from pydantic import BaseModel


class Financial(BaseModel):
    """
    Financial data model depending on given year.
    """

    year: int
    ebit: float
    equity: float
    retained_earnings: float
    sales: float
    total_assets: float
    total_liabilities: float
    working_capital: float


class FinancialPayload(BaseModel):
    """
    Financial data payload model.
    """

    financials: List[Financial]


class ZScore(BaseModel):
    """
    Z-score data model.
    """

    year: int
    zscore: float


class CompanyZScores(BaseModel):
    """
    Company Z-Score data response model.
    """

    scores: List[ZScore]
