2024-01-01 07:04:00 이 형식으로는 안 돌아가고 아래 형식으로 바꾸니 돼 다시 구현


  start_datetime, end_datetime = st.slider(
        "날짜와 시간을 선택하세요",
        min_value=datetime(2019, 1, 1, 9, 30),
        max_value=datetime(2020, 1, 1, 9, 30),
        # value=(min_datetime, max_datetime),
        format="YYYY-MM-DD hh:mm"
    )
