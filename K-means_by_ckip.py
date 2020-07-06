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
article = []
i=0
for each_article in file_list:
    article_path = path + "/" + each_article
    with open(article_path, 'r', encoding = 'utf-8') as f:
        temp = f.read()
        article.append("")
        # print(temp)
        for line in temp:
            article[i] += line
    i += 1
print(article)


# ckip word cut
from ckiptagger import WS, POS, NER

# define word_count function by ckip
def word_count(test_data):
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

    for i in ckip_word_list:
        ckip_dict[i[0]] =i [1]

    return (ckip_dict)


# all_article = ""
#
# for j in article:
#     all_article += j
article_dict = word_count(article[0])
print(article_dict)




# def getList(dict):
#     list = []
#     for key in dict.keys():
#         list.append(key)
#
#     return list
#
# def comb_key(dict_list, k):
#     list = []
#     for j in dict_list:
#         for i in j:
#             if i in list:
#                 pass
#             elif i in getList(j)[:k]:
#                 list.append(i)
#     return list
#

# # define combine key function for mutl article
# def comb_key(list, dict_list):
#     """
#     :param list: before list
#     :param dict_list: article dict
#     :return: after modify list
#     """
#     for j in dict_list:
#         for i in j:
#             if i in list:
#                 pass
#             else:
#                 list.append(i)
#     return list


# dd = pd.DataFrame(A_1, index=[0])
# print(dd)


# # import sklearn cluster
# from sklearn import cluster
#
# # KMeans 演算法
# kmeans_fit = cluster.KMeans(n_clusters = 5).fit(dd)
#
# # 印出分群結果
# cluster_labels = kmeans_fit.labels_
# print("分群結果：")
# print(cluster_labels)
# print("---")
