# -*- coding: utf-8 -*-

__author__ = 'wangjz'


"""
【注意，我将data.txt文件头部插入了一行，否则读取出问题，原因未知】

读取文件，生成user<->order 和 news<->order 双向翻译字典
序列化到文件里
"""

FILE_PATH = '../../data/data.txt'
with open(FILE_PATH, 'r') as f:
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


import pickle
u2o_path = '../../data/u2o_dic.pickle'
i2o_path = '../../data/i2o.pickle'
o2u_path = '../../data/o2u.pickle'
o2i_path = '../../data/o2i.pickle'

with open(u2o_path, 'wb') as f:
    pickle.dump(u2o_dic, f)

with open(i2o_path, 'wb') as f:
    pickle.dump(i2o_dic, f)

with open(o2u_path, 'wb') as f:
    pickle.dump(o2u_dic, f)

with open(o2i_path, 'wb') as f:
    pickle.dump(o2i_dic, f)
