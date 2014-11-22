# -*- coding: utf-8 -*-

__author__ = 'wangjz'

"""
执行计算的脚本
利用i2i相似度 进行Item Based CF
"""

from CONSTANT import *
import cPickle
import numpy as np
from cf_recommender import IBCFilter


def commit_cf():
    #[1] load data
    with open(CLK_MATRIX_PATH, 'r') as f:
        clk_matrix = cPickle.load(f)

    #将稀疏矩阵转化为python 2D list
    clk_matrix = np.int16(clk_matrix.todense()).tolist()

    with open(IMPROVE_SIMILARITY_PATH, 'r') as f:
        i2i_matrix = cPickle.load(f)

    ibcf = IBCFilter(i2i_matrix, clk_matrix, k_nearest_item=30, l_top_rec=15)
    ibcf.start_cf()

    with open(REC_RESULT, 'wb') as f:
        cPickle.dump(ibcf.result, f)