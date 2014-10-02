# -*- coding: utf-8 -*-

__author__ = 'wangjz'

from tool import jaccard_distance

'''
根据user_item矩阵 计算 u2u相似度矩阵
输入输出与 i2i的计算类似
'''

def calculate_u2u(ui_matrix, similar_method=jaccard_distance):
    M = len(ui_matrix)
    u2u_matrix = [[0 for col in range(M)] for row in range(M)]
    for i in range(M):
        for j in range(i+1, M):
            u2u_matrix[i][j] = similar_method(ui_matrix[i], ui_matrix[j])
    return u2u_matrix


ui_mat =[[1,0,0,1],
        [1,1,1,1],
        [0,0,1,1]]
u2u_mat = calculate_u2u(ui_mat)
print(u2u_mat)