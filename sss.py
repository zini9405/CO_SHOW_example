import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import datetime

# Streamlit 페이지 설정
st.set_page_config(
    page_title="EQP X 값 비교",
    page_icon="📊",
    layout="wide"
)

# Streamlit UI 제목
st.title("📊 EQP_1 vs EQP_2 - X 값 비교")

# 날짜 선택
start_date = st.sidebar.date_input("Start date", datetime.date.today() - datetime.timedelta(days=60))
end_date = st.sidebar.date_input("End date", datetime.date.today())

# 데이터 가져오기 (예제 데이터)
df_eqp = st.session_state['df_Y'][(st.session_state['df_Y'].HST_REG_DTTM.between(start_date, end_date, inclusive='both'))]

# 비교할 EQP_ID 선택
eqp_1 = st.sidebar.selectbox("Select EQP_1", df_eqp['EQP_ID_MODULE_NAME'].unique())
eqp_2 = st.sidebar.selectbox("Select EQP_2", df_eqp['EQP_ID_MODULE_NAME'].unique())

# 비교할 X 값 선택 (사용자가 선택 가능)
x_columns = [
    'AVG_ROTATION_SPEED_AT_CH_MOTIONCTRL_ROTATION_RVEL_STEP_MEAN',
    'BLOWER_AIR_BOTTOM_PRESSURE_BOTTOM_AT_CHA_STEP_MEAN',
    'BLOWER_AIR_PRESSURE_AT_CHA_STEP_MEAN',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK01_MFC_RFLOW_STEP_MEAN',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK02_MFC_RFLOW_STEP_MEAN',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK03_MFC_RFLOW_STEP_MEAN',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK04_MFC_RFLOW_STEP_MEAN',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK05_MFC_RFLOW_STEP_MEAN',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK06_MFC_RFLOW_STEP_MEAN',
    'LIFT_TORQUE_AT_CHA_MOTIONCTRL_LIFT_RTORQUE_STEP_MEAN',
    'PRESSURE_AT_BUFFER_VACSYS_PRESSGAUGE_RPRESSURE_STEP_MEAN',
    'PRESSURE_AT_CH_MAN1000T_RPRESSURE_STEP_MEAN',
    'SCR_POWER_AT_CH_TEMPCTRL_HEATER_TOP_INNER_RPOWER_STEP_MEAN',
    'SCR_POWER_AT_CH_TEMPCTRL_HEATER_TOP_OUTER_RPOWER_STEP_MEAN',
    'SCR_POWER_AT_CH_TEMPCTRL_HEATER_BOTTOM_INNER_RPOWER_STEP_MEAN',
    'SCR_POWER_AT_CH_TEMPCTRL_HEATER_BOTTOM_OUTER_RPOWER_STEP_MEAN',
    'TEMPERATURE_READING_AT_CH_TEMPCTRL_HEATER_BOTTOM_PYROMETER_RTEMP_STEP_MEAN',
    'TEMPERATURE_READING_AT_CH_TEMPCTRL_HEATER_EDGE_PYROMETER_RTEMP_STEP_MEAN',
    'TEMPERATURE_READING_AT_CH_TEMPCTRL_HEATER_TOP_PYROMETER_RTEMP_STEP_MEAN'
]

selected_x = st.sidebar.selectbox("비교할 X 값 선택", x_columns)

# EQP_1, EQP_2 데이터 필터링
df_eqp1 = df_eqp[df_eqp.EQP_ID_MODULE_NAME == eqp_1].groupby("HST_REG_DTTM")[selected_x].mean().reset_index()
df_eqp1["EQP"] = eqp_1

df_eqp2 = df_eqp[df_eqp.EQP_ID_MODULE_NAME == eqp_2].groupby("HST_REG_DTTM")[selected_x].mean().reset_index()
df_eqp2["EQP"] = eqp_2

# EQP_1, EQP_2 데이터 합치기
df_combined = pd.concat([df_eqp1, df_eqp2])

# 날짜 형식 변환 (YYYY-MM-DD)
df_combined['HST_REG_DTTM'] = pd.to_datetime(df_combined['HST_REG_DTTM']).dt.strftime('%Y-%m-%d')

# Altair 차트 생성
chart = alt.Chart(df_combined).mark_line(point=True).encode(
    x=alt.X('HST_REG_DTTM:T', axis=alt.Axis(format='%Y-%m-%d', labelAngle=45), title="날짜"),
    y=alt.Y(f"{selected_x}:Q", title="X 값"),
    color=alt.Color('EQP:N', title="EQP ID"),
    tooltip=['HST_REG_DTTM', 'EQP', selected_x]
).properties(title=f'📊 {eqp_1} vs {eqp_2} - {selected_x} 비교')

# Streamlit에 차트 출력
st.altair_chart(chart, use_container_width=True)