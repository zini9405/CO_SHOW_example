# 사용자 정의 HuberLoss 스코어러 수정
def huber_loss_scorer(y_true, y_pred):
    y_pred_tensor = torch.tensor(y_pred, dtype=torch.float32)
    y_true_tensor = torch.tensor(y_true, dtype=torch.float32)
    criterion = nn.HuberLoss(delta=1.0)
    return criterion(y_pred_tensor, y_true_tensor).item()  # 양수 반환

# HuberLoss를 스코어러로 등록
huber_scorer = make_scorer(huber_loss_scorer, greater_is_better=False)

# Cross Validation 실행
print("Performing Cross Validation...")
cross_val_scores = cross_val_score(xgb_model, X, y, cv=kfold, scoring=huber_scorer)

# Cross Validation 결과 출력
print(f"Cross Validation Huber Loss (mean): {cross_val_scores.mean():.4f}")
print(f"Cross Validation Huber Loss (std): {cross_val_scores.std():.4f}")