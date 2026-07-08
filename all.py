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

if people='3人':
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
elif people='4人':
clique_result = process_clique_matching_4ppl(kid_df, w_df, mbti_df, start_node=0)

# 結果の表示
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
    st.text("条件に合致する4人グループが見つかりませんでした。")
elif people='5人':
# 関数の呼び出し
clique_5_result = process_clique_matching_5ppl(kid_df, w_df, mbti_df, start_node=0)

# 結果の表示
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
    st.text("条件に合致する5人グループが見つかりませんでした。")
else:
st.text("6人以上には対応していません")




import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

def process_matching_and_get_details(g_df, mbti_df, data23, start_node=0):
    """
    ネットワーク分析から最適なマッチングペアを抽出し、その詳細情報を取得する関数。
    
    Parameters:
    -----------
    g_df : pandas.DataFrame
        ユーザー間の評価値を持つデータフレーム（インデックスがユーザーID）
    mbti_df : pandas.DataFrame
        各ユーザーの詳細（MBTIなど）が格納されたデータフレーム
    data23 : list
        エッジ（関係性）の有無や種類を表すフラグのリスト
    start_node : int or str
        BFS（幅優先探索）の起点となる「あなた」のノードID（デフォルト: 0）
        
    Returns:
    --------
    tuple or None
        (user1_id, user2_id, user1_details, user2_details) のタプル。
        マッチング対象が見つからなかった場合は None。
    """
    # ----------------------------------------------------
    # 1. グラフの構築
    # ----------------------------------------------------
    user_id = g_df.index
    node_list = user_id.to_list()
    
    # 重複のないエッジリストの作成 (自分自身へのエッジを除く)
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
    
    # (オプション) グラフを描画したい場合はコメントアウトを解除してください
    # nx.draw(G, with_labels=True)
    # plt.show()
    
    # ----------------------------------------------------
    # 2. BFS（幅優先探索）による階層関係の抽出
    # ----------------------------------------------------
    ab = dict(enumerate(nx.bfs_layers(G, [start_node])))
    
    # 必要なレイヤー（1層目と2層目）が存在することを確認
    ad = ab.get(1, [])
    ac = ab.get(2, [])
    
    # ----------------------------------------------------
    # 3. 三者関係（パターンyとパターンp）の抽出
    # ----------------------------------------------------
    # パターン1: あなた(start_node) -> ad -> ac -> あなた(start_node) の循環関係
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
                
    # パターン2: あなた(start_node) -> adの2人が相互に繋がっている関係
    datap = set()
    for m in ad:
        for n in ad:
            neighbor1 = list(G[m].keys())
            neighbor2 = list(G[n].keys())
            if (m != n) and (m in neighbor2) and (n in neighbor1):
                datap.add((start_node, min(m, n), max(m, n)))
                
    datavv = datay + list(datap)
    
    if not datavv:
        print("マッチング候補が見つかりませんでした。")
        return None
        
    # ----------------------------------------------------
    # 4. 評価データの集計とスコア化
    # ----------------------------------------------------
    id2pos = {id_val: pos for pos, id_val in enumerate(g_df.index)}
    
    dataq = []
    for g in datavv:
        for i, j in product(range(3), range(3)):
            if i != j:
                dataq.append(g_df.iat[id2pos[g[i]], id2pos[g[j]]])
                
    n = 6
    datar = [dataq[c:c+n] for c in range(0, len(dataq), n)]
    
    # データフレームの作成と評価値の計算
    o1_df = pd.DataFrame(datavv, columns=['あなた', 'user1', 'user2'])
    o2_df = pd.DataFrame(datar, columns=[
        'user1からあなたへの評価', 'user2からあなたへの評価', 
        'あなたからuser1への評価', 'user2からuser1への評価', 
        'あなたからuser2への評価', 'user1からuser2への評価'
    ])
    o_df = pd.concat([o1_df, o2_df], axis=1)
    
    # 数値計算 (ベクトル化処理で高速化)
    eval_values = o_df.iloc[:, 3:9].values
    o_df['合計'] = np.sum(eval_values, axis=1)
    o_df['分散'] = np.var(eval_values, axis=1)
    o_df['優劣値'] = o_df['合計'] - o_df['分散']
    
    # ----------------------------------------------------
    # 5. 重複削除と最適な組み合わせの選択
    # ----------------------------------------------------
    # スコア順にソート
    fin_df = o_df.sort_values('優劣値', ascending=False).copy()
    
    # ユーザーの組み合わせ重複を削除
    user_cols = ["user1", "user2"]
    fin_df["group_key"] = fin_df[user_cols].apply(lambda x: tuple(sorted(x)), axis=1)
    fin_df = fin_df.drop_duplicates(subset="group_key").drop(columns="group_key")
    
    # 完全に一意なユーザーの組み合わせを抽出
    used_nums = set()
    selected_indices = []
    
    for idx, row in fin_df.iterrows():
        current_values = set(row[user_cols].values)
        current_values.discard(start_node)  # 起点ノードは重複カウントから除外
        
        if not (current_values & used_nums):
            selected_indices.append(idx)
            used_nums.update(current_values)
            
    unique_rows0_df = fin_df.loc[selected_indices]
    
    if unique_rows0_df.empty:
        return None
        
    # ----------------------------------------------------
    # 6. マッチング上位1組の詳細情報を抽出
    # ----------------------------------------------------
    best_match = unique_rows0_df.iloc[0]
    user1_id = best_match['user1']
    user2_id = best_match['user2']
    
    # mbti_df から詳細情報を取得 (インデックス参照。データ構造に合わせて要微調整)
    # 元コードの iloc[id-1, 0:4] に則っています
    user1_details = mbti_df.iloc[int(user1_id) - 1, 0:4]
    user2_details = mbti_df.iloc[int(user2_id) - 1, 0:4]
    
    return user1_id, user2_id, user1_details, user2_details



