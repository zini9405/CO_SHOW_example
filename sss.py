너는 streamlit 전문가야.
    
현재 streamlit 구성이 아래와 같이 되어있어.

Main
  Main
Wire Saw
  Wire Saw
  Wire Saw EQP
  Wire Saw Warp
DSP Analysis
  GBIR Analysis
DSP Quality
  GBIR Quality
EPI Analysis
  SFQR Analysis
  ZDD Analysis
EPI Quality
  SFQR Quality
  ZDD Quality

이렇게 만드니, 속도가 너무 느려지는 문제가 있어.

Wire Saw를 누르면 한 페이지에 상단 위에 Wire Saw Wire Saw EQP Wire Saw Warp 각 버튼을 만들고 해당 버튼을 누루면 상단 아래에 정보가 나오게 하는 코드 구현해줄래?
DSP Analysis 누르면  한 페이지에 상단 위에 GBIR Analysis 버튼을 만들고 해당 버튼을 누루면 상단 아래에 정보가 나오게 하는 코드 구현해줄래?
나머지도 마찬가지로 구현해줘.


------------------------------------------------------------------------------------------------------------

front.py 코드

import streamlit as st


# 📌 페이지 객체 생성 (기존 코드 유지)
main = st.Page('main.py', title='Main', default=True)

ws = st.Page('pages/wiresaw.py', title='Wire Saw')
ws1 = st.Page('pages/wiresaw_eqp.py', title='Wire Saw EQP')
ws2 = st.Page('pages/wiresaw_warp.py', title='Wire Saw Warp')

epi = st.Page('pages/SFQR.py', title='SFQR Analysis')
epi2 = st.Page('pages/ZDD.py', title='ZDD Analysis')
epi3 = st.Page('pages/SFQR_pred.py', title='SFQR Quality')
epi4 = st.Page('pages/ZDD_pred.py', title='ZDD Quality')

DSP_Analysis = st.Page('pages/GBIR.py', title='GBIR Analysis')
DSP_quality = st.Page('pages/GBIR_pred.py', title='GBIR Quality')

# 📌 네비게이션 객체 생성 (기존 코드 유지)
pg = st.navigation({
    'Main': [main],
    'Wire Saw': [ws, ws1, ws2], 
    'DSP Analysis': [DSP_Analysis],
    'DSP Quality': [DSP_quality],
    'EPI Analysis': [epi, epi2],  # SFQR/ZDD Analysis
    'EPI Quality': [epi3, epi4],  # SFQR/ZDD Quality
})

# 📌 네비게이션 실행 (기존 코드 유지)
pg.run()

------------------------------------------------------------------------------------------------------------

main.py 코드

import streamlit as st
base_url = 'http://10.150.9.121/tttm_go_back_address'

st.set_page_config(
    page_title = 'SMART TTTM',
    page_icon = '📊',
    initial_sidebar_state = 'collapsed',
    layout = 'wide'
)

def set_title(title):
    return f"<h2 style = 'text-align: center; color: black;'>{title}</h1>"

st.image('./asset/wire_saw_summary/front/banner.PNG', use_column_width = True)
st.markdown('---')


col11, col12, col13, col14 = st.columns(4)

with col11:
    st.markdown(set_title('WIRE SAW'), unsafe_allow_html = True)

with col12:
    st.markdown(set_title('DSP'), unsafe_allow_html = True)

with col13:
    st.markdown(set_title('FCS'), unsafe_allow_html = True)

with col14:
    st.markdown(set_title('EPI'), unsafe_allow_html = True)


col21, col22, col23, col24 = st.columns(4)

with col21: st.image('./asset/wire_saw_summary/front/wiresaw.gif')
with col22: st.image('./asset/wire_saw_summary/front/dsp.gif')
with col23: st.image('./asset/wire_saw_summary/front/fcs.gif')
with col24: st.image('./asset/wire_saw_summary/front/epi.gif')


col31, col32, col33, col34 = st.columns(4)

