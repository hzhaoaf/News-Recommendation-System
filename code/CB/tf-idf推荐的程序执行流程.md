###content-based下利用tf-idf推荐的程序执行流程


1.拆分训练集，运行code/utils/data_preprocessing.py文件，将官方提供的训练集拆成两份，一份作为训练集，一份作为测试集。拆分规则：每个用户阅读的最后一条数据作为测试集；其他作为测试集;代码在code/utils

#####以下代码全部在CB的目录下

2.python preprocessing_train_data.py 从训练集中读入数据，对title和content进行分词，并去掉停用词，用分词后的结果替代原始数据集；同时生成另外一份数据，根据newsid进行消重得到文章的全集，用来后续计算tfidf值；

3.python tf_idf.py 运行此模块生成文章的tfidf值。输入两个参数: 1中消重后的文章合集路径，tfidf的输出结果目录；每篇文章的tfidf值保存在此目录下，以文章newsid命名

4.python generate_user_keywords_by_tfidf.py 此模块根据每篇文章的tfidf值取出TopN的关键词，结合用户的阅读历史，生成用户的兴趣关键词;

5.接下来就可以进行推荐:
	
	1.	python filter_recommend_candidates.py 这个模块用来为每个用户选择推荐的candidate文章；选择规则为每个用户最后的阅读时间的前一天，后3天时间范围的文章；
	2.	根据1中filter的文章，利用文章的关键词（tfidf）和用户的关键词进行相似度计算，选择cosine距离，返回相似度最高的top 3作为最终的推荐结果；