#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import streamlit as st
import numpy as np
import itertools
import pprint
from sklearn.cluster import KMeans


# In[ ]:





# In[ ]:





# In[10]:


import streamlit as st
import pandas as pd
import os

# 設定
EXCEL_FILE = 'user_data_with_links.xlsx'
SAVE_DIR = 'uploaded_images'

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.title("プロフィール")

with st.form("input_form"):
    name=st.text_input('ニックネームを入力')
    sex=st.selectbox(' 性別を選択',['男','女'])
    age=st.text_input('年齢を入力')
    mbti=st.selectbox(' MBTIを選択',["ISFP","ISFJ","ISTP","ISTJ","INFP","INFJ","INTP","INTJ","ESFP","ESFJ","ESTP","ESTJ","ENFP","ENFJ","ENTP","ENTJ"])
    uploaded_file = st.file_uploader("写真をアップロード", type=["jpg", "png", "jpeg"])
    submitted = st.form_submit_button("保存")

if submitted and uploaded_file is not None:
    # 1. 写真をフォルダに保存
    img_path = os.path.join(SAVE_DIR, uploaded_file.name)
    # Excelでリンクとして機能させるため、絶対パス（フルパス）を取得
    full_path = os.path.abspath(img_path)
    
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 2. Excel保存用のデータ
    # Excelの数式 =HYPERLINK("パス", "表示名") を作成します
    link_formula = f'=HYPERLINK("{full_path}", "画像を開く")'
    new_data = pd.DataFrame([[name, sex, age, mbti, link_formula]], columns=['名前', '性別', '年齢','MBTI', '写真のリンク'])

    # 3. 保存処理
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    # 保存
    df.to_excel(EXCEL_FILE, index=False)
    
    st.success("保存完了")


# In[ ]:





# In[ ]:




