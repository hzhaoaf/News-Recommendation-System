# -*- coding: utf-8 -*-

__author__ = 'wangjz'

"""
计算u2u余弦相似度,保存在稀疏矩阵中
"""

import cPickle
from CONSTANT import *
from scipy.sparse import csr_matrix
from CF.calculate_u2u import calculate_u2u_cos
import numpy as np

with open(CLK_MATRIX_PATH, 'r') as f:
    clk_matrix = cPickle.load(f)

u2u_matrix = calculate_u2u_cos(clk_matrix)
u2u_matrix = u2u_matrix.todense()

u2u_matrix = np.float16(u2u_matrix)

u2u_matrix[u2u_matrix < 0.4] = 0.0 #余弦相似度小于这个值的，舍弃

u2u_matrix = csr_matrix(u2u_matrix) #转换成稀疏矩阵，再存储

print(u2u_matrix[0])

with open(COS_U2U_SIM_MATRIX_PATH, 'wb') as f:
    cPickle.dump(u2u_matrix, f)

