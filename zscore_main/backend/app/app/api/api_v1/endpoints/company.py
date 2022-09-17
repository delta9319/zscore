from fastapi import APIRouter, HTTPException, Path

from app import schemas, utils

router = APIRouter()


@router.put(
    "/{country_iso_code}/{id}",
    name="Company Z-Scores",
    summary="Calcuation of Z-Scores for 5 financial years with given company in the given country.",
    description="Calculate Z-Scores with Z-Score formula for predicting bankruptcy, created by \
             Professor Edward Altman, the co-founder of WiserFunding.",
    response_description="Dict of z-scores data per each year",
    response_model=schemas.CompanyZScores,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "scores": [
                            {"year": 2020, "zscore": 6.539547842049954},
                            {"year": 2019, "zscore": 6.786510311168614},
                            {"year": 2018, "zscore": 6.6714673215855385},
                            {"year": 2017, "zscore": 6.460657488940055},
                            {"year": 2016, "zscore": 6.602816418774483},
                        ]
                    }
                }
            }
        },
        422: {
            "description": "Validation Error.",
            "content": {
                "application/json": {"example": {"detail": "Invalid country code"}}
            },
        },
    },
)
def financial_scores(
    payload: schemas.FinancialPayload,
    country_iso_code: str = Path(..., description="Country ISO Code."),
    id: str = Path(..., description="Company ID."),
):
    """
    Get Z-scores for 5 financial years

    Args:
        iso_code (str): country iso code
        id (str): company id
        financial (Financial): financial data
    """
    if not utils.validate_country_code(country_iso_code):
        raise HTTPException(status_code=422, detail="Invalid country code")

    if not utils.validate_id(id):
        raise HTTPException(status_code=422, detail="Invalid company id")

    financials = payload.financials

    scores = []
    for financial in financials:
        score = schemas.ZScore(
            year=financial.year,
            zscore=utils.calc_zscore(financial, country_iso_code),
        )
        scores.append(score)

    result = dict(scores=scores)
    return result
