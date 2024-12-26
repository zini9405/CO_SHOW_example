import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn

# 데이터 로드 및 전처리
file = 'transformed_df.csv'
df = pd.read_csv(file)

# 필요한 컬럼만 선택
df = df[['MAIN_RUNTIME', 'DD_USE_NUM', 'SLURRY_USE_NUM', 'PAD_COUNT', 'CARRIER_MTL_USE_NUM', 'GBIR']]
df = df[df['GBIR'] < 1.0]  # 'GBIR' 값이 1 미만인 데이터만 선택

# X, y 분리
X = df[['MAIN_RUNTIME', 'DD_USE_NUM', 'SLURRY_USE_NUM', 'PAD_COUNT', 'CARRIER_MTL_USE_NUM']].values
y = df['GBIR'].values

# 데이터 정규화
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Cross Validation 설정
kfold = KFold(n_splits=5, shuffle=True, random_state=1234)

# PyTorch HuberLoss 정의
criterion = nn.HuberLoss(delta=1.0)

# 사용자 정의 Huber 손실 함수 (scikit-learn 호환)
def huber_loss_scorer(estimator, X, y):
    y_pred = estimator.predict(X)
    y_pred_tensor = torch.tensor(y_pred, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)
    return -criterion(y_pred_tensor, y_tensor).item()  # 음수 반환 (scorer는 높은 점수를 선호)

huber_scorer = make_scorer(huber_loss_scorer, greater_is_better=False)

# 개별 모델 정의
models = {
    "XGBoost": XGBRegressor(n_estimators=500, learning_rate=0.01, max_depth=6, random_state=1234),
    "LightGBM": LGBMRegressor(n_estimators=500, learning_rate=0.01, max_depth=6, random_state=1234),
    "CatBoost": CatBoostRegressor(n_estimators=500, learning_rate=0.01, max_depth=6, random_state=1234, verbose=0),
    "RandomForest": RandomForestRegressor(n_estimators=500, max_depth=10, random_state=1234),
    "GradientBoosting": GradientBoostingRegressor(n_estimators=500, learning_rate=0.01, max_depth=6, random_state=1234),
}

# 각 모델에 대해 Cross Validation 수행
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=kfold, scoring=huber_scorer)
    print(f"{name} Cross-Val Huber Loss: {-scores.mean():.4f} (± {scores.std():.4f})")

# 개별 모델 학습 및 예측
trained_models = {name: model.fit(X, y) for name, model in models.items()}

# 앙상블 모델 구성 (Voting Regressor)
ensemble_model = VotingRegressor(estimators=[(name, model) for name, model in trained_models.items()])
ensemble_scores = cross_val_score(ensemble_model, X, y, cv=kfold, scoring=huber_scorer)
print(f"Ensemble Model Cross-Val Huber Loss: {-ensemble_scores.mean():.4f} (± {ensemble_scores.std():.4f})")

# 앙상블 모델 최종 학습
ensemble_model.fit(X, y)

# 예측 및 평가
y_pred = ensemble_model.predict(X)
y_pred_tensor = torch.tensor(y_pred, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.float32)
final_loss = criterion(y_pred_tensor, y_tensor)
print(f"Ensemble Model Final Huber Loss: {final_loss.item():.4f}")