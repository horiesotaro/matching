import streamlit as st
import os
from supabase import create_client
import streamlit as st
import pandas as pd
import numpy as np
import itertools
import pprint
from sklearn.cluster import KMeans
import networkx as nx
import matplotlib.pyplot as plt
from IPython import embed


mbti_df = pd.read_excel('Bookb.xlsx',index_col=0)

st.title("プロフィール")

with st.form("input_form"):

    sex = st.selectbox('マッチしたい性別を選択', ['男', '女','両方'])
    agemin=st.selectbox('マッチ相手の年齢の最小値',range(20,55))
    agemax=st.selectbox('マッチ相手の年齢の最大値',range(20,55))
    people=st.selectbox('何人で遊びたいかを選択',['3人','4人','5人'])
    day = st.selectbox('希望日を選択', ['6/7', '6/8','6/9'])
    time = st.selectbox('希望時間を選択', ['昼', '夜'])
    mbti = st.selectbox('MBTIを選択', [
        "ISFP","ISFJ","ISTP","ISTJ","INFP","INFJ","INTP","INTJ",
        "ESFP","ESFJ","ESTP","ESTJ","ENFP","ENFJ","ENTP","ENTJ"
    ])
    st.text('\n以下は1～5を選択してください')
    st.text('1:全くそう思わない 2:そう思わない　3:どちらでもない 4:そう思う 5:とてもそう思う')
    tension=st.selectbox('1:同じようなテンション感の人と遊びたい',range(1,6))
    idea=st.selectbox('2:似た考え方の人と遊びたい',range(1,6))
    judge=st.selectbox('3:協調性が高い人or思考力が高い人と遊びたい',range(1,6))
    st.text('1:協調性が高い人 2:やや協調性寄り　3:どちらでもない 4:やや思考力寄り 5:思考力が高い人')
    plan=st.selectbox('4:前々からみんなでしっかり計画を練りたいorその場の流れで遊びたい',range(1,6))
    st.text('1:綿密な計画を決めておきたい 2:やや1寄り　3:行く場所くらいは決めたい 4:やや5寄り 5:時間と集合場所だけでOK')
    submitted = st.form_submit_button("保存")

if submitted:
    st.write("保存完了！")
        
a = mbti[0:4]


def orientation(a,tension,idea,judge,plan):
    if a[0]=='E':
        e=int(tension)
        i=6-int(tension)
    else:
        i=int(tension)
        e=6-int(tension)
    if a[1]=='N':
        n=int(idea)
        s=6-int(idea)
    else:
        s=int(idea)
        n=6-int(idea)
        
    t=int(judge)
    f=6-int(judge)
    p=int(plan)
    j=6-int(plan)
    return e,i,n,s,t,f,p,j


# In[85]:
minage=int(agemin)
maxage=int(agemax)

result0_df=(mbti_df[(mbti_df['性別'] == sex)&(mbti_df['希望日'] == day)&((mbti_df['希望時間'] == time))])
result1_df=(mbti_df[(mbti_df['希望日'] == day)&((mbti_df['希望時間'] == time))])

if (sex=='両方'):
    y_df=result1_df
else:
    y_df=result0_df
d_df=(y_df[(y_df['年齢']>=minage)&((y_df['年齢']<=maxage))])

# 各MBTIの人数をカウントする
mbti_counts = d_df['MBTI'].value_counts()


def scoring(e,i,n,s,t,f,p,j):
    ISFP=(i+s+f+p)*2
    ISFJ=(i+s+f+j)*2
    ISTP=(i+s+t+p)*2
    ISTJ=(i+s+t+j)*2
    INFP=(i+n+f+p)*2
    INFJ=(i+n+f+j)*2
    INTP=(i+n+t+p)*2
    INTJ=(i+n+t+j)*2
    ESFP=(e+s+f+p)*2
    ESFJ=(e+s+f+j)*2
    ESTP=(e+s+t+p)*2
    ESTJ=(e+s+t+j)*2
    ENFP=(e+n+f+p)*2
    ENFJ=(e+n+f+j)*2
    ENTP=(e+n+t+p)*2
    ENTJ=(e+n+t+j)*2
    return (ISFP,ISFJ,ISTP,ISTJ,INFP,INFJ,INTP,INTJ,ESFP,ESFJ,ESTP,ESTJ,ENFP,ENFJ,ENTP,ENTJ)


