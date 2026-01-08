import pandas as pd
from datetime import datetime


ALLOWED_CHANNELS = {
    "Google Ads",
    "Meta Ads",
    "Email",
    "Affiliate"
}


REQUIRED_COLUMNS = [
    "date",
    "channel",
    "spend",
    "impressions",
    "clicks",
    "conversions",
    "revenue"
]


def validate_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates raw daily marketing data.
    Returns the validated DataFrame or raises ValueError.
    """

    # ---------- Schema validation ----------
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    extra_cols = set(df.columns) - set(REQUIRED_COLUMNS)

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    if extra_cols:
        raise ValueError(f"Unexpected extra columns: {extra_cols}")

    # ---------- Null checks ----------
    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError("Null values detected in required columns")

    # ---------- Date validation ----------
    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD")

    if (df["date"] > datetime.today()).any():
        raise ValueError("Future dates detected")

    # ---------- Channel validation ----------
    invalid_channels = set(df["channel"].unique()) - ALLOWED_CHANNELS
    if invalid_channels:
        raise ValueError(f"Invalid channel values detected: {invalid_channels}")

    # ---------- Numeric domain rules ----------
    numeric_checks = {
        "spend": df["spend"] < 0,
        "revenue": df["revenue"] < 0,
        "impressions": df["impressions"] < 0,
        "clicks": df["clicks"] < 0,
        "conversions": df["conversions"] < 0,
    }

    for col, condition in numeric_checks.items():
        if condition.any():
            raise ValueError(f"Negative values detected in column: {col}")

    # ---------- Hierarchy rules ----------
    if not (df["impressions"] >= df["clicks"]).all():
        raise ValueError("Impressions must be >= clicks")

    if not (df["clicks"] >= df["conversions"]).all():
        raise ValueError("Clicks must be >= conversions")

    # ---------- Duplicate check ----------
    if df.duplicated(subset=["date", "channel"]).any():
        raise ValueError("Duplicate (date, channel) rows detected")

    return df
