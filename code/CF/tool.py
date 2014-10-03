# -*- coding: utf-8 -*-

__author__ = 'wangjz'


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



def jaccard_distance(l1, l2):
    """
    计算Jaccard距离，
    【输入】两个位向量
    【输入】J(A,B) = |A交B|/|A并B|
    """

    union_num = 0
    intersect_num = 0
    for i in range(len(l1)):
        if l1[i] == 1 and l2[i] == 1:
            intersect_num += 1
        if l1[i] == 1 or l2[i] == 1:
            union_num += 1

    if union_num == 0:
        return 0
    else:
        return 1.0 * intersect_num/union_num
