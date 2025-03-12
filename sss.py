import pandas as pd

# 파일 로드
file_path = "X.csv"
df = pd.read_csv(file_path)

# 빈값 처리: 각 열에서 빈값을 평균으로 채우고, 빈값만 있는 경우 0으로 채움
for col in df.columns:
    if df[col].isna().all():
        df[col] = 0  # 모든 값이 NaN이면 0으로 채움
    else:
        df[col] = df[col].fillna(df[col].mean())  # NaN을 평균값으로 채움

# SFQR_AFS2 - SFQR_AFS2_SUB 값 계산하여 새로운 열 추가
df["SFQR"] = df["SFQR_AFS2"] - df["SFQR_AFS2_SUB"]

# 제거할 열 목록
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

# 열 제거
df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors="ignore")

# 결과 저장
df.to_csv("processed_X.csv", index=False)

# 처리 완료 메시지 출력
print("데이터 처리 완료! 결과 파일: processed_X.csv")