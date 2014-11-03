#coding=utf8
'''
    保存user_profile中的一些util函数
'''
import time
from datetime import datetime

from util import unicode2str

def generate_uid2newsids_map(user_read_list_path):
    '''
        从用户阅读历史列表中生成用户的阅读列表（newsid表示）
    '''
    print 'run generate_uid2newsids_map...'
    uid2newsids_map = {}
    f = open(user_read_list_path, 'r')
    line = f.readline()
    while line:
        parts = line.strip().split(':')
        uid2newsids_map[parts[0]] = parts[2].strip().split(',')
        line = f.readline()
    print 'finish generating %s uid2newsids elements' % len(uid2newsids_map.items())
    return uid2newsids_map

def generate_newsid2pubtime(corpus_file):
    '''
        从原始语料中生成每篇文章id与发布时间的映射，时间转换为时间戳
    '''
    print 'run generate_newsid2pubtime...'
    id2pubtime = {}
    f = open(corpus_file, 'r')
    line = f.readline()
    while line:
        parts = line.strip().split('\t')
        id_ = parts[1].strip()
        pubtime_str = parts[5].strip()
        if pubtime_str.lower() == 'null':
            line = f.readline()
            continue
        print pubtime_str
        if ':' not in pubtime_str:
            #存在没有分和秒的
            pubtime_str += '00:00'
        pub_time = datetime.strptime(unicode2str(pubtime_str), unicode2str(u'%Y年%m月%d日%H:%M'))
        pub_time = int(time.mktime(pub_time.timetuple()))
        id2pubtime[id_] = pub_time
        line = f.readline()
    print 'finish generating %s id2pubtime elements' % len(id2pubtime.items())
    return id2pubtime

def genereate_user_newest_readtime(train_data_path):
    '''
        从训练集中获取用户阅读文章的全部时间，返回最大的时间，以时间戳形式返回
    '''
    print 'run genereate_user_newest_time...'
    uid2readtime = {}
    f = open(train_data_path, 'r')
    line = f.readline()
    while line:
        parts = line.strip().split('\t')
        uid = parts[0].strip()
        readtime = int(parts[2].strip())
        if not uid2readtime.get(uid) or readtime > uid2readtime.get(uid, 0):
            uid2readtime[uid] = readtime
        line = f.readline()

    print 'finish generating %s uid2readtime items' % len(uid2readtime.items())
    return uid2readtime

