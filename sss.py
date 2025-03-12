import pandas as pd

# 파일 로드
file_path = "X.csv"
df = pd.read_csv(file_path)

# 문자열 컬럼 목록
text_columns = ['ANALYSIS_GROUP', 'SUBLOT', 'WAFER_ID', 'EQP_NM', 'DATE']

# 숫자형 컬럼만 선택 (제거할 컬럼 제외)
columns_to_remove = [
    "ESFQD_ZONE1MEAN_AFS2", "ESFQD2_ZONE1MEAN_AFS2", "ESFQR2_ZONE1MAX_AFS2", 
    "MEANSFQRFULLSITESONLY_AFS2", "MAXSFQRFULLSITESONLY_AFS2", "GBIR_AFS2", "SFQR_AFS2",
    "ZDDFRONTMEAN_01_AFS2", "ZDDFRONTMEAN_05_AFS2", "ZDDBACKMEAN_01_AFS2", "ZDDBACKMEAN_05_AFS2", 
    "WARP_BF_AFS2", "BOW_BF_AFS2", "NANO_THA2_AFS2", "NANO_THA4_AFS2", "SITE_NT_PARTMAX_AFS2", 
    "DELTA_MEAN_SFQR_FULLSITE", "DELTA_MAX_SFQR_FULLSITE", "Delta_ESFQD2", "Delta_SFQR", "Delta_GBIR", 
    "Delta_ZDD", "DELTA_SITE_NT", "DELTA_WARP_BF_AFS2", "DELTA_BOW_BF_AFS2", "ESFQD_ZONE1MEAN_AFS2_SUB", 
    "ESFQD2_ZONE1MEAN_AFS2_SUB", "MAXSFQRFULLSITESONLY_AFS2_SUB", "MEANSFQRFULLSITESONLY_AFS2_SUB", 
    "NANO_THA2_AFS2_SUB", "NANO_THA4_AFS2_SUB", "GBIR_AFS2_SUB", "SFQR_AFS2_SUB", "BOW_BF_AFS2_SUB", 
    "WARP_BF_AFS2_SUB", "ZDDBACKMEAN_01_AFS2_SUB", "ZDDBACKMEAN_05_AFS2_SUB", "ZDDFRONTMEAN_01_AFS2_SUB", 
    "ZDDFRONTMEAN_05_AFS2_SUB", "SITE_NT_PARTMAX_AFS2_SUB"
]

# 1️⃣ **문자열 컬럼 결측치 처리 (NaN → "Unknown")**
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")  

# 2️⃣ **숫자형 컬럼만 선택하여 EQP_NM별 평균 계산**
numeric_columns = [col for col in df.columns if col not in text_columns and col not in columns_to_remove]

# EQP_NM 그룹별 평균값으로 결측치 채움
df[numeric_columns] = df.groupby("EQP_NM")[numeric_columns].transform(lambda x: x.fillna(x.mean()))

# **모든 값이 NaN이었던 경우 0으로 채우기**
df[numeric_columns] = df[numeric_columns].fillna(0)

# 3️⃣ **SFQR_AFS2 - SFQR_AFS2_SUB 값 계산하여 새로운 열 추가**
if "SFQR_AFS2" in df.columns and "SFQR_AFS2_SUB" in df.columns:
    df["SFQR"] = df["SFQR_AFS2"] - df["SFQR_AFS2_SUB"]

# 4️⃣ **불필요한 열 제거**
df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors="ignore")

# 5️⃣ **최종 데이터 저장**
df.to_csv("processed_X_grouped.csv", index=False)

# 완료 메시지 출력
print("EQP_NM 기준으로 그룹화 후 데이터 처리 완료! 결과 파일: processed_X_grouped.csv")