__author__ = "Matthew Poole"

from typing import List

import pycountry
from schemas import Financial


def calc_zscore(financial: Financial, country_code: str):
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

    x1 = financial["working_capital"] / financial["total_assets"]
    x2 = financial["retained_earnings"] / financial["total_assets"]
    x3 = financial["ebit"] / financial["total_assets"]
    x4 = financial["equity"] / financial["total_liabilities"]
    x5 = financial["sales"] / financial["total_assets"]

    z = (
        coeffecients[0] * x1
        + coeffecients[1] * x2
        + coeffecients[2] * x3
        + coeffecients[3] * x4
        + coeffecients[4] * x5
    )

    return z


def get_zscore_coeffecients(country_code):

    coeffecients = {
        "gb": [1.2, 1.4, 3.3, 0.6, 1.0],
        "fr": [1.1, 1.3, 3.2, 0.5, 1.1],
    }

    return coeffecients.get(country_code, [1.0, 1.2, 3.1, 0.4, 1.2])


def validate_country_code(code):
    """
    Validate country code

    Args:
        code ([str]): country iso code

    Returns:
        [bool]: validation value
    """
    validation = False
    alpha_2 = code.upper()
    country = pycountry.countries.get(alpha_2=alpha_2)

    if country is not None:
        validation = True

    return validation


def validate_id(id):
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
