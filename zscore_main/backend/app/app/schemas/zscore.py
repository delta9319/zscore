from typing import List

from pydantic import BaseModel


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
