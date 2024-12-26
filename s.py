import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import torch.nn as nn
import torch

# 데이터 로드 및 전처리
file = 'transformed_df.csv'
df = pd.read_csv(file)

# 필요한 컬럼만 선택
df = df[['MAIN_RUNTIME', 'DD_USE_NUM', 'SLURRY_USE_NUM', 'PAD_COUNT', 'CARRIER_MTL_USE_NUM', 'GBIR']]
df = df[df['GBIR'] < 1.0]  # 'GBIR' 값이 1 미만인 데이터만 선택

# X, y 분리
X = df[['MAIN_RUNTIME', 'DD_USE_NUM', 'SLURRY_USE_NUM', 'PAD_COUNT', 'CARRIER_MTL_USE_NUM']].values
y = df['GBIR'].values

# 데이터 스플릿 (80% 학습 데이터, 20% 테스트 데이터)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

# # 데이터 정규화
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

# XGBoost 모델
print("Training XGBoost Model...")
xgb_model = XGBRegressor(
    n_estimators=85, 
    learning_rate=0.05, 
    max_depth=20, 
    subsample=0.7, 
    colsample_bytree=1, 
    random_state=1234
)
xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=True)
criterion = nn.HuberLoss(delta=1.0)

# XGBoost 결과 평가
xgb_pred = xgb_model.predict(X_test)
xgb_pred_tensor = torch.tensor(xgb_pred, dtype= torch.float32)
y_test_tensor = torch.tensor(y_test, dtype= torch.float32)

xgb_r2 = r2_score(y_test, xgb_pred)
# xgb_rmse = mean_squared_error(y_test, xgb_pred, squared=False)

xgb_rmse = criterion(xgb_pred_tensor, y_test_tensor)
print(f"XGBoost R2 Score: {xgb_r2:.4f}")
print(f"XGBoost RMSE: {xgb_rmse:.4f}")

# # Random Forest 모델
# print("Training Random Forest Model...")
# rf_model = RandomForestRegressor(
#     n_estimators=500, 
#     max_depth=10, 
#     random_state=1234
# )
# rf_model.fit(X_train, y_train)

# # Random Forest 결과 평가
# rf_pred = rf_model.predict(X_test)
# rf_r2 = r2_score(y_test, rf_pred)
# rf_rmse = mean_squared_error(y_test, rf_pred, squared=False)
# print(f"Random Forest R2 Score: {rf_r2:.4f}")
# print(f"Random Forest RMSE: {rf_rmse:.4f}")
