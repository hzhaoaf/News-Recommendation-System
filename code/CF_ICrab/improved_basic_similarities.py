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
        self.similar_dic = defaultdict(dict)

    def save_similar_dic(self,path):
        with open(path, 'w') as f:
            cPickle.dump(self.similar_dic, f)

    def load_similar_dic(self,path):
        with open(path, 'r') as f:
            self.similar_dic = cPickle.load(f)

    def compute_similarities(self):
        self.similar_dic.clear()
        item_ids = self.model.item_ids()
        n = len(item_ids)
        for i in range(n):
            for j in range(i+1, n):
                tmp_distance = self.__pre_get_similarity(item_ids[i], item_ids[j])
                self.similar_dic[item_ids[i]][item_ids[j]] = tmp_distance
                # print item_ids[i], item_ids[j], tmp_distance

    def __pre_get_similarity(self, source_id, target_id):
        """
        Origin get_similarity function now becomes the hidden func.
        """
        source_preferences = self.model.preferences_for_item(source_id)
        target_preferences = self.model.preferences_for_item(target_id)

        if self.model.has_preference_values():
            source_preferences, target_preferences = \
                find_common_elements(source_preferences, target_preferences)

        if source_preferences.ndim == 1 and target_preferences.ndim == 1:
            source_preferences = np.asarray([source_preferences])
            target_preferences = np.asarray([target_preferences])

        if self.distance == loglikehood_coefficient:
            return self.distance(self.model.items_count(), source_preferences, target_preferences) \
                if not source_preferences.shape[1] == 0 and \
                    not target_preferences.shape[1] == 0 else np.array([[np.nan]])

        #Evaluate the similarity between the two users vectors.
        return self.distance(source_preferences, target_preferences) \
            if not source_preferences.shape[1] == 0 and \
                not target_preferences.shape[1] == 0 else np.array([[np.nan]])

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