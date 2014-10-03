# -*- coding: utf-8 -*-

__author__ = 'wangjz'

from CONSTANT import *

"""
【注意，我将data.txt文件头部插入了一行，否则读取出问题，原因未知】

读取文件，生成user<->order 和 news<->order 双向翻译字典
序列化到文件里
"""
#-----------------Step 1: read and parse-----------------#


with open(ORIGIN_DATA_PATH, 'r') as f:
    lines = f.readlines()[1:]#为啥从第一行读就有错误？
f.close()
user_set = set()
news_set = set()

for line in lines:
    items = line.split('\t')
    user_set.add(int(items[0]))
    news_set.add(int(items[1]))


user_list = sorted(list(user_set))
news_list = sorted(list(news_set))

u2o_dic = {}
i2o_dic = {}
o2u_dic = {}
o2i_dic = {}

for i in range(len(user_list)):
    u2o_dic[user_list[i]] = i
    o2u_dic[i] = user_list[i]

for j in range(len(news_list)):
    i2o_dic[news_list[j]] = j
    o2i_dic[j] = news_list[j]

#-----------------Step 2: save on disk-----------------#

import cPickle

with open(U2O_PATH, 'wb') as f:
    cPickle.dump(u2o_dic, f)

with open(I2O_PATH, 'wb') as f:
    cPickle.dump(i2o_dic, f)

with open(O2U_PATH, 'wb') as f:
    cPickle.dump(o2u_dic, f)

with open(O2I_PATH, 'wb') as f:
    cPickle.dump(o2i_dic, f)
