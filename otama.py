#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import streamlit as st
import numpy as np
import itertools
import pprint
from sklearn.cluster import KMeans


# In[ ]:





# In[8]:


import streamlit as st
import pandas as pd
import os
from PIL import Image


name=st.text_input('ニックネームを入力')
sex=st.selectbox(' 性別を選択',['男','女'])
age=st.selectbox('年齢を選択',options=list(range(20,100)))
mbti=st.selectbox(' MBTIを選択',["ISFP","ISFJ","ISTP","ISTJ","INFP","INFJ","INTP","INTJ","ESFP","ESFJ","ESTP","ESTJ","ENFP","ENFJ","ENTP","ENTJ"])
# 設定
EXCEL_FILE = 'user_data_with_photos.xlsx'
SAVE_DIR = 'uploaded_images'  # 写真を保存するフォルダ名

# フォルダがなければ作成
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.title("写真と情報の登録アプリ")

with st.form("user_form"):
    uploaded_file = st.file_uploader("写真を選択してください", type=["jpg", "png", "jpeg"])
    submitted = st.form_submit_button("登録する")

if submitted and uploaded_file is not None:
    # 1. 写真を保存する
    # ファイル名が重ならないように「名前_元のファイル名」にする
    img_path = os.path.join(SAVE_DIR, f"{name}_{uploaded_file.name}")
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # 2. Excel用のデータを作成（写真の保存場所を記録）
    new_data = pd.DataFrame([[name, sex, age, mbti, img_path]], columns=['名前', '性別', '年齢','MBTI','写真のパス'])

    # 3. Excelに追記
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    df.to_excel(EXCEL_FILE, index=False)
    
    st.success(f"保存完了！写真は {img_path} に保存されました。")
    st.image(img_path, width=300)


# In[11]:





# In[ ]:





# In[ ]:




