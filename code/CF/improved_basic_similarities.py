#-*- coding:utf-8 -*-

import cPickle
import numpy as np
from scikits.crab.similarities.base import BaseSimilarity
from scikits.crab.metrics import loglikehood_coefficient
from scikits.crab.similarities.basic_similarities import find_common_elements


class ImprovedItemSimilarity(BaseSimilarity):
    """
    Improved ItemSimilarity By JZ 2014.10.5
    """

    def __init__(self, model, distance, num_best=None):
        BaseSimilarity.__init__(self, model, distance, num_best)
        n = len(model.item_ids())
        self.similar_matrix = [[0 for _ in range(n)] for _ in range(n)]

    def save_similar_dic(self, path):
        with open(path+"_similar_matrix.pickle", 'w') as f:
            cPickle.dump(self.similar_matrix, f)

    def load_similar_dic(self,path):
        with open(path+"_similar_matrix.pickle", 'w') as f:
            self.similar_matrix = cPickle.load(f)

    def compute_similarities(self):
        item_orders = self.model.item_ids()
        item_orders = item_orders.tolist()# to int list
        for i in range(len(item_orders)):
            item_orders[i] = int(item_orders[i])
        n = len(item_orders)
        for i in range(n):
            print item_orders[i]
            for j in range(i+1, n):#（对角线熵都是0，自身和自身相比相似度为0）
                tmp = self.__pre_get_similarity(item_orders[i], item_orders[j])
                self.similar_matrix[item_orders[i]][item_orders[j]] = tmp
                self.similar_matrix[item_orders[j]][item_orders[i]] = tmp

    def __pre_get_similarity(self, source_order, target_order):
        """
        Origin get_similarity function now becomes the hidden func.
        """
        source_preferences = self.model.preferences_for_item(source_order)
        target_preferences = self.model.preferences_for_item(target_order)

        if self.model.has_preference_values():
            source_preferences, target_preferences = find_common_elements(source_preferences, target_preferences)

        if source_preferences.ndim == 1 and target_preferences.ndim == 1:
            source_preferences = np.asarray([source_preferences])
            target_preferences = np.asarray([target_preferences])

        if self.distance == loglikehood_coefficient:
            if not source_preferences.shape[1] == 0 and not target_preferences.shape[1] == 0:
                return self.distance(self.model.items_count(), source_preferences, target_preferences)[0, 0]
            else:
                return 0#np.array([[np.nan]])

        #Evaluate the similarity between the two users vectors.
        if not source_preferences.shape[1] == 0 and not target_preferences.shape[1] == 0:
            return self.distance(source_preferences, target_preferences)[0, 0]
        else:
            return 0 #np.array([[np.nan]])

    def get_similarity(self, source_order, target_order):
        return self.similar_matrix[source_order][target_order]

    def get_similarities(self, source_order):
        return self.similar_matrix[source_order]

    def __iter__(self):
        """
        For each object in model, compute the similarity function against all other objects and yield the result.
        """
        for item_id in self.model.item_ids():
            yield item_id, self[item_id]