with col31:
    is_WARP_clicked = st.button(
        label = 'WARP', 
        use_container_width = True
    )
    if is_WARP_clicked:
        st.switch_page(f'./pages/wiresaw.py')

    is_BOW_clicked = st.button(
        label = 'BOW', 
        use_container_width = True, 
        disabled = True
    )
    if is_BOW_clicked:
        #st.switch_page(f'./pages/wiresaw.py')
        pass

    is_NANO_clicked = st.button(
        label = 'NANO', 
        use_container_width = True, 
        disabled = True
    )
    if is_NANO_clicked:
        #st.switch_page(f'./pages/wiresaw.py')
        pass

# with col32:

#     is_SFQR_clicked = st.button(
#         label = 'GBIR', 
#         use_container_width = True
#     )
#     if is_SFQR_clicked:
#         st.switch_page(f'./pages/GBIR.py')

with col32:
    is_GBIR_clicked = st.button(
        label = 'GBIR', 
        use_container_width = True
    )
    if is_GBIR_clicked:
        st.switch_page(f'./pages/GBIR.py')

    st.link_button(
        label = 'SFQR', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )
    st.link_button(
        label = 'ESFQR', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )

with col33:
    st.link_button(
        label = 'LLS (47 nm)', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )
    st.link_button(
        label = 'METAL', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )

with col34:
    is_SFQR_clicked = st.button(
        label = 'SFQR', 
        use_container_width = True
    )
    if is_SFQR_clicked:
        st.switch_page(f'./pages/SFQR.py')

    is_ZDD_clicked = st.button(
        label = 'ZDD', 
        use_container_width = True
    )
    if is_ZDD_clicked:
        st.switch_page(f'./pages/ZDD.py')

    st.link_button(
        label = 'SITE NT', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )
    st.link_button(
        label = 'DELTA TEMP', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )

for _ in range(9):
    st.write('')
#st.write('해당 페이지는 품질 현황과 장비의 TTTM Point 제안을 위해 개발되었습니다.')
st.write('문의사항: Smart제조AI팀 이주영T, Smart제조AI팀 이채현P, Smart제조AI팀 이준원P')


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

GBIR.py 코드

import streamlit as st
import pandas as pd
import altair as alt
import datetime



# Streamlit 페이지 설정
st.set_page_config(
    page_title="EQP 데이터 비교",
    page_icon="📊",
    layout="wide"
)

# 데이터 로드
if 'df_gbir_pred' not in st.session_state:
    df_gbir_pred = pd.read_csv('./asset/gbir/final_result_6900.csv', low_memory=False)

    df_gbir_pred['BASE_DT'] = df_gbir_pred['BASE_DT'].map(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())

    st.session_state['df_gbir_pred'] = df_gbir_pred

df_gbir_pred = st.session_state['df_gbir_pred']

# print(df_gbir_pred)

# Streamlit UI 제목
st.markdown("<h2 style='text-align: center;'> EQP 데이터 비교 (GBIR_AFS2 vs Pred)</h2>", unsafe_allow_html=True)


# EQP_ID 선택
eqp_list = df_gbir_pred['EQP_ID'].unique()
selected_eqp = st.sidebar.selectbox("EQP_ID 선택", eqp_list)

# 선택한 EQP에 해당하는 데이터 필터링
df_filtered_eqp = df_gbir_pred[df_gbir_pred['EQP_ID'] == selected_eqp]

# BASE_DT 선택 (해당 EQP에서 날짜 목록만 가져오기)
date_list = df_filtered_eqp['BASE_DT'].unique()

selected_date = st.sidebar.selectbox("BASE_DT 선택", date_list)

# 선택한 날짜의 데이터 필터링
df_filtered_date = df_filtered_eqp[df_filtered_eqp['BASE_DT'] == selected_date]


# ✅ 전체 WAF_ID 데이터를 **수평 정렬된 그래프**로 표시
df_melted_all = df_filtered_date.melt(id_vars=['WAF_ID'], value_vars=['6900_GBIR_AFS2', 'pred'],
                                      var_name='Variable', value_name='Value')

# 📊 WAF_ID별 그래프 (X축을 WAF_ID로 설정하여 수평 정렬)
chart_all = alt.Chart(df_melted_all).mark_circle(size=80).encode(
    x=alt.X('WAF_ID:N', title="WAF_ID", sort='ascending'),
    y=alt.Y('Value:Q', title="값"),
    color=alt.Color('Variable:N'),
    tooltip=['WAF_ID', 'Variable', 'Value']
).properties(title=f'📊 {selected_date} - 전체 WAF_ID 데이터')

