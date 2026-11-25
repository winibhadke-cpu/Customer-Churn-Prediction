# Telecom Customer Churn Prediction — Analytics + ML

Institute-provided **synthetic** dataset, 8,000 customers, 27 columns; target `Churn`. This repository covers data profiling, cleaning, SQL, EDA, Power BI instructions, classification and explainability.

## Quick start
```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/train_and_analyze.py
jupyter notebook notebooks/01_churn_analysis.ipynb
```
Run from project root. Outputs: `data/customer_churn_clean.csv`, `figures/*.png`, `reports/model_comparison.csv`, `reports/feature_importance.csv`, `reports/holdout_customer_risk_scores.csv`, `models/churn_pipeline.joblib`.

## Data leakage and ethics
CustomerID is excluded. Train/test split is stratified. Imputation, scaling, and encoding occur inside training-fold pipelines. Do not use information only available after churn. Audit demographic feature fairness. Dataset is synthetic; no causal or real-world performance claims.

## Structure
- `data/`: raw and cleaned CSV, data dictionary
- `notebooks/`: walkthrough notebook
- `src/`: reproducible modeling and EDA script
- `sql/`: MySQL schema, KPI queries, CTEs, view, joins, window functions
- `powerbi/`: dashboard/DAX implementation guide
- `reports/`: draft report and generated model results
- `figures/`: generated visualizations
- `models/`: trained pipeline after execution

## Submission
Create Power BI `.pbix` in Desktop. Finalize institute report (up to 10 pages) and slides (5–7) after metrics and dashboard are validated. Do not upload sensitive customer data to public GitHub without permission (this source is synthetic).
