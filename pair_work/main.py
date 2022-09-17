__author__ = "Matthew Poole"

from fastapi import Body, FastAPI, HTTPException, Path
from schemas import CompanyZScores, Financial, ZScore
from utils import calc_zscore, validate_country_code, validate_id

app = FastAPI(
    title="WiserFunding Technical Assignment",
    description="This API was built with FastAPI and exists to calcuate z-scores for 5 financial years related to company given the ID.",
    version="1.0.0",
)


@app.get("/", name="index")
async def root():
    return {"WiserFunding": "Technical Assignment"}


@app.put(
    "/company/{country_iso_code}/{id}",
    name="Company Z-Scores",
    summary="Calcuation of Z-Scores for 5 financial years with given company in the given country.",
    description="Calculate Z-Scores with Z-Score formula for predicting bankruptcy, created by \
             Professor Edward Altman, the co-founder of WiserFunding.",
    response_description="Dict of z-scores data per each year",
    response_model=CompanyZScores,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "financials": {
                                "type": "array",
                                "items": Financial.schema(
                                    ref_template="#/components/schemas/{model}"
                                ),
                            }
                        },
                    }
                }
            }
        }
    },
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
    tags=["Routes"],
)
async def financial_scores(
    country_iso_code: str = Path(..., description="Country ISO Code."),
    id: str = Path(..., description="Company ID."),
    payload: dict = Body(
        ...,
        description="Financial data for given company with 5 years.",
        example={
            "financials": [
                {
                    "year": 2020,
                    "ebit": 123.45,
                    "equity": 234.56,
                    "retained_earnings": 345.67,
                    "sales": 1234.56,
                    "total_assets": 345.67,
                    "total_liabilities": 456.78,
                    "working_capital": 23.45,
                },
                {
                    "year": 2019,
                    "ebit": 122.63,
                    "equity": 224.56,
                    "retained_earnings": 325.33,
                    "sales": 1214.99,
                    "total_assets": 325.04,
                    "total_liabilities": 426.78,
                    "working_capital": 23.45,
                },
                {
                    "year": 2018,
                    "ebit": 120.17,
                    "equity": 214.06,
                    "retained_earnings": 225.00,
                    "sales": 1204.01,
                    "total_assets": 305.11,
                    "total_liabilities": 426.78,
                    "working_capital": 23.45,
                },
                {
                    "year": 2017,
                    "ebit": 118.23,
                    "equity": 204.96,
                    "retained_earnings": 125.97,
                    "sales": 1200.00,
                    "total_assets": 290.75,
                    "total_liabilities": 426.78,
                    "working_capital": 23.45,
                },
                {
                    "year": 2016,
                    "ebit": 116.05,
                    "equity": 234.56,
                    "retained_earnings": 105.11,
                    "sales": 1010.82,
                    "total_assets": 250.13,
                    "total_liabilities": 426.78,
                    "working_capital": 23.45,
                },
            ]
        },
    ),
):
    """
    Get Z-scores for 5 financial years

    Args:
        iso_code (str): country iso code
        id (str): company id
        financial (Financial): financial data
    """
    if not validate_country_code(country_iso_code):
        raise HTTPException(status_code=422, detail="Invalid country code")

    if not validate_id(id):
        raise HTTPException(status_code=422, detail="Invalid company id")

    financials = payload["financials"]

    scores = []
    for financial in financials:
        score = ZScore(
            year=financial["year"], zscore=calc_zscore(financial, country_iso_code)
        )
        scores.append(score)

    result = dict(scores=scores)
    return result
