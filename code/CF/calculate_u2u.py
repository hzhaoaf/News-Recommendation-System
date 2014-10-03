# -*- coding: utf-8 -*-

__author__ = 'wangjz'

from tool import jaccard_distance, print_matrix
import scipy.sparse as sp
import numpy as np

'''
根据user_item矩阵 计算 u2u相似度矩阵
输入输出与 i2i的计算类似
'''


def calculate_u2u_cos(clk_matrix):
    #参考http://blog.acmol.com/pages/cf-implements.html
    #multiply The product of x1 and x2, element-wise. Returns a scalar if both x1 and x2 are scalars.
    clk_matrix = clk_matrix.todense()
    sq_sum = np.multiply(clk_matrix, clk_matrix).sum(1)
    sq_sum = sq_sum * sq_sum.T
    u2u_matrix = sp.csc_matrix(clk_matrix)
    u2u_matrix = (u2u_matrix * u2u_matrix.T).todense()
    np.divide(u2u_matrix, np.power(sq_sum, 0.5, sq_sum), u2u_matrix)
    return sp.csc_matrix(u2u_matrix)

# def calculate_u2u(clk_matrix, similar_method=jaccard_distance):
#     M_USERs = clk_matrix.shape[0]
#     u2u_matrix = lil_matrix((M_USERs, M_USERs))
#     for i in range(M_USERs):
#         print "user %d" % i
#         row1 = clk_matrix[i]
#         for j in range(i+1, M_USERs):
#             row2 = clk_matrix[j]
#             sim_dis = similar_method(row1, row2)
#             if sim_dis >= 0.000001:
#                 u2u_matrix[i, j] = u2u_matrix[j, i] = sim_dis
#     return u2u_matrix


