# -*- coding: utf-8 -*-

__author__ = 'wangjz'

"""
执行计算的脚本
利用i2i相似度 进行Item Based CF
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


with open(FINAL_DATA, 'w') as f:
    for i in range(len(recommends)):
        user_id = o2u_dic[i]
        item_id1 = o2i_dic[recommends[i][0][1]]
        item_id2 = o2i_dic[recommends[i][1][1]]
        item_id3 = o2i_dic[recommends[i][2][1]]

        #[(0.12532051282051279, 2680), (0.11757917337627483, 2681), (0.09198717948717948, 6179)]
        f.write(str(user_id) + ',' + str(item_id1) + "\n")
        f.write(str(user_id) + ',' + str(item_id2) + "\n")
        f.write(str(user_id) + ',' + str(item_id3) + "\n")