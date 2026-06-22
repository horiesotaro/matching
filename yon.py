#!/usr/bin/env python
# coding: utf-8

# In[2]:

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
    day = st.selectbox('希望日を選択', ['6/7', '6/8','6/9'])
    time = st.selectbox('希望時間を選択', ['昼', '夜','一日'])
    mbti = st.selectbox('MBTIを選択', [
        "ISFP","ISFJ","ISTP","ISTJ","INFP","INFJ","INTP","INTJ",
        "ESFP","ESFJ","ESTP","ESTJ","ENFP","ENFJ","ENTP","ENTJ"
    ])
    tension=st.selectbox('1:似たテンションの人とマッチしたい割合',range(0,11))
    idea=st.selectbox('2:似た考えの人とマッチしたい割合',range(0,11))
    judge=st.selectbox('3:感情的な人とマッチしたい割合',range(0,11))
    plan=st.selectbox('4:一緒に計画を立てたいしたい割合',range(0,11))
    submitted = st.form_submit_button("保存")

if submitted:
    st.write("保存完了！")
        
max1=('一日')
a = mbti[0:4]


def orientation(a,tension,idea,judge,plan):
    if a[0]=='E':
        e=int(tension)
        i=10-int(tension)
    else:
        i=int(tension)
        e=10-int(tension)
    if a[1]=='N':
        n=int(idea)
        s=10-int(idea)
    else:
        s=int(idea)
        n=10-int(idea)
        
    f=int(judge)
    t=10-int(judge)
    j=int(plan)
    p=10-int(plan)
    return e,i,n,s,f,t,j,p


# In[85]:


result0_df=(mbti_df[(mbti_df['性別'] == sex)&(mbti_df['希望日'] == day)&((mbti_df['希望時間'] == time)|(mbti_df['希望時間'] == max1))])
result1_df=(mbti_df[(mbti_df['希望日'] == day)&((mbti_df['希望時間'] == time)|(mbti_df['希望時間'] == max1))])#性別両方
result2_df=(mbti_df[(mbti_df['性別'] == sex)&(mbti_df['希望日'] == day)]) #希望時間一日
result3_df=(mbti_df[(mbti_df['希望日'] == day)]) #性別両方かつ希望時間一日
#ここにif文を入れる
if (sex=='両方')&(time=='一日'):
    y_df=result3_df
elif (time=='一日'):
    y_df=result2_df
elif (sex=='両方'):
    y_df=result1_df
else:
    y_df=result0_df
d_df=y_df.copy()



def scoring(e,i,n,s,f,t,j,p):
    ISFP=i+s+f+p
    ISFJ=i+s+f+j
    ISTP=i+s+t+p
    ISTJ=i+s+t+j
    INFP=i+n+f+p
    INFJ=i+n+f+j
    INTP=i+n+t+p
    INTJ=i+n+t+j
    ESFP=e+s+f+p
    ESFJ=e+s+f+j
    ESTP=e+s+t+p
    ESTJ=e+s+t+j
    ENFP=e+n+f+p
    ENFJ=e+n+f+j
    ENTP=e+n+t+p
    ENTJ=e+n+t+j
    return (ISFP,ISFJ,ISTP,ISTJ,INFP,INFJ,INTP,INTJ,ESFP,ESFJ,ESTP,ESTJ,ENFP,ENFJ,ENTP,ENTJ)


# In[88]:


x_df=["ISFP","ISFJ","ISTP","ISTJ","INFP","INFJ","INTP","INTJ","ESFP","ESFJ","ESTP","ESTJ","ENFP","ENFJ","ENTP","ENTJ"]
w_df=pd.DataFrame(x_df, columns = ["MBTI"])
# e_df=(ISFP,ISFJ,ISTP,ISTJ,INFP,INFJ,INTP,INTJ,ESFP,ESFJ,ESTP,ESTJ,ENFP,ENFJ,ENTP,ENTJ)
(e,i,n,s,f,t,j,p)=orientation(a,tension,idea,judge,plan)
e_df = scoring(e,i,n,s,f,t,j,p)
c_df=pd.DataFrame(e_df, columns = ["相手への評価"])
q_df=pd.concat([w_df,c_df],axis=1)



