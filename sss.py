import datetime

# 년, 월, 일만 추출
df_Y['HST_REG_DTTM'] = df_Y['HST_REG_DTTM'].map(
    lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').date()
)