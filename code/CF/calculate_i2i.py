# -*- coding: utf-8 -*-

__author__ = 'wangjz'

from tool import jaccard_distance

'''
根据user_item矩阵 计算 i2i相似度矩阵
【输入】
    ui_matrix (大小是M X N)
    similar_method 相似度计算方式（默认使用Jaccard Distance）

【输出】i2i_matrix (大小是 N X N) 是一个对称矩阵，对角线上默认是0 (自身与自身的相似度不予考虑)

'''


def calculate_i2i(ui_matrix, similar_method=jaccard_distance):
    N = len(ui_matrix[0])
    i2i_matrix = [[0 for col in range(N)] for row in range(N)]
    for i in range(N):
        for j in range(i+1, N):
            item_i = [u[i] for u in ui_matrix]
            item_j = [u[j] for u in ui_matrix]
            i2i_matrix[i][j] = similar_method(item_i, item_j)
    return i2i_matrix


ui_mat =[[1,0,0,1],
        [1,1,1,1],
        [0,0,1,1]]
i2i_mat = calculate_i2i(ui_mat)
print(i2i_mat)