# 그래프 출력
st.altair_chart(chart_all, use_container_width=True)

# ✅ Streamlit selectbox로 WAF_ID 선택
selected_waf = st.sidebar.selectbox("WAF_ID 선택", df_filtered_date['WAF_ID'].unique())

# 선택한 WAF_ID 데이터 필터링
df_final = df_filtered_date[df_filtered_date['WAF_ID'] == selected_waf]

# 데이터 확인 및 개별 그래프 생성
if df_final.empty:
    st.warning("선택한 WAF_ID에 대한 데이터가 없습니다.")
else:
    # ✅ 📌 Altair 시각화를 위한 데이터 변환
    df_melted = df_final.melt(id_vars=['BASE_DT'], value_vars=['6900_GBIR_AFS2', 'pred'], var_name='Variable', value_name='Value')

    # ✅ 📊 선택한 WAF_ID의 상세 그래프
    chart = alt.Chart(df_melted).mark_line(point=True).encode(
        x=alt.X('BASE_DT:T', title="날짜"),
        y=alt.Y('Value:Q', title="값"),
        color=alt.Color('Variable:N'),
        tooltip=['BASE_DT', 'Variable', 'Value']
    ).properties(title=f'📊 {selected_waf} - GBIR_AFS2 vs Pred')

    # 개별 그래프 출력
    st.altair_chart(chart, use_container_width=True)

    # ✅ 📋 선택한 WAF_ID의 데이터 테이블
    st.markdown(f"### 📋 {selected_waf}의 상세 데이터")
    st.dataframe(df_final)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

GBIR.py 코드

import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import datetime
from glob import glob
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from src.process_gbir import get_golden_tool_GBIR, to_dict_gbir
from src.graph_gbir import plot_cluster_gbir

if 'df_gbir' not in st.session_state:
    df_gbir = pd.read_csv('./asset/gbir/final_result_6900.csv', low_memory=False)
    df_gbir.rename(columns={'6900_GBIR_AFS2': 'GBIR_AFS2_6900'}, inplace=True)
    df_gbir['BASE_DT'] = df_gbir['BASE_DT'].map(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())
    st.session_state['df_gbir'] = df_gbir
    
if 'df_cluster_gbir' not in st.session_state:
    st.session_state['df_cluster_gbir'] = pd.read_csv('./asset/gbir/embedding_results_gbir.csv')

if 'dict_cluster_gbir' not in st.session_state:
    st.session_state['dict_cluster_gbir'] = to_dict_gbir(st.session_state['df_cluster_gbir'])

st.set_page_config(
    page_title = 'EPI - gbir',
    page_icon = '📊',
    initial_sidebar_state = 'collapsed',
    layout = 'wide'
)

end_date_gbir_gbir, end_date_gbir = st.sidebar.slider('Date',
                                            min_value = st.session_state['df_gbir'].sort_values('BASE_DT').BASE_DT.iloc[0],
                                            max_value=datetime.date.today(),
                                            value=(datetime.date.today() - datetime.timedelta(days=30),datetime.date.today()),
                                            format='YYYY-MM-DD'
                                        )

list_lot_id = st.session_state['df_gbir'][(st.session_state['df_gbir'].BASE_DT.between(end_date_gbir_gbir, end_date_gbir, inclusive='both'))].WAF_ID.tolist()


st.markdown('## DSP GBIR')

###############################################################
df_GBIR_AFS2_6900 = st.session_state['df_gbir'][st.session_state['df_gbir'].WAF_ID.isin(list_lot_id)].groupby('EQP_ID').GBIR_AFS2_6900.mean().reset_index().sort_values('GBIR_AFS2_6900')
eqps = df_GBIR_AFS2_6900.sort_values('EQP_ID')
warps = eqps['GBIR_AFS2_6900'].values
idx_init = int(np.argmax(warps))

###############################################################

col1, col2 = st.columns(2)

with col1:
    eqp_1 = st.selectbox(
        label = '대상 장비',
        options = eqps,
        index = idx_init
    )

    df_score = st.session_state['df_gbir'][st.session_state['df_gbir']['EQP_ID'] == eqp_1]

