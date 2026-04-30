import streamlit as st
import os
from supabase import create_client
import streamlit as st

# パスワード保護
PASSWORD = "48691229"  # ここを好きなパスワードに変更

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("ログイン")
    pwd = st.text_input("パスワードを入力", type="password")
    if st.button("ログイン"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("パスワードが違います")
    st.stop()

# ここから下が既存のコード
# Supabase接続
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("プロフィール")

with st.form("input_form"):
    name = st.text_input('ニックネームを入力')
    sex = st.selectbox('性別を選択', ['男', '女'])
    age = st.text_input('年齢を入力')
    mbti = st.selectbox('MBTIを選択', [
        "ISFP","ISFJ","ISTP","ISTJ","INFP","INFJ","INTP","INTJ",
        "ESFP","ESFJ","ESTP","ESTJ","ENFP","ENFJ","ENTP","ENTJ"
    ])
    age1 = st.text_input('グループメンバーの年齢（最小）')
    age2 = st.text_input('グループメンバーの年齢（最大）')
    sex1 = st.selectbox('グループメンバーの性別を選択', [
        "同性だけ","男女混合"
    ])
    adress =st.selectbox('所在地を選択', [
        "北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
        "新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県",
        "鳥取県","島根県","岡山県","広島県","山口県",
        "徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"
    ])
    uploaded_file = st.file_uploader("写真をアップロード", type=["jpg", "png", "jpeg"])
    submitted = st.form_submit_button("保存")

if submitted:
    if not name or not age or uploaded_file is None:
        st.warning("全て入力してください")
    else:
        # 1. Storageに写真をアップロード
        file_bytes = uploaded_file.read()
        file_name = uploaded_file.name
        try:
            supabase.storage.from_("images").upload(
                path=file_name,
                file=file_bytes
            )
        except Exception:
    # 同名ファイルが既にある場合は上書き
            supabase.storage.from_("images").update(
                path=file_name,
                file=file_bytes
            )
        
        # 2. 写真の公開URLを取得
        image_url = supabase.storage.from_("images").get_public_url(file_name)
        
        # 3. profilesテーブルに保存
        data = {
            "name": name,
            "sex": sex,
            "age": age,
            "mbti": mbti,
            "image_url": image_url
        }
        supabase.table("profiles").insert(data).execute()
        
        st.success("保存完了！")
        st.image(image_url, caption=name, width=300)


