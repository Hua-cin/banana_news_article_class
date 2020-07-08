# -*- coding: utf-8 -*-
'''
1.word cut
    1.1.news word cut (jieba) from source folder './02_data_warehouse/[related, no_related]
    1.2.use stop word list form file './01_ref_data/stopword.txt'
    1.3.use mydict list from file './01_ref_data/mydict.txt'
2.
'''

import os
import jieba
import math
import pandas as pd
# import sklearn cluster
from sklearn import cluster
import re

def main():



    # insert related source data----------------------
    related_path = r'./02_data_warehouse/related'
    related_file_list = os.listdir(related_path)

    related_text = ''
    for each_article in related_file_list:
        article_path = related_path + "/" + each_article
        with open(article_path, 'r', encoding='utf-8') as f:
            temp = f.read()
            for line in temp:
                related_text += line
    # print(no_related_text)

    related_word_cut_dict = func_jieba(related_text)
    # print(related_word_cut_dict)


    # insert no related source data--------------------
    no_related_path = r'./02_data_warehouse/no_related'
    no_related_file_list = os.listdir(no_related_path)

    no_related_text = ''
    for each_article in no_related_file_list:
        article_path = no_related_path + "/" + each_article
        with open(article_path, 'r', encoding = 'utf-8') as f:
            temp = f.read()
            for line in temp:
                no_related_text += line
    # print(no_related_text)

    no_related_word_cut_dict = func_jieba(no_related_text)
    # print(no_related_word_cut_dict)


    countlist = [related_word_cut_dict, no_related_word_cut_dict]

    # tfidf create base
    def tf(word, count):
        return count[word] / sum(count.values())
    def n_containing(word, count_list):
        return sum(1 for count in count_list if word in count)
    def idf(word, count_list):
        # print('{}'.format(len(count_list) / (1+n_containing(word, count_list))))
        # print('{}'.format(math.log(len(count_list) / (1+n_containing(word, count_list)))))
        # print('--')
        return math.log(1 + len(count_list) / (1+n_containing(word, count_list)))
    def tfidf(word, count, count_list):
        # print('{}*{}'.format(tf(word, count), idf(word, count_list)))
        return tf(word, count) * idf(word, count_list)
    base = {}
    j = 0
    for i, count in enumerate(countlist):
        # print("Top words in document {}".format(i+1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        cd ={}
        for word, score in sorted_words[0:100]:
            # print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
            cd[word] = round(score, 5)

        base[j]=cd
        j += 1
    # print(base)


    # insert sample
    # insert no related source data--------------------
    sample_path = r'./02_data_warehouse/sample'
    sample_file_list = os.listdir(sample_path)


    #---------------------------------


    sample_text = ''
    for each_article in sample_file_list:
        article_path = sample_path + "/" + each_article
        with open(article_path, 'r', encoding='utf-8') as f:
            temp = f.read()
            for line in temp:
                sample_text += line
    # print(sample_text)

    sample_word_cut_dict = func_jieba(sample_text)
    # print("sample")
    # print(sample_word_cut_dict)


    base[2] = sample_word_cut_dict
    # print(base)

    columns = []
    for i in range(3):
        columns = comb_key(columns, base[i])

    content = []

    for y in base:
        content.append(base[y])
    # print(content)

    h = pd.DataFrame(data=content, columns=columns)
    h = h.fillna(0)

    h.iloc[:2, :] = h.iloc[:2, :] * 2000
    h.iloc[:1, :5] = h.iloc[:1, :5] * 1/2

    m_5 = ['價格', '颱風','產量','市場','農民', '採收', '損失', '農業', '外銷', '出口']
    if h.loc[2,"香蕉"] >= 4:
        for i in m_5:
            if h.loc[2,i] > 0:
                h.loc[2,i] = h.loc[0,i]
                h.loc[1,i] = 0


    late = h.iloc[:,1:]

    # print(late)

    # KMeans 演算法
    kmeans_fit = cluster.KMeans(n_clusters=2).fit(late)

    # 印出分群結果
    cluster_labels = kmeans_fit.labels_
    # print("分群結果：")
    print(cluster_labels)

    if cluster_labels[0]==cluster_labels[1]:
        print("無相關")
    elif cluster_labels[1] == cluster_labels[2]:
        print("無相關")
    else:
        print("相關")





    # 使用pandas 將資料轉為csv檔
    late.to_csv('./dd.csv', index=0, encoding="utf_8_sig")

def func_jieba(text):
    '''
    :param text:
    :return: word count dict
    '''

    # insert stopword list
    stopword_path = r'./01_ref_data/stopword.txt'
    stopword_list = []
    with open(stopword_path, 'r', encoding='utf-8') as f_stop:
        for temp in f_stop.readlines():
            stopword_list.append(temp.replace('\n', ''))
    # print(stopword_list)

    jieba.load_userdict(r'./01_ref_data/mydict.txt')
    s = jieba.cut(text)
    jieba_word_count = {}
    for i in s:
        if i in jieba_word_count:
            jieba_word_count[i] += 1
        else:
            jieba_word_count[i] = 1

    jieba_word = [(k, jieba_word_count[k]) for k in jieba_word_count if (len(k) > 1) and (k not in stopword_list) and not re.match(r'[0-9a-zA-Z]+',k)]
    jieba_word.sort(key=lambda item: item[1], reverse=True)

    jieba_dict = {}

    for i in jieba_word:
        jieba_dict[i[0]] =i [1]

    return jieba_dict

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

if __name__=="__main__":
    '''
    
    main function
    
    '''
    main()