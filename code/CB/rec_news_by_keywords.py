#coding=utf8
'''
    这个模块用来实现content-based的新闻推荐，利用用户生成的keywords，
    使用xapian进行检索，返回结果中，filter掉用户已经读过的，进行推荐
'''

import os

from sklearn.metrics.pairwise import pairwise_distances as distance

from config import user_topkeywords_path, user_read_list_path
from config import indexed_file_path, recommend_res_path
from config import REC_NUM
from config import user_keywords_by_tfidf, user_candidate_newsids_path, news_tfidf_dir

from util import print_map, unicode2str
from search import search

def get_user_keywords():
    '''
        从用户的关键词列表中获得keywords
        example: 5533175 克里米亚-1,感谢-1,何华章-1,官方-1,处置-1
        输出: {uid:[k1, k2, k3, k4, k5],...}
    '''
    print 'run get_user_keywords, input: %s' % user_topkeywords_path
    lines = open(user_topkeywords_path, 'r+').readlines()
    user_keywords = {}
    for l in lines:
        parts = l.strip().split('\t')
        uid = parts[0].strip()
        keywords = [r.split('-')[0] for r in parts[1].split(',')]
        user_keywords[uid] = keywords

    print 'finish get user_keywords, example is\n %s ' % print_map(user_keywords)
    return user_keywords

def get_user_read_list():
    '''
        从user_read_list文件中读入每个用户的阅读历史，两个作用:
        1,从返回的结果中过滤掉这部分内容
        2,用来控制xapian中对每个用户的返回值结果
        输入样例: uid:N:newsid1,newsid2,
        输出: {uid: [newid1, newsid2]}
    '''
    print 'run get_user_read_list, input: %s' % user_read_list_path
    lines = open(user_read_list_path, 'r').readlines()
    uid2newsids = {}
    for l in lines:
        parts = l.split(':')
        #如果用户阅读数小于等于10，则不给他推荐
        #if int(parts[1]) <= 10:
        #    continue
        uid = parts[0].strip()
        nids = parts[2].split(',')
        uid2newsids[uid] = nids

    print 'finish get user_read_list, example is\n %s ' % print_map(uid2newsids)
    return uid2newsids

def get_recommend_news_by_xapian():
    '''
        根据每个用户的关键词，使用xapian进行检索，每个用户返回的结果为用户的
        阅读数+N(暂定为5)
    '''
    print 'run get_recommend_news...'
    user_keywords = get_user_keywords()
    uid2newsids = get_user_read_list()

    def generate_query_str(keywords):
        return ' '.join(['title:%s content:%s' % (k, k) for k in keywords])

    rec_res = []
    for uid, keywords in user_keywords.items():
        if not keywords:
            #rec_res.append(uid, [])
            continue
        if uid not in uid2newsids:
            continue
        query_str = generate_query_str(keywords)
        read_news = set(uid2newsids.get(uid, []))
        read_num = len(read_news)
        search_res = search(indexed_file_path, query_str, ret_num=read_num+REC_NUM)
        user_rec_news = [r for r in search_res if r not in read_news]
        rec_res.append((uid, user_rec_news[:REC_NUM]))

    f = open(recommend_res_path, 'w+')
    f.write('userid,newsid\n')
    for uid, rec_news in rec_res:
        print uid, rec_news
        f.write('\n'.join([','.join((uid, unicode2str(nid))) for nid in rec_news]))
        f.write('\n')

    f.close()
    print 'finish recommending, res saved in %s' % recommend_res_path

def get_user_tfidf_terms(user_terms_file, topN):
    '''
        从用户的tfidf的关键词中返回TopN
    '''
    lines = open(user_terms_file, 'r').readlines()
    parts = [l.strip().split(',') for l in lines]
    #print parts[:10]
    return [(t, float(w)) for t, w in parts][:topN]

def get_user_candidate_newsids(user_candidate_newsids_path):
    '''
        从user_candidate_newsids的文件中读入所有用户的candidate_newsids
        返回dict{uid:[nid1, nid2]}
    '''
    lines = open(user_candidate_newsids_path, 'r').readlines()
    parts = [l.strip().split(':') for l in lines]
    uid2can_newsids = {}
    for uid, num, nids_str in parts:
        nids = nids_str.strip().split(',')
        uid2can_newsids[uid] = nids
    return uid2can_newsids

