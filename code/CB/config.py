#coding=utf8
'''
    存储实验中所有的配置信息，包括各种文件路径，以及TopN信息
'''
#控制使用哪一部分数据做实验，为true表示使用完全版的训练集
use_contest_data = False

#控制用户关键词的数目
User_Keywords_topN = 5

#总的目录
dir_ = '/Users/huanzhao/projects/recommendation-system-contest/data/'


#不同实验对应的目录
data_dir = dir_ + 'splited_data/'
if use_contest_data:
    data_dir = dir_ + 'contest_data/'


#计算tfidf需要用到的文件
corpus_path =  data_dir + 'train_data_unique_nid.txt'
news_tfidf_dir = data_dir + 'tfidf_res/'
user_keywords_by_tfidf = data_dir + 'user_keywords_by_tfidf/'

#分词，去停用词后的训练集
train_data_path = data_dir + 'segmented_train_data.txt'

#用户的TopN keywords保存路径
user_topkeywords_path = data_dir + 'uid2top%skeywords.txt' % User_Keywords_topN

#用户阅读列表保存路径
user_read_list_path = data_dir + 'user_read_list.txt'

#待索引的文件
raw_data_path = data_dir + 'train_data_unique_nid.txt'

#索引保存路径
indexed_file_path = data_dir + 'index_file'

#控制最终给用户推荐的文章数
REC_NUM = 3

#通过时间和阅读历史过滤出的待推荐的文章合集
user_candidate_newsids_path = data_dir + 'user_candidate_newsids.txt'

#推荐结果
recommend_res_path = data_dir + 'recommend_news_by_tfidf.csv'
