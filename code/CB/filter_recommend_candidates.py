#coding=utf8
'''
    针对每个用户，选择待推荐的candidates,
    筛选规则:
        1,用户阅读的最后一篇文章的阅读时间的前1天，后3天（这两个时间可以配置）
        2,去掉用户已经阅读过的
'''

from config import train_data_path, user_read_list_path, corpus_path
from config import user_candidate_newsids_path

from user_util import generate_uid2newsids_map, generate_newsid2pubtime, genereate_user_newest_readtime

def filter():

    uid2newsids = generate_uid2newsids_map(user_read_list_path)
    uid2readtime = genereate_user_newest_readtime(train_data_path)
    nid2pubtime = generate_newsid2pubtime(corpus_path)

    user_candidate_newsids = {}
    cnt = 0
    for uid, readtime in uid2readtime.items():
        cnt += 1
        if cnt % 100 == 0:
            print 'filter news for the %d user...' % cnt
        read_nids = set(uid2newsids.get(uid, []))#读过的文章
        DAY_SECONDS = 86400
        start, end = readtime - DAY_SECONDS, readtime + 3 * DAY_SECONDS
        for nid, pubtime in nid2pubtime.items():
            if nid in read_nids:
                continue
            if pubtime > end or pubtime < start:
                continue
            user_candidate_newsids.setdefault(uid, []).append(nid)

    user_candidate_newsids = sorted(user_candidate_newsids.items(), key=lambda d: len(d[1]), reverse=True)
    fw = open(user_candidate_newsids_path, 'w+')
    fw.write('\n'.join(['%s:%s:%s' % (uid, len(nids), ','.join(nids)) for uid, nids in user_candidate_newsids]))
    fw.close()
    print 'finish filter news for %d users...' % len(user_candidate_newsids)

if __name__ == '__main__':
    filter()