with col2:
    eqp_2 = st.selectbox(
        label = 'Golden tool',
        options = get_golden_tool_GBIR(st.session_state['dict_cluster_gbir'], eqp_1),
        index = 0
    )

# 1. warp trend
st.markdown('---')
st.markdown('### 1. GBIR 품질 현황')

def assign_color(row):
    if row['EQP_ID'] == eqp_2:
        return 'blue'
    elif row['EQP_ID'] == eqp_1:
        return 'red'
    else:
        return 'silver'

df_GBIR_AFS2_6900['color'] = df_GBIR_AFS2_6900.apply(assign_color, axis=1)

y_min = df_GBIR_AFS2_6900['GBIR_AFS2_6900'].min()
y_max = df_GBIR_AFS2_6900['GBIR_AFS2_6900'].max()

# NaN, inf 체크 후 기본값 설정
if np.isnan(y_min) or np.isnan(y_max) or np.isinf(y_min) or np.isinf(y_max):
    print("⚠️ Warning: y_min or y_max is NaN/Inf. Assigning default values.")
    y_min, y_max = 0, 1  # 기본값 설정

chart = alt.Chart(df_GBIR_AFS2_6900).mark_bar().encode(
    x = alt.X('EQP_ID:N', title = None, sort = '-y'),
    y = alt.Y('GBIR_AFS2_6900:Q', title = 'ZDD Curvature', scale = alt.Scale(domain = [y_min, y_max], clamp = True)),
    color=alt.Color('color:N', scale=alt.Scale(domain=['blue', 'red', 'silver'], range=['blue', 'red', 'silver']), legend=None),
    tooltip=['EQP_ID', 'GBIR_AFS2_6900'],
)
st.altair_chart(chart, use_container_width = True)

# 2. clustering
st.markdown('---')
st.markdown('### 2. Golden Tool 탐색')

col3, col4 = st.columns([0.7,1.0])

with col3:
    fig = plot_cluster_gbir(
        df_cluster_gbir = st.session_state['df_cluster_gbir'], 
        eqp_1 = eqp_1, 
        eqp_2 = eqp_2
    )

    st.pyplot(fig, use_container_width = True)

