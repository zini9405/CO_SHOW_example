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


- page
-- SFQR.py
-- SFQR_pred.py
-- ZDD.py
-- ZDD_pred.py


SFQR을 클릭하고 SFQR_pred하면 파일이 작동이 돼.
ZDD를 클릭학과 ZDD_pred하면 파일이 작동이 돼
SFQR을 클릭하고 ZDD_pred하면 파일이 엉켜서 작동이 이상하게 돼.
ZDD를 클릭학과 SFQR_pred하면 파일이 엉켜서 작동이 이상하게 돼.

해결해줘.