# In[89]:


y_df['相手への評価'] = 0
for i in range(y_df.shape[0]):
    #print(y_df.iloc[i,3])
    mbti2 = y_df.iloc[i,3]
    y_df.iloc[i,8]=q_df[q_df['MBTI'] == mbti2].loc[:,'相手への評価'].values[0]
s_df=y_df.copy()



# In[90]:


user0 = pd.DataFrame([[sex, day, time, mbti, tension,idea,judge,plan,0]], columns =['性別','希望日','希望時間','MBTI', 'EI', 'SN', 'TF', 'PJ', '相手への評価'])
s_df = pd.concat([user0,s_df])
for i in range(1,len(s_df.index)):
    p_a,p_tension,p_idea,p_judge,p_plan = s_df.iloc[i,3:8]
    # print(p_a,p_tension,p_idea,p_judge,p_plan)
    p_e,p_i,p_n,p_s,p_f,p_t,p_j,p_p = orientation(p_a,p_tension,p_idea,p_judge,p_plan)
    p_e_df = scoring(p_e,p_i,p_n,p_s,p_f,p_t,p_j,p_p)
    s_df['相手からの評価'+str(i+1)] = 0
    for j in range(len(s_df.index)):
        if i == j:
            s_df.iloc[j,i+8] = 0
        else:
            s_df.iloc[j,i+8] = p_e_df[x_df.index(s_df.iloc[j,3])]
            


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
        if x!=y:
            a = df.iloc[x, y]
            b = df.iloc[y, x]
            if (a >= 15 and b >= 15 ) and (a >= 25 or b >= 25):
                mask.iloc[x, y] = True
                mask.iloc[y, x] = True

# 条件を満たす部分だけ残す（他はNaN）
kid_df = df.where(mask,0)



# In[94]:




# In[128]:




# In[95]:


new_df=kid_df.where(kid_df>=25,"x")



# In[96]:







# In[98]:


data23 = np.empty((0,1))
for j in range(len(new_df.index)):
    v3_df=new_df.iloc[0:,j:j+1]
    # print(v3_df.values.shape)
    data23 = np.vstack((data23,v3_df.values))



# In[99]:


user_id = g_df.index


# In[100]:


from itertools import product

node_list = user_id.to_list()
edge_list = [ (x,y) for x, y in product(node_list,node_list) ]


# In[101]:


datax=[]
datay=[]
for i in range(len(data23)):
    if data23[i]==("x"):
        datay.append(edge_list[i])
    else:
        datax.append(edge_list[i])

kid_df.columns=kid_df.index

G = nx.Graph(nx.from_pandas_adjacency(kid_df))
nx.draw(G, with_labels = True)
plt.show()

from itertools import combinations

cliques = nx.find_cliques(G)

result = []

for c in cliques:
    if 0 in c and len(c) >= 4:
        for sub in combinations(c, 4):
            if 0 in sub:
                result.append(list(sorted(sub)))

id2pos = {}
for pos, id, in enumerate(g_df.index):
    id2pos[id] = pos
print(id2pos)


# In[103]:
dataq=[]
datar=[]
for g in result:
    for i,j in product(range(4),range(4)):
        if i != j:
            dataq.append(g_df.iat[id2pos[g[i]],id2pos[g[j]]])
n=12
for c in range(0,len(dataq),n):
    datar.append(dataq[c:c+n])






# In[66]:

datai=[]
for i in range(0,len(datar)):
    datai.append(sum(datar[i]))




# In[71]:


o1_df=pd.DataFrame(result, columns =['あなた','user1','user2','user3'])
o2_df=pd.DataFrame(datar, columns =['user1からあなたへの評価','user2からあなたへの評価','user3からあなたへの評価','あなたからuser1への評価','user2からuser1への評価','user3からuser1への評価','あなたからuser2への評価','user1からuser2への評価','user3からuser2への評価','あなたからuser3への評価','user1からuser3への評価','user2からuser3への評価'])
o_df=pd.concat([o1_df,o2_df],axis=1)

o_df.loc[:,['user2','user3']]=np.sort(o_df.loc[:,['user2','user3']].values)
gya_df=o_df.sort_values('user2')
gya_df=gya_df.drop_duplicates(subset=['あなた','user1','user2','user3'])
# In[72]:


