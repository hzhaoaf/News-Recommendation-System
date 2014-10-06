# -*- coding: utf-8 -*-


__author__ = 'wangjz'


from experiment.CONSTANT import *
import cPickle

from scikits.crab.models import MatrixPreferenceDataModel,MatrixBooleanPrefDataModel
from scikits.crab.metrics import pearson_correlation,jaccard_coefficient,cosine_distances
from improved_basic_similarities import ImprovedItemSimilarity
from scikits.crab.recommenders.knn import ItemBasedRecommender

with open(IMPROVE_SIMILARITY_PATH) as f:
    simi = cPickle.load(f)

print(len(simi.items()))
print "ok"
# recommender = ItemBasedRecommender(model, similarity, with_preference=False)
# result_list = []
# for uid in user_ids:
#     print(uid)
#     print(recommender.recommend(uid, 5))
# print(len(result_list))
# print(result_list[:3])
