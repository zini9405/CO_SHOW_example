import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import datetime
from glob import glob
from src.process import to_dict, get_golden_tool, to_dict_
from src.graph import plot_cluster, plot_pie_chart, get_color, plot_shape
#from src.graph import *
from src.misc import mode, get_fname
import os

if 'df_Y' not in st.session_state:
    df_Y = pd.read_csv('./asset/wire_saw_summary/sfqr/all_minmax_with_predictions_and_importance.csv', low_memory=False)
    df_Y['HST_REG_DTTM'] = df_Y['HST_REG_DTTM'].map(lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').date())
    st.session_state['df_Y'] = df_Y
    
if 'df_cluster' not in st.session_state:
    st.session_state['df_cluster'] = pd.read_csv('./asset/wire_saw_summary/sfqr/embedding_results.csv')

if 'list_recipe' not in st.session_state:
    st.session_state['list_recipe'] = st.session_state['df_Y'].RECIPE_ID.unique().tolist()

if 'dict_cluster' not in st.session_state:
    st.session_state['dict_cluster'] = to_dict_(st.session_state['df_cluster'])

st.set_page_config(
    page_title = 'WIRE SAW - WARP',
    page_icon = '📊',
    initial_sidebar_state = 'collapsed',
    layout = 'wide'
)


start_date = st.sidebar.date_input('Start date', datetime.date.today() - datetime.timedelta(days=60))
end_date = st.sidebar.date_input('End date', datetime.date.today())
print(st.session_state['df_Y'])

list_lot_id = st.session_state['df_Y'][(st.session_state['df_Y'].HST_REG_DTTM.between(start_date, end_date, inclusive='both'))].WAF_ID.tolist()


st.markdown('## EPI SFQR')

# 1. warp trend
st.markdown('---')
st.markdown('### 1. SFQR 품질 현황')



df_warp = st.session_state['df_Y'][st.session_state['df_Y'].WAF_ID.isin(list_lot_id)].groupby('EQP_ID_MODULE_NAME').ZDDFRONTMEAN_01_AFS2.mean().reset_index().sort_values('ZDDFRONTMEAN_01_AFS2')
print(df_warp)

chart = alt.Chart(df_warp).mark_bar(color = '#E1002A').encode(
    x = alt.X('EQP_NM', title = None, sort = '-y'),
    y = alt.Y('WARP_BF', title = 'WARP (um)', scale = alt.Scale(domain = [6, 16], clamp = True))
)

st.altair_chart(chart, use_container_width = True)

###############################################################

eqps = df_warp.sort_values('EQP_ID_MODULE_NAME')
warps = eqps['ZDDFRONTMEAN_01_AFS2'].values
idx_init = int(np.argmax(warps))

###############################################################


ValueError: Unable to determine data type for the field "EQP_NM"; verify that the field name is not misspelled. If you are referencing a field from a transform, also confirm that the data type is specified correctly.
