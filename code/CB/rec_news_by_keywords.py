#coding=utf8
'''
    这个模块用来实现content-based的新闻推荐，利用用户生成的keywords，
    使用xapian进行检索，返回结果中，filter掉用户已经读过的，进行推荐
'''

from util import print_map
from search import search

data_dir = '/Users/huanzhao/projects/recommendation-system-contest/data/splited_data/'
user_topkeywords_path = data_dir + 'uid2top5keywords.txt'
user_read_list_path = data_dir + 'user_read_list.txt'

index_file_path = data_dir + 'index_file'

REC_NUM = 3 # 控制最终给用户推荐的文章数
recommend_res_path = data_dir + 'recommend_news.txt'

def get_user_keywords():
    '''
        从用户的关键词列表中获得keywords
        example: 5533175 克里米亚-1,感谢-1,何华章-1,官方-1,处置-1
    '''
    print 'run get_user_keywords, input: %s' % user_topkeywords_path
    lines = open(user_topkeywords_path, 'r+').readlines()
    user_keywords = {}
    for l in lines:
        parts = l.strip().split('\t')
        uid = parts[0]
        keywords = [r.split('-')[0] for r in parts[1].split(',')]
        user_keywords[uid] = keywords

    print 'finish get user_keywords, example is\n %s ' % print_map(user_keywords)
    return user_keywords

def get_user_read_list():
    '''
        从user_read_list文件中读入每个用户的阅读历史，两个作用:
        user_read_list每一行的样例: uid:N:newsid1,newsid2,
        1,从返回的结果中过滤掉这部分内容
        2,用来控制xapian中对每个用户的返回值结果
        输出: {uid: [newid1, newsid2]}
    '''
    print 'run get_user_read_list, input: %s' % user_read_list_path
    lines = open(user_read_list_path, 'r').readlines()
    uid2newsids = {}
    for l in lines:
        parts = l.split(':')
        #如果用户阅读数小于等于10，则不给他推荐
        if int(parts[1]) <= 10:
            continue
        uid = parts[0]
        nids = parts[2].split(',')
        uid2newsids[uid] = nids

    print 'finish get user_read_list, example is\n %s ' % print_map(uid2newsids)
    return uid2newsids


def get_recommend_news():
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
        search_res = search(index_file_path, query_str, ret_num=read_num+REC_NUM)
        user_rec_news = [r for r in search_res if r not in read_news]
        rec_res.append((uid, user_rec_news[:REC_NUM]))

    f = open(recommend_res_path, 'w+')
    f.write('#userid,newsid\n')
    for uid, rec_news in rec_res:
        f.write('\n'.join([','.join((uid, nid)) for nid in rec_news]))
        f.write('\n')

    f.close()
    print 'finish recommending, res saved in %s' % recommend_res_path

def run():
    get_recommend_news()

if __name__ == '__main__':
    run()


