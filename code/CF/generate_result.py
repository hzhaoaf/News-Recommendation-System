# -*- coding: utf-8 -*-

__author__ = 'wangjz'

"""
取排名最高的前K个作为推荐给用户的最终的结果
翻译回user_id and item_id
"""

from collections import defaultdict
from CONSTANT import *
import cPickle


#加入每个user最后一条阅读附近的热门新闻
users_nearby_hots_dic = defaultdict(set)

NUM_HOTS = 40
with open(HOT_NEWS, 'r') as f:
    for line in f.readlines():
        items = line[:-1].split(":")
        user_id = int(items[0])
        candis = items[1].split(",")[:NUM_HOTS]
        candis = [int(i) for i in candis]
        users_nearby_hots_dic[user_id] = set(candis)

with open(O2U_PATH, 'r') as f:
    o2u_dic = cPickle.load(f)

with open(O2I_PATH, 'r') as f:
    o2i_dic = cPickle.load(f)

M_USERs = len(o2u_dic.items())
N_NEWs = len(o2i_dic.items())

with open(REC_RESULT, 'r') as f:
    recommends = cPickle.load(f)

#每个用户,包含几个，推荐 几个？
M_INCLUDE = 10
K_RECOMMEND = 4
FINAL_DATA = DATA_PATH + 'hot_news.csv'
with open(FINAL_DATA, 'w') as f:
    for i in range(len(recommends)):
        user_id = o2u_dic[i]
        candi_set = users_nearby_hots_dic[user_id]
        cnt_cand = 0
        for j in range(M_INCLUDE):
            if cnt_cand == K_RECOMMEND:
                break
            item_id = o2i_dic[recommends[i][j][1]]
            if item_id in candi_set:
                cnt_cand += 1
                f.write(str(user_id) + ',' + str(item_id) + "\n")
            #[(0.12532051282051279, 2680), (0.11757917337627483, 2681), (0.09198717948717948, 6179)]


