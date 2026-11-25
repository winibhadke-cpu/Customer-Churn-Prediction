# Power BI dashboard build guide
Import `data/customer_churn_clean.csv` using Get Data > Text/CSV. Set ChurnFlag to whole number.

## DAX measures
```dax
Customers = DISTINCTCOUNT(customer_churn_clean[CustomerID])
Churned Customers = CALCULATE([Customers], customer_churn_clean[ChurnFlag] = 1)
Churn Rate = DIVIDE([Churned Customers], [Customers])
Average Monthly Charges = AVERAGE(customer_churn_clean[MonthlyCharges])
Average Tenure = AVERAGE(customer_churn_clean[TenureMonths])
```
Adjust table name to the actual imported Power BI table. Format Churn Rate as percentage.

## Pages
1. Executive overview: KPI cards, churn by contract, tenure and internet service; slicers for contract, payment method, internet service.
2. Drivers: churn by satisfaction, support calls, monthly charges and complaints; drill-through on ContractType.
3. ML results: import reports/model_comparison.csv and reports/holdout_customer_risk_scores.csv after running Python; show model metrics and customer risk distributions.

A `.pbix` file must be created and saved in Power BI Desktop; this guide is not a PBIX file.