with col4:
    interval_selector = alt.selection_interval('interval_selection', encodings=['x'])
    df_eqp = st.session_state['df_gbir'][(st.session_state['df_gbir'].BASE_DT.between(end_date_gbir_gbir, end_date_gbir, inclusive='both'))]

    col41, col42 = st.columns([0.5, 0.5])

    df_eqp1 = df_eqp.loc[df_eqp.EQP_ID == eqp_1]
    df_eqp1 = df_eqp1[(df_eqp1.BASE_DT.between(end_date_gbir_gbir, end_date_gbir, inclusive='both'))].sort_values('BASE_DT')

    df_eqp_grp1 = df_eqp1.groupby(['BASE_DT', 'WAF_ID'])
    df_eqp_grp1 = df_eqp_grp1.agg({'GBIR_AFS2_6900':'mean'}).reset_index()
    df_eqp_grp1['MEAN_GBIR_AFS2_6900'] = df_eqp_grp1.groupby('BASE_DT')['GBIR_AFS2_6900'].transform('mean')
    

    df_eqp2 = df_eqp.loc[df_eqp.EQP_ID == eqp_2]
    df_eqp2 = df_eqp2[(df_eqp2.BASE_DT.between(end_date_gbir_gbir, end_date_gbir, inclusive='both'))].sort_values('BASE_DT')

    df_eqp_grp2 = df_eqp2.groupby(['BASE_DT', 'WAF_ID'])
    df_eqp_grp2 = df_eqp_grp2.agg({'GBIR_AFS2_6900':'mean'}).reset_index()
    df_eqp_grp2['MEAN_GBIR_AFS2_6900'] = df_eqp_grp2.groupby('BASE_DT')['GBIR_AFS2_6900'].transform('mean')

    with col41:
        chart1 = alt.Chart(df_eqp_grp1).mark_bar().encode(
            x=alt.X('BASE_DT:T', axis=alt.Axis(format='%Y-%m-%d', labelAngle=90), title = None, sort = alt.EncodingSortField('BASE_DT', order = 'ascending')),
            y=alt.Y('MEAN_GBIR_AFS2_6900:Q', scale=alt.Scale(domain=[0, 1]), title = 'GBIR', stack=False), 
            color=alt.condition(interval_selector, alt.value('#E1002A'), alt.value('darkred'), legend=None),
            tooltip = ['BASE_DT', 'MEAN_GBIR_AFS2_6900']
        ).properties(title=alt.TitleParams(text=f'EQP: {eqp_1}', anchor='middle', fontSize=20)).add_params(interval_selector)
        event = st.altair_chart(chart1, use_container_width = True, on_select = 'rerun')

        # print()
        sub_df_eqp1 = df_eqp_grp1
        if 'BASE_DT' in event['selection']['interval_selection']:
            interval_end_date_gbir_gbir = datetime.datetime.fromtimestamp(event['selection']['interval_selection']['BASE_DT'][0]/1000)
            interval_end_date_gbir = datetime.datetime.fromtimestamp(event['selection']['interval_selection']['BASE_DT'][1]/1000)


            sub_df_eqp1 = df_eqp_grp1[pd.to_datetime(df_eqp_grp1['BASE_DT']).between(interval_end_date_gbir_gbir, interval_end_date_gbir, inclusive='both')].sort_values('BASE_DT')
    
        # 날짜 형식 변환 (YYYY-MM-DD)
        sub_df_eqp1['BASE_DT'] = pd.to_datetime(sub_df_eqp1['BASE_DT']).dt.strftime('%Y-%m-%d')

        # 날짜별 WAF_ID 개수 계산
        date_counts = sub_df_eqp1['BASE_DT'].value_counts()

        # x축을 가장 많은 개수를 가진 날짜 기준으로 설정 (0부터 시작)
        sub_df_eqp1 = sub_df_eqp1.sort_values(['BASE_DT', 'WAF_ID']).reset_index(drop=True)
        sub_df_eqp1['x_index'] = sub_df_eqp1.groupby('BASE_DT').cumcount()

        # Altair 차트 생성 (날짜별 점이 따로 표시됨, 연결되지 않음)
        chart = alt.Chart(sub_df_eqp1).mark_line().encode(
            x=alt.X('x_index:Q', title=f"WAF_ID Number"),
            y=alt.Y('GBIR_AFS2_6900:Q', title="GBIR_AFS2_6900"),
            color=alt.Color('BASE_DT:N', title="날짜"),
            tooltip=['BASE_DT', 'WAF_ID', 'GBIR_AFS2_6900']
        ).interactive()

        # Streamlit에 차트 출력
        st.altair_chart(chart, use_container_width=True)

    with col42: 
        chart2 = alt.Chart(df_eqp_grp2).mark_bar().encode(
            x=alt.X('BASE_DT:T', axis=alt.Axis(format='%Y-%m-%d', labelAngle=90), title = None, sort = alt.EncodingSortField('BASE_DT', order = 'ascending')),
            y=alt.Y('MEAN_GBIR_AFS2_6900:Q', scale=alt.Scale(domain=[0, 1]), title = 'GBIR', stack=False), 
            color=alt.condition(interval_selector, 'Origin', alt.value('darkblue'), legend=None),
            tooltip = ['BASE_DT', 'MEAN_GBIR_AFS2_6900']
        ).properties(title=alt.TitleParams(text=f'EQP: {eqp_2}', anchor='middle', fontSize=20)).add_params(interval_selector)
        event = st.altair_chart(chart2, use_container_width = True, on_select = 'rerun')

        # print()
        sub_df_eqp2 = df_eqp_grp2
        if 'BASE_DT' in event['selection']['interval_selection']:
            interval_end_date_gbir_gbir = datetime.datetime.fromtimestamp(event['selection']['interval_selection']['BASE_DT'][0]/1000)
            interval_end_date_gbir = datetime.datetime.fromtimestamp(event['selection']['interval_selection']['BASE_DT'][1]/1000)


            sub_df_eqp2 = df_eqp_grp2[pd.to_datetime(df_eqp_grp2['BASE_DT']).between(interval_end_date_gbir_gbir, interval_end_date_gbir, inclusive='both')].sort_values('BASE_DT')


        # 날짜 형식 변환 (YYYY-MM-DD)
        sub_df_eqp2['BASE_DT'] = pd.to_datetime(sub_df_eqp2['BASE_DT']).dt.strftime('%Y-%m-%d')

        # 날짜별 WAF_ID 개수 계산
        date_counts = sub_df_eqp2['BASE_DT'].value_counts()

        # 가장 WAF_ID 개수가 많은 날짜 찾기
        max_date = date_counts.idxmax()

        # x축을 가장 많은 개수를 가진 날짜 기준으로 설정 (0부터 시작)
        sub_df_eqp2 = sub_df_eqp2.sort_values(['BASE_DT', 'WAF_ID']).reset_index(drop=True)
        sub_df_eqp2['x_index'] = sub_df_eqp2.groupby('BASE_DT').cumcount()

        # Altair 차트 생성 (날짜별 점이 따로 표시됨, 연결되지 않음)
        chart = alt.Chart(sub_df_eqp2).mark_line().encode(
            x=alt.X('x_index:Q', title=f"WAF_ID Number"),
            y=alt.Y('GBIR_AFS2_6900:Q', title="GBIR_AFS2_6900"),
            color=alt.Color('BASE_DT:N', title="날짜"),
            tooltip=['BASE_DT', 'WAF_ID', 'GBIR_AFS2_6900']
        ).interactive()

        # Streamlit에 차트 출력
        st.altair_chart(chart, use_container_width=True)

