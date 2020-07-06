# -*- coding: utf-8 -*-
'''

1.news word cut (ckip) from source folder './02_data_warehouse'
2.use stop word list form file './01_ref_data/stopword.txt'

'''

import os

# insert stopword list
stopword_path = r'./01_ref_data/stopword.txt'
stopword_list = []
with open(stopword_path, 'r', encoding = 'utf-8') as f_stop:
    for temp in f_stop.readlines():
        stopword_list.append(temp.replace('。\n', ''))
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

# import ckiptagger
from ckiptagger import WS, POS, NER
dict_for_CKIP = {'。':1}

from ckiptagger import construct_dictionary
dict_for_CKIP = construct_dictionary(dict_for_CKIP)


ws = WS("../data")
ws_results = ws([text])
ckip_word_count = {}

for i in ws_results[0]:
    if i in ckip_word_count:
        ckip_word_count[i] += 1
    else:
        ckip_word_count[i] = 1
print(ckip_word_count)

ckip_word_list = [(k, ckip_word_count[k]) for k in ckip_word_count if (len(k)>1) and (k not in stopword_list)]
ckip_word_list.sort(key=lambda item: item[1], reverse=True)
print(ckip_word_list)
