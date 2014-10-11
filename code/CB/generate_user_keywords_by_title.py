#coding=utf8
'''
    从标题分词的结果中进行统计分析，生成每个user的keywords
    1, 从训练数据中生成news_id和title（分词后）的映射
    2, 从user_read_list文件中中获取用户的阅读列表uid-newsids
    3, 利用1中生成的map获取用户阅读的全部关键词
    4，对关键词进行统计，输出topN by frequency
'''


def generate_newsid2title_map(train_data_path):
    '''
        完成step1
    '''
    print 'run generate_newsid2title_map...'
    lines = open(train_data_path, 'r').readlines()
    newsid2title_map = {}
    for l in lines:
        parts = l.strip().split('\t')
        if parts[0] in newsid2title_map:
            continue
        title_segments = parts[3].split()
        newsid2title_map[parts[1]] = title_segments
    return newsid2title_map

def generate_uid2newsids_map(user_read_list_path):
    '''
        完成step2
    '''
    print 'run generate_uid2newsids_map...'
    uid2newsids_map = {}
    f = open(user_read_list_path, 'r')
    line = f.readline()
    while line:
        parts = line.strip().split(':')
        uid2newsids_map[parts[0]] = parts[2].strip().split(',')
        line = f.readline()
    return uid2newsids_map

def generate_user_keywords(uid2newsids_map, newsid2title_map):
    '''
        完成step3
    '''
    print 'run generate_user_keywords...'
    user_keywords = []
    for uid, newsids in uid2newsids_map.items():
        keywords = []
        for nid in newsids:
            keywords.extend(newsid2title_map.get(nid, []))
        user_keywords.append((uid, keywords))
    return user_keywords

def generate_top_keywords(user_keywords, user_topkeywords_path, topN):
    '''
        完成step4
        结果存在文件中
    '''
    print 'run generate_top_keywords...'
    def get_keywords_cnt(keywords):
        '''
            传入一个keywords列表，统计次数，按照cnt降序返回(keyword, cnt)的list
        '''
        words_cnt = {}
        for kwd in keywords:
            words_cnt[kwd] = words_cnt.get(kwd, 0) + 1
        keywords_cnt = sorted(words_cnt.items(), key=lambda d: d[1], reverse=True)
        return keywords_cnt

    user_topkeywords = []
    for uid, keywords in user_keywords:
        #import pdb;pdb.set_trace()
        keywords_cnt = get_keywords_cnt(keywords)
        user_topkeywords.append((uid, keywords_cnt))
    #keywords的形式 (kwd, cnt)，这里排序是希望最后的user-topkeywords的结果
    #按照top 1的word的cnt降序排列，便于观察数据
    #user_topkeywords= sorted(user_topkeywords, key=lambda d: d[1][0][1], reverse=True)

    f = open(user_topkeywords_path, 'w+')
    for uid, keywords_cnt in user_topkeywords:
        line = uid + '\t' + ','.join([kwd+'-'+str(cnt) for kwd, cnt in keywords_cnt[:topN]])
        f.write(line + '\n')
    f.close()

def generate_user_topkeywords(train_data_path, user_read_list_path, user_topkeywords_path, topN=5):
    print 'run generate_user_top%skeywords, consist of 4 steps...\n' % topN

    newsid2title_map = generate_newsid2title_map(train_data_path)
    print_map(newsid2title_map)

    uid2newsids_map = generate_uid2newsids_map(user_read_list_path)
    print_map(uid2newsids_map)

    user_keywords = generate_user_keywords(uid2newsids_map, newsid2title_map)

    generate_top_keywords(user_keywords, user_topkeywords_path, topN)

    print '\nfinished, res saved in %s' % user_topkeywords_path

def print_map(map_, limit=5):
    info = []
    for k, w in map_.items():
        if isinstance(w, list):
            w = '-'.join(w)
        unit = '(%s, %s)' % (k, w)
        info.append(unit)
        if len(info) > limit:
            break
    print ','.join(info)

def main():
    generate_user_topkeywords()

if __name__ == '__main__':
    main()






