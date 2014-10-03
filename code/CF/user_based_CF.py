# -*- coding: utf-8 -*-

__author__ = 'wangjz'

import heapq
import itertools
import numpy as np

class UBCFilter:
    """
        User Based Collaborative Filtering
    """

    def __init__(self, u2u_mat, clk_mat, k_nearest=100, l_top=10):
        """
        【输入】
            K_nearest 在K个最相似的用户中生成 文章集

        【输出】
            rec_result:每一行对应一个用户，每个tuple分别是阅读次数、文章号索引
            [[(10,2),(8,1),(7,3)],
            [(),(),()],
            [(),(),()],
            [(),(),()],
            [(),(),()]
            ]
        """
        self.__u2u_matrix = u2u_mat
        self.__clk_matrix = clk_mat
        self.__K_NEAR = k_nearest
        self.__L_TOP = l_top
        # s = clk_mat.shape
        self.__M_USERS = len(clk_mat)
        self.__N_NEWS = len(clk_mat[0])
        self.result = []

    def __get_top_l(self, row):
        """
        计算所有新闻中，阅读次数最多的L个
        返回值形如[(8, 0), (5, 2), (3, 1), (1, 3)]，第一列是阅读次数，第二列是文章号索引
        """
        return heapq.nlargest(self.__L_TOP, zip(row, itertools.count()))

    def __get_nearest_k(self, target_index):
        """
        通过相似矩阵，计算某个item最为相似的K个 用户(或新闻)
        返回值形如[(8, 0), (5, 2), (3, 1), (1, 3)]，第一列是相似度，第二列是用户号索引
        """
        row = self.__u2u_matrix[target_index].todense().tolist()[0]

        #按说应该多召回一个，删除第一个(因为第一个是自己)

        return heapq.nlargest(self.__K_NEAR, zip(row, itertools.count()))

    def start_cf(self):
        """
        找到与用户u最相似的K个用户，根据相似性对每一篇文章进行加权求和
        """
        for i in range(self.__M_USERS):
            if i % 100 == 0:
                print "user %d" % i

            news_ratings = [0 for _ in range(self.__N_NEWS)]
            cur_read = self.__clk_matrix[i]
            near_users = self.__get_nearest_k(i)
            for (similar, index) in near_users:
                tmp_read = self.__clk_matrix[index]
                for j in range(self.__N_NEWS):
                    #只计算当前用户没有阅读过的文章
                    if cur_read[j] == 0:
                        news_ratings[j] += self.__u2u_matrix[i, index] * tmp_read[j]

            top = self.__get_top_l(news_ratings)
            print top
            self.result.append(top)


def unit_test():
    a = [8,3,5,1]
    b = heapq.nlargest(4, zip(a, itertools.count()))
    print b