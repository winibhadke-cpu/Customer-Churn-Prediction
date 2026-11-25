CREATE DATABASE IF NOT EXISTS telecom_churn;
USE telecom_churn;
-- Import data/customer_churn_clean.csv via MySQL Workbench Table Data Import Wizard.
-- Preserve blank fields as NULL; ChurnFlag must be 0 or 1.
CREATE TABLE IF NOT EXISTS customers (
  `CustomerID` VARCHAR(80) PRIMARY KEY,
  `Gender` VARCHAR(80),
  `SeniorCitizen` INT,
  `Partner` VARCHAR(80),
  `Dependents` VARCHAR(80),
  `TenureMonths` INT,
  `PhoneService` VARCHAR(80),
  `MultipleLines` VARCHAR(80),
  `InternetService` VARCHAR(80),
  `OnlineSecurity` VARCHAR(80),
  `OnlineBackup` VARCHAR(80),
  `DeviceProtection` VARCHAR(80),
  `TechSupport` VARCHAR(80),
  `StreamingTV` VARCHAR(80),
  `StreamingMovies` VARCHAR(80),
  `ContractType` VARCHAR(80),
  `PaperlessBilling` VARCHAR(80),
  `PaymentMethod` VARCHAR(80),
  `MonthlyCharges` DECIMAL(12,2),
  `TotalCharges` DECIMAL(12,2),
  `SupportCallsLast90Days` INT,
  `ComplaintRaised` VARCHAR(80),
  `AvgMonthlyDataUsageGB` DECIMAL(12,2),
  `AvgMonthlyCalls` INT,
  `SatisfactionScore` INT,
  `DaysSinceLastContact` INT,
  `Churn` VARCHAR(80),
  ChurnFlag TINYINT NOT NULL
);

select * from customers;

-- KPI queries
SELECT COUNT(*) AS Customers, ROUND(AVG(ChurnFlag)*100,2) AS ChurnRatePct FROM customers;
SELECT ContractType,COUNT(*) AS Customers,ROUND(AVG(ChurnFlag)*100,2) AS ChurnRatePct FROM customers GROUP BY ContractType ORDER BY ChurnRatePct DESC;
SELECT InternetService,COUNT(*) AS Customers,ROUND(AVG(ChurnFlag)*100,2) AS ChurnRatePct FROM customers GROUP BY InternetService;
-- CTE and window ranking
WITH contract_rates AS (SELECT ContractType, COUNT(*) AS CustomerCount, AVG(ChurnFlag) AS ChurnRate FROM customers GROUP BY ContractType) SELECT *,DENSE_RANK() OVER (ORDER BY ChurnRate DESC) AS RiskRank FROM contract_rates;
-- View for Power BI
CREATE OR REPLACE VIEW vw_churn_dashboard AS SELECT CustomerID,ContractType,InternetService,PaymentMethod,TenureMonths,MonthlyCharges,SupportCallsLast90Days,SatisfactionScore,ChurnFlag FROM customers;
-- Join example using a derived contract summary table
SELECT c.CustomerID,c.ContractType,c.ChurnFlag,r.ContractChurnRate FROM customers c JOIN (SELECT ContractType,ROUND(AVG(ChurnFlag)*100,2) AS ContractChurnRate FROM customers GROUP BY ContractType) r ON c.ContractType=r.ContractType LIMIT 25;