# In[88]:


x_df=["ISFP","ISFJ","ISTP","ISTJ","INFP","INFJ","INTP","INTJ","ESFP","ESFJ","ESTP","ESTJ","ENFP","ENFJ","ENTP","ENTJ"]
w_df=pd.DataFrame(x_df, columns = ["MBTI"])
# e_df=(ISFP,ISFJ,ISTP,ISTJ,INFP,INFJ,INTP,INTJ,ESFP,ESFJ,ESTP,ESTJ,ENFP,ENFJ,ENTP,ENTJ)
(e,i,n,s,t,f,p,j)=orientation(a,tension,idea,judge,plan)
e_df = scoring(e,i,n,s,t,f,p,j)
aaa=scoring(e,i,n,s,t,f,p,j)
c_df=pd.DataFrame(e_df, columns = ["相手への評価"])
q_df=pd.concat([w_df,c_df],axis=1)
datacd=[]
for i in range(16):
    if aaa[i]>=24:
        datacd.append(x_df[i])
impo=len(datacd)

# 1. まずd_dfからMBTIの人数を集計してデータフレームにする
mbti_counts = d_df['MBTI'].value_counts().reset_index()
mbti_counts.columns = ['MBTI', '人数']

# 2. 集計結果と q_df を結合する
summary_df = pd.merge(q_df, mbti_counts, on='MBTI', how='left')

 #1. 相手への評価が24以上のMBTIのリストを取得する
if max(aaa)>=28:
    target_mbti = q_df[q_df['相手への評価'] >= 28]['MBTI'].tolist()
else:
    target_mbti = q_df[q_df['相手への評価'] >= (max(aaa))]['MBTI'].tolist()

# 2. d_dfの中で、そのMBTIリストに含まれるユーザー（行）の数をカウントする
total_users = d_df['MBTI'].isin(target_mbti).sum()

print(f"相手への評価が28or MAX以上のMBTIに属するユーザーの合計人数: {total_users}人")

a=(total_users)/(len(d_df))

if a>=0.86:
    bbq=32
elif (a>=0.71)and(a<0.86):
    bbq=30
elif (a>=0.56)and(a<0.71):
    bbq=28
elif (a>=0.41)and(a<0.56):
    bbq=26
else:
    bbq=24
print(bbq) 


y_df['相手への評価'] = 0
for i in range(y_df.shape[0]):
    #print(y_df.iloc[i,3])
    mbti2 = y_df.iloc[i,4]
    y_df.iloc[i,9]=q_df[q_df['MBTI'] == mbti2].loc[:,'相手への評価'].values[0]
s_df=y_df.copy()



# In[90]:


user0 = pd.DataFrame([[sex, day, time, minage,mbti, tension,idea,judge,plan,0]], columns =['性別','希望日','希望時間','年齢','MBTI', 'EI', 'SN', 'TF', 'PJ', '相手への評価'])
s_df = pd.concat([user0,s_df])
for i in range(1,len(s_df.index)):
    p_a,p_tension,p_idea,p_judge,p_plan = s_df.iloc[i,4:9]
    # print(p_a,p_tension,p_idea,p_judge,p_plan)
    p_e,p_i,p_n,p_s,p_f,p_t,p_j,p_p = orientation(p_a,p_tension,p_idea,p_judge,p_plan)
    p_e_df = scoring(p_e,p_i,p_n,p_s,p_f,p_t,p_j,p_p)
    s_df['相手からの評価'+str(i+1)] = 0
    for j in range(len(s_df.index)):
        if i == j:
            s_df.iloc[j,i+9] = 0
        else:
            s_df.iloc[j,i+9] = p_e_df[x_df.index(s_df.iloc[j,4])]
            


# In[91]:


g_df=s_df.iloc[0:,8:]


# In[92]:




# In[93]:


import numpy as np
import pandas as pd

df = g_df.copy()

# 空のマスク（全部False）
mask = pd.DataFrame(False, index=df.index, columns=df.columns)


