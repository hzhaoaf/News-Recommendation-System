#-*- coding:utf-8 -*-

import cPickle
from collections import defaultdict
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
        N = len(model.item_ids())
        self.similar_matrix = [[0 for col in range(N)] for row in range(N)]
        self.item2order_dic = defaultdict(int)
        self.order2item_dic = defaultdict(str)

    def save_similar_dic(self, path):
        with open(path+"_similar_matrix.pickle", 'w') as f:
            cPickle.dump(self.similar_matrix, f)
        with open(path+"_item2order_dic.pickle", 'w') as f:
            cPickle.dump(self.item2order_dic, f)
        with open(path+"item2order_dic.pickle", 'w') as f:
            cPickle.dump(self.item2order_dic, f)

    def load_similar_dic(self,path):
        with open(path+"_similar_matrix.pickle", 'w') as f:
            self.similar_matrix = cPickle.load(f)
        with open(path+"_item2order_dic.pickle", 'w') as f:
            self.item2order_dic = cPickle.load(f)
        with open(path+"item2order_dic.pickle", 'w') as f:
            self.item2order_dic = cPickle.load(f)

    def compute_similarities(self):
        self.similar_matrix.clear()
        item_ids = self.model.item_ids()
        n = len(item_ids)

        for i in range(n):
            self.item2order_dic[item_ids[i]] = i
            self.order2item_dic[i] = item_ids[i]

        for i in range(n):
            print item_ids[i]
            for j in range(i+1, n):
                tmp = self.__pre_get_similarity(item_ids[i], item_ids[j])
                self.similar_matrix[i][j] = tmp
                self.similar_matrix[j][i] = tmp

    def __pre_get_similarity(self, source_id, target_id):
        """
        Origin get_similarity function now becomes the hidden func.
        """
        source_preferences = self.model.preferences_for_item(source_id)
        target_preferences = self.model.preferences_for_item(target_id)

        if self.model.has_preference_values():
            source_preferences, target_preferences = find_common_elements(source_preferences, target_preferences)

        if source_preferences.ndim == 1 and target_preferences.ndim == 1:
            source_preferences = np.asarray([source_preferences])
            target_preferences = np.asarray([target_preferences])

        if self.distance == loglikehood_coefficient:
            if not source_preferences.shape[1] == 0 and not target_preferences.shape[1] == 0:
                return self.distance(self.model.items_count(), source_preferences, target_preferences)
            else:
                return np.array([[np.nan]])

        #Evaluate the similarity between the two users vectors.
        if not source_preferences.shape[1] == 0 and not target_preferences.shape[1] == 0:
            return self.distance(source_preferences, target_preferences)
        else:
            return 0 #np.array([[np.nan]])

    def get_similarity(self, source_id, target_id):
        """Find in similar_dic, O(1) time"""
        if source_id in self.similar_dic:
            if target_id in self.similar_dic[source_id]:
                return self.similar_dic[source_id][target_id]
        return self.similar_dic[target_id][source_id]

    def get_similarities(self, source_id):
        return [(other_id, self.get_similarity(source_id, other_id)) for other_id in self.model.item_ids()]

    def __iter__(self):
        """
        For each object in model, compute the similarity function against all other objects and yield the result.
        """
        for item_id in self.model.item_ids():
            yield item_id, self[item_id]