import numpy as np

# 1. 初期化（大文字・小文字の表記ミスを防ぐため o_df に統一）
gya_df['合計'] = 0.0
gya_df['分散'] = 0.0
gya_df['優劣値'] = 0.0

# 2. ループ処理による計算と格納
for i in range(gya_df.shape[0]):
    # 4列目から16列目（インデックス4〜16）の値を取得
    x = gya_df.iloc[i, 4:16].values
    
    # 計算結果を .iat を使って確実に行・列に代入
    gya_df.iat[i, 16] = float(np.sum(x))       # 合計
    gya_df.iat[i, 17] = float(np.var(x))      # 分散
    gya_df.iat[i, 18] = float(np.sum(x) - np.var(x))  # 優劣値

# 3. 並び替え
fin_df = gya_df.sort_values('優劣値', ascending=False)

dataw=[]
for i in range(0,len(fin_df)):
    if((max(fin_df.iloc[i,4:7])>=25)and(max(fin_df.iloc[i,7:10])>=25)and(max(fin_df.iloc[i,10:13])>=25)and(max(fin_df.iloc[i,13:16])>=25)
    and(max(fin_df.iloc[i,7],fin_df.iloc[i,10],fin_df.iloc[i,13])>=25)and(max(fin_df.iloc[i,4],fin_df.iloc[i,11],fin_df.iloc[i,14])>=25)
    and(max(fin_df.iloc[i,5],fin_df.iloc[i,8],fin_df.iloc[i,15])>=25)and(max(fin_df.iloc[i,6],fin_df.iloc[i,9],fin_df.iloc[i,12])>=25)):
        dataw.append(fin_df.iloc[i,:])
      
last_df=pd.DataFrame(dataw)
cols = last_df.columns.difference([ '分散', '優劣値'])

last_df[cols] = last_df[cols].round().astype(int)
# In[75]:
used_nums = set()
selected_indices = []

# 対象とする列のリスト
target_cols = ['user1', 'user2', 'user3']

for idx, row in last_df.iterrows():
    # その行のユーザーたちの数値を取得
    current_values = set(row[target_cols].values)
    
    # 0（「あなた」の値など）は重複チェックから除外する場合
    current_values.discard(0)
    
    # すでに使われた数値と重なりがあるかチェック
    if not (current_values & used_nums):
        selected_indices.append(idx)
        used_nums.update(current_values)

# 重複のない行だけを抽出
unique_rows0_df = last_df.loc[selected_indices]

user_cols = ["user1", "user2"]

# 各行のユーザーをソートしてタプル化（順序を統一）
fin_df["group_key"] = fin_df[user_cols].apply(lambda x: tuple(sorted(x)), axis=1)

# 重複削除
fin_df = fin_df.drop_duplicates(subset="group_key")

# 不要なら削除
fin_df = fin_df.drop(columns="group_key")


# In[74]:





# In[76]:


used_nums = set()
selected_indices = []

# 対象とする列のリスト
target_cols = ['user1', 'user2']

for idx, row in fin_df.iterrows():
    # その行のユーザーたちの数値を取得
    current_values = set(row[target_cols].values)
    
    # 0（「あなた」の値など）は重複チェックから除外する場合
    current_values.discard(0)
    
    # すでに使われた数値と重なりがあるかチェック
    if not (current_values & used_nums):
        selected_indices.append(idx)
        used_nums.update(current_values)

# 重複のない行だけを抽出
unique_rows0_df = fin_df.loc[selected_indices]
# In[137]:
unique_rows0_df

a=unique_rows0_df.iloc[0,1]
b=unique_rows0_df.iloc[0,2]
c=unique_rows0_df.iloc[0,3]
st.text(f"あなたは{a}さん、{b}さん、{c}さんとマッチしました")

st.text(f"{a}さんの詳細")
d=mbti_df.iloc[a-1,0:4]
st.text(d)
st.text("")
st.text(f"{b}さんの詳細")
e=mbti_df.iloc[b-1,0:4]
st.text(e)
st.text(f"{c}さんの詳細")
f=mbti_df.iloc[c-1,0:4]
st.text(f)

# In[ ]:
