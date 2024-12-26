import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, make_scorer
from sklearn.model_selection import train_test_split, cross_val_score, KFold
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

# XGBoost 모델
xgb_model = XGBRegressor(
    n_estimators=85,
    learning_rate=0.05,
    max_depth=20,
    subsample=0.7,
    colsample_bytree=1,
    random_state=1234
)

# PyTorch HuberLoss 정의
criterion = nn.HuberLoss(delta=1.0)

# 사용자 정의 HuberLoss 스코어러
def huber_loss_scorer(estimator, X, y):
    y_pred = estimator.predict(X)
    y_pred_tensor = torch.tensor(y_pred, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)
    return -criterion(y_pred_tensor, y_tensor).item()  # 음수 반환 (scorer는 높은 점수를 선호)

# HuberLoss를 스코어러로 등록
huber_scorer = make_scorer(huber_loss_scorer, greater_is_better=False)

# Cross Validation 설정
kfold = KFold(n_splits=5, shuffle=True, random_state=1234)

# Cross Validation 실행
print("Performing Cross Validation...")
cross_val_scores = cross_val_score(xgb_model, X, y, cv=kfold, scoring=huber_scorer)

# Cross Validation 결과 출력
print(f"Cross Validation Huber Loss (mean): {-cross_val_scores.mean():.4f}")
print(f"Cross Validation Huber Loss (std): {cross_val_scores.std():.4f}")

# XGBoost 학습
print("Training XGBoost Model...")
xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=True)

# XGBoost 결과 평가
xgb_pred = xgb_model.predict(X_test)
xgb_pred_tensor = torch.tensor(xgb_pred, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

xgb_r2 = r2_score(y_test, xgb_pred)
xgb_rmse = criterion(xgb_pred_tensor, y_test_tensor)
print(f"XGBoost R2 Score: {xgb_r2:.4f}")
print(f"XGBoost Huber Loss: {xgb_rmse:.4f}")