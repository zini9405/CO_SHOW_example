import pandas as pd

# CSV 파일 로드
df = pd.read_csv("x.csv")

### 1. SUS_SUP_SHAFT- & WAFER_LIFT_SHAFT- → WAVY_SUSCEP- 변환 ###
def combine_shaft_columns(df, feature):
    cols = [f"SUS_SUP_SHAFT-{feature}", f"WAFER_LIFT_SHAFT-{feature}"]
    existing_cols = [col for col in cols if col in df.columns]  # 존재하는 열만 선택
    if existing_cols:
        df[f"WAVY_SUSCEP-{feature}"] = df[existing_cols].max(axis=1)  # 최댓값 적용

# 변환할 열 목록
shaft_features = [
    "ARM_LEN_B", "ARM_LEN_L", "ARM_LEN_R", "ARM_ANGL_B", "ARM_ANGL_L", "ARM_ANGL_R",
    "FLAT_A", "FLAT_B", "FLAT_L", "FLAT_R"
]

for feature in shaft_features:
    combine_shaft_columns(df, feature)

# 기존 SUS_SUP_SHAFT- 및 WAFER_LIFT_SHAFT- 열 삭제
shaft_columns_to_remove = [col for col in df.columns if col.startswith(("SUS_SUP_SHAFT-", "WAFER_LIFT_SHAFT-"))]
df.drop(columns=shaft_columns_to_remove, inplace=True)

### 2. WAVY_SUSCEP- & HOLED_SUSCEP- → SUSCEP- 변환 (최댓값 적용) ###
def combine_suscep_columns(df, feature):
    cols = [f"WAVY_SUSCEP-{feature}", f"HOLED_SUSCEP-{feature}"]
    existing_cols = [col for col in cols if col in df.columns]  # 존재하는 열만 선택
    if existing_cols:
        df[f"SUSCEP-{feature}"] = df[existing_cols].max(axis=1)  # 최댓값 적용

# 변환할 열 목록
suscep_features = [
    "SUSCEPTOR_D_3D", "CENTER_TO_P0_3D", "CENTER_TO_P110_3D", "CENTER_TO_P100_3D",
    "POCKET_HEIGHT_3D", "LEDGE_HEIGHT_3D", "LEDGE_DISTANCE110_3D", "LEDGE_DISTANCE100_3D",
    "LEDGE_FLATNESS_3D", "LEDGE_ANGLE_3D", "INNER_DEPTH_AVG_3D", "INNER_DEPTH_RANGE_3D",
    "C_TO_LEDGE_D_3D", "CONCAVE_TO_ID_3D"
]

for feature in suscep_features:
    combine_suscep_columns(df, feature)

# 기존 WAVY_SUSCEP- 및 HOLED_SUSCEP- 열 삭제
suscep_columns_to_remove = [col for col in df.columns if col.startswith(("WAVY_SUSCEP-", "HOLED_SUSCEP-"))]
df.drop(columns=suscep_columns_to_remove, inplace=True)

# 새로운 CSV 파일 저장
df.to_csv("x_transformed.csv", index=False)
print("변환 완료: x_transformed.csv 저장됨")