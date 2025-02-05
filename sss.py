
with col4:
    interval_selector = alt.selection_interval('interval_selection', encodings=['x'])
    df_eqp = st.session_state['df_Y'][(st.session_state['df_Y'].HST_REG_DTTM.between(start_date, end_date, inclusive='both'))]

    col41, col42 = st.columns([0.5, 0.5])

    df_eqp1 = df_eqp.loc[df_eqp.EQP_ID_MODULE_NAME == eqp_1]
    df_eqp1 = df_eqp1[(df_eqp1.HST_REG_DTTM.between(start_date, end_date, inclusive='both'))].sort_values('HST_REG_DTTM')

    df_eqp_grp1 = df_eqp1.groupby(['HST_REG_DTTM', 'WAF_ID'])
    df_eqp_grp1 = df_eqp_grp1.agg({'ZDDFRONTMEAN_01_AFS2':'mean'}).reset_index()
    df_eqp_grp1['MEAN_ZDDFRONTMEAN_01_AFS2'] = df_eqp_grp1.groupby('HST_REG_DTTM')['ZDDFRONTMEAN_01_AFS2'].transform('mean')
    

    df_eqp2 = df_eqp.loc[df_eqp.EQP_ID_MODULE_NAME == eqp_2]
    df_eqp2 = df_eqp2[(df_eqp2.HST_REG_DTTM.between(start_date, end_date, inclusive='both'))].sort_values('HST_REG_DTTM')

    df_eqp_grp2 = df_eqp2.groupby(['HST_REG_DTTM', 'WAF_ID'])
    df_eqp_grp2 = df_eqp_grp2.agg({'ZDDFRONTMEAN_01_AFS2':'mean'}).reset_index()
    df_eqp_grp2['MEAN_ZDDFRONTMEAN_01_AFS2'] = df_eqp_grp2.groupby('HST_REG_DTTM')['ZDDFRONTMEAN_01_AFS2'].transform('mean')

    df_eqp_warp_max = np.ceil(max(df_eqp_grp1['MEAN_ZDDFRONTMEAN_01_AFS2'].max(), df_eqp_grp2['MEAN_ZDDFRONTMEAN_01_AFS2'].max()))
    df_eqp_warp_min = np.ceil(min(df_eqp_grp1['MEAN_ZDDFRONTMEAN_01_AFS2'].min(), df_eqp_grp2['MEAN_ZDDFRONTMEAN_01_AFS2'].min()))

    with col41:
        chart1 = alt.Chart(df_eqp_grp1).mark_bar().encode(
            x=alt.X('HST_REG_DTTM:T', axis=alt.Axis(format='%Y-%m-%d', labelAngle=90), title = None, sort = alt.EncodingSortField('HST_REG_DTTM', order = 'ascending')),
            y=alt.Y('MEAN_ZDDFRONTMEAN_01_AFS2:Q', scale=alt.Scale(domain=[df_eqp_warp_min, df_eqp_warp_max]), title = 'ZDD Curvature', stack=False), 
            color=alt.condition(interval_selector, alt.value('#E1002A'), alt.value('darkred'), legend=None),
            tooltip = ['HST_REG_DTTM', 'MEAN_ZDDFRONTMEAN_01_AFS2']
        ).properties(title=alt.TitleParams(text=f'EQP: {eqp_1}', anchor='middle', fontSize=20)).add_params(interval_selector)
        event = st.altair_chart(chart1, use_container_width = True, on_select = 'rerun')

        # print()
        sub_df_eqp1 = df_eqp_grp1
        if 'HST_REG_DTTM' in event['selection']['interval_selection']:
            interval_start_date = datetime.datetime.fromtimestamp(event['selection']['interval_selection']['HST_REG_DTTM'][0]/1000)
            interval_end_date = datetime.datetime.fromtimestamp(event['selection']['interval_selection']['HST_REG_DTTM'][1]/1000)


            sub_df_eqp1 = df_eqp_grp1[pd.to_datetime(df_eqp_grp1['HST_REG_DTTM']).between(interval_start_date, interval_end_date, inclusive='both')].sort_values('HST_REG_DTTM')
    
    # 날짜 형식 변환 (YYYY-MM-DD)
    sub_df_eqp1['HST_REG_DTTM'] = pd.to_datetime(sub_df_eqp1['HST_REG_DTTM']).dt.strftime('%Y-%m-%d')

    # 날짜별 WAF_ID 개수 계산
    date_counts = sub_df_eqp1['HST_REG_DTTM'].value_counts()


    # # 가장 WAF_ID 개수가 많은 날짜 찾기
    # max_date = date_counts.idxmax()
    # min_date = date_counts.idxmin()

    # x축을 가장 많은 개수를 가진 날짜 기준으로 설정 (0부터 시작)
    sub_df_eqp1 = sub_df_eqp1.sort_values(['HST_REG_DTTM', 'WAF_ID']).reset_index(drop=True)
    sub_df_eqp1['x_index'] = sub_df_eqp1.groupby('HST_REG_DTTM').cumcount()

    # Altair 차트 생성 (날짜별 점이 따로 표시됨, 연결되지 않음)
    chart = alt.Chart(sub_df_eqp1).mark_line().encode(
        x=alt.X('x_index:Q', title=f"WAF_ID Number"),
        y=alt.Y('ZDDFRONTMEAN_01_AFS2:Q', title="ZDDFRONTMEAN_01_AFS2"),
        color=alt.Color('HST_REG_DTTM:N', title="날짜"),
        tooltip=['HST_REG_DTTM', 'WAF_ID', 'ZDDFRONTMEAN_01_AFS2']
    ).interactive()

    # Streamlit에 차트 출력
    st.altair_chart(chart, use_container_width=True)