# # 3. X 중요도
st.markdown('---')
st.markdown('### 3. X 인자 중요도 및  비교 (대상 장비 vs Golden tool)')


col5,col6 = st.columns([0.4,0.5])

with col5:
    score = df_score[pd.to_datetime(df_score.BASE_DT, format = '%Y%m%d').dt.date.between(end_date_gbir_gbir, end_date_gbir, inclusive='both')]

    importance_cols = [
        'SLOT_NO_importance',
        'RECIPE_ID_importance',
        'INTERNLA_GEAR_RPM_ACTUAL_STEP_MEAN_importance',
        'PAD_TEMP_STEP_MEAN_importance',
        'RING_GEAR_MOTOR_CURRENT_STEP_MEAN_importance',
        'SLURRY_1_FLOW_STEP_MEAN_importance',
        'SLURRY_IN_TEMP_STEP_MEAN_importance',
        'SUN_GEAR_MOTOR_CURRENT_STEP_MEAN_importance',
        'SUN_GEAR_RPM_ACTUAL_STEP_MEAN_importance',
        'SURFACTANT_FLOW_ACTUAL_STEP_MEAN_importance',
        'PRS_PRES_ACTUAL__STEP_MEAN_importance',
        'UPPER_COOLING_IN_TEMP_STEP_MEAN_importance',
        'UPPER_COOLING_OUT_TEMP_STEP_MEAN_importance',
        'UPPER_COOLING_FLOW_STEP_MEAN_importance',
        'UPPER_MOTOR_CURRENT_STEP_MEAN_importance',
        'UPPER_RPM_ACTUAL_STEP_MEAN_importance',
        'LOWER_COOLING_IN_TEMP_STEP_MEAN_importance',
        'LOWER_COOLING_OUT_TEMP_STEP_MEAN_importance',
        'LOWER_COOLING_FLOW_STEP_MEAN_importance',
        'LOWER_MOTOR_CURRENT_STEP_MEAN_importance',
        'LOWER_RPM_ACTUAL_STEP_MEAN_importance',
        'PRS_PRES_ACTUAL__STEP_COUNT_importance',
        'PAD_COUNT_importance',
        'SLURRY_USE_NUM_importance',
        'DD_USE_NUM_importance',
        'MAIN_RUNTIME_importance',
        'CARRIER_MTL_USE_NUM_importance']


    # 2. 중요도 열의 평균 계산
    mean_importance = score[importance_cols].mean().reset_index()
    mean_importance.columns = ['col', 'SCORE']  # 열 이름 변경

    mean_importance['col'] = mean_importance['col'].str.replace('_importance', '', regex=False)

    # 3. 중요도 평균값 기준으로 정렬
    df_sorted = mean_importance.sort_values('SCORE', ascending=False)

    chart = alt.Chart(df_sorted.iloc[:-1]).mark_bar(color = '#E1002A').encode(
        x = alt.X('SCORE', title = 'IMPORTANCE (%)'),
        y = alt.Y('col', title = None, sort = '-x', axis = alt.Axis(labelLimit = 200))
    ).properties(title=alt.TitleParams(text=f'{eqp_1}', anchor='middle', fontSize=25))

    st.altair_chart(chart, use_container_width = True)

