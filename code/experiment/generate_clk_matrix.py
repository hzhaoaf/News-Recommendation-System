# -*- coding: utf-8 -*-

__author__ = 'wangjz'

from CONSTANT import *
import cPickle

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
clk_matrix = [[int(0) for col in range(N_NEWs)] for row in range(M_USERs)]

for l in lines:
    items = l.split('\t')
    user_id = int(items[0])
    item_id = int(items[1])
    user_order = u2o_dic[user_id]
    item_order = i2o_dic[item_id]
    clk_matrix[user_order][item_order] = int(1)

# Step 3 : save on disk
with open(CLK_MATRIX_PATH, 'wb') as f:
    cPickle.dump(clk_matrix, f)