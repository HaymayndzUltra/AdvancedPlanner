# Baseline Model: Purchase Propensity (7-day)

- Problem: Binary classification (purchase within 7 days of session start)
- Label: Any `warehouse.fact_transactions.status in {captured, settled}` within 7 days
- Features:
  - user_country_code (categorical)
  - session_events_7d (integer)
  - total_spend_30d (decimal)
- Model: Logistic Regression (scikit-learn) or XGBoost baseline
- Evaluation: Train/validation split by event_date; metrics AUC-ROC, PR-AUC
- Bias & Fairness: Monitor by country and device_type segments
- Drift: PSI for features monthly; label rate drift weekly
- Reproducibility: Fixed random seed; versioned dataset snapshots