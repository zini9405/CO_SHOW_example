import pandas as pd
import numpy as np

# CSV 파일 로드
df = pd.read_csv("x.csv")

# 결측값을 채우는 함수 정의
def fill_missing_values(series):
    values = series.values.copy()

    for i in range(len(values)):
        if pd.isna(values[i]):
            # 이전 값 찾기
            prev_idx = i - 1
            while prev_idx >= 0 and pd.isna(values[prev_idx]):
                prev_idx -= 1

            # 다음 값 찾기
            next_idx = i + 1
            while next_idx < len(values) and pd.isna(values[next_idx]):
                next_idx += 1

            # 이전과 다음 값이 모두 존재하면 평균으로
            if prev_idx >= 0 and next_idx < len(values) and not pd.isna(values[next_idx]):
                values[i] = (values[prev_idx] + values[next_idx]) / 2
            else:
                # 둘 중 하나라도 없으면 전체 평균값으로 채움
                mean_value = np.nanmean(values)
                values[i] = mean_value

    return pd.Series(values, index=series.index)

# 그룹화하고 결측값 채우기
def fill_group(group):
    for col in group.columns:
        if group[col].isnull().any() and col not in ['ANALYSIS_GROUP', 'EQP_NM']:
            group[col] = fill_missing_values(group[col])
    return group

# 그룹별 적용
df_filled = df.groupby(['ANALYSIS_GROUP', 'EQP_NM'], group_keys=False).apply(fill_group)

# 결과 저장
df_filled.to_csv("x_filled.csv", index=False)