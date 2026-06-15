#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import itertools
import pprint
from sklearn.cluster import KMeans
import networkx as nx
import matplotlib.pyplot as plt
from IPython import embed


# In[3]:


mbti_df = pd.read_excel('C:\\Users\\sougo\\OneDrive\\Bookb.xlsx',index_col=0)
mbti_df


# In[4]:


print(' マッチしたい相手の性別を選択')
print(' 男: 女: 両方: から選択して入力')
sex=input('')
print(' \n希望日を入力　例:6/7')
print(' 6/7: 6/8: 6/9: から選択して入力')
day=input('')
print(' \n希望時間を選択')
print(' 昼: 夜: 一日: から選択して入力')
time=input('')
max1=('一日')
print(max1)
print(' \nMBTIを入力 例:ISTP')
mbti=input('')

print('\n以下は0～10で入力してください * 1と2の合計が10になるようにしてください')
print('例 1:似たテンションの人とマッチしたい 6  2:異なるテンションの人とマッチしたい 4')

print('\n質問A テンションについて')
print('1:似たテンションの人とマッチしたい割合 2:異なるテンションの人とマッチしたい割合')
print('1:似たテンションの人とマッチしたい割合')
tension=input('')
print(f"1:似たテンションの人とマッチしたい割合 {tension}割 ,2:異なるテンションの人とマッチしたい割合 {10-int(tension)}割")

print('\n質問B 考え方について')
print('1:似た考え方の人とマッチしたい割合 2:異なる考え方の人とマッチしたい割合')
print('1:似た考え方の人とマッチしたい割合')
idea=input('')
print(f"1:似たテンションの人とマッチしたい割合 {idea}割 ,2:異なるテンションの人とマッチしたい割合 {10-int(idea)}割")

print('\n質問C　判断について')
print('1:感情的な人とマッチしたい割合 2:論理的な人とマッチしたい割合')
print('1:感情的な人とマッチしたい割合')
judge=input('')
print(f"1:感情的な人とマッチしたい割合 {judge}割 ,2:論理的な人とマッチしたい割合 {10-int(judge)}割")

print('\n質問D 計画について')
print('1:一緒に計画を練りたい割合 2:その場の流れで遊びたい割合')
print('1:一緒に計画を練りたい割合')
plan=input('')
print(f"1:一緒に計画を練りたい割合 {plan}割 ,2:その場の流れで遊びたい割合 {10-int(plan)}割")


# In[5]:


a = mbti[0:4]


# In[6]:


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


# In[7]:


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


# In[8]:


d_df


# In[9]:


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


# In[10]:


x_df=["ISFP","ISFJ","ISTP","ISTJ","INFP","INFJ","INTP","INTJ","ESFP","ESFJ","ESTP","ESTJ","ENFP","ENFJ","ENTP","ENTJ"]
w_df=pd.DataFrame(x_df, columns = ["MBTI"])
# e_df=(ISFP,ISFJ,ISTP,ISTJ,INFP,INFJ,INTP,INTJ,ESFP,ESFJ,ESTP,ESTJ,ENFP,ENFJ,ENTP,ENTJ)
(e,i,n,s,f,t,j,p)=orientation(a,tension,idea,judge,plan)
e_df = scoring(e,i,n,s,f,t,j,p)
c_df=pd.DataFrame(e_df, columns = ["相手への評価"])
q_df=pd.concat([w_df,c_df],axis=1)
print(q_df)


# In[11]:


y_df['相手への評価'] = 0
for i in range(y_df.shape[0]):
    #print(y_df.iloc[i,3])
    mbti2 = y_df.iloc[i,3]
    y_df.iloc[i,8]=q_df[q_df['MBTI'] == mbti2].loc[:,'相手への評価'].values[0]
s_df=y_df.copy()
s_df


# In[12]:


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
            
s_df


# In[13]:


g_df=s_df.iloc[0:,8:]
g_df