import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product, combinations

def process_clique_matching_4ppl(kid_df, w_df, mbti_df, start_node=0):
    """
    隣接行列から4人の完全グラフ(クリーク)を検出し、相互評価スコアと詳細情報を取得する関数。
    
    Parameters:
    -----------
    kid_df : pandas.DataFrame
        ネットワーク構築用の隣接行列（インデックスとカラムがユーザーID）
    w_df : pandas.DataFrame
        ユーザー間の詳細な評価値を持つデータフレーム
    mbti_df : pandas.DataFrame
        各ユーザーの詳細（MBTIなど）が格納されたデータフレーム
    start_node : int or str
        起点となる「あなた」のノードID（デフォルト: 0）
        
    Returns:
    --------
    tuple or None
        (user1_id, user2_id, user3_id, detail_a, detail_b, detail_c) のタプル。
        条件に合うマッチングが見つからなかった場合は None。
    """
    # 1. 隣接行列からグラフを構築
    kid_df.columns = kid_df.index
    G = nx.Graph(nx.from_pandas_adjacency(kid_df))
    
    # (オプション) グラフを描画したい場合はコメントアウトを解除してください
    # nx.draw(G, with_labels=True)
    # plt.show()
    
    # 2. クリーク探索（あなた(0)を含み、4人以上の完全グラフから4人の組み合わせを抽出）
    cliques = nx.find_cliques(G)
    result = []
    for c in cliques:
        if start_node in c and len(c) >= 4:
            for sub in combinations(c, 4):
                if start_node in sub:
                    result.append(list(sorted(sub)))
                    
    if not result:
        print("4人グループの候補(クリーク)が見つかりませんでした。")
        return None

    # 3. ユーザーIDから位置(インデックス)へのマッピング
    id2pos = {id_val: pos for pos, id_val in enumerate(w_df.index)}
    
    # 4. 4人同士の全対全(12通り)の評価値データを抽出
    dataq = []
    for g in result:
        for i, j in product(range(4), range(4)):
            if i != j:
                dataq.append(w_df.iat[id2pos[g[i]], id2pos[g[j]]])
                
    n = 12
    datar = [dataq[c:c+n] for c in range(0, len(dataq), n)]
    
    # 5. データフレームの結合と重複削除
    o1_df = pd.DataFrame(result, columns=['あなた', 'user1', 'user2', 'user3'])
    o2_df = pd.DataFrame(datar, columns=[
        'user1からあなたへの評価', 'user2からあなたへの評価', 'user3からあなたへの評価',
        'あなたからuser1への評価', 'user2からuser1への評価', 'user3からuser1への評価',
        'あなたからuser2への評価', 'user1からuser2への評価', 'user3からuser2への評価',
        'あなたからuser3への評価', 'user1からuser3への評価', 'user2からuser3への評価'
    ])
    o_df = pd.concat([o1_df, o2_df], axis=1)
    
    # 重複判定のためにソートして一意にする
    o_df.loc[:, ['user2', 'user3']] = np.sort(o_df.loc[:, ['user2', 'user3']].values)
    gya_df = o_df.sort_values('user2').drop_duplicates(subset=['あなた', 'user1', 'user2', 'user3']).copy()
    
    # 6. ベクトル化処理による合計・分散・優劣値の計算
    eval_values = gya_df.iloc[:, 4:16].values
    gya_df['合計'] = np.sum(eval_values, axis=1)
    gya_df['分散'] = np.var(eval_values, axis=1)
    gya_df['優劣値'] = gya_df['合計'] - gya_df['分散']
    
    # 優劣値順にソート
    fin_df = gya_df.sort_values('優劣値', ascending=False)
    
    # 7. 各評価軸の「最大値が25以上」という特定条件でフィルタリング
    dataw = []
    for i in range(len(fin_df)):
        row = fin_df.iloc[i]
        # 各ユーザーへの評価・被評価の組み合わせ条件
        if (max(row[4:7]) >= 25 and max(row[7:10]) >= 25 and max(row[10:13]) >= 25 and max(row[13:16]) >= 25 and
            max(row[7], row[10], row[13]) >= 25 and max(row[4], row[11], row[14]) >= 25 and
            max(row[5], row[8], row[15]) >= 25 and max(row[6], row[9], row[12]) >= 25):
            dataw.append(row)
            
    if not dataw:
        print("評価値の条件(>=25)を満たすグループが見つかりませんでした。")
        return None
        
    last_df = pd.DataFrame(dataw)
    cols = last_df.columns.difference(['分散', '優劣値'])
    last_df[cols] = last_df[cols].round().astype(int)
    
    # 8. 重複のない一意なユーザーの組み合わせを抽出 (user1, user2, user3)
    used_nums = set()
    selected_indices = []
    target_cols = ['user1', 'user2', 'user3']
    
    for idx, row in last_df.iterrows():
        current_values = set(row[target_cols].values)
        current_values.discard(start_node) # 起点ノードは除外
        
        if not (current_values & used_nums):
            selected_indices.append(idx)
            used_nums.update(current_values)
            
    unique_rows0_df = last_df.loc[selected_indices]
    
    if unique_rows0_df.empty:
        return None
        
    # 9. 最上位1組のマッチング結果と詳細情報を取得
    best_match = unique_rows0_df.iloc[0]
    a = best_match['user1']
    b = best_match['user2']
    c = best_match['user3']
    
    # mbti_dfから詳細情報を取得
    detail_a = mbti_df.iloc[int(a) - 1, 0:4]
    detail_b = mbti_df.iloc[int(b) - 1, 0:4]
    detail_c = mbti_df.iloc[int(c) - 1, 0:4]
    
    return a, b, c, detail_a, detail_b, detail_c



