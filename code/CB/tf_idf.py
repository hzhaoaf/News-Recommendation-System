#coding=utf8
'''
    调用sklearn的api进行tf-idf的计算
'''

from util import unicode2str

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

vectorizer = CountVectorizer()
transformer = TfidfTransformer()

def test():
    corpus = ['my name is Jim',
              'i love football',
              'he watches tv games'
                ]

    X = vectorizer.fit_transform(corpus)
    print X.toarray()
    print vectorizer.get_feature_names()

    tfidf = transformer.fit_transform(X)
    print tfidf.toarray()

def generate_copurs_from_file(corpus_path):
    '''
        从训练集中读入分词后的新闻，每篇文档是一个term的list，放入一个大的list中返回
        同时，返回newsid作为保存tfidf的文件名
    '''
    f = open(corpus_path, 'r')
    line = f.readline()
    corpus, newsids = [], []
    while line:
        parts = line.split('\t\t')
        corpus.append(parts[4])
        newsids.append(parts[1].strip())
        line = f.readline()
    return newsids, corpus

def generate_tfidf(corpus_path, tfidf_dir):
    '''
        从分词和去停用词后的文档集中读入corpus和文档id,然后计算tf-idf值，结果保存在以文档id作为
        文件名的文件中
    '''
    newsids, corpus = generate_copurs_from_file(corpus_path)
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    terms = vectorizer.get_feature_names()
    weights = tfidf.toarray()
    tfidf_res = []
    for i, id_ in enumerate(newsids):
        each_tf_idf = []
        save_file = tfidf_dir + id_
        if i % 100 == 0:
            print i
        for j, term in enumerate(terms):
            if weights[i][j] > 0.0001:
                each_tf_idf.append((terms[j], weights[i][j]))
        each_tf_idf = sorted(each_tf_idf, key=lambda d: d[1], reverse=True)
        fw = open(save_file, 'w+')
        fw.write('\n'.join(['%s,%s' % (unicode2str(t), w) for t, w in each_tf_idf]))
        fw.close()

if __name__ == '__main__':
    from config import corpus_path, tfidf_dir
    generate_tfidf(corpus_path, tfidf_dir)