with col6:
    # Streamlit UI 제목
    st.markdown(f"<h2 style='text-align: center;'> {eqp_1} vs {eqp_2}</h2>", unsafe_allow_html=True)

    # 데이터 가져오기 (예제 데이터)
    df_eqp = st.session_state['df_gbir'][(st.session_state['df_gbir'].BASE_DT.between(end_date_gbir_gbir, end_date_gbir, inclusive='both'))]

    # 비교할 X 값 선택 (사용자가 선택 가능)
    x_columns = [
        'SLOT_NO',
        'RECIPE_ID',
        'INTERNLA_GEAR_RPM_ACTUAL_STEP_MEAN',
        'PAD_TEMP_STEP_MEAN',
        'RING_GEAR_MOTOR_CURRENT_STEP_MEAN',
        'SLURRY_1_FLOW_STEP_MEAN',
        'SLURRY_IN_TEMP_STEP_MEAN',
        'SUN_GEAR_MOTOR_CURRENT_STEP_MEAN',
        'SUN_GEAR_RPM_ACTUAL_STEP_MEAN',
        'SURFACTANT_FLOW_ACTUAL_STEP_MEAN',
        'PRS_PRES_ACTUAL__STEP_MEAN',
        'UPPER_COOLING_IN_TEMP_STEP_MEAN',
        'UPPER_COOLING_OUT_TEMP_STEP_MEAN',
        'UPPER_COOLING_FLOW_STEP_MEAN',
        'UPPER_MOTOR_CURRENT_STEP_MEAN',
        'UPPER_RPM_ACTUAL_STEP_MEAN',
        'LOWER_COOLING_IN_TEMP_STEP_MEAN',
        'LOWER_COOLING_OUT_TEMP_STEP_MEAN',
        'LOWER_COOLING_FLOW_STEP_MEAN',
        'LOWER_MOTOR_CURRENT_STEP_MEAN',
        'LOWER_RPM_ACTUAL_STEP_MEAN',
        'PRS_PRES_ACTUAL__STEP_COUNT',
        'PAD_COUNT',
        'SLURRY_USE_NUM',
        'DD_USE_NUM',
        'MAIN_RUNTIME',
        'CARRIER_MTL_USE_NUM',
    ]

    selected_x = st.sidebar.selectbox("비교할 X 값 선택", x_columns)

    # EQP_1, EQP_2 데이터 필터링
    df_eqp1 = df_eqp[df_eqp.EQP_ID == eqp_1].groupby("BASE_DT")[selected_x].mean().reset_index()
    df_eqp1["EQP"] = eqp_1

    df_eqp2 = df_eqp[df_eqp.EQP_ID == eqp_2].groupby("BASE_DT")[selected_x].mean().reset_index()
    df_eqp2["EQP"] = eqp_2

    # EQP_1, EQP_2 데이터 합치기
    df_combined = pd.concat([df_eqp1, df_eqp2])

    # 날짜 형식 변환 (YYYY-MM-DD)
    df_combined['BASE_DT'] = pd.to_datetime(df_combined['BASE_DT']).dt.strftime('%Y-%m-%d')

    # Altair 차트 생성
    chart = alt.Chart(df_combined).mark_line(point=True).encode(
        x=alt.X('BASE_DT:T', axis=alt.Axis(format='%Y-%m-%d', labelAngle=45), title="날짜"),
        y=alt.Y(f"{selected_x}:Q", title="X 값"),
        color=alt.Color('EQP:N', title="EQP ID"),
        tooltip=['BASE_DT', 'EQP', selected_x]
    ).properties(title=alt.TitleParams(text=f'{selected_x} 비교', anchor='middle', fontSize=15))

    # Streamlit에 차트 출력
    st.altair_chart(chart, use_container_width=True)

    
