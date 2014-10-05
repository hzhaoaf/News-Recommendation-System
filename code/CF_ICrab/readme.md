Improved Crab
===

改进的地方

1. Similarity对象是实时的计算两个向量的相似度，这非常不灵活，改进为批处理任意两个向量的相似度，并序列化到本地，下次可以load进来
2，ItemBasedRecommender找某个user_id最相似的前k个item_id的时候使用了全部排序，再找出前K个，改用堆