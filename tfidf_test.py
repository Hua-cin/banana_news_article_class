# -*- coding: utf-8 -*-
import os
import pandas as pd
import math

# setting stop word list
stopword_path = r'./01_ref_data/stopword.txt'
stopword_list = []
with open(stopword_path, 'r', encoding = 'utf-8') as f_stop:
    for temp in f_stop.readlines():
        stopword_list.append(temp.replace('\n', ''))


# insert article
path1 = r'./04_tfidf_file/class_01'
file_list1 = os.listdir(path1)
# print("normal 文章數：{}".format(len(file_list)))
article1 = ''
i=0
for each_article in file_list1:
    article_path = path1 + "/" + each_article
    with open(article_path, 'r', encoding = 'utf-8') as f:
        temp = f.read()
        article1 +=temp
print(article1)

print("-----------------")

# insert article
path2 = r'./04_tfidf_file/class_02'
file_list2 = os.listdir(path2)
# print("normal 文章數：{}".format(len(file_list)))
article2 = ''
i=0
for each_article in file_list2:
    article_path = path2 + "/" + each_article
    with open(article_path, 'r', encoding = 'utf-8') as f:
        temp = f.read()
        article2 +=temp
print(article2)

print("-----------------")

# insert article
path3 = r'./04_tfidf_file/class_03'
file_list3 = os.listdir(path3)
# print("normal 文章數：{}".format(len(file_list)))
article3 = ''
i=0
for each_article in file_list3:
    article_path = path3 + "/" + each_article
    with open(article_path, 'r', encoding = 'utf-8') as f:
        temp = f.read()
        article3 +=temp
print(article3)

print("-----------------")

# insert article
path4 = r'./04_tfidf_file/class_04'
file_list4 = os.listdir(path4)
# print("normal 文章數：{}".format(len(file_list)))
article4 = ''
i=0
for each_article in file_list4:
    article_path = path4 + "/" + each_article
    with open(article_path, 'r', encoding = 'utf-8') as f:
        temp = f.read()
        article4 +=temp
print(article4)




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

t1 = word_count(article1)
print(t1)
t2 = word_count(article2)
print(t2)
t3 = word_count(article3)
print(t3)
t4 = word_count(article4)
print(t4)


# article_lst_dict = {}
# for j in article:
#     # print(j)
#     article_lst_dict[j] = word_count(j,article[j])

# t1 = word_count(text[0])
# t2 = word_count(text[1])
# t5 = word_count(text[5])
#
# # print(t1)
# print(word_count(text[0]))
# print(word_count(text[1]))
#
countlist = [t1, t2, t3, t4]
# print(countlist)
# #
def tf(word, count):
    return count[word] / sum(count.values())
def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)
def idf(word, count_list):
    return math.log(len(count_list) / (1+n_containing(word, count_list)))
def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)

ab = []
for i, count in enumerate(countlist):
    print("Top words in document {}".format(i+1))
    scores = {word: tfidf(word, count, countlist) for word in count}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    cd =[]
    for word, score in sorted_words[:50]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
        cd.append(word)
    ab.append(cd)

print(ab[0])
print(ab[1])
print(ab[2])
print(ab[3])

