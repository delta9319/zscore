__author__ = "Matthew Poole"

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

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


def test_financial_scores_in_germany_are_default():
    response = client.put("/company/de/10212356", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "scores": [
            {"year": 2020, "zscore": 6.8661517296099515},
            {"year": 2019, "zscore": 7.13880714484832},
            {"year": 2018, "zscore": 7.11875256899471},
            {"year": 2017, "zscore": 7.005949360640461},
            {"year": 2016, "zscore": 7.105545038787994},
        ]
    }


def test_financial_scores_in_uk():
    response = client.put("/company/gb/10149809", json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "scores": [
            {"year": 2020, "zscore": 6.539547842049954},
            {"year": 2019, "zscore": 6.786510311168614},
            {"year": 2018, "zscore": 6.6714673215855385},
            {"year": 2017, "zscore": 6.460657488940055},
            {"year": 2016, "zscore": 6.602816418774483},
        ]
    }


def test_financial_scores_in_france():
    response = client.put("/company/fr/10213542", json=payload)
    assert response.status_code == 200
    assert response.json() != {
        "scores": [
            {"year": 2020, "zscore": 6.539547842049954},
            {"year": 2019, "zscore": 6.786510311168614},
            {"year": 2018, "zscore": 6.6714673215855385},
            {"year": 2017, "zscore": 6.460657488940055},
            {"year": 2016, "zscore": 6.602816418774483},
        ]
    }


def test_financial_scores_bad_country_code():
    response = client.put("/company/gbh/10149809", json=payload)
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid country code"}


def test_financial_scores_bad_id():
    response = client.put("/company/gb/abc123", json=payload)
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid company id"}
