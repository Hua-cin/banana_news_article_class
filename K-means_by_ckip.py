# -*- coding: utf-8 -*-
'''

1. article class by K-means and use ckip word cut

'''

import os
import pandas as pd
import math

class_1 = ['泰國', '農場', '美人蕉', '大埔', '春節', '飆到', '飆破', '小偷', '陳文嬋', '看漲', '元旦', '86', '拜拜', '黃旭磊', '創下', '椪柑', '黑糖', '芭比', '75', '耕堡', '江志雄', '下滑', '成本', '上漲', '十五', '蘇茂祥', '農曆', '無語', '蒼天', '不敷', '豐收', '大增', '甜度', '杜鵑', '飆高', '七十三', '工人', '缺貨', '覬覦', '居民', '減半', '尾聲', '產地價', '九十七', '異常', '1996年', '有如', '鍍金', '敬果', '鬆軟']
class_2 = ['設施', '搶收', '尼莎', '防颱', '水稻', '農損', '氣象', '白鹿', '損害', '黃化', '敏豆', '來襲', '作物', '災情', '預估', '估計', '清晨', '產物', '下田', '16日', '恆春', '半島', '香菜', '勘查', '落果', '信義鄉', '陳依秀', '金額', '台東', '喜憂', '參半', '預測', '即將', '跌破', '12月', '300多', '換算', '順利', '大卡車', '小番茄', '風浪', '光合作用', '黃淑莉', '5點', '台中市', '11%', '番石榴', '鄉公所', '長流村', '受風面']
class_3 = ['澱粉', '蛋糕', '抗性', '冰箱', '早餐', '纖維', '攝取', '含有', '豐富', '減肥', '製作', '成分', '體重', '熱量', '含量', '彭素娟', '脂肪', '奇異果', '維生素', '氧化', '血清素', '泡麵', '期刊', '早上', '產生', '酵素', '營養師', '運動', '牛奶', '冰品', '疾病', '外皮', '葡萄籽', '洋芋片', '研究', '食物', '富含', '食用', '補充', '果肉', '血糖', '減重', '野蓮', '解決', '地雷', '嘗試', '鋁箔紙', '吃起來', 'PO', '張存薇']
class_4 = ['收入', '植株', '保險', '投保', '理賠', '黃葉病', '荔枝', '太平', '認養', '真菌', '舉辦', '針對', '羅欣貞', '通路', '勘損', '7.5億', '賴正鎰', '韓國瑜', '壟斷', '產險', '保費', '中壽', '潘孟安', '補助', '市長', 'OIRSA', '辦公室', '哥倫比亞', '採果', '公平會', '空拍', '民進黨', '總農家', '陳吉仲', '簽約', '瓜地馬拉', '國合會', '邀請', '共同', '全球', '簡良智', '荔枝節', '聯合', '東京', '保險費', '啟動', '發揮', '公益', '社會', '期間']

# setting stop word list
stopword_path = r'./01_ref_data/stopword.txt'
stopword_list = []
with open(stopword_path, 'r', encoding = 'utf-8') as f_stop:
    for temp in f_stop.readlines():
        stopword_list.append(temp.replace('\n', ''))
print(stopword_list)


# insert article
path = r'./02_data_warehouse'
file_list = os.listdir(path)
print("normal 文章數：{}".format(len(file_list)))
article = {}
i=0
for each_article in file_list:
    article_path = path + "/" + each_article
    with open(article_path, 'r', encoding = 'utf-8') as f:
        temp = f.read()
        article[each_article] = temp
print(article)


# ckip word cut
from ckiptagger import WS, POS, NER

# define word_count function by ckip
def word_count(name ,test_data):
    """
    :param test_data: article string
    :return: ckip dict
    """
    ws = WS("../data")
    ws_results = ws([test_data])
    ckip_word_count = {}

    for i in ws_results[0]:
        if i in ckip_word_count:
            ckip_word_count[i] += 1
        else:
            ckip_word_count[i] = 1

    ckip_word_list = [(k, ckip_word_count[k]) for k in ckip_word_count if (len(k)>1) and (k not in stopword_list)]
    ckip_word_list.sort(key=lambda item: item[1], reverse=True)

    # print(ckip_word_list)
    ckip_dict = {}
    ckip_dict["article_name"] = name

    for i in ckip_word_list:
        ckip_dict[i[0]] =i [1]

    return (ckip_dict)

article_lst_dict = {}
for j in article:
    # print(j)
    article_lst_dict[j] = word_count(j,article[j])

for x in article_lst_dict:
    print(x,article_lst_dict[x])

def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)

    return list

def comb_key(list, dict_list, k):

    for j in dict_list:
        if j in list:
            pass
        elif j in getList(j)[:k]:
            list.append(i)
    return list


# define combine key function for mutl article
def comb_key(list, dict_list):
    """
    :param list: before list
    :param dict_list: article dict
    :return: after modify list
    """
    for j in dict_list:
        if j in list:
            pass
        else:
            list.append(j)
    return list

# produce columns
columns = ["article_name"]
content=[]
for y in article_lst_dict:
    comb_key(columns, article_lst_dict[y])
    content.append(article_lst_dict[y])



print(columns)
print(content)

dict = {}
dict['article_name']="01"
for i in class_1:
    dict[i]=1
content.append(dict)
comb_key(columns, dict)

dict = {}
dict['article_name']="02"
for i in class_2:
    dict[i]=1
content.append(dict)
comb_key(columns, dict)

dict = {}
dict['article_name']="03"
for i in class_3:
    dict[i]=1
content.append(dict)
comb_key(columns, dict)

dict = {}
dict['article_name']="04"
for i in class_4:
    dict[i]=1
content.append(dict)
comb_key(columns, dict)


dd = pd.DataFrame(data=content,columns=columns)
dd = dd.fillna(value=0)
for i in range(dd.shape[0]):
    if dd["香蕉"][i] == 0:
        dd.iloc[i, 1:] = dd.iloc[i, 1:] * 1000
    else:
        dd.iloc[i,1:] = dd.iloc[i,1:] / dd["香蕉"][i]


dd = dd.set_index("article_name")
dd = dd.sort_index(axis=0)

# dd["\n"] = dd["\n"]*0
# dd['。\n'] = dd['。\n']*0

print(dd)

# import sklearn cluster
from sklearn import cluster

# KMeans 演算法
kmeans_fit = cluster.KMeans(n_clusters = 4).fit(dd)

# 印出分群結果
cluster_labels = kmeans_fit.labels_
print("分群結果：")
print(cluster_labels)
print("---")


# 使用pandas 將資料轉為csv檔
dd.to_csv('./dd.csv', index=0, encoding="utf_8_sig")