import pandas as pd
from sklearn.linear_model import LinearRegression


FEATURE_COLUMNS = [
    "weekly_spend",
    "weekly_clicks",
    "weekly_conversions",
    "weekly_revenue",
    "roi",
    "weekly_spend_lag_1",
    "weekly_revenue_lag_1",
    "roi_lag_1",
]


TARGET_COLUMN = "delayed_revenue"


def train_delayed_revenue_model(df: pd.DataFrame) -> LinearRegression:
    """
    Trains a simple, interpretable linear regression model
    to estimate delayed revenue.
    """

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    model = LinearRegression()
    model.fit(X, y)

    return model
