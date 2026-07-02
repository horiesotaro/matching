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


result0_df=(mbti_df[(mbti_df['性別'] == sex)&(mbti_df['希望日'] == day)&((mbti_df['希望時間'] == time))])
result1_df=(mbti_df[(mbti_df['希望日'] == day)&((mbti_df['希望時間'] == time))])

if (sex=='両方'):
    y_df=result1_df
else:
    y_df=result0_df
d_df=y_df.copy()

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
a


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
bbq


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


w_df=s_df.iloc[0:,8:]
w_df.columns=w_df.index
kids_df=w_df



# In[93]:


import numpy as np
import pandas as pd

df = w_df.copy()

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

# In[94]:




# In[128]:




# In[95]:

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

# 結果の確認



# In[96]:







# In[98]:


data23 = np.empty((0,1))
for j in range(len(new_df.index)):
    v3_df=new_df.iloc[0:,j:j+1]
    # print(v3_df.values.shape)
    data23 = np.vstack((data23,v3_df.values))



# In[99]:


user_id = w_df.index


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
    if 0 in c and len(c) >= 5:
        for sub in combinations(c, 5):
            if 0 in sub:
                result.append(list(sorted(sub)))
result

id2pos = {}
for pos, id, in enumerate(w_df.index):
    id2pos[id] = pos
print(id2pos)


# In[103]:
dataq=[]
datar=[]
for g in result:
    for i,j in product(range(5),range(5)):
        if i != j:
            dataq.append(w_df.iat[id2pos[g[i]],id2pos[g[j]]])
n=20
for c in range(0,len(dataq),n):
    datar.append(dataq[c:c+n])






# In[66]:

datai=[]
for i in range(0,len(datar)):
    datai.append(sum(datar[i]))




# In[71]:


o1_df=pd.DataFrame(result, columns =['あなた','user1','user2','user3','user4'])
o2_df=pd.DataFrame(datar, columns =['user1からあなたへの評価','user2からあなたへの評価','user3からあなたへの評価','user4からあなたへの評価','あなたからuser1への評価','user2からuser1への評価','user3からuser1への評価','user4からuser1への評価','あなたからuser2への評価','user1からuser2への評価','user3からuser2への評価','user4からuser2への評価','あなたからuser3への評価','user1からuser3への評価','user2からuser3への評価','user4からuser3への評価','あなたからuser4への評価','user1からuser4への評価','user2からuser4への評価','user3からuser4への評価'])
o_df=pd.concat([o1_df,o2_df],axis=1)
o_df
o_df.loc[:,['user2','user3','user4']]=np.sort(o_df.loc[:,['user2','user3','user4']].values)
gya_df=o_df.sort_values('user2')
# In[72]:
gya_df=gya_df.drop_duplicates(subset=['あなた','user1','user2','user3','user4'])

import numpy as np
gya_df['合計'] = 0.0
gya_df['分散'] = 0.0
gya_df['優劣値'] = 0.0
for i in range(gya_df.shape[0]):
    x = gya_df.iloc[i,5:25].values
    # print(np.sum(x),np.var(x))
    gya_df.iloc[i,25] = float(np.sum(x))
    gya_df.iloc[i,26] = float(np.var(x))
    gya_df.iloc[i,27] = float((np.sum(x)-np.var(x)))
fin_df=gya_df.sort_values('優劣値',ascending=False)
fin_df

dataw=[]
for i in range(0,len(fin_df)):
    if((max(fin_df.iloc[i,5:9])>=24)and(max(fin_df.iloc[i,9:13])>=24)and(max(fin_df.iloc[i,13:17])>=24)and(max(fin_df.iloc[i,17:21])>=24)and(max(fin_df.iloc[i,21:25])>=24)
    and(max(fin_df.iloc[i,9],fin_df.iloc[i,13],fin_df.iloc[i,17],fin_df.iloc[i,21])>=24)and(max(fin_df.iloc[i,5],fin_df.iloc[i,14],fin_df.iloc[i,18],fin_df.iloc[i,22])>=24)
    and(max(fin_df.iloc[i,6],fin_df.iloc[i,10],fin_df.iloc[i,19],fin_df.iloc[i,23])>=24)and(max(fin_df.iloc[i,7],fin_df.iloc[i,11],fin_df.iloc[i,15],fin_df.iloc[i,24])>=24)
    and(max(fin_df.iloc[i,8],fin_df.iloc[i,12],fin_df.iloc[i,16],fin_df.iloc[i,20])>=24)):
        dataw.append(fin_df.iloc[i,:])
      
      
last_df=pd.DataFrame(dataw)
cols = last_df.columns.difference([ '分散', '優劣値'])

last_df[cols] = last_df[cols].round().astype(int)

used_nums = set()
selected_indices = []

# 対象とする列のリスト
target_cols = ['user1', 'user2', 'user3', 'user4']

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
unique_rows_df = last_df.loc[selected_indices]
unique_rows_df


a=unique_rows_df.iloc[0,1]
b=unique_rows_df.iloc[0,2]
c=unique_rows_df.iloc[0,3]
d=unique_rows_df.iloc[0,4]
st.text(f"あなたは{a}さん、{b}さん、{c}さん,{d}さんとマッチしました")

st.text(f"{a}さんの詳細")
e=mbti_df.iloc[a-1,0:4]
st.text(e)
st.text("")
st.text(f"{b}さんの詳細")
f=mbti_df.iloc[b-1,0:4]
st.text(f)
st.text(f"{c}さんの詳細")
g=mbti_df.iloc[c-1,0:4]
st.text(g)
st.text(f"{d}さんの詳細")
h=mbti_df.iloc[d-1,0:4]
st.text(h)
