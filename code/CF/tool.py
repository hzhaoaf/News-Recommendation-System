# -*- coding: utf-8 -*-

__author__ = 'wangjz'

'''
计算Jaccard距离，
【输入】两个位向量
【输入】J(A,B) = |A交B|/|A并B|
'''


def jaccard_distance(l1, l2):
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
