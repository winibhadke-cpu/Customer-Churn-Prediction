# Telecom Customer Churn Prediction — Project Report (Draft)

## Executive summary
This educational project analyzes 8,000 synthetic telecom customer records and builds a binary classifier to predict customer churn. The source workbook reports 1,440 churners (18%) and 6,560 retained customers. Results and recommendations must be completed after running the analysis.

## Business problem
Customer attrition can reduce recurring revenue. The goal is to understand associated service and contract factors and rank customers by churn risk.

## Data and methods
Source: institute-provided synthetic dataset (27 columns). Target: Churn (Yes/No). The workflow includes validation, EDA, SQL KPIs, dashboarding, and a stratified 80/20 holdout evaluation. Preprocessing is fitted within cross-validation pipelines.

## Models and evaluation
Compare DummyClassifier, Logistic Regression, Random Forest, and optional XGBoost. Select using five-fold training ROC-AUC, then report holdout accuracy, precision, recall, F1, ROC-AUC, confusion matrix and model explanations. Do not claim model performance before running code.

## Limitations and safeguards
The dataset is synthetic. Associations are not causal. Verify feature timestamps and prevent data leakage before real deployment. Consider fairness review for demographic attributes. Probability calibration, validation-based threshold selection, monitoring and cost-based decisions are recommended future work.

## Results, recommendations and conclusion
TO COMPLETE: Insert charts, tested model metrics, top features, SQL findings, dashboard screenshots, customer-risk recommendations, limitations and citations after executing the pipeline.
