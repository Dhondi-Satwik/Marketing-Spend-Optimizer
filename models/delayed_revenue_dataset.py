import pandas as pd


def build_delayed_revenue_dataset(weekly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds an ML-ready dataset to predict delayed revenue.
    Target: delayed_revenue = revenue(t+1) + revenue(t+2)
    One row per channel per week (t).
    """

    df = weekly_df.copy()

    # Ensure proper sorting to avoid leakage
    df = df.sort_values(["channel", "week_start_date"]).reset_index(drop=True)

    # Lagged features (t-1)
    df["weekly_spend_lag_1"] = df.groupby("channel")["weekly_spend"].shift(1)
    df["weekly_revenue_lag_1"] = df.groupby("channel")["weekly_revenue"].shift(1)
    df["roi_lag_1"] = df.groupby("channel")["roi"].shift(1)

    # Future revenue for target
    df["revenue_t_plus_1"] = df.groupby("channel")["weekly_revenue"].shift(-1)
    df["revenue_t_plus_2"] = df.groupby("channel")["weekly_revenue"].shift(-2)

    # Target definition
    df["delayed_revenue"] = df["revenue_t_plus_1"] + df["revenue_t_plus_2"]

    # Drop rows with missing lags or missing future revenue
    required_cols = [
        "weekly_spend_lag_1",
        "weekly_revenue_lag_1",
        "roi_lag_1",
        "delayed_revenue",
    ]
    df = df.dropna(subset=required_cols)

    # Select final feature set
    final_df = df[
        [
            "week_start_date",
            "channel",
            "weekly_spend",
            "weekly_clicks",
            "weekly_conversions",
            "weekly_revenue",
            "roi",
            "weekly_spend_lag_1",
            "weekly_revenue_lag_1",
            "roi_lag_1",
            "delayed_revenue",
        ]
    ].reset_index(drop=True)

    return final_df
