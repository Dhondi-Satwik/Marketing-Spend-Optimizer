import pandas as pd


DELAYED_REVENUE_THRESHOLD = 0.10  # 10% of current revenue


def apply_ml_blocker(
    rules_df: pd.DataFrame,
    weekly_df: pd.DataFrame,
    ml_predictions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Applies ML as a blocker only.
    Prevents budget reduction if delayed revenue is significant.

    rules_df:
        Output of rule-based allocation with columns:
        - channel
        - recommended_budget

    weekly_df:
        Weekly metrics with columns:
        - channel
        - weekly_revenue

    ml_predictions:
        ML output with columns:
        - channel
        - predicted_delayed_revenue
    """

    df = rules_df.merge(
        weekly_df[["channel", "weekly_revenue"]],
        on="channel",
        how="left",
    ).merge(
        ml_predictions,
        on="channel",
        how="left",
    )

    df["predicted_delayed_revenue"] = df["predicted_delayed_revenue"].fillna(0)

    # Block reduction if delayed revenue is material
    def block_if_needed(row):
        if row["predicted_delayed_revenue"] >= (
            DELAYED_REVENUE_THRESHOLD * row["weekly_revenue"]
        ):
            return row["weekly_revenue"]
        return row["recommended_budget"]

    df["final_budget"] = df.apply(block_if_needed, axis=1)

    return df[["channel", "final_budget"]]
