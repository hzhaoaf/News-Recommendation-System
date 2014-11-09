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

from scipy.sparse import lil_matrix

#[1] load data

with open(CLK_MATRIX_PATH, 'r') as f:
    clk_matrix = cPickle.load(f)

#将稀疏矩阵转化为python 2D list
clk_matrix = np.int16(clk_matrix.todense()).tolist()

with open(IMPROVE_SIMILARITY_PATH, 'r') as f:
    i2i_matrix = cPickle.load(f)

#def __init__(self, i2i_mat, clk_mat, k_nearest_item=100, l_top_rec=10):
ibcf = IBCFilter(i2i_matrix, clk_matrix, k_nearest_item=30, l_top_rec=15)
ibcf.start_cf()

with open(REC_RESULT, 'wb') as f:
    cPickle.dump(ibcf.result, f)

# with open(O2U_PATH, 'r') as f:
#     o2u_dic = cPickle.load(f)
#
# with open(I2O_PATH, 'r') as f:
#     o2i_dic = cPickle.load(f)
#
# M_USERs = len(o2u_dic.items())
# N_NEWs = len(o2i_dic.items())