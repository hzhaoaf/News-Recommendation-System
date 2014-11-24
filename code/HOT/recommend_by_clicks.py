#coding=utf8
'''
    基于热门点击进行推荐，具体策略如下:
        1, 选择用户最后一条阅读时间为基准，选择过去一段时间内的热门点击新闻；
        2, 这个一段的选择如下:
            a)如果是在早上12点以前，往后推12个小时；
            b)如果是在白天12点以后阅读，只往前推6个小时；
    基本是拍脑袋的决定
'''
import os, sys
import time
import logging
from datetime import datetime

sys.path.append('../')

log_file = 'log/hot_news-%s.log' % datetime.now().strftime('%Y-%m-%d')
#logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')

from CB.user_util import genereate_user_newest_readtime, generate_uid2newsids_map
from CB.config import train_data_path, user_read_list_path, REC_NUM, golden_test_path, news_clicks_path

def get_news_total_clicks(news_clicks_path):
    '''
        从news_clicks_stats中获取一条新闻最终的点击量
    '''
    lines = open(news_clicks_path, 'r').readlines()
    parts = [l.strip().split('\t') for l in lines]
    nid2clicks = {nid: clicks for nid, clicks, title in parts}
    return nid2clicks

def get_user_read_from_golden_test(golden_test_path):
    '''
        从golden_test中获取用户的的阅读记录，和用户的推荐列表中的点击数进行对比
    '''
    lines = open(golden_test_path, 'r').readlines()
    lines = [l.strip().split(',') for l in lines] #第一行是‘userid,newsid’
    uid2nid = {uid: nid for uid, nid in lines[1:]}
    return uid2nid

def get_user_recommend_timerange(latest_read_time):
    '''
        传入的类型为时间戳,
        返回(from, to)时间戳区间，用来计算这段时间的热门新闻
    '''
    hour = datetime.fromtimestamp(latest_read_time).hour
    if hour > 12:
        interval = 6
    elif hour <= 12:
        interval = 12
    #interval = 24
    to_ = latest_read_time + 3600 * interval
    from_ = latest_read_time - 3600 * interval
    return from_, to_

def get_news_info(train_data_path):
    '''
        从训练集中读入news的nid, read_time，用来计算热门新闻
    '''
    f = open(train_data_path, 'r')
    line = f.readline()
    news_info = []
    while line:
        parts = line.strip().split('\t')
        nid = parts[1]
        read_timestamp = int(parts[2])
        title = parts[3]
        news_info.append((nid, read_timestamp))
        line = f.readline()
    news_info = sorted(news_info, key=lambda d: d[1], reverse=True)
    return news_info

def get_hot_news_by_timerange(from_, to_, news_info, nid2clicks, user_read_news, real_clicked_nid, retNum=3):
    '''
        从训练集中读入
        news_info里已经按照时间戳降序排列，所以可以用简单的剪纸，提高查询效率
        日志记录: 推荐的N条新闻的clicks,用户实际阅读的新闻的clicks，以及排名
    '''
    def get_rank(news_clicks, nid):
        '''
            给一个newsid,从排序后的推荐候选集返回其排名
            不存在返回-1
        '''
        cnt = 0
        for nid_, _ in news_clicks:
            cnt += 1
            if nid == nid_:
                return cnt
        return -1

    can_news_clicks = {}
    for nid, ts in news_info:
        if ts > to_:
            continue
        elif ts < from_:
            #说明后面的都已经很小了
            break
        else:
            can_news_clicks[nid] = can_news_clicks.get(nid, 0) + 1

    news_clicks = sorted(can_news_clicks.items(), key=lambda d:d[1], reverse=True)
    logging.info('candidate_hot_news(%s): %s', len(news_clicks), ' '.join(['%s=%s(%s)' % (nid, clicks, nid2clicks[nid]) for nid, clicks in news_clicks[:5]]))
    logging.info('user_read_news: %s, can_rank=%s, present_clicks=%s, total_clicks=%s', real_clicked_nid, get_rank(news_clicks, real_clicked_nid), can_news_clicks.get(real_clicked_nid, -1), nid2clicks.get(real_clicked_nid, -1))
    rec_news = [nid for nid, click_num in news_clicks if nid not in user_read_news]
    logging.info('recommend news: %s', ','.join(rec_news[:10]))
    return rec_news[:retNum] if retNum else rec_news

