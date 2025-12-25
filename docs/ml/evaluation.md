# Evaluation Protocol

- Data Split: Time-based split, train on T-60..T-14, validate on T-13..T-7
- Metrics: AUC-ROC primary, PR-AUC secondary; calibration via Brier score
- Baseline: AUC >= 0.70; track std dev across 3 seeds
- Reporting: Save metrics to `docs/ml/reports/` per run with timestamp and git SHA