# -*- coding: utf-8 -*-

__author__ = 'wangjz'

import numpy as np


def print_range_matrix(mat, row_start, row_end, col_start, col_end):
    """
    打印矩阵范围内的数
    """
    for row in mat[row_start:row_end]:
        for ele in row[col_start:col_end]:
            print "%.2f\t" % ele,
        print "\n"


def print_matrix(mat):
    """
    打印矩阵
    """
    for row in mat:
        for ele in row:
            print "%.2f\t" % ele,
        print "\n"


def jaccard_distance(row1, row2):
    """
    计算Jaccard距离，
    【输入】两个 稀疏矩阵的行
    【输入】J(A,B) = |A交B|/|A并B|
    """
    l1_index = row1.nonzero()[1]
    l2_index = row2.nonzero()[1]

    intersect_num = np.intersect1d(l1_index, l2_index).size
    if intersect_num == 0:
        return 0

    union_num = np.union1d(l1_index, l2_index).size
    if union_num == 0:
        return 0

    else:
        return 1.0 * intersect_num/union_num
