#coding=utf8
'''
    根据tfidf生成每篇文章的topN关键词，然后基于这些关键词的tfidf值生成用户的特征关键词
'''
import os

from config import tfidf_dir, user_keywords_by_tfidf, user_read_list_path

from util import unicode2str
from user_util import generate_uid2newsids_map


def get_terms_weights(newsid):
    '''
        从保存的文章tfidf中读取该newsid的全部term的tfidf值，文件名就是newsid
        有的newsid最终没有生成tfidf文件，这个时候返回空dict
    '''
    weight_file = tfidf_dir + newsid
    if not os.path.isfile(weight_file):
        return {}
    lines = open(weight_file, 'r').readlines()
    terms_weights = [l.strip().split(',') for l in lines]
    return {t: w for t, w in terms_weights if t != 'null'}#null词不需要

def save_uid_terms(saved_file, uid_terms_weights):
    fw = open(saved_file, 'w+')
    fw.write('\n'.join(['%s,%s' % (unicode2str(t), w) for t, w in uid_terms_weights]))
    fw.close()

def cal_user_read_weights(uid2newsids_map):
    '''
        根据用户阅读列表获得每篇文章全部term的tfidf，累加，然后求平均，排序返回
    '''
    cnt = 0
    for uid, newsids in uid2newsids_map.items():
        cnt += 1
        uid_terms_weights = {}
        news_num = len(newsids) * 1.0
        if cnt % 100 == 0:
            print 'finish %s users, read %s news' % (str(cnt), str(news_num))
        for id_ in newsids:
            terms_weights = get_terms_weights(id_)
            for t, w in terms_weights.items():
                uid_terms_weights[t] = uid_terms_weights.get(t, 0.0) + float(w)
        uid_terms_weights = sorted(uid_terms_weights.items(), key=lambda d:d[1], reverse=True)
        uid_terms_weights = [(t, w/news_num) for t, w in uid_terms_weights]
        saved_file = os.path.join(user_keywords_by_tfidf, uid)
        save_uid_terms(saved_file, uid_terms_weights)

if __name__ == '__main__':
    uid2newsids_map = generate_uid2newsids_map(user_read_list_path)
    cal_user_read_weights(uid2newsids_map)


