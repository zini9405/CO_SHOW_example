import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import json
#from src.misc import load_json
from src.graph import get_color
import re


def load_json(
    path: str
) -> dict:
    
    with open(path, 'r') as f:
        obj = json.load(f)
    return obj

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]


if 'df_Y' not in st.session_state:
    st.session_state['df_Y'] = pd.read_csv('./asset/SFQR/pred.csv', low_memory=False) # 전체 데이터

if 'SFQR_json' not in st.session_state:
    st.session_state['SFQR_json'] = load_json('./asset/SFQR/SFQR_jsonSFQR.json')


이 코드는 streamlit를 통해 웹페이지를 만드는 거야.
내가 만들고 싶은 걸 이야기할게.

먼저 st.session_state['SFQR_json']를 통해 아래와 같이 selectbox를 만들어야돼.

with col11:
    st.subheader('EQP SFQR')
    eqp = sorted(st.session_state['SFQR_json']['EQP_ID_MODULE_NAME'], key=natural_sort_key)

    eqp = st.selectbox(
        label = 'EQP NAME',
        options = eqp,
        index = 0
    )
그리고 선택된 eqp를 통해 st.session_state['df_Y']의 'EQP_ID_MODULE_NAME' 열에 동일한 값을 들고와.
선택된 값들에 HST_REG_DTTM라는 열이 날짜야. 여기도 날짜를 선택할 수 있는게 만들어줘. 단, 날짜를 연속으로 선택도 할 수 있게 만들어줘. 
예시 1) 2024-01-01 7:04 한개 선택
예시 1) 2024-01-01 7:04 부터 2024-05-01

그러면 선택된 값에 해당되는 WAF_ID를 selectbox로 만들어줘.

마지막으로 날짜에 해당하는 Pred과 SFQR_AFS2을 그래프로 표시해줘.