n = len(df)

for x in range(n):
    for y in range(n):
        if x != y:
            a = df.iloc[x, y]
            b = df.iloc[y, x]

            if(max(aaa)>=28):
                # 1行目（x=0）または1列目（y=0）が絡む場合
                if y == 0:
                # 一方が24以上、もう一方が（bbq）以上なら残す
                    if (a >= 28 and b >= bbq):
                        mask.iloc[x, y] = True
                        mask.iloc[y, x] = True
                elif x == 0:
                    if (b >= 28 and a >= bbq):
                        mask.iloc[x, y] = True
                        mask.iloc[y, x] = True
                
            
            # 1行目、1列目以外の一般のデータの場合
                else:
                # お互いに28以上（28以上で統一）なら残す
                    if max(a,b)>=28 and min(a,b)>=24:
                        mask.iloc[x, y] = True
                        mask.iloc[y, x] = True
                        
                        
            if(max(aaa)<28):
                if y == 0:
                # 一方が24以上、もう一方が（bbq）以上なら残す
                    if (a >= max(aaa) and b >= bbq):
                        mask.iloc[x, y] = True
                        mask.iloc[y, x] = True
                elif x == 0:
                    if (b >= max(aaa) and a >= bbq):
                        mask.iloc[x, y] = True
                        mask.iloc[y, x] = True
                
            
            # 1行目、1列目以外の一般のデータの場合
                else:
                # お互いに28以上（28以上で統一）なら残す
                    if max(a,b)>=28 and min(a,b)>=24:
                        mask.iloc[x, y] = True
                        mask.iloc[y, x] = True
                            
                            

# 条件を満たす部分だけ残す
kid_df = df.where(mask, 0)


# 1. 元のデータフレームをコピーしてベースを作成
new_df = kid_df.copy()

# 2. 条件分岐
if max(aaa) < 28:
    # --- max(aaa)が28未満の時 ---
    
    # 1行目 (indexが0) または 1列目 (columnsの最初) の条件マスク
    # ※お使いのデータのインデックス名/カラム名に合わせて指定してください
    row0_mask = new_df.index == new_df.index[0]
    col0_mask = new_df.columns == new_df.columns[0]
    is_first_row_or_col = row0_mask[:, None] | col0_mask[None, :]
    
    # 条件A: 1行目・1列目で、値が max(aaa) 未満
    mask_a = is_first_row_or_col & (new_df < max(aaa))
    
    # 条件B: それ以外（1行目・1列目ではない）で、値が 28 未満
    mask_b = ~is_first_row_or_col & (new_df < 28)
    
    # 両方の条件を結合し、当てはまる場所を "x" に置換
    final_mask = mask_a | mask_b
    new_df = new_df.mask(final_mask, "x")

else:
    # --- max(aaa)が28以上の時 ---
    # 全ての行列で28未満の数字に "x"
    new_df = new_df.mask(new_df < 28, "x")

data23 = np.empty((0,1))
for j in range(len(new_df.index)):
    v3_df=new_df.iloc[0:,j:j+1]
    # print(v3_df.values.shape)
    data23 = np.vstack((data23,v3_df.values))




# ====================================================
# 必要ライブラリのインポート（関数の外で一括定義）
# ====================================================
from itertools import product, combinations
import networkx as nx
import pandas as pd
import numpy as np
import streamlit as st

