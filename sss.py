그래도 안되네...
front.py

import streamlit as st



main = st.Page('main.py',title='Main', default=True)

ws = st.Page('pages/wiresaw.py',title='Wire Saw')
ws1 = st.Page('pages/wiresaw_eqp.py',title='Wire Saw EQP')
ws2 = st.Page('pages/wiresaw_warp.py',title='Wire Saw Warp')


epi = st.Page('pages/SFQR.py',title='SFQR Analysis')
epi2 = st.Page('pages/ZDD.py',title='ZDD Analysis')
epi3 = st.Page('pages/SFQR_pred.py',title='SFQR Quality')
epi4 = st.Page('pages/ZDD_pred.py',title='ZDD Quality')

DSP_Analysis = st.Page('pages/GBIR.py',title='GBIR Qnalysis')
DSP_quality = st.Page('pages/GBIR_pred.py',title='GBIR Quality')

pg = st.navigation({
    'Main': [main],
    'Wire Saw': [ws, ws1, ws2], 
    'DSP Analysis': [DSP_Analysis],
    'DSP Quality': [DSP_quality],
    'EPI Analysis': [epi, epi2],
    'EPI quality': [epi3, epi4]
})

pg.run()

여기가 문제인가?
ZDD Quality클릭하고 SFQR Quality클릭하면 되는데 그 뒤로 ZDD Analysi 등 나머지 클릭하면 안돼
