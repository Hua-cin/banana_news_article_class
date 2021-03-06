# -*- coding: utf-8 -*-
'''

1. ckip test

'''



# from ckiptagger import data_utils
# data_utils.download_data_gdown("./")
from ckiptagger import WS, POS, NER

text = '傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。'
ws = WS("../data")
pos = POS("../data")
ner = NER("../data")

ws_results = ws([text])
pos_results = pos(ws_results)
ner_results = ner(ws_results, pos_results)

print(ws_results)
print(pos_results)
for name in ner_results[0]:
    print(name)

print("end")