import streamlit as st
import pandas as pd
import os
from supabase import create_client

# Supabase接続
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

SAVE_DIR = 'uploaded_images'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.title("プロフィール")

with st.form("input_form"):
    name = st.text_input('ニックネームを入力')
    sex = st.selectbox('性別を選択', ['男', '女'])
    age = st.text_input('年齢を入力')
    mbti = st.selectbox('MBTIを選択', [
        "ISFP","ISFJ","ISTP","ISTJ","INFP","INFJ","INTP","INTJ",
        "ESFP","ESFJ","ESTP","ESTJ","ENFP","ENFJ","ENTP","ENTJ"
    ])
    uploaded_file = st.file_uploader("写真をアップロード", type=["jpg", "png", "jpeg"])
    submitted = st.form_submit_button("保存")

if submitted:
    if not name or not age or uploaded_file is None:
        st.warning("全て入力してください")
    else:
        # Supabaseに保存
        data = {
            "name": name,
            "sex": sex,
            "age": age,
            "mbti": mbti,
            "image_url": uploaded_file.name
        }
        supabase.table("profiles").insert(data).execute()
        st.success("保存完了！")



