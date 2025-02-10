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
