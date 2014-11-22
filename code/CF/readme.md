Improved Crab
===

###类

####cf_recommender
包含了
1)UBCFilter 基于用户的CF（没有用上）
2)IBCFilter 基于物品的CF

####improved_item_similarity
包含了
ImprovedItemSimilarity
是基于crab中的ItemSimilarity改进的计算I2I相似度的，原始的写法复杂度太高

###执行脚本

####generate_translate_dic

1. 读取文件，生成user<->order 和 news<->order 双向翻译字典
2. 序列化到文件里

####generate_sim_and_clk

1. 计算i2i 相似度，直接序列化
2. 生成点击矩阵，稀疏表示后进行序列化

关键代码：

similarity = ImprovedItemSimilarity(model, jaccard_coefficient, num_best=10)
similarity.compute_similarities()#计算I2I相似度
similarity.save_similar_dic(IMPROVE_SIMILARITY_PATH)#保存I2I矩阵

####commit_cf

执行CF计算

关键代码：

ibcf = IBCFilter(i2i_matrix, clk_matrix, k_nearest_item=30, l_top_rec=15)
ibcf.start_cf()


####generate_result

结合热门新闻，给出每个用户最终的推荐结果


###改进的地方(待续)

1. Similarity对象是实时的计算两个向量的相似度，这非常不灵活，改进为批处理任意两个向量的相似度，并序列化到本地，下次可以load进来