with col42: 
    chart2 = alt.Chart(df_eqp_grp2).mark_bar().encode(
        x=alt.X('HST_REG_DTTM:T', axis=alt.Axis(format='%Y-%m-%d', labelAngle=90), title = None, sort = alt.EncodingSortField('HST_REG_DTTM', order = 'ascending')),
        y=alt.Y('MEAN_ZDDFRONTMEAN_01_AFS2:Q', scale=alt.Scale(domain=[df_eqp_warp_min, df_eqp_warp_max]), title = 'ZDD Curvature', stack=False), 
        color=alt.condition(interval_selector, 'Origin', alt.value('darkblue'), legend=None),
        tooltip = ['HST_REG_DTTM', 'MEAN_ZDDFRONTMEAN_01_AFS2']
    ).properties(title=alt.TitleParams(text=f'EQP: {eqp_2}', anchor='middle', fontSize=20)).add_params(interval_selector)
    event = st.altair_chart(chart2, use_container_width = True, on_select = 'rerun')

    # print()
    sub_df_eqp2 = df_eqp_grp2
    if 'HST_REG_DTTM' in event['selection']['interval_selection']:
        interval_start_date = datetime.datetime.fromtimestamp(event['selection']['interval_selection']['HST_REG_DTTM'][0]/1000)
        interval_end_date = datetime.datetime.fromtimestamp(event['selection']['interval_selection']['HST_REG_DTTM'][1]/1000)


        sub_df_eqp2 = df_eqp_grp2[pd.to_datetime(df_eqp_grp2['HST_REG_DTTM']).between(interval_start_date, interval_end_date, inclusive='both')].sort_values('HST_REG_DTTM')


    # 날짜 형식 변환 (YYYY-MM-DD)
    sub_df_eqp2['HST_REG_DTTM'] = pd.to_datetime(sub_df_eqp2['HST_REG_DTTM']).dt.strftime('%Y-%m-%d')

    # 날짜별 WAF_ID 개수 계산
    date_counts = sub_df_eqp2['HST_REG_DTTM'].value_counts()

    # 가장 WAF_ID 개수가 많은 날짜 찾기
    max_date = date_counts.idxmax()

    # x축을 가장 많은 개수를 가진 날짜 기준으로 설정 (0부터 시작)
    sub_df_eqp2 = sub_df_eqp2.sort_values(['HST_REG_DTTM', 'WAF_ID']).reset_index(drop=True)
    sub_df_eqp2['x_index'] = sub_df_eqp2.groupby('HST_REG_DTTM').cumcount()

    # Altair 차트 생성 (날짜별 점이 따로 표시됨, 연결되지 않음)
    chart = alt.Chart(sub_df_eqp2).mark_line().encode(
        x=alt.X('x_index:Q', title=f"WAF_ID Number"),
        y=alt.Y('ZDDFRONTMEAN_01_AFS2:Q', title="ZDDFRONTMEAN_01_AFS2"),
        color=alt.Color('HST_REG_DTTM:N', title="날짜"),
        tooltip=['HST_REG_DTTM', 'WAF_ID', 'ZDDFRONTMEAN_01_AFS2']
    ).interactive()

    # Streamlit에 차트 출력
    st.altair_chart(chart, use_container_width=True)

# # 3. X 중요도
st.markdown('---')
st.markdown('### 3. X 인자 중요도')
st.markdown(f'{eqp_1} - FDC 인자')

그래프가 4개 균둥하게 만들어주면 좋겠는데, col41이 이상한데 그려지는 문제가 생겨