def get_news_top_terms(candidate_newsids, topN):
    '''
        从给定的newsid的list中，去tfidf_res文件夹中寻找对应的文件，返回对应topN的term
        返回一个数组，[[(t1, w1), (t2, w2)],
                       ...
                       ]
        和candidate_newsids中的nid一一对应
                                                    ]
    '''
    def get_top_terms(filename, topN):
        lines = open(filename, 'r').readlines()
        parts = [l.strip().split(',') for l in lines]
        return [(t, float(w)) for t, w in parts][:topN]

    news_top_terms = []
    for nid in candidate_newsids:
        nid_file = os.path.join(news_tfidf_dir, nid)
        top_terms = get_top_terms(nid_file, topN)
        news_top_terms.append(top_terms)
    return news_top_terms

def generate_feature_vectors(user_terms, candidate_news_top_terms, topN):
    '''
        利用用户的topN terms和candidate news的topN terms,生成计算相似度的向量
        已user_terms为标准对齐全部的features
        生成的维度为topN * 2，不存在的term记为0.0
        返回user_vector: [w1, w2, w3, ..., w(2N)]
           can_news_vectors = [[w1, w2, w3, ..., w(2N)],
                               [z1, z2, z3, ..., z(2N)]
                                ]
    '''
    user_vector = [w for _, w in user_terms] + [0.0] * (topN * 2 - len(user_terms))#用户的terms可能不足topN个
    can_news_vectors = []
    for each_news_terms in candidate_news_top_terms:
        news_vector = [0.0] * topN * 2
        pos = topN
        for term, weight in each_news_terms:
            #不在用户的terms中，从topN个开始补齐
            if term not in user_terms:
                news_vector[pos] = weight
                pos += 1
            #否则按照该词在user_terms中对应的位置填好weight
            else:
                pos = user_temrs.index(term)
                news_vector[pos] = weight
        can_news_vectors.append(news_vector)

    return user_vector, can_news_vectors

def get_recommend_news_by_tfidf_sim():
    '''
        基于tfidf生成的user profile和文章的keywords(topN,设为20)，从用户的candidate articles中选出相似度最大的TopN返回
    '''
    topN = 20
    uids = os.listdir(user_keywords_by_tfidf)
    uid2can_newsids = get_user_candidate_newsids(user_candidate_newsids_path)
    user_recommend_res = []
    #recommend_res_path = recommend_res_path.replace('.csv', '_by_tfidf.csv')
    cnt =0
    for uid in uids:
        cnt += 1
        if cnt % 100 == 0:
            print 'recommend %d user: %s' % (cnt, uid)
        user_terms = get_user_tfidf_terms(os.path.join(user_keywords_by_tfidf, uid), topN)
        candidate_newsids = uid2can_newsids.get(uid, [])
        if not candidate_newsids:
            continue
        candidate_news_top_terms = get_news_top_terms(candidate_newsids, topN)
        #can_news_vectors和candidate_newsids中的nid一一对应
        user_vector, can_news_vectors = generate_feature_vectors(user_terms, candidate_news_top_terms, topN)
        #调用sklearn接口，可以一次计算user和全部news的cosine distance
        #注意，该接口的值是1-product(v1, v2), 所以值越小，越相似，表示distance越小
        user_news_distances = distance(user_vector, Y=can_news_vectors, metric='cosine')
        user_news_distances = zip(candidate_newsids, user_news_distances.tolist()[0])
        user_news_distances = sorted(user_news_distances, key=lambda d: d[1])

        user_recommend_res.append((uid, [nid for nid, d in user_news_distances][:REC_NUM]))

    fw = open(recommend_res_path, 'w+')
    fw.write('userid,newsid\n')
    cnt = 0
    for uid, rec_news in user_recommend_res:
        #import pdb;pdb.set_trace()
        cnt += 1
        if cnt % 100 == 0:
            print 'finish %d user: %s, %s' %(cnt, uid, ' '.join(rec_news))
        fw.write('\n'.join([','.join((uid, unicode2str(nid))) for nid in rec_news]))
        fw.write('\n')
    fw.close()
    print 'finish recommending, res saved in %s' % recommend_res_path

def run():
    get_recommend_news_by_tfidf_sim()

if __name__ == '__main__':
    run()

