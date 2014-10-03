# -*- coding: utf-8 -*-

__author__ = 'wangjz'

"""
生成 训练集 和 测试集
用户浏览的最后一条news 作为测试集，其它作为训练集 one_out_clk_matrix
"""

from CONSTANT import *
import cPickle
from scipy.sparse import lil_matrix

# Step 1 : load origin data and translate dics

with open(U2O_PATH, 'r') as f:
    u2o_dic = cPickle.load(f)

with open(I2O_PATH, 'r') as f:
    i2o_dic = cPickle.load(f)

with open(ORIGIN_DATA_PATH, 'r') as f:
    lines = f.readlines()[1:]

# Step 2 : generate click matrix

M_USERs = len(u2o_dic.items())
N_NEWs = len(i2o_dic.items())

# (M X N)的一个矩阵，一行代表一个用户，一列代表一条新闻
# ont_out_clk_matrix = [[int(0) for col in range(N_NEWs)] for row in range(M_USERs)]
ont_out_clk_matrix = lil_matrix((M_USERs, N_NEWs))

one_out_test_data = [] #训练集
users_order_set = set() #记录已经出现的用户

#用户第一次出现的是他最后一次阅读的文章，将(user_id,item_id)加入到测试集中

for l in lines:
    items = l.split('\t')
    user_id = int(items[0])
    item_id = int(items[1])
    user_order = u2o_dic[user_id]
    item_order = i2o_dic[item_id]
    if user_order in users_order_set:
        ont_out_clk_matrix[user_order, item_order] = 1.0
    else:
        one_out_test_data.append((user_id, item_id))
        users_order_set.add(user_order)

# Step 3 : save on disk
with open(ONE_OUT_CLK_MATRIX_PATH, 'wb') as f:
    cPickle.dump(ont_out_clk_matrix, f)

with open(ONE_OUT_TEST_DATA_PATH, 'wb') as f:
    cPickle.dump(one_out_test_data, f)

print len(one_out_test_data)