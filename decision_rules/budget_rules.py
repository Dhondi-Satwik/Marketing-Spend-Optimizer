import pandas as pd


TOTAL_WEEKLY_BUDGET = 500000
CHANNEL_CAP_RATIO = 0.40


def apply_budget_rules(weekly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies rule-based budget allocation.
    Expects one row per channel per week with ROI and stability metrics.
    Returns recommended budget per channel for the next week.
    """

    df = weekly_df.copy()

    # Base allocation: proportional to ROI (only positive ROI contributes)
    df["positive_roi"] = df["roi"].apply(lambda x: max(x, 0))
    total_positive_roi = df["positive_roi"].sum()

    if total_positive_roi == 0:
        # Equal split if no channel is profitable
        df["recommended_budget"] = TOTAL_WEEKLY_BUDGET / len(df)
    else:
        df["recommended_budget"] = (
            df["positive_roi"] / total_positive_roi
        ) * TOTAL_WEEKLY_BUDGET

    # Apply channel cap (40%)
    cap_value = CHANNEL_CAP_RATIO * TOTAL_WEEKLY_BUDGET
    df["recommended_budget"] = df["recommended_budget"].apply(
        lambda x: min(x, cap_value)
    )

    # Re-normalize to ensure total budget is conserved
    budget_sum = df["recommended_budget"].sum()
    if budget_sum != TOTAL_WEEKLY_BUDGET:
        df["recommended_budget"] = (
            df["recommended_budget"] / budget_sum
        ) * TOTAL_WEEKLY_BUDGET

    return df[["channel", "recommended_budget"]]
