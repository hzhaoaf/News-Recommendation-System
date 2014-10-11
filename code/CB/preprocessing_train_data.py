#coding=utf8
'''
    这个模块用来对训练数据进行预处理，包括:
        1,对训练结果进行分词
'''
import time
from util import unicode2str, text_segment

data_dir = '/Users/huanzhao/projects/recommendation-system-contest/data/'
stop_words_path = data_dir + 'stopwords_ch.txt'

def load_stopwords():
    '''
        加载stopwords，返回停用词set
    '''
    lines = open(stop_words_path, 'r').readlines()
    stopwords = [l.strip() for l in lines if l]
    print 'load stopwords, example: %s...' % (','.join(stopwords[:10]))
    return set(stopwords)

def segment_train_data(train_data_path, saved_original_file, saved_unique_file):
    '''
        包括对title和content的分词与去掉停用词
        生成两份文件:
            1,和原数据结构保持一致的分词后结果;
            2,将文章利用newsid进行消重,得到一份新的data，用来index中使用(unique_news)
    '''
    stopwords = load_stopwords()
    def filter_stopwords(words):
        return [r for r in words if r not in stopwords]

    print 'run segment_train_data...'
    f = open(train_data_path, 'r')
    line = f.readline()
    nid2tc, original_news, unique_news, newsids = {}, [], [], set()
    start_time, round_start, cnt = time.time(), time.time(), 0
    while line:
        parts = line.strip().split('\t')
        original_news.append(parts)
        nid = parts[1].strip()
        if  nid in newsids:
            line = f.readline()
            continue
        newsids.add(nid)
        cnt += 1

        parts[3] = unicode2str(' '.join(filter_stopwords(text_segment(parts[3], is_ret_utf8=True))))
        parts[4] = unicode2str(' '.join(filter_stopwords(text_segment(parts[4], is_ret_utf8=True))))
        unique_news.append('\t'.join(parts))
        nid2tc[parts[1]] = (parts[3], parts[4])

        if cnt % 1000 == 0:
            round_cost = (time.time() - round_start)
            round_start = time.time()
            print 'segmenting %s, cost %.3fs, aver=%.3fs' % (cnt, round_cost, round_cost / 100.0 )

        line = f.readline()
    end_time = time.time()
    total_cost = (end_time - start_time) / 60.0
    aver_cost = total_cost / float(cnt)
    print 'segmenting all %s records(cnt=%s), total cost=%.3fmin, average=%.3fmin' % (len(unique_news), cnt, total_cost, aver_cost)

    save_original_data(original_news, nid2tc, saved_original_file)

    save_unique_data(unique_news, saved_unique_file)

def save_unique_data(unique_news, saved_unique_file):
    fw = open(saved_unique_file, 'w+')
    fw.write('\n'.join(unique_news))
    fw.close()
    print 'unique_news is saved in %s' % saved_unique_file

def save_original_data(original_news, nid2tc, saved_original_file):
    fw = open(saved_original_file, 'w+')
    for parts in original_news:
        seg_title, seg_content = nid2tc.get(parts[1], ('', ''))
        parts[3], parts[4] = seg_title, seg_content
        line = '\t'.join(parts)
        fw.write(line + '\n')
    fw.close()
    print 'segmented original data saved in %s' % saved_original_file

def run():
    train_dir = 'splited_data/'
    train_data_path = data_dir + train_dir + 'splited_train_data.txt'
    saved_original_file = data_dir + train_dir + 'segmented_train_data.txt'
    saved_unique_file = data_dir + train_dir + 'train_data_unique_nid.txt'
    segment_train_data(train_data_path, saved_original_file, saved_unique_file)

if __name__ == '__main__':
    run()
