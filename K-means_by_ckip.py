# -*- coding: utf-8 -*-
'''

1. article class by K-means and use ckip word cut

'''

import os
import pandas as pd

class_1 = ['泰國', '美人蕉', '農場', '大埔', '春節', '飆到', '元旦', '拜拜', '陳文嬋', '看漲', '小偷', '黃旭磊', '創下', '椪柑', '飆破', '下滑', '黑糖', '芭比', '耕堡', '江志雄', '成本', '上漲', '十五', '蘇茂祥', '農曆', '整體', '附加', '藝術', '1996年', '有如']
class_2 = ['設施', '其次', '搶收', '水稻', '現金', '防颱', '農損', '敏豆', '氣象', '公告', '損害', '黃化', '作物', '災情', '來襲', '估計', '預估', '信義鄉', '陳依秀', '恆春', '半島', '其餘', '清晨', '產物', '下田', '落果', '香菜', '勘查', '16日', '金額']
class_3 = ['澱粉', '蛋糕', '抗性', '冰箱', '早餐', '纖維', '豐富', '攝取', '含有', '減肥', '製作', '成分', '體重', '含量', '熱量', '彭素娟', '泡麵', '脂肪', '奇異果', '血清素', '維生素', '氧化', '洋芋片', '期刊', '產生', '早上', '牛奶', '冰品', '營養師', '運動']
class_4 = ['收入', '植株', '保險', '投保', '理賠', '黃葉病', '荔枝', '真菌', '太平', '認養', '針對', '通路', '勘損', '羅欣貞', '舉辦', '韓國瑜', '保費', '中壽', '產險', '賴正鎰', '壟斷', '活動', '7.5億', '潘孟安', '補助', '民進黨', '市長', '總農家', '空拍', '公平會']

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

# for x in article_lst_dict:
#     print(x,article_lst_dict[x])

# def getList(dict):
#     list = []
#     for key in dict.keys():
#         list.append(key)
#
#     return list
#
# def comb_key(list, dict_list, k):
#
#     for j in dict_list:
#         if j in list:
#             pass
#         elif j in getList(j)[:k]:
#             list.append(i)
#     return list


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

dd = pd.DataFrame(data=content,columns=columns)

for i in range(dd.shape[0]):
    if dd["香蕉"][i] == 0:
        dd.iloc[i, 1:] = dd.iloc[i, 1:] / 100
    else:
        dd.iloc[i,1:] = dd.iloc[i,1:] / dd["香蕉"][i]
# test.iloc[0,1:] = test.iloc[0,1:]/test["A"][0]

dd = dd.set_index("article_name")
dd = dd.sort_index(axis=0)
dd = dd.fillna(value=0)
print(dd)

# import sklearn cluster
from sklearn import cluster

# KMeans 演算法
kmeans_fit = cluster.KMeans(n_clusters = 3).fit(dd)

# 印出分群結果
cluster_labels = kmeans_fit.labels_
print("分群結果：")
print(cluster_labels)
print("---")
