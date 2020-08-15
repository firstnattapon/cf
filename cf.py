import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import streamlit as st
import base64
st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("json file", type="json")
if uploaded_file is not None:
    df = pd.read_json(uploaded_file)
    df = pd.json_normalize(df['messages'])
    Market = df['from'].values[-1]
    dd = df['text']
    dd = dd.str.split("current_order:" , expand=True)
    dd = dd[1]
    dd = dd.str.replace("'"  , '')
    dd = dd.str.replace(")"  , '')
    dd = dd.str.replace(" ,  pl:"  , '')
    dd = dd.str[:3]
    dd = dd.astype(np.float32)
    df = df['text']
    df = df.str.split(":" , expand=True)
    df = df[4]
    df = df.str.replace("'"  , '')
    df = df.str.replace(")"  , '')
    df = df.astype(np.float32)
    df = np.cumsum(df)
    df = df.dropna()
    df = df.reset_index(drop=True)
    df = df.to_frame('cumsum')
    df['cf'] =   df.shift(0) - df.shift(1) ; df['cf'][0] = df['cumsum'][0]
    df['avg'] =  df.cf.mean()
    df['dd'] = np.max(dd)
    st.write('Market : ', Market)
    st.write('number : ', round(df.index.values[-1] , 2))
    st.write('cumsum : ', round(df['cumsum'].values[-1] , 2))
    st.write('avg    : ', round(df['avg'].values[-1] , 2))
    st.write('dd     : ', round(df['dd'].values[-1] , 2))
    _ , axs = plt.subplots(3 , figsize=(15 ,15))
    axs[0].plot(df['cumsum'])
    axs[1].bar( df.index , height= df['cf'].T )
    axs[1].plot(df['avg'])
    axs[2].plot(df['dd'])
    axs[2].plot(20)
    axs[2].plot(0)
    st.pyplot()
    st.write(df.tail(1))
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)