import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product, combinations

def process_clique_matching_5ppl(kid_df, w_df, mbti_df, start_node=0):
    """
    隣接行列から5人の完全グラフ(クリーク)を検出し、20通りの相互評価スコアから
    最適な組み合わせを取得して詳細情報を返す関数。
    
    Parameters:
    -----------
    kid_df : pandas.DataFrame
        ネットワーク構築用の隣接行列（インデックスとカラムがユーザーID）
    w_df : pandas.DataFrame
        ユーザー間の詳細な評価値を持つデータフレーム
    mbti_df : pandas.DataFrame
        各ユーザーの詳細（MBTIなど）が格納されたデータフレーム
    start_node : int or str
        起点となる「あなた」のノードID（デフォルト: 0）
        
    Returns:
    --------
    tuple or None
        (user1, user2, user3, user4, detail_a, detail_b, detail_c, detail_d) のタプル。
        条件に合うマッチングが見つからなかった場合は None。
    """
    # 1. 隣接行列からグラフを構築
    kid_df.columns = kid_df.index
    G = nx.Graph(nx.from_pandas_adjacency(kid_df))
    
    # (オプション) グラフを描画したい場合はコメントアウトを解除してください
    # nx.draw(G, with_labels=True)
    # plt.show()
    
    # 2. クリーク探索（あなた(0)を含み、5人以上の完全グラフから5人の組み合わせを抽出）
    cliques = nx.find_cliques(G)
    result = []
    for c in cliques:
        if start_node in c and len(c) >= 5:
            for sub in combinations(c, 5):
                if start_node in sub:
                    result.append(list(sorted(sub)))
                    
    if not result:
        print("5人グループの候補(クリーク)が見つかりませんでした。")
        return None

    # 3. ユーザーIDから位置(インデックス)へのマッピング
    id2pos = {id_val: pos for pos, id_val in enumerate(w_df.index)}
    
    # 4. 5人同士の全対全(20通り)の評価値データを抽出
    dataq = []
    for g in result:
        for i, j in product(range(5), range(5)):
            if i != j:
                dataq.append(w_df.iat[id2pos[g[i]], id2pos[g[j]]])
                
    n = 20
    datar = [dataq[c:c+n] for c in range(0, len(dataq), n)]
    
    # 5. データフレームの結合と重複削除
    o1_df = pd.DataFrame(result, columns=['あなた', 'user1', 'user2', 'user3', 'user4'])
    o2_df = pd.DataFrame(datar, columns=[
        'user1からあなたへの評価', 'user2からあなたへの評価', 'user3からあなたへの評価', 'user4からあなたへの評価',
        'あなたからuser1への評価', 'user2からuser1への評価', 'user3からuser1への評価', 'user4からuser1への評価',
        'あなたからuser2への評価', 'user1からuser2への評価', 'user3からuser2への評価', 'user4からuser2への評価',
        'あなたからuser3への評価', 'user1からuser3への評価', 'user2からuser3への評価', 'user4からuser3への評価',
        'あなたからuser4への評価', 'user1からuser4への評価', 'user2からuser4への評価', 'user3からuser4への評価'
    ])
    o_df = pd.concat([o1_df, o2_df], axis=1)
    
    # 順序を揃えて重複を排除
    o_df.loc[:, ['user2', 'user3', 'user4']] = np.sort(o_df.loc[:, ['user2', 'user3', 'user4']].values)
    gya_df = o_df.sort_values('user2').drop_duplicates(subset=['あなた', 'user1', 'user2', 'user3', 'user4']).copy()
    
    # 6. NumPyによる合計・分散・優劣値の一括計算（高速化）
    eval_values = gya_df.iloc[:, 5:25].values  # 評価データの列(5列目〜24列目)
    gya_df['合計'] = np.sum(eval_values, axis=1)
    gya_df['分散'] = np.var(eval_values, axis=1)
    gya_df['優劣値'] = gya_df['合計'] - gya_df['分散']
    
    # 優劣値順にソート
    fin_df = gya_df.sort_values('優劣値', ascending=False)
    
    # 7. 評価スコアが閾値（>=24）を満たしているかチェック
    dataw = []
    for i in range(len(fin_df)):
        row = fin_df.iloc[i]
        
        # 縦横の各評価軸に対するmaxチェック（元の複雑なスライス・条件をそのまま再現しています）
        if (max(row[5:9]) >= 24 and max(row[9:13]) >= 24 and max(row[13:17]) >= 24 and max(row[17:21]) >= 24 and max(row[21:25]) >= 24 and
            max(row[9], row[13], row[17], row[21]) >= 24 and
            max(row[5], row[14], row[18], row[22]) >= 24 and
            max(row[6], row[10], row[19], row[23]) >= 24 and
            max(row[7], row[11], row[15], row[24]) >= 24 and
            max(row[8], row[12], row[16], row[20]) >= 24):
            dataw.append(row)
            
    if not dataw:
        print("評価値の条件(>=24)を満たす5人グループが見つかりませんでした。")
        return None
        
    last_df = pd.DataFrame(dataw)
    cols = last_df.columns.difference(['分散', '優劣値'])
    last_df[cols] = last_df[cols].round().astype(int)
    
    # 8. 重複のない一意なユーザーの組み合わせを抽出
    used_nums = set()
    selected_indices = []
    target_cols = ['user1', 'user2', 'user3', 'user4']
    
    for idx, row in last_df.iterrows():
        current_values = set(row[target_cols].values)
        current_values.discard(start_node)
        
        if not (current_values & used_nums):
            selected_indices.append(idx)
            used_nums.update(current_values)
            
    unique_rows_df = last_df.loc[selected_indices]
    
    if unique_rows_df.empty:
        return None
        
    # 9. 最上位のマッチング結果を取得
    best_match = unique_rows_df.iloc[0]
    a = best_match['user1']
    b = best_match['user2']
    c = best_match['user3']
    d = best_match['user4']
    
    # mbti_df から各ユーザーの詳細（MBTI等）を取得
    detail_a = mbti_df.iloc[int(a) - 1, 0:4]
    detail_b = mbti_df.iloc[int(b) - 1, 0:4]
    detail_c = mbti_df.iloc[int(c) - 1, 0:4]
    detail_d = mbti_df.iloc[int(d) - 1, 0:4]
    
    return a, b, c, d, detail_a, detail_b, detail_c, detail_d
