import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def financial_payload() -> dict:
    payload = {
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
    }
    return payload


def default_scores() -> dict:
    scores = {
        "scores": [
            {"year": 2020, "zscore": 6.8661517296099515},
            {"year": 2019, "zscore": 7.13880714484832},
            {"year": 2018, "zscore": 7.11875256899471},
            {"year": 2017, "zscore": 7.005949360640461},
            {"year": 2016, "zscore": 7.105545038787994},
        ]
    }
    return scores


def uk_scores() -> dict:
    scores = {
        "scores": [
            {"year": 2020, "zscore": 6.539547842049954},
            {"year": 2019, "zscore": 6.786510311168614},
            {"year": 2018, "zscore": 6.6714673215855385},
            {"year": 2017, "zscore": 6.460657488940055},
            {"year": 2016, "zscore": 6.602816418774483},
        ]
    }
    return scores
