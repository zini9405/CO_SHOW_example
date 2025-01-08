import pandas as pd
import altair as alt
import streamlit as st

# 데이터 로드
df_Y = pd.read_csv('./asset/wire_saw_summary/sfqr/all_minmax_with_predictions_and_importance.csv', low_memory=False)

# 그룹화 대상 특정 이름 (예: 'eqp_1')
group_name = 'eqp_1'

# 중요도 열 리스트
importance_cols = [
    'SLOT_NO_importance', 'RECIPE_ID_importance',
    'AVG_ROTATION_SPEED_AT_CH_MOTIONCTRL_ROTATION_RVEL_STEP_MEAN_importance',
    'BLOWER_AIR_BOTTOM_PRESSURE_BOTTOM_AT_CHA_STEP_MEAN_importance',
    'BLOWER_AIR_PRESSURE_AT_CHA_STEP_MEAN_importance',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK01_MFC_RFLOW_STEP_MEAN_importance',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK02_MFC_RFLOW_STEP_MEAN_importance',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK03_MFC_RFLOW_STEP_MEAN_importance',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK04_MFC_RFLOW_STEP_MEAN_importance',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK05_MFC_RFLOW_STEP_MEAN_importance',
    'CURRENT_FLOW_AT_CH_GASPANEL_STICK06_MFC_RFLOW_STEP_MEAN_importance',
    'LIFT_TORQUE_AT_CHA_MOTIONCTRL_LIFT_RTORQUE_STEP_MEAN_importance',
    'PRESSURE_AT_BUFFER_VACSYS_PRESSGAUGE_RPRESSURE_STEP_MEAN_importance',
    'PRESSURE_AT_CH_MAN1000T_RPRESSURE_STEP_MEAN_importance',
    'SCR_POWER_AT_CH_TEMPCTRL_HEATER_TOP_INNER_RPOWER_STEP_MEAN_importance',
    'SCR_POWER_AT_CH_TEMPCTRL_HEATER_TOP_OUTER_RPOWER_STEP_MEAN_importance',
    'SCR_POWER_AT_CH_TEMPCTRL_HEATER_BOTTOM_INNER_RPOWER_STEP_MEAN_importance',
    'SCR_POWER_AT_CH_TEMPCTRL_HEATER_BOTTOM_OUTER_RPOWER_STEP_MEAN_importance',
    'TEMPERATURE_READING_AT_CH_TEMPCTRL_HEATER_BOTTOM_PYROMETER_RTEMP_STEP_MEAN_importance',
    'TEMPERATURE_READING_AT_CH_TEMPCTRL_HEATER_EDGE_PYROMETER_RTEMP_STEP_MEAN_importance',
    'TEMPERATURE_READING_AT_CH_TEMPCTRL_HEATER_TOP_PYROMETER_RTEMP_STEP_MEAN_importance',
    'VP_ACCUSET_IN_STEP_MEAN_importance', 'VP_ACCUSET_OUT_STEP_MEAN_importance',
    'VP_MULTIRUN_ORDER_STEP_MEAN_importance', 'VP_RCP_CNT_STEP_MAX_importance',
    'VP_SUSCEPTORHEIGHT_STEP_MAX_importance', 'VP_RCP_CNT2_STEP_MAX_importance',
    'CH_SAVED_TRAINED_EXTENDED_EXTENSION_B1_STEP_MEAN_importance',
    'CH_SAVED_TRAINED_EXTENDED_ROTATION_B1_STEP_MEAN_importance',
    'ACTUAL_SPEED_AT_CH_TEMPCTRL_HEATER_BOTTOM_VSB_RSPEED_STEP_MEAN_importance',
    'ACTUAL_SPEED_AT_CH_TEMPCTRL_HEATER_TOP_VSB_RSPEED_STEP_MEAN_importance',
    'ZDDFRONTMEAN_01_AFS2_SUB_importance'
]

# 1. 특정 이름으로 필터링
df_filtered = df_Y[df_Y['EQP_ID_MODULE_NAME'] == group_name]

# 2. 중요도 열의 평균 계산
mean_importance = df_filtered[importance_cols].mean().reset_index()
mean_importance.columns = ['col', 'SCORE']  # 열 이름 변경

# 3. 중요도 평균값 기준으로 정렬
df_sorted = mean_importance.sort_values('SCORE', ascending=False)

# 4. Altair 차트 생성
chart = alt.Chart(df_sorted.iloc[:10]).mark_bar(color='#E1002A').encode(
    x=alt.X('SCORE', title='IMPORTANCE (%)'),
    y=alt.Y('col', title=None, sort='-x', axis=alt.Axis(labelLimit=200))
)

# 5. Streamlit에서 차트 표시
st.altair_chart(chart, use_container_width=True)