EQP_ID_MODULE_NAME 선택 - HST_REG_DTTM 선택(동일한 날짜는 순서대로 점으로 표시) - WAF_ID 선택하면 ZDDFRONTMEAN_01_AFS2값과 pred값 두개 비교하는 그래프 그려줘.


  if 'df_Y' not in st.session_state:
    df_Y = pd.read_csv('./asset/wire_saw_summary/sfqr/all_minmax_with_predictions_and_importance.csv', low_memory=False)
    df_Y['HST_REG_DTTM'] = df_Y['HST_REG_DTTM'].map(lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').date())
    st.session_state['df_Y'] = df_Y