# ====================================================
# 【確定版】3人マッチング用関数
# ====================================================
def process_matching_and_get_details(g_df, mbti_df, data23, start_node=0):
    user_id = g_df.index
    node_list = user_id.to_list()
    
    edge_list = [(x, y) for x, y in product(node_list, node_list) if x != y]
    
    datax = []
    datay_temp = []
    for i in range(min(len(data23), len(edge_list))):
        if data23[i] == "x":
            datay_temp.append(edge_list[i])
        else:
            datax.append(edge_list[i])
            
    G = nx.DiGraph()
    G.add_nodes_from(node_list)
    G.add_edges_from(datax)
    
    ab = dict(enumerate(nx.bfs_layers(G, [start_node])))
    ad = ab.get(1, [])
    ac = ab.get(2, [])
    
    datav = []
    for n in ac:
        neighbor = list(G[n].keys())
        if start_node in neighbor:
            datav.append(n)
            
    datay = []
    for m in ad:
        neighbor1 = list(G[m].keys())
        for n in neighbor1:
            if n in datav:
                datay.append((start_node, m, n))
                
    datap = set()
    for m in ad:
        for n in ad:
            neighbor1 = list(G[m].keys())
            neighbor2 = list(G[n].keys())
            if (m != n) and (m in neighbor2) and (n in neighbor1):
                datap.add((start_node, min(m, n), max(m, n)))
                
    datavv = datay + list(datap)
    
    if not datavv:
        return None
        
    id2pos = {id_val: pos for pos, id_val in enumerate(g_df.index)}
    
    dataq = []
    for g in datavv:
        for i, j in product(range(3), range(3)):
            if i != j:
                dataq.append(g_df.iat[id2pos[g[i]], id2pos[g[j]]])
                
    n = 6
    datar = [dataq[c:c+n] for c in range(0, len(dataq), n)]
    
    o1_df = pd.DataFrame(datavv, columns=['あなた', 'user1', 'user2'])
    o2_df = pd.DataFrame(datar, columns=[
        'user1 からあなたへの評価', 'user2 からあなたへの評価',
        'あなたから user1 への評価', 'user2 から user1 への評価',
        'あなたから user2 への評価', 'user1 から user2 への評価'
    ])
    o_df = pd.concat([o1_df, o2_df], axis=1)
    
    eval_values = o_df.iloc[:, 3:9].values
    o_df['合計'] = np.sum(eval_values, axis=1)
    o_df['分散'] = np.var(eval_values, axis=1)
    o_df['優劣値'] = o_df['合計'] - o_df['分散']
    
    fin_df = o_df.sort_values('優劣値', ascending=False).copy()
    user_cols = ["user1", "user2"]
    fin_df["group_key"] = fin_df[user_cols].apply(lambda x: tuple(sorted(x)), axis=1)
    fin_df = fin_df.drop_duplicates(subset="group_key").drop(columns="group_key")
    
    used_nums = set()
    selected_indices = []
    for idx, row in fin_df.iterrows():
        current_values = set(row[user_cols].values)
        current_values.discard(start_node)
        if not (current_values & used_nums):
            selected_indices.append(idx)
            used_nums.update(current_values)
            
    unique_rows0_df = fin_df.loc[selected_indices]
    if unique_rows0_df.empty:
        return None
        
    best_match = unique_rows0_df.iloc[0]
    user1_id = best_match['user1']
    user2_id = best_match['user2']
    
    user1_details = mbti_df.iloc[int(user1_id) - 1, 0:4]
    user2_details = mbti_df.iloc[int(user2_id) - 1, 0:4]
    return user1_id, user2_id, user1_details, user2_details