def recommend_hot_news():
    logging.info('*****This is the log for hot_news_recommendataion****')
    logging.info('timerange config from=t-interval, to=t+inteval, inverval=12 if hour < 12 else 6')
    uid2newsids = generate_uid2newsids_map(user_read_list_path)
    uid2readtime = genereate_user_newest_readtime(train_data_path)
    uid2nid = get_user_read_from_golden_test(golden_test_path)
    news_info = get_news_info(train_data_path)
    nid2clicks = get_news_total_clicks(news_clicks_path)

    cnt = 0

    rec_res = []
    start_time, round_start = time.time(), time.time()
    for uid, read_nids in uid2newsids.items():
        cnt += 1
        #import pdb;pdb.set_trace();
        if uid not in uid2readtime:
            continue
        if cnt % 100 == 0:
            round_end = time.time()
            aver_cost = (round_end - round_start) / 100.0
            logging.info('finish process %d users, aver cost(recent 100 users):  %.2fs', cnt, aver_cost)
            round_start = time.time()
        latest_read_time = uid2readtime[uid]
        from_, to_ = get_user_recommend_timerange(latest_read_time)
        real_clicked_nid = uid2nid.get(uid, '0')
        rec_news = get_hot_news_by_timerange(from_, to_, news_info, nid2clicks, read_nids, real_clicked_nid, retNum=REC_NUM)
        [rec_res.append((uid, nid)) for nid in rec_news]

    filename = 'rec_hot_news_top%d.csv' % REC_NUM
    fw = open(filename, 'w+')
    fw.write('')
    fw.write('userid,newsid\n')
    fw.write('\n'.join(['%s,%s' % (uid, nid) for uid, nid in rec_res]))
    fw.close()
    logging.info('*****res saved in %s, hot_news_recommendataion finished!!!****', filename)

def get_user_candidate_hot_news():
    '''
        这个函数用来生成给用户推荐的新闻集合，根据用户阅读最后一条新闻的时间，得到一个时间区间的热门新闻；
        时间区间的生成方法:
            1，如果时间是中午12点以后，则前后扩展6小时；
            2，如果是12点以前，则前后扩展12小时
        这个扩展规则是目前基于热门新闻进行推荐在本地测试集中最好的结果
    '''
    uid2newsids = generate_uid2newsids_map(user_read_list_path)
    uid2readtime = genereate_user_newest_readtime(train_data_path)
    uid2nid = get_user_read_from_golden_test(golden_test_path)
    news_info = get_news_info(train_data_path)
    nid2clicks = get_news_total_clicks(news_clicks_path)

    user_can_hot_news = []

    for uid, read_nids in uid2newsids.items():
        latest_read_time = uid2readtime[uid]
        from_, to_ = get_user_recommend_timerange(latest_read_time)
        from_time = datetime.fromtimestamp(from_)
        to_time = datetime.fromtimestamp(to_)
        logging.info('user=%s, clicks=%s, recommend time from (%s, %s)', uid, len(read_nids), from_time.strftime('%m-%d %H:%M'), to_time.strftime('%m-%d %H:%M'))
        real_clicked_nid = uid2nid.get(uid, '0')
        hot_news = get_hot_news_by_timerange(from_, to_, news_info, nid2clicks, read_nids, real_clicked_nid, retNum=-1)
        user_can_hot_news.append((uid, ','.join(hot_news)))

    fw = open('user_candidate_hot_news.txt', 'w+')
    fw.write('\n'.join(['%s:%s' % (uid, nids) for uid, nids in user_can_hot_news]))
    fw.close()


if __name__ == '__main__':
    #recommend_hot_news()
    get_user_candidate_hot_news()


