# -*- coding: utf-8 -*-

__author__ = 'wangjz'

"""
取排名最高的前K个作为推荐给用户的最终的结果
翻译回user_id and item_id
"""

from CONSTANT import *
import cPickle

with open(O2U_PATH, 'r') as f:
    o2u_dic = cPickle.load(f)

with open(O2I_PATH, 'r') as f:
    o2i_dic = cPickle.load(f)

M_USERs = len(o2u_dic.items())
N_NEWs = len(o2i_dic.items())

with open(REC_RESULT, 'r') as f:
    recommends = cPickle.load(f)

#每个用户推荐 几个？
K_RECOMMEND = 2 
with open(FINAL_DATA, 'w') as f:
    for i in range(len(recommends)):
        user_id = o2u_dic[i]
        for j in range(K_RECOMMEND):
            item_id = o2i_dic[recommends[i][j][1]]
            #[(0.12532051282051279, 2680), (0.11757917337627483, 2681), (0.09198717948717948, 6179)]
            f.write(str(user_id) + ',' + str(item_id) + "\n")
