# -*- coding: utf-8 -*-


__author__ = 'wangjz'


from experiment.CONSTANT import *

with open(ORIGIN_DATA_PATH, 'r') as f:
    lines = f.readlines()[1:]

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

from scikits.crab.models import MatrixPreferenceDataModel,MatrixBooleanPrefDataModel
from scikits.crab.metrics import pearson_correlation,jaccard_coefficient,cosine_distances
from improved_basic_similarities import ImprovedItemSimilarity
from scikits.crab.recommenders.knn import ItemBasedRecommender

model = MatrixBooleanPrefDataModel(news_data_dic)
similarity = ImprovedItemSimilarity(model, jaccard_coefficient, num_best=10)
similarity.compute_similarities()
similarity.save_similar_dic(IMPROVE_SIMILARITY_PATH)

# recommender = ItemBasedRecommender(model, similarity, with_preference=False)
# result_list = []
# for uid in user_ids:
#     print(uid)
#     print(recommender.recommend(uid, 5))
# print(len(result_list))
# print(result_list[:3])
