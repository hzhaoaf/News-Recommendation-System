#coding=utf8
'''
    存储实验中所有的配置信息，包括各种文件路径，以及TopN信息
'''

#控制用户关键词的数目
User_Keywords_topN = 5

#总的目录
data_dir = '/Users/huanzhao/projects/recommendation-system-contest/data/splited_data/'

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

#推荐结果
recommend_res_path = data_dir + 'recommend_news.txt'
