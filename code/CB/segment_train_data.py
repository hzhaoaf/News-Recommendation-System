#coding=utf8
'''
    这个将训练数据中的title，content进行分词，然后存入新的文件
    同时会基于newsid进行消重
'''

import time

from util import text_segment, load_stopwords, unicode2str

data_dir = '/Users/huanzhao/projects/recommendation-system-contest/data/'
train_data_path = data_dir + 'train_data.txt'
stop_words_path = data_dir + 'stopwords_ch.txt'


def segment_train_data(train_data_path, saved_file):
    '''
    '''

    #filter_stopwords = lambda x: text_segment(x)
    stopwords = load_stopwords()

    def filter_stopwords(words):
        #import pdb;pdb.set_trace()
        return [r for r in words if r not in stopwords]

    print 'run segment_train_data...'
    titles = []
    f = open(train_data_path, 'r')
    line = f.readline()
    start_time = time.time()
    res = []
    cnt = 0
    newsids = set()
    round_start = time.time()
    while line:
        #line = unicode2str(line)
        parts = line.strip().split('\t')
        if parts[1].strip() in newsids:
            line = f.readline()
            continue

        newsids.add(parts[1].strip())
        cnt += 1
        parts[3] = unicode2str(' '.join(filter_stopwords(text_segment(parts[3], is_ret_utf8=True))))
        parts[4] = unicode2str(' '.join(filter_stopwords(text_segment(parts[4], is_ret_utf8=True))))
        res.append('\t\t'.join(parts))

        if cnt % 1000 == 0:
            round_cost = (time.time() - round_start)
            round_start = time.time()
            print 'segmenting %s, cost %.3fs, aver=%.3fs' % (cnt, round_cost, round_cost / 100.0 )

        line = f.readline()

    end_time = time.time()
    total_cost = (end_time - start_time) / 60.0
    aver_cost = total_cost / float(cnt)

    print 'segmenting all %s records, total cost=%.3fmin, average=%.3fmin' % (cnt, total_cost, aver_cost)

    fw = open(data_dir + saved_file, 'w+')
    fw.write('\n'.join(res))
    fw.close()
    print 'res is saved in %s' % (saved_file)

def main():
    saved_file = 'train_data_with_segmenting.txt'
    segment_train_data(train_data_path, saved_file)

if __name__ == '__main__':
    main()
