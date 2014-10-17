# -*- coding: utf-8 -*-

__author__ = 'wangjz'

from CONSTANT import *
import cPickle
import numpy as np


with open(CLK_MATRIX_PATH, 'r') as f:
    clk_matrix = cPickle.load(f)

#将稀疏矩阵转化为python 2D list
clk_matrix = np.int16(clk_matrix.todense()).tolist()


train_file = open(FM_TRAIN_DATA, 'w')
test_file = open(FM_TEST_DATA, 'w')

ROW = len(clk_matrix)
COL = len(clk_matrix[0])
for i in range(ROW):
    for j in range(COL):
        #1 9745:1 540:1
        #0 897:1 234:1
        if clk_matrix[i][j] == 1:
            train_file.write("1 "+str(i)+":1 "+str(j)+":1\n")
        else:
            test_file.write("0 "+str(i)+":1 "+str(j)+":1\n")

train_file.close()
test_file.close()