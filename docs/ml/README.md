# ML Plan

- Objective: Predict probability of purchase within 7 days using session events and user attributes.
- Baseline: Logistic regression with minimal features (event counts, recency, country).
- Datasets: `warehouse.dim_users`, `warehouse.fact_session_events`, `warehouse.fact_transactions`.
- Evaluation: AUC-ROC, PR-AUC; baseline target AUC >= 0.70.
- Drift Monitoring: Population stability index (PSI) monthly; label shift via transactions rate.
- Privacy: Use masked PII only; no raw PAN or IPs.