# ====================================================
# 【確定版】4人マッチング用関数 (第2引数を g_df に固定)
# ====================================================
def process_clique_matching_4ppl(kid_df, g_df, mbti_df, start_node=0):
    kid_df.columns = kid_df.index
    g_df_keys = g_df.index
    kid_df_keys = kid_df.index.astype(g_df_keys.dtype)
    
    kid_df.index = kid_df_keys
    kid_df.columns = kid_df_keys
    
    common_users = kid_df_keys.intersection(g_df_keys)
    if len(common_users) == 0:
        return None
        
    kid_df = kid_df.loc[common_users, common_users]
    typed_start_node = g_df_keys.dtype.type(start_node)
    
    G = nx.Graph(nx.from_pandas_adjacency(kid_df))
    cliques = nx.find_cliques(G)
    result = []
    for c in cliques:
        if typed_start_node in c and len(c) >= 4:
            for sub in combinations(c, 4):
                if typed_start_node in sub:
                    result.append(list(sorted(sub)))
                    
    if not result:
        return None
        
    id2pos = {id_val: pos for pos, id_val in enumerate(g_df.index)}
    
    dataq = []
    for g in result:
        for i, j in product(range(4), range(4)):
            if i != j:
                dataq.append(g_df.iat[id2pos[g[i]], id2pos[g[j]]])
                
    n = 12
    datar = [dataq[c:c+n] for c in range(0, len(dataq), n)]
    
    o1_df = pd.DataFrame(result, columns=['あなた', 'user1', 'user2', 'user3'])
    eval_cols = [
        'user1 からあなたへの評価', 'user2 からあなたへの評価', 'user3 からあなたへの評価',
        'あなたから user1 への評価', 'user2 から user1 への評価', 'user3 から user1 への評価',
        'あなたから user2 への評価', 'user1 から user2 への評価', 'user3 から user2 への評価',
        'あなたから user3 への評価', 'user1 から user3 への評価', 'user2 から user3 への評価'
    ]
    o2_df = pd.DataFrame(datar, columns=eval_cols)
    o_df = pd.concat([o1_df, o2_df], axis=1)
    
    o_df.loc[:, ['user2', 'user3']] = np.sort(o_df.loc[:, ['user2', 'user3']].values)
    gya_df = o_df.drop_duplicates(subset=['あなた', 'user1', 'user2', 'user3']).copy()
    
    eval_values = gya_df[eval_cols].values
    gya_df['合計'] = np.sum(eval_values, axis=1)
    gya_df['分散'] = np.var(eval_values, axis=1)
    gya_df['優劣値'] = gya_df['合計'] - gya_df['分散']
    
    fin_df = gya_df.sort_values('優劣値', ascending=False)
    
    dataw = []
    for idx, row in fin_df.iterrows():
        cond1 = max(row['user1 からあなたへの評価'], row['user2 からあなたへの評価'], row['user3 からあなたへの評価']) >= 24
        cond2 = max(row['あなたから user1 への評価'], row['user2 から user1 への評価'], row['user3 から user1 への評価']) >= 24
        cond3 = max(row['あなたから user2 への評価'], row['user1 から user2 への評価'], row['user3 から user2 への評価']) >= 24
        cond4 = max(row['あなたから user3 への評価'], row['user1 から user3 への評価'], row['user2 から user3 への評価']) >= 24
        cond5 = max(row['あなたから user1 への評価'], row['あなたから user2 への評価'], row['あなたから user3 への評価']) >= 24
        cond6 = max(row['user1 からあなたへの評価'], row['user1 から user2 への評価'], row['user1 から user3 への評価']) >= 24
        cond7 = max(row['user2 からあなたへの評価'], row['user2 から user1 への評価'], row['user2 から user3 への評価']) >= 24
        cond8 = max(row['user3 からあなたへの評価'], row['user3 から user1 への評価'], row['user3 から user2 への評価']) >= 24
        
        if cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7 and cond8:
            dataw.append(row)
            
    if not dataw:
        return None
        
    last_df = pd.DataFrame(dataw)
    cols = last_df.columns.difference(['分散', '優劣値'])
    last_df[cols] = last_df[cols].round().astype(int)
    
    used_nums = set()
    selected_indices = []
    target_cols = ['user1', 'user2', 'user3']
    for idx, row in last_df.iterrows():
        current_values = set(row[target_cols].values)
        current_values.discard(typed_start_node)
        if not (current_values & used_nums):
            selected_indices.append(idx)
            used_nums.update(current_values)
            
    unique_rows0_df = last_df.loc[selected_indices]
    if unique_rows0_df.empty:
        return None
        
    best_match = unique_rows0_df.iloc[0]
    a = best_match['user1']
    b = best_match['user2']
    c = best_match['user3']
    
    detail_a = mbti_df.iloc[int(a) - 1, 0:4]
    detail_b = mbti_df.iloc[int(b) - 1, 0:4]
    detail_c = mbti_df.iloc[int(c) - 1, 0:4]
    return a, b, c, detail_a, detail_b, detail_c


