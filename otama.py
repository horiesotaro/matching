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
    tension=st.selectbox('1:似たテンションの人とマッチしたい割合',range(0,10))
    idea=st.selectbox('2:似た考えの人とマッチしたい割合',range(0,10))
    judge=st.selectbox('3:感情的な人とマッチしたい割合',range(0,10))
    plan=st.selectbox('4:一緒に計画を立てたいしたい割合',range(0,10))
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


# In[132]:


(320,76) in datax


# In[102]:


from itertools import product

# Graphオブジェクトの作成
G = nx.DiGraph()

node_list = user_id.to_list()
edge_list = [ (x,y) for x, y in product(node_list,node_list) if x != y]

# print(edge_list)
print(type(node_list[0]))
# nodeデータの追加
G.add_nodes_from(node_list)
G.add_edges_from(datax)
nx.draw(G, with_labels = True)
plt.show()


# In[103]:


import networkx as nx
ab=dict(enumerate(nx.bfs_layers(G,[0])))
ac=ab[2]
ad=ab[1]
if(len(ab)==4):
    ae=ab[3]



# In[124]:





# In[123]:


datayy=[]
for m in ad:
    neighbor1=list(G[m].keys())


# In[117]:


import networkx as nx
ab=dict(enumerate(nx.bfs_layers(G,[0])))
ac=ab[2]
ad=ab[1]
if(len(ab)==4):
    ae=ab[3]

datav=[]
for n in ac:
    neighbor=list(G[n].keys())
    if 0 in neighbor:
        datav.append(n)
datay=[]
for m in ad:
    neighbor1=list(G[m].keys())
    for n in neighbor1:
        if n in datav:
            datay.append((0,m,n))



# In[106]:


datap = set()

for m in ad:
    for n in ad:
        if m != n:
            datap.add((0, min(m, n), max(m, n)))

datap = list(datap)



# In[61]:


datavv=datay+datap


# In[63]:





# In[ ]:





# In[26]:





# In[27]:


id2pos = {}
for pos, id, in enumerate(g_df.index):
    id2pos[id] = pos



# In[ ]:





# In[64]:


dataq=[]
datar=[]
for g in datavv:
    for i,j in product(range(3),range(3)):
        if i != j:
            dataq.append(g_df.iat[id2pos[g[i]],id2pos[g[j]]])
n=6
for c in range(0,len(dataq),n):
    datar.append(dataq[c:c+n])



# In[65]:


len(dataq)


# In[66]:


datai=[]
for i in range(0,len(datar)):
    datai.append(sum(datar[i]))



# In[71]:


o1_df=pd.DataFrame(datavv, columns =['あなた','user1','user2'])
o2_df=pd.DataFrame(datar, columns =['use1からあなたへの評価','use2からあなたへの評価','あなたからuser1への評価','user2からuser1への評価','あなたからuser2への評価','user1からuser2への評価'])
o_df=pd.concat([o1_df,o2_df],axis=1)


# In[72]:


o_df['合計'] = 0
o_df['分散'] = 0
o_df['優劣値'] = 0
# 【追加】10番目と11番目の列を、あらかじめ小数（float）を受け付ける型に変えておく
o_df.iloc[:, 10] = o_df.iloc[:, 10].astype(float)
o_df.iloc[:, 11] = o_df.iloc[:, 11].astype(float)
for i in range(o_df.shape[0]):
    x = o_df.iloc[i,3:9].values
    # print(np.sum(x),np.var(x))
    o_df.iloc[i,9] = np.sum(x)
    o_df.iloc[i,10] = np.var(x)
    o_df.iloc[i,11] = (np.sum(x)-np.var(x))
fin_df=o_df.sort_values('優劣値',ascending=False)



# In[75]:


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


unique_rows0_df.iloc[:10,:]


# In[ ]:








