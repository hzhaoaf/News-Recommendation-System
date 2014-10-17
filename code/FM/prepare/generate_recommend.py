# -*- coding: utf-8 -*-

__author__ = 'wangjz'
"""
将libfm输出的预测结果文件和 test输入文件读入进来，找到每一个结果对应的user_order和item_order
填充一个评分矩阵
对矩阵中的每一行，也就是每一个用户，找到top l个最大评分的
将l个最大评分序列化到结果中

所以结果是一个M*l*2的矩阵
最后一个2代表的是(评分,item_order)
"""


from CONSTANT import *
import heapq
import itertools
import cPickle


#通过clk matrix 来获取用户和新闻的数量
with open(CLK_MATRIX_PATH, 'r') as f:
    clk_matrix = cPickle.load(f)

M_Users = clk_matrix.shape[0]
N_News = clk_matrix.shape[1]
L_TOP = 5

result_file = open(LIBFM_OUT, 'r')
test_file = open(FM_TEST_DATA, 'r')
rating_mat = [[0 for _ in range(N_News)] for _ in range(M_Users)]

while True:
    #0 0:1 0:1
    test_info = test_file.readline()
    if not test_info:
        break
    test_info = test_info[:-1].split(' ')
    u_order = int(test_info[1].split(':')[0])
    i_order = int(test_info[2].split(':')[0])
    score = result_file.readline()[:-1]
    score = float(score)
    rating_mat[u_order][i_order] = score


result_file.close()
test_file.close()

top_list = [[] for i in range(M_Users)]
for cnt, row_vec in enumerate(rating_mat):
    top_list[cnt] = heapq.nlargest(L_TOP, zip(row_vec, itertools.count()))

"""
存入的是每个user top l个新闻的order
[[(0.02,200001),(0.5,2000005)],
 [(0.23,200001),(0.2,2000002)],
 [(0.33,200001),(0.1,2000004)]
]
"""

with open(FM_RECOMMEND_WITH_SCORE, 'wb') as f:
    cPickle.dump(top_list, f)