# ====================================================
# 【修正版・確定】5人マッチング用関数 (カラム名指定安全ver)
# ====================================================
def process_clique_matching_5ppl(kid_df, g_df, mbti_df, start_node=0):
    kid_df.columns = kid_df.index
    g_df_keys = g_df.index
    kid_df_keys = kid_df.index.astype(g_df_keys.dtype)
    
    kid_df.index = kid_df_keys
    kid_df.columns = kid_df_keys
    
    common_users = kid_df_keys.intersection(g_df_keys)
    if len(common_users) == 0:
        return None
        
    kid_df = kid_df.loc[common_users, common_users]
    typed_start_node = g_df_keys.dtype.type(start_node)
    
    G = nx.Graph(nx.from_pandas_adjacency(kid_df))
    cliques = nx.find_cliques(G)
    result = []
    for c in cliques:
        if typed_start_node in c and len(c) >= 5:
            for sub in combinations(c, 5):
                if typed_start_node in sub:
                    result.append(list(sorted(sub)))
                    
    if not result:
        return None
        
    id2pos = {id_val: pos for pos, id_val in enumerate(g_df.index)}
    
    dataq = []
    for g in result:
        for i, j in product(range(5), range(5)):
            if i != j:
                dataq.append(g_df.iat[id2pos[g[i]], id2pos[g[j]]])
                
    n = 20
    datar = [dataq[c:c+n] for c in range(0, len(dataq), n)]
    
    o1_df = pd.DataFrame(result, columns=['あなた', 'user1', 'user2', 'user3', 'user4'])
    
    # 20個の評価カラムを定義
    eval_cols = [
        'user1 からあなたへの評価', 'user2 からあなたへの評価', 'user3 からあなたへの評価', 'user4 からあなたへの評価',
        'あなたから user1 への評価', 'user2 から user1 への評価', 'user3 から user1 への評価', 'user4 から user1 への評価',
        'あなたから user2 への評価', 'user1 から user2 への評価', 'user3 から user2 への評価', 'user4 から user2 への評価',
        'あなたから user3 への評価', 'user1 から user3 への評価', 'user2 から user3 への評価', 'user4 から user3 への評価',
        'あなたから user4 への評価', 'user1 から user4 への評価', 'user2 から user4 への評価', 'user3 から user4 への評価'
    ]
    o2_df = pd.DataFrame(datar, columns=eval_cols)
    o_df = pd.concat([o1_df, o2_df], axis=1)
    
    o_df.loc[:, ['user2', 'user3', 'user4']] = np.sort(o_df.loc[:, ['user2', 'user3', 'user4']].values)
    gya_df = o_df.drop_duplicates(subset=['あなた', 'user1', 'user2', 'user3', 'user4']).copy()
    
    eval_values = gya_df[eval_cols].values
    gya_df['合計'] = np.sum(eval_values, axis=1)
    gya_df['分散'] = np.var(eval_values, axis=1)
    gya_df['優劣値'] = gya_df['合計'] - gya_df['分散']
    
    fin_df = gya_df.sort_values('優劣値', ascending=False)
    
    dataw = []
    for idx, row in fin_df.iterrows():
        # 【改善】インデックス番号ではなく、カラム名で直接最大値を判定 (各関係性で24以上があるか)
        cond_recv0 = max(row['user1 からあなたへの評価'], row['user2 からあなたへの評価'], row['user3 からあなたへの評価'], row['user4 からあなたへの評価']) >= 24
        cond_recv1 = max(row['あなたから user1 への評価'], row['user2 から user1 への評価'], row['user3 から user1 への評価'], row['user4 から user1 への評価']) >= 24
        cond_recv2 = max(row['あなたから user2 への評価'], row['user1 から user2 への評価'], row['user3 から user2 への評価'], row['user4 から user2 への評価']) >= 24
        cond_recv3 = max(row['あなたから user3 への評価'], row['user1 から user3 への評価'], row['user2 から user3 への評価'], row['user4 から user3 への評価']) >= 24
        cond_recv4 = max(row['あなたから user4 への評価'], row['user1 から user4 への評価'], row['user2 から user4 への評価'], row['user3 から user4 への評価']) >= 24
        
        cond_send0 = max(row['あなたから user1 への評価'], row['あなたから user2 への評価'], row['あなたから user3 への評価'], row['あなたから user4 への評価']) >= 24
        cond_send1 = max(row['user1 からあなたへの評価'], row['user1 から user2 への評価'], row['user1 から user3 への評価'], row['user1 から user4 への評価']) >= 24
        cond_send2 = max(row['user2 からあなたへの評価'], row['user2 から user1 への評価'], row['user2 から user3 への評価'], row['user2 から user4 への評価']) >= 24
        cond_send3 = max(row['user3 からあなたへの評価'], row['user3 から user1 への評価'], row['user3 から user2 への評価'], row['user3 から user4 への評価']) >= 24
        cond_send4 = max(row['user4 からあなたへの評価'], row['user4 から user1 への評価'], row['user4 から user2 への評価'], row['user4 から user3 への評価']) >= 24
        
        if (cond_recv0 and cond_recv1 and cond_recv2 and cond_recv3 and cond_recv4 and 
            cond_send0 and cond_send1 and cond_send2 and cond_send3 and cond_send4):
            dataw.append(row)
            
    if not dataw:
        return None
        
    last_df = pd.DataFrame(dataw)
    cols = last_df.columns.difference(['分散', '優劣値'])
    last_df[cols] = last_df[cols].round().astype(int)
    
    used_nums = set()
    selected_indices = []
    target_cols = ['user1', 'user2', 'user3', 'user4']
    for idx, row in last_df.iterrows():
        current_values = set(row[target_cols].values)
        current_values.discard(typed_start_node)
        if not (current_values & used_nums):
            selected_indices.append(idx)
            used_nums.update(current_values)
            
    unique_rows_df = last_df.loc[selected_indices]
    if unique_rows_df.empty:
        return None
        
    best_match = unique_rows_df.iloc[0]
    a = best_match['user1']
    b = best_match['user2']
    c = best_match['user3']
    d = best_match['user4']
    
    detail_a = mbti_df.iloc[int(a) - 1, 0:4]
    detail_b = mbti_df.iloc[int(b) - 1, 0:4]
    detail_c = mbti_df.iloc[int(c) - 1, 0:4]
    detail_d = mbti_df.iloc[int(d) - 1, 0:4]
    return a, b, c, d, detail_a, detail_b, detail_c, detail_d


