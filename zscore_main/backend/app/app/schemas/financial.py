from typing import List

from pydantic import BaseModel


# Financial data
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


# Financial payload
class FinancialPayload(BaseModel):
    """
    Financial data payload model.
    """

    financials: List[Financial]

    class Config:
        schema_extra = {
            "description": "Financial data for given company with 5 years.",
            "example": {
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
            },
        }
