import pandas as pd

# CSV 파일 로드
df = pd.read_csv("x.csv")

# 새로운 열을 계산하는 함수 (최댓값 사용)
def combine_columns(df, feature):
    cols = [f"LIFT_PIN{i}-{feature}" for i in range(1, 4)]
    if all(col in df.columns for col in cols):  # 모든 컬럼이 존재하는 경우에만 계산
        df[f"LIFT_PIN123-{feature}"] = df[cols].max(axis=1)

# 대상 열 목록
features = [
    "HEAD_DIA_3D", "BODY_DIA_3D", "TOTAL_LENGTH_3D", "HEAD_ROC_3D", "HEAD_ANGLE_3D",
    "HEAD_DIA", "BODY_DIA", "TOTAL_LENGTH", "HEAD_ROC", "HEAD_ANGLE"
]

# 새로운 열 생성
for feature in features:
    combine_columns(df, feature)

# 기존 LIFT_PIN1, LIFT_PIN2, LIFT_PIN3 관련 열 제거
columns_to_remove = [col for col in df.columns if col.startswith(("LIFT_PIN1-", "LIFT_PIN2-", "LIFT_PIN3-"))]
df.drop(columns=columns_to_remove, inplace=True)

# 새로운 CSV 파일 저장 (LIFT_PIN123-... 열만 남김)
df.to_csv("x_transformed.csv", index=False)
print("변환 완료: x_transformed.csv 저장됨")