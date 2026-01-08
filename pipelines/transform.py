import pandas as pd


def aggregate_weekly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates validated daily marketing data into weekly metrics.
    Returns one row per channel per week.
    """

    df = df.copy()

    # Ensure date is datetime
    df["date"] = pd.to_datetime(df["date"])

    # Compute week start date (Monday)
    df["week_start_date"] = df["date"] - pd.to_timedelta(df["date"].dt.weekday, unit="D")

    grouped = (
        df.groupby(["week_start_date", "channel"], as_index=False)
        .agg(
            weekly_spend=("spend", "sum"),
            weekly_impressions=("impressions", "sum"),
            weekly_clicks=("clicks", "sum"),
            weekly_conversions=("conversions", "sum"),
            weekly_revenue=("revenue", "sum"),
        )
    )

    # Derived metrics
    grouped["roi"] = grouped.apply(
        lambda x: x["weekly_revenue"] / x["weekly_spend"] if x["weekly_spend"] > 0 else 0,
        axis=1,
    )

    grouped["cpc"] = grouped.apply(
        lambda x: x["weekly_spend"] / x["weekly_clicks"] if x["weekly_clicks"] > 0 else 0,
        axis=1,
    )

    grouped["conversion_rate"] = grouped.apply(
        lambda x: x["weekly_conversions"] / x["weekly_clicks"] if x["weekly_clicks"] > 0 else 0,
        axis=1,
    )

    return grouped
