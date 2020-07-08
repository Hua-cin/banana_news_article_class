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
from sklearn import cluster
import re

def main():
    '''

    :return:
    '''


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
        return math.log(1 + len(count_list) / (1+n_containing(word, count_list)))
    def tfidf(word, count, count_list):
        return tf(word, count) * idf(word, count_list)
    base = {}
    j = 0
    for i, count in enumerate(countlist):
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        cd ={}
        for word, score in sorted_words[0:100]:
            cd[word] = round(score, 5)

        base[j]=cd
        j += 1
    # print(base, file = open('./01_ref_data/base.txt', 'w'))
    #
    # with open('./01_ref_data/base.txt', 'r', encoding='utf-8') as f:
    #     base_temp = f.read()
        # print(base_temp)

    base_copy = base.copy()

    # insert sample
    # insert no related source data--------------------
    sample_path = r'./02_data_warehouse/sample'
    sample_file_list = os.listdir(sample_path)

    #---------------------------------

    content_dict = {}
    for each_article in sample_file_list:
        sample_text = ''
        article_path = sample_path + "/" + each_article

        with open(article_path, 'r', encoding='utf-8') as f:
            temp = f.read()
            for line in temp:
                sample_text += line
            content_dict[each_article]=sample_text
    # print(sample_text)

    # print(content_dict)
    for k in content_dict:

        sample_word_cut_dict = func_jieba(content_dict[k])
        # print("sample")
        # print(sample_word_cut_dict)


        base_copy[2] = sample_word_cut_dict
        # print(base)

        columns = []
        for i in range(2):
            columns = comb_key(columns, base_copy[i])

        content = []

        for y in base_copy:
            content.append(base_copy[y])

        h = pd.DataFrame(data=content, columns=columns)

        # 修改數值, 相關改為 +1, 不相關改為 -1
        # h.iloc[:2, :] = h.iloc[:2, :] * 2000
        h.iloc[1:2,:] = h.iloc[1:2,:] * (-1)

        # 取得非香蕉部份
        late = h.iloc[:,1:]

        # late dataframe 空值補0
        late = late.fillna(0)

        for x in range(0,2):
            for y in late:
                if late.loc[x, y]>0:
                    late.loc[x, y] = 1
                elif late.loc[x, y]<0:
                    late.loc[x, y] = -1
                else:
                    late.loc[x, y] = 0
        for z in late:
            if late.loc[1, z] < 0:
                late.loc[2, z] =late.loc[2, z] * (-1)
        late['全部'] = [20,-19.5,0]

        # KMeans 演算法
        kmeans_fit = cluster.KMeans(n_clusters=2).fit(late)

        # 印出分群結果
        cluster_labels = kmeans_fit.labels_

        print("\n----------------")
        print("{}\n分群結果：\n{}".format(k, cluster_labels))

        # 判定結果
        if h.loc[2,'香蕉'] > 2:
            if cluster_labels[0]==cluster_labels[1]:
                print("無相關")
                result = False
            elif cluster_labels[1] == cluster_labels[2]:
                print("無相關")
                result = False
            else:
                print("相關")
                result = True
        else:
            print("無相關")
            result = False

    # 回傳結果
    return result

    # # 使用pandas 將資料轉為csv檔
    # late.to_csv('./dd.csv', index=0, encoding="utf_8_sig")

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