# In[14]:


g_df.iloc[:10,:10]


# In[15]:


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

kid_df


# In[16]:


new_df=kid_df.where(kid_df>=25,"x")
new_df


# In[17]:


new_df.iloc[:10,:10]


# In[18]:


data23 = np.empty((0,1))
for j in range(len(new_df.index)):
    v3_df=new_df.iloc[0:,j:j+1]
    # print(v3_df.values.shape)
    data23 = np.vstack((data23,v3_df.values))
data23


# In[19]:


user_id = g_df.index
print(user_id)


# In[20]:


from itertools import product

node_list = user_id.to_list()
edge_list = [ (x,y) for x, y in product(node_list,node_list) ]


# In[21]:


datax=[]
datay=[]
for i in range(len(data23)):
    if data23[i]==("x"):
        datay.append(edge_list[i])
    else:
        datax.append(edge_list[i])


# In[22]:


kid_df.columns=kid_df.index


# In[23]:


G = nx.Graph(nx.from_pandas_adjacency(kid_df))


# In[24]:


nx.draw(G, with_labels = True)
plt.show()


# In[25]:


neighbors = list(G.neighbors(0))
sub_nodes = neighbors + [0]
subG = G.subgraph(sub_nodes)

cliques = nx.find_cliques(subG)

result = [c for c in cliques if len(c) == 5 and 0 in c]


# In[26]:


len(result)


# In[27]:


result


# In[28]:


id2pos = {}
for pos, id, in enumerate(g_df.index):
    id2pos[id] = pos
print(id2pos)


# In[29]:


dataq=[]
datar=[]
for g in result:
    for i,j in product(range(5),range(5)):
        if i != j:
            dataq.append(g_df.iat[id2pos[g[i]],id2pos[g[j]]])
n=20
for c in range(0,len(dataq),n):
    datar.append(dataq[c:c+n])
len(datar)


# In[30]:


datai=[]
for i in range(0,len(datar)):
    datai.append(sum(datar[i]))
len(datai)


# In[31]:


o1_df=pd.DataFrame(result, columns =['あなた','user1','user2','user3','user4'])
o2_df=pd.DataFrame(datar, columns =['user1からあなたへの評価','user2からあなたへの評価','user3からあなたへの評価','user4からあなたへの評価','あなたからuser1への評価','user2からuser1への評価','user3からuser1への評価','user4からuser1への評価','あなたからuser2への評価','user1からuser2への評価','user3からuser2への評価','user4からuser2への評価','あなたからuser3への評価','user1からuser3への評価','user2からuser3への評価','user4からuser3への評価','あなたからuser4への評価','user1からuser4への評価','user2からuser4への評価','user3からuser4への評価'])
o_df=pd.concat([o1_df,o2_df],axis=1)
o_df


# In[32]:


o_df.loc[:,['user2','user3','user4']]=np.sort(o_df.loc[:,['user2','user3','user4']].values)
gya_df=o_df.sort_values('user2')


# In[33]:


gya_df=gya_df.drop_duplicates(subset=['あなた','user1','user2','user3','user4'])


# In[ ]:





# In[34]:


gya_df['合計'] = 0
gya_df['分散'] = 0
gya_df['優劣値'] = 0
for i in range(gya_df.shape[0]):
    x = gya_df.iloc[i,5:25].values
    # print(np.sum(x),np.var(x))
    gya_df.iloc[i,25] = np.sum(x)
    gya_df.iloc[i,26] = np.var(x)
    gya_df.iloc[i,27] = (np.sum(x)-np.var(x))
fin_df=gya_df.sort_values('優劣値',ascending=False)
fin_df


# In[35]:


used_nums = set()
selected_indices = []

# 対象とする列のリスト
target_cols = ['user1', 'user2', 'user3', 'user4']

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


# In[36]:


unique_rows0_df


# In[ ]:


