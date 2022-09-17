import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import emails
import pycountry
from emails.template import JinjaTemplate
from jose import jwt

from app.core.config import settings
from app.schemas import Financial, ZScore


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


def calc_zscore(financial: Financial, country_code: str) -> float:
    """
    Calculation Z-score per each financial year.

        Professor Edward Altman, the co-founder of WiserFunding, created the Z-Score formula for
        predicting bankruptcy.

        Z = 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5
        X1 = working_capital / total_assets
        X2 = retained_earnings / total_assets
        X3 = ebit / total_assets
        X4 = equity / total_liabilities
        X5 = sales / total_assets

    Args:
        financial (Financial): financial data per each year

    Returns:
        [float]: z-score
    """
    coeffecients = get_zscore_coeffecients(country_code)

    x1 = financial.working_capital / financial.total_assets
    x2 = financial.retained_earnings / financial.total_assets
    x3 = financial.ebit / financial.total_assets
    x4 = financial.equity / financial.total_liabilities
    x5 = financial.sales / financial.total_assets

    z = (
        coeffecients[0] * x1
        + coeffecients[1] * x2
        + coeffecients[2] * x3
        + coeffecients[3] * x4
        + coeffecients[4] * x5
    )

    return z


def get_zscore_coeffecients(country_code) -> list:
    """
    Get coeffecients of zscore formula depending on country_code

    Args:
        country_code (str): country iso code

    Returns:
        list: zscore formula coeffecients
    """
    coeffecients = {
        "gb": [1.2, 1.4, 3.3, 0.6, 1.0],  # UK
        "fr": [1.1, 1.3, 3.2, 0.5, 1.1],  # France
    }

    return coeffecients.get(country_code, [1.0, 1.2, 3.1, 0.4, 1.2])


def validate_country_code(code) -> bool:
    """
    Validate country code

    Args:
        code (str): country iso code

    Returns:
        [bool]: validated value
    """
    validation = False
    alpha_2 = code.upper()
    country = pycountry.countries.get(alpha_2=alpha_2)

    if country is not None:
        validation = True

    return validation


def validate_id(id) -> bool:
    """
    Validate company id

    Args:
        id (str): company id

    Returns:
        [bool]: validated value
    """
    validation = False
    if id.isnumeric():
        validation = True

    return validation
