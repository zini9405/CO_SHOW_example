import pandas as pd

# 예제 데이터 (초 정보가 없는 데이터 포함)
data = {
    'HST_REG_DTTM': [
        '2024-01-01 07:00:04', 
        '2025-03-16 5:30', 
        '2025-03-16 05:30', 
        '2025-03-16 05:30:00', 
        '2025-03-16 12:45',
        '2023-12-31 23:59'
    ]
}
renewal = pd.DataFrame(data)

# HST_REG_DTTM을 문자열에서 datetime 형식으로 변환 (초 정보가 없으면 NaT 방지)
renewal['HST_REG_DTTM'] = renewal['HST_REG_DTTM'].astype(str)

# 초 정보가 없는 경우를 찾아 "00초"를 추가
renewal['HST_REG_DTTM'] = renewal['HST_REG_DTTM'].apply(
    lambda x: x + ':00' if len(x.split(':')) == 2 else x
)

# 다시 datetime 형식으로 변환
renewal['HST_REG_DTTM'] = pd.to_datetime(renewal['HST_REG_DTTM'], errors='coerce')

# 결과 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="Updated Renewal Data", dataframe=renewal)