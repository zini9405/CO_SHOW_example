import numpy as np

# y_min과 y_max 계산
y_min = df_warp['ZDDFRONTMEAN_01_AFS2'].min()
y_max = df_warp['ZDDFRONTMEAN_01_AFS2'].max()

# NaN, inf 체크 후 기본값 설정
if np.isnan(y_min) or np.isnan(y_max) or np.isinf(y_min) or np.isinf(y_max):
    print("⚠️ Warning: y_min or y_max is NaN/Inf. Assigning default values.")
    y_min, y_max = 0, 1  # 기본값 설정

# 데이터 출력 (디버깅)
print(f"✅ y_min: {y_min}, y_max: {y_max}")

chart = alt.Chart(df_warp).mark_bar(color='#E1002A').encode(
    x=alt.X('EQP_ID_MODULE_NAME', title=None, sort='-y'),
    y=alt.Y('ZDDFRONTMEAN_01_AFS2', title='ZDD', scale=alt.Scale(domain=[y_min, y_max], clamp=False))
)

# JSON 변환 후 검사
json_data = chart.to_json()
print("Generated JSON Data:")
print(json_data)  # JSON이 정상적으로 생성되는지 확인

# Streamlit 차트 출력
st.altair_chart(chart, use_container_width=True)