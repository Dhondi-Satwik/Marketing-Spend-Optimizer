Marketing Spend Decision System

Rules-First, ML-Advised, Production-Style Analytics Project

Overview

This project implements a real-world marketing budget decision system designed the way enterprise analytics platforms are actually built.
It allocates a fixed weekly marketing budget across multiple channels using deterministic business rules, with Machine Learning used only as a controlled advisory layer.

This is not an academic ML project.
This is a decision-support system.

Business Problem

Marketing teams spend significant budgets across channels (Google Ads, Meta Ads, Email, Affiliate) but face:

Unclear ROI at the channel level

Overreaction to short-term performance

Risk of cutting channels with delayed revenue impact

Low trust in black-box ML recommendations

Objective:
Build a system that produces explainable, auditable, weekly budget recommendations while controlling risk and volatility.

Key Constraints (Business-Locked)

Weekly decision cadence

Fixed total weekly budget: ₹5,00,000

Maximum 40% cap per channel

Decisions must be explainable to non-technical stakeholders

ML must never directly allocate money

System Philosophy

Rules own decisions

ML is advisory only

Explainability > accuracy

Failure-safe > optimization

Schema contracts enforced at every stage

This mirrors real enterprise decision systems.

High-Level Architecture
Raw Daily Data
   ↓
Validation Layer (schema enforcement)
   ↓
Weekly Aggregation + KPI Engine
   ↓
Rule-Based Budget Allocation
   ↓
ML Advisory Blocker (delayed revenue protection)
   ↓
Final Weekly Budget Output (CSV)

Repository Structure
marketing-spend-decision-system/
│
├── data/
│   └── raw/marketing_daily.csv
│
├── pipelines/
│   ├── validate.py
│   ├── transform.py
│   └── run_weekly_decision.py
│
├── decision_rules/
│   ├── budget_rules.py
│   └── ml_blocker.py
│
├── models/
│   ├── delayed_revenue_dataset.py
│   └── delayed_revenue_model.py
│
├── docs/
│   └── schema.py
│
├── outputs/
│   └── weekly_recommendations.csv
│
└── README.md

Core Logic
1. Rule-Based Budget Engine (Primary)

Filters channels with positive ROI

Allocates budget proportional to ROI

Enforces channel caps

Guarantees full budget utilization

Fully deterministic and auditable

2. ML Advisory Layer (Guardrail Only)

Predicts delayed revenue using future revenue signals

Uses interpretable linear regression

Can only block premature budget cuts

Cannot increase or reallocate budgets

This ensures ML adds safety, not volatility.

Output (Business Artifact)

The system produces a file consumed directly by a Marketing Manager:

week_start_date,channel,final_budget
2025-01-06,Google Ads,178000
2025-01-06,Email,142000
2025-01-06,Meta Ads,100000
2025-01-06,Affiliate,80000

Technologies Used

Python

Pandas, NumPy

Scikit-learn (Linear Regression)

Deterministic rule engines

Schema-based data validation

What This Project Demonstrates

Business-first analytics thinking

Production-style pipeline design

Safe ML integration

Governance and explainability

End-to-end operational execution

Status

Complete. End-to-end runnable. Production-aligned.