# ====================================================
# メインの画面出力処理（条件分岐）
# ====================================================
# セレクトボックスの値に空白があっても判定できるように .strip() を適用
clean_people = people.strip()

if clean_people in ['3人', '3 人']:
    result = process_matching_and_get_details(g_df, mbti_df, data23, start_node=0)
    if result is not None:
        a, b, detail_a, detail_b = result
        st.text(f"あなたは{a}さん、{b}さんとマッチしました")
        st.text(f"{a}さんの詳細")
        st.text(detail_a)
        st.text("")
        st.text(f"{b}さんの詳細")
        st.text(detail_b)
    else:
        st.text("マッチング条件に合うユーザーが見つかりませんでした。")

elif clean_people in ['4人', '4 人']:
    clique_result = process_clique_matching_4ppl(kid_df, g_df, mbti_df, start_node=0)
    if clique_result is not None:
        a, b, c, detail_a, detail_b, detail_c = clique_result
        st.text(f"あなたは{a}さん、{b}さん、{c}さんとマッチしました")
        st.text(f"{a}さんの詳細")
        st.text(detail_a)
        st.text("")
        st.text(f"{b}さんの詳細")
        st.text(detail_b)
        st.text("")
        st.text(f"{c}さんの詳細")
        st.text(detail_c)
    else:
        st.text("条件に合致する 4 人グループが見つかりませんでした。")

elif clean_people in ['5人', '5 人']:
    clique_5_result = process_clique_matching_5ppl(kid_df, g_df, mbti_df, start_node=0)
    if clique_5_result is not None:
        a, b, c, d, detail_a, detail_b, detail_c, detail_d = clique_5_result
        st.text(f"あなたは{a}さん、{b}さん、{c}さん、{d}さんとマッチしました")
        st.text(f"{a}さんの詳細")
        st.text(detail_a)
        st.text("")
        st.text(f"{b}さんの詳細")
        st.text(detail_b)
        st.text("")
        st.text(f"{c}さんの詳細")
        st.text(detail_c)
        st.text("")
        st.text(f"{d}さんの詳細")
        st.text(detail_d)
    else:
        st.text("条件に合致する 5 人グループが見つかりませんでした。")
else:
    st.text("6人以上には対応していません")
