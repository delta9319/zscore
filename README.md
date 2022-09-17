# Z-score api

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mattpoole84/zscore/master.svg?badge_token=VWnIp4vsQ6GsPq4pRkUjfQ)](https://results.pre-commit.ci/latest/github/mattpoole84/zscore/master?badge_token=VWnIp4vsQ6GsPq4pRkUjfQ)

## Z-Score for Predicting bankruptcy

Professor Edward Altman, the co-founder of WiserFunding, created the Z-Score formula for predicting bankruptcy.

Coeffecients of Z-score formula are depending on the country.

```
Z = 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5

X1 = working_capital / total_assets
X2 = retained_earnings / total_assets
X3 = ebit / total_assets
X4 = equity / total_liabilities
X5 = sales / total_assets
```

## Pair Work

On the pair programming stage of this solution, we implement an API endpoint `company/<country iso code>/<id>` to accept PUT that expects a JSON payload on financials for 5 years using FastAPI without any generators and completed test scenarios according to country codes.

### Request

`PUT /company/<country_iso_code>/<id>`

Payload:

```
{
    "financials": [
        {"year": 2020, "ebit": 123.45, "equity": 234.56, "retained_earnings": 345.67, "sales":1234.56, "total_assets": 345.67, "total_liabilities": 456.78, "working_capital": 23.45},
        {"year": 2019, "ebit": 122.63, "equity": 224.56, "retained_earnings": 325.33, "sales":1214.99, "total_assets": 325.04, "total_liabilities": 426.78, "working_capital": 23.45},
        {"year": 2018, "ebit": 120.17, "equity": 214.06, "retained_earnings": 225.00, "sales":1204.01, "total_assets": 305.11, "total_liabilities": 426.78, "working_capital": 23.45},
        {"year": 2017, "ebit": 118.23, "equity": 204.96, "retained_earnings": 125.97, "sales":1200.00, "total_assets": 290.75, "total_liabilities": 426.78, "working_capital": 23.45},
        {"year": 2016, "ebit": 116.05, "equity": 234.56, "retained_earnings": 105.11, "sales":1010.82, "total_assets": 250.13, "total_liabilities": 426.78, "working_capital": 23.45}
    ]
}
```

returns a JSON response for the scores where xxx are the Z-scores for those 5 years.

```
{
    "scores": [
        {"year": 2020, "zscore": xxx},
        {"year": 2019, "zscore": xxx},
        {"year": 2018, "zscore": xxx},
        {"year": 2017, "zscore": xxx},
        {"year": 2016, "zscore": xxx}
    ]
}
```

## ZScore Main

Z-Score Solution using [Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql)

## Deployment to free tier on AWS

[ZScore Main](http://54.176.14.131)

    username: admin@localhost.com
    password: root#123

[API Documentation Docs](http://54.176.14.131/docs)

[API Documentation Redoc](http://54.176.14.131/redoc)

## Additional Points

- API documentation and examples using SwaggerUI and ReDoc
- Use of pre-commit, black, mypy, isort etc. (pre-commit with Github paid plan)
- docker compose up to run locally
- Build and deploy to free cloud tier on AWS.
