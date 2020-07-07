# -*- coding: utf-8 -*-
'''

1.news word cut (jieba) from source folder './02_data_warehouse'
2.use stop word list form file './01_ref_data/stopword.txt'

'''

import os

# insert stopword list
stopword_path = r'./01_ref_data/stopword.txt'
stopword_list = []
with open(stopword_path, 'r', encoding = 'utf-8') as f_stop:
    for temp in f_stop.readlines():
        stopword_list.append(temp.replace('\n', ''))
print(stopword_list)

# insert source data
path = r'./02_data_warehouse'
file_list = os.listdir(path)
text = ''

for each_article in file_list:
    article_path = path + "/" + each_article
    with open(article_path, 'r', encoding = 'utf-8') as f:
        temp = f.read()
        for line in temp:
            text += line

# import jieba
import jieba
jieba.load_userdict(r'./01_ref_data/mydict.txt')
s = jieba.cut(text)
jieba_word_count={}
for i in s:
    if i in jieba_word_count:
        jieba_word_count[i] += 1
    else:
        jieba_word_count[i] = 1

jieba_word = [(k, jieba_word_count[k]) for k in jieba_word_count if (len(k)>1) ]#and (k not in stopword_list)]
jieba_word.sort(key=lambda item: item[1], reverse=True)
# print(jieba_word)
jieba_word_list = []
for i in jieba_word:
    x=[]
    x.append(i[0])
    x.append(i[1])
    jieba_word_list.append(x)

print(jieba_word_list)
