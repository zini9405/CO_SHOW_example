import streamlit as st

# 📌 현재 페이지 상태 관리 (없으면 기본값 설정)
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = None  # 선택된 페이지 초기화

# 📌 상태 초기화 함수 (불필요한 세션 데이터 제거)
def reset_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]  # 모든 세션 키 삭제 (완전 초기화)
    st.session_state['current_page'] = None

# 📌 페이지 정의
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

# 📌 네비게이션 정의 (페이지 이동 시 상태 초기화 적용)
pg = st.navigation({
    'Main': [main],
    'Wire Saw': [ws, ws1, ws2], 
    'DSP Analysis': [DSP_Analysis],
    'DSP Quality': [DSP_quality],
    'EPI Analysis': [epi, epi2],  # SFQR/ZDD Analysis
    'EPI Quality': [epi3, epi4],  # SFQR/ZDD Quality
})

# 📌 페이지 전환 시 상태 초기화 적용
if pg.current_page in ['SFQR Analysis', 'ZDD Analysis', 'SFQR Quality', 'ZDD Quality']:
    reset_state()
    st.session_state['current_page'] = pg.current_page  # 현재 페이지 저장

# 📌 네비게이션 실행
pg.run()