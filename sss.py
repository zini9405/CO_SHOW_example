# 1. warp trend
st.markdown('---')
st.markdown('### 1. SFQR 품질 현황')

df_warp = st.session_state['df_Y'][st.session_state['df_Y'].WAF_ID.isin(list_lot_id)].groupby('EQP_ID_MODULE_NAME').ZDDFRONTMEAN_01_AFS2.mean().reset_index().sort_values('ZDDFRONTMEAN_01_AFS2')

y_min = df_warp['ZDDFRONTMEAN_01_AFS2'].min()
y_max = df_warp['ZDDFRONTMEAN_01_AFS2'].max()

chart = alt.Chart(df_warp).mark_bar(color = '#E1002A').encode(
    x = alt.X('EQP_ID_MODULE_NAME', title = None, sort = '-y'),
    y = alt.Y('ZDDFRONTMEAN_01_AFS2', title = 'ZDD', scale = alt.Scale(domain = [y_min, y_max], clamp = False))
)

st.altair_chart(chart, use_container_width = True)
