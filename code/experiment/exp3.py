# -*- coding: utf-8 -*-

__author__ = 'wangjz'

import cPickle
from CONSTANT import *
from CF.cf_recommender import IBCFilter
import numpy as np


with open(ONE_OUT_CLK_MATRIX_PATH, 'r') as f:
    clk_matrix = cPickle.load(f)

clk_matrix = np.int16(clk_matrix.todense()).tolist()
m = len(clk_matrix)
n = len(clk_matrix[0])

i2i_matrix = [[0.5 for _ in range(n)] for _ in range(n)]#伪造i2i数据

 #__init__(self, i2i_mat, clk_mat, k_nearest_item=100, l_top_rec=10):
cf = IBCFilter(i2i_matrix, clk_matrix, k_nearest_item=5, l_top_rec=5)
cf.start_cf()
res = cf.result

with open(REC_RESULT, 'wb') as f:
    cPickle.dump(res, f)