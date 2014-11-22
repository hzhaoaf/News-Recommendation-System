# -*- coding: utf-8 -*-

__author__ = 'wangjz'

"""
1）计算i2i 相似度，直接序列化
2）生成点击矩阵，稀疏表示后进行序列化
"""

from CONSTANT import *
import cPickle
from scipy.sparse import lil_matrix
from scikits.crab.models import MatrixBooleanPrefDataModel
from scikits.crab.metrics import jaccard_coefficient
from improved_basic_similarities import ImprovedItemSimilarity


def generate_sim_and_clk():
    #[1] load data
    with open(ORIGIN_DATA_PATH, 'r') as f:
        lines = f.readlines()[1:]

    with open(U2O_PATH, 'r') as f:
        u2o_dic = cPickle.load(f)

    with open(I2O_PATH, 'r') as f:
        i2o_dic = cPickle.load(f)

    M_USERs = len(u2o_dic.items())
    N_NEWs = len(i2o_dic.items())

    # (M X N)的一个矩阵，一行代表一个用户，一列代表一条新闻
    clk_matrix = lil_matrix((M_USERs, N_NEWs))

    cf_input_dic = {}

    for l in lines:
        items = l.split('\t')
        user_order = u2o_dic[int(items[0])]
        item_order = i2o_dic[int(items[1])]

        #set click matrix
        clk_matrix[user_order, item_order] = 1.0

        #set cf input dictionary
        if user_order in cf_input_dic:
            cf_input_dic[user_order][item_order] = 1
        else:
            cf_input_dic[user_order] = {item_order: 1}

    #save click matrix
    with open(CLK_MATRIX_PATH, 'wb') as f:
        cPickle.dump(clk_matrix, f)

    model = MatrixBooleanPrefDataModel(cf_input_dic)
    similarity = ImprovedItemSimilarity(model, jaccard_coefficient, num_best=10)
    similarity.compute_similarities()
    similarity.save_similar_dic(IMPROVE_SIMILARITY_PATH)
