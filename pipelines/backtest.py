import pandas as pd

from pipelines.transform import aggregate_weekly
from decision_rules.budget_rules import apply_budget_rules
from decision_rules.ml_blocker import apply_ml_blocker
from models.delayed_revenue_dataset import build_delayed_revenue_dataset
from models.delayed_revenue_model import train_delayed_revenue_model


def backtest_rules_vs_ml(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Walk-forward backtest comparing:
    - Rules-only
    - Rules + ML blocker
    """

    weekly_df = aggregate_weekly(daily_df)
    weekly_df = weekly_df.sort_values(["channel", "week_start_date"]).reset_index(drop=True)

    results = []

    unique_weeks = weekly_df["week_start_date"].unique()

    for i in range(len(unique_weeks) - 2):
        current_week = unique_weeks[i]

        history_df = weekly_df[weekly_df["week_start_date"] <= current_week]
        future_df = weekly_df[weekly_df["week_start_date"] > current_week]

        # Skip if insufficient history
        ml_dataset = build_delayed_revenue_dataset(history_df)
        if ml_dataset.empty:
            continue

        model = train_delayed_revenue_model(ml_dataset)

        feature_df = ml_dataset.iloc[-len(ml_dataset["channel"].unique()):]
        predictions = model.predict(feature_df.drop(columns=["delayed_revenue"]))

        ml_predictions = pd.DataFrame({
            "channel": feature_df["channel"].values,
            "predicted_delayed_revenue": predictions
        })

        current_week_df = weekly_df[weekly_df["week_start_date"] == current_week]

        rules_out = apply_budget_rules(current_week_df)
        final_out = apply_ml_blocker(
            rules_out,
            current_week_df,
            ml_predictions
        )

        realized_future_revenue = (
            future_df.groupby("channel")["weekly_revenue"]
            .apply(lambda x: x.iloc[:2].sum())
            .reset_index(name="realized_delayed_revenue")
        )

        comparison = (
            final_out
            .merge(rules_out, on="channel", suffixes=("_ml", "_rules"))
            .merge(realized_future_revenue, on="channel", how="left")
        )

        comparison["week_start_date"] = current_week
        results.append(comparison)

    return pd.concat(results, ignore_index=True)
