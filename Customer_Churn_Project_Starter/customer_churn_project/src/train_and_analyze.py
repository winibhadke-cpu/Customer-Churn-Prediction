from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay, RocCurveDisplay, classification_report

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
REPORTS = ROOT / 'reports'
FIGURES = ROOT / 'figures'
for directory in [DATA, REPORTS, FIGURES]: directory.mkdir(exist_ok=True)
df = pd.read_csv(DATA / 'customer_churn_raw.csv')
print('Shape:', df.shape)
print('Missing by column:\n', df.isna().sum().sort_values(ascending=False))
print('Duplicate rows:', df.duplicated().sum())
print('Duplicate IDs:', df.CustomerID.duplicated().sum())
print('Churn distribution:\n', df.Churn.value_counts(dropna=False))
assert df.Churn.notna().all(), 'Missing target labels require investigation'
assert df.CustomerID.is_unique, 'Investigate duplicate customer identifiers'
assert set(df.Churn.unique()) == {'Yes','No'}, 'Unexpected target labels'

# Minimal, transparent cleaning; fit missing-value imputers on TRAINING data only.
df = df.drop_duplicates().copy()
for c in ['TotalCharges','MonthlyCharges','AvgMonthlyDataUsageGB','SatisfactionScore','DaysSinceLastContact']:
    df[c] = pd.to_numeric(df[c], errors='coerce')
assert df['TenureMonths'].dropna().ge(0).all()
assert df['MonthlyCharges'].dropna().ge(0).all()
assert df['SatisfactionScore'].dropna().between(1,5).all()
df['ChurnFlag'] = df.Churn.map({'No':0,'Yes':1})
# Export for SQL/Power BI, retaining missing cells rather than leaking imputation statistics.
df.to_csv(DATA / 'customer_churn_clean.csv', index=False)

plt.figure(figsize=(6,4));df['Churn'].value_counts().reindex(['No','Yes']).plot.bar();plt.title('Churn distribution');plt.tight_layout();plt.savefig(FIGURES/'churn_distribution.png',dpi=160);plt.close()
plt.figure(figsize=(8,4));df.groupby('ContractType')['ChurnFlag'].mean().plot.bar();plt.title('Churn rate by contract');plt.ylabel('Churn rate');plt.tight_layout();plt.savefig(FIGURES/'churn_by_contract.png',dpi=160);plt.close()

# Features known at prediction time only: validate event timestamps before real-world use.
X = df.drop(columns=['CustomerID','Churn','ChurnFlag'])
y = df.ChurnFlag.astype(int)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.20,random_state=42,stratify=y)
numeric = X_train.select_dtypes(include='number').columns.tolist()
categorical = X_train.select_dtypes(exclude='number').columns.tolist()
preprocessor = ColumnTransformer([
 ('num',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),numeric),
 ('cat',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore'))]),categorical)
])
models = {
 'Dummy baseline':DummyClassifier(strategy='most_frequent'),
 'Logistic Regression':LogisticRegression(max_iter=2000,class_weight='balanced',random_state=42),
 'Random Forest':RandomForestClassifier(n_estimators=250,min_samples_leaf=3,class_weight='balanced',random_state=42,n_jobs=-1)
}
try:
 from xgboost import XGBClassifier
 models['XGBoost'] = XGBClassifier(n_estimators=250,max_depth=4,learning_rate=.05,subsample=.9,colsample_bytree=.9,eval_metric='logloss',random_state=42,n_jobs=2)
except ImportError:
 print('Optional XGBoost unavailable: pip install xgboost')
cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=42)
results=[]; fitted={}
for name,estimator in models.items():
 pipeline=Pipeline([('prep',preprocessor),('model',estimator)])
 scores=cross_validate(pipeline,X_train,y_train,cv=cv,scoring={'f1':'f1','roc_auc':'roc_auc','recall':'recall','precision':'precision'},n_jobs=1,zero_division=0) if False else cross_validate(pipeline,X_train,y_train,cv=cv,scoring={'f1':'f1','roc_auc':'roc_auc','recall':'recall','precision':'precision'},n_jobs=1)
 pipeline.fit(X_train,y_train)
 pred=pipeline.predict(X_test)
 prob=pipeline.predict_proba(X_test)[:,1]
 row={'Model':name,'CV_F1':np.mean(scores['test_f1']),'CV_ROC_AUC':np.mean(scores['test_roc_auc']),'Accuracy':accuracy_score(y_test,pred),'Precision':precision_score(y_test,pred,zero_division=0),'Recall':recall_score(y_test,pred,zero_division=0),'F1':f1_score(y_test,pred,zero_division=0),'ROC_AUC':roc_auc_score(y_test,prob)}
 results.append(row);fitted[name]=(pipeline,pred,prob)
 print(name,classification_report(y_test,pred,zero_division=0))
results_df=pd.DataFrame(results).sort_values('CV_ROC_AUC',ascending=False)
results_df.to_csv(REPORTS/'model_comparison.csv',index=False)
print(results_df.to_string(index=False))
# Choose using TRAINING cross-validation, not test scores.
best_name=results_df.iloc[0]['Model'];best,pred,prob=fitted[best_name]
ConfusionMatrixDisplay.from_predictions(y_test,pred,display_labels=['Retained','Churn']);plt.title(best_name);plt.tight_layout();plt.savefig(FIGURES/'confusion_matrix.png',dpi=160);plt.close()
RocCurveDisplay.from_predictions(y_test,prob);plt.title(best_name);plt.tight_layout();plt.savefig(FIGURES/'roc_curve.png',dpi=160);plt.close()
scored=df.loc[X_test.index,['CustomerID','Churn']].copy();scored['ChurnProbability']=prob;scored['PredictedChurn'] = np.where(pred==1,'Yes','No');scored.to_csv(REPORTS/'holdout_customer_risk_scores.csv',index=False)
# Model-agnostic permutation importance on untouched test data, for interpretation only.
from sklearn.inspection import permutation_importance
importance=permutation_importance(best,X_test,y_test,n_repeats=5,random_state=42,scoring='roc_auc',n_jobs=1)
pd.DataFrame({'Feature':X_test.columns,'ImportanceMean':importance.importances_mean,'ImportanceStd':importance.importances_std}).sort_values('ImportanceMean',ascending=False).to_csv(REPORTS/'feature_importance.csv',index=False)
import joblib
joblib.dump(best,ROOT/'models/churn_pipeline.joblib')
print('Selected by training CV ROC-AUC:',best_name)
