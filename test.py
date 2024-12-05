csv 파일에 HST_REG_DTTM 열으 시간을 나타내는 값이 있어.
예) 20240101070004090000 -> 2024-01-01 07:00:04 
예)처럼 변경주는 코드 구현


import pandas as pd

# 예시 데이터프레임 생성
data = {'HST_REG_DTTM': ['20240101070004090000', '20240202080005090000']}
df = pd.DataFrame(data)

# 변환 함수 정의
def format_hst_reg_dttm(value):
    return f"{value[:4]}-{value[4:6]}-{value[6:8]} {value[8:10]}:{value[10:12]}:{value[12:14]}"

# HST_REG_DTTM 열 변환
df['HST_REG_DTTM'] = df['HST_REG_DTTM'].apply(format_hst_reg_dttm)

# 결과 출력
print(df)