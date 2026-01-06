# Marketing Spend Optimization System — Assumptions

## 1. Business Assumptions

- The decision owner is a Marketing Manager responsible for weekly budget allocation.
- A fixed total marketing budget of ₹5,00,000 is allocated every week.
- Budget decisions are made once per week and apply to the following week.
- Budget allocation decisions are advisory; execution is manual and outside the system.

## 2. Marketing Channels

The system supports the following channels only:
- Google Ads
- Meta Ads
- Email
- Affiliate

No additional channels are considered unless explicitly added in future versions.

## 3. Attribution Model

- All revenue is attributed using a last-click attribution model.
- Revenue is fully assigned to the channel that generated the final customer interaction.
- Multi-touch or fractional attribution is explicitly out of scope.

## 4. Data Granularity and Time Window

- Raw marketing data is assumed to be available at a daily granularity.
- All decisions are made using weekly aggregated data.
- A week is defined as Monday to Sunday.

## 5. Rule-Based Decision System (Baseline)

- Rule-based logic is the authoritative decision mechanism.
- Rules enforce:
  - Loss protection
  - Stability rewards
  - Volatility control
  - Channel-level budget caps
  - Total budget conservation
- Rule outputs must always sum to ₹5,00,000.
- Rule-based decisions are explainable and deterministic.

## 6. Machine Learning Usage (Future Phase)

- Machine Learning is not used in Phase 1.
- In Phase 2, ML is used only to estimate delayed revenue effects.
- Delayed revenue is defined as revenue realized in weeks t+1 and t+2.
- ML models do not allocate budgets and do not override rules.
- ML outputs can only prevent premature budget reductions.

## 7. Explicit Non-Goals

- No real-time budget optimization.
- No automated media buying.
- No reinforcement learning or black-box optimizers.
- No ROI maximization without constraints.

## 8. Failure Handling

- If ML outputs are unavailable or unreliable, the system defaults fully to rule-based decisions.
- Rule-based decisions must always produce a valid weekly recommendation.

