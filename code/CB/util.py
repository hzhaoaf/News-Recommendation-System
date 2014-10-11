#coding=utf8
'''
    一些工具函数，辅助
'''
import time
import logging

import jieba

data_dir = '/Users/huanzhao/projects/recommendation-system-contest/data/splited_train_data.txt'
train_data_path = data_dir + 'train_data.txt'

def unicode2str(str_):
    if isinstance(str_, unicode):
        return str_.encode('utf8')
    return str_

def str2unicode(str_):
    if isinstance(str_, str):
        return str_.decode('utf8')
    return str_

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


def extract_title(saved_file, is_remove_stopwords=False):
    '''
        从训练数据中提取所有的标题，存入文件中
    '''
    print 'run extract_title...'
    titles = []
    f = open(train_data_path, 'r')
    if is_remove_stopwords:
        stopwords = load_stopwords()
    line = f.readline()
    start_time = time.time()
    while line:
        parts = line.strip().split('\t')
        segres = text_segment(parts[3])
        segres = [r.encode('utf-8') for r in segres]
        if is_remove_stopwords:
            #import pdb;pdb.set_trace()
            segres = [r for r in segres if r not in stopwords]
        titles.append((parts[1], parts[3], '-'.join(segres)))
        line = f.readline()
    end_time = time.time()

    print 'extract %s titles(remove_stopwords=%s), average cost %.3fs' % (len(titles), is_remove_stopwords, (end_time-start_time)/float(len(titles)))

    fw = open(data_dir + saved_file, 'w+')
    fw.write('\n'.join(['\t'.join(t) for t in titles]))
    fw.close()
    print 'res is saved in %s' % (saved_file)

def text_segment(raw_text, is_ret_utf8=False):
    '''
        调用jieba的分词，输入整句，返回list，每个元素为一个词
    '''
    try:
        segres = jieba.cut(raw_text)
        res =  list(segres)
        if is_ret_utf8:
            res = [unicode2str(r) for r in res]
        return [r for r in res if r.strip()]
    except Exception as e:
        print 'error occured in fenci: %s' % e
        res = re.split(ur'\s', text) if text else []
        return [r for r in res if r.strip()]

def test_stopwords():
    stopwords = load_stopwords()
    word = '的'
    print list(stopwords)[2]
    print word in stopwords

def log_matches(querystring, offset, pagesize, matches):
    logger = logging.getLogger("xapian.search")
    logger.info(
        "'%s'[%i:%i] = %s",
        querystring,
        offset,
        offset + pagesize,
        ' '.join(str(docid) for docid in matches),
        )

def main():
    extract_title('newsid_title_map.txt', is_remove_stopwords=True)
    #test_stopwords()


if __name__ == '__main__':
    main()
