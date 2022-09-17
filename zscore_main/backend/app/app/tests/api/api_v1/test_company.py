from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import default_scores, financial_payload, uk_scores


def test_financial_scores_in_germany_are_default(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.put(
        f"{settings.API_V1_STR}/company/de/10212356",
        headers=superuser_token_headers,
        json=financial_payload(),
    )

    assert r.status_code == 200
    scores = r.json()
    assert scores
    assert scores == default_scores()


def test_financial_scores_in_uk(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.put(
        f"{settings.API_V1_STR}/company/gb/10149809",
        headers=superuser_token_headers,
        json=financial_payload(),
    )

    assert r.status_code == 200
    scores = r.json()
    assert scores
    assert scores == uk_scores()


def test_financial_scores_in_france_are_not_same_as_in_uk(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.put(
        f"{settings.API_V1_STR}/company/fr/10213542",
        headers=superuser_token_headers,
        json=financial_payload(),
    )

    assert r.status_code == 200
    scores = r.json()
    assert scores
    assert scores != uk_scores()


def test_financial_scores_with_bad_country_code(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.put(
        f"{settings.API_V1_STR}/company/gbh/10149809",
        headers=superuser_token_headers,
        json=financial_payload(),
    )

    assert r.status_code == 422
    assert r.json() == {"detail": "Invalid country code"}


def test_financial_scores_with_bad_company_id(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.put(
        f"{settings.API_V1_STR}/company/gb/abc123",
        headers=superuser_token_headers,
        json=financial_payload(),
    )

    assert r.status_code == 422
    assert r.json() == {"detail": "Invalid company id"}
