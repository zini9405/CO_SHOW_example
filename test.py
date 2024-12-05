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


나는 WAF_ID열을 묶어서 STEP_ID열을 0부터 13까지 값이 있을거야. 단, 0부터 13까지 중 없는 숫자가 있으면
EQP_ID	MODULE_NAME	WAF_ID RECIPE_ID STEP_ID STEP_NAME HST_REG_DTTM 빼고 나머지 열의 값은 -1로 채워줘.
그리고 묶은 WAF_ID을 다시 하나의 WAF_ID로 만들어줘.

그리고 -1로 채운 값은 모델에 입력으로 사용할때 학습 안되면 좋겠는데 어뜨케하면 좋을까?

