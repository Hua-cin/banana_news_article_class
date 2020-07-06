# -*- coding: utf-8 -*-
'''

1. article class by K-means and use ckip word cut

'''

import os
import pandas as pd

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
