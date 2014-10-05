# -*- coding: utf-8 -*-

"""这段代码太慢了，几乎预测每个用户要10分钟的样子"""

__author__ = 'wangjz'

from scipy.sparse import lil_matrix
import numpy as np
from numpy.random import random

from experiment.CONSTANT import *
import cPickle

with open(ORIGIN_DATA_PATH, 'r') as f:
    lines = f.readlines()[1:]

#construct dataset {user_id:{item_id: preference, item_id2: preference, ...}, user_id2: {...}, ...}.

news_data_dic = {}

for l in lines:
    items = l.split('\t')
    user_id = items[0]
    item_id = items[1]
    if user_id in news_data_dic:
        tmp_dic = news_data_dic[user_id]
        tmp_dic[item_id] = 1
    else:
        news_data_dic[user_id] = {item_id:1}

user_ids = news_data_dic.keys()

from scikits.crab.models import MatrixBooleanPrefDataModel
from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.metrics import jaccard_coefficient, pearson_correlation
from scikits.crab.similarities import UserSimilarity,ItemSimilarity
from scikits.crab.recommenders.knn import UserBasedRecommender,ItemBasedRecommender


#Build the model
model = MatrixPreferenceDataModel(news_data_dic)

#Build the similarity
similarity = ItemSimilarity(model, pearson_correlation, num_best=10)
#Build the User based recommender
recommender = ItemBasedRecommender(model, similarity, with_preference=False)

#Recommend items for the user 5 (Toby)
result_list = []
for uid in user_ids:
    # result_list.append(uid, recommender.recommend(uid, 20))
    print(uid)
    print(recommender.recommend(uid, 5))

print(len(result_list))
print(result_list[:3])
