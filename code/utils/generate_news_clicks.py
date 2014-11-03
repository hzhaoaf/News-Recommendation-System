#coding=utf8
'''
    读入训练集，遍历全部的阅读记录，获得文章的点击量，按照点击量排序，输出到文件
'''

data_dir = '/Users/huanzhao/projects/recommendation-system-contest/data/contest_data/'
train_data_path = data_dir + 'train_data.txt'
news_clicks_path = data_dir + 'news_clicks_stat.txt'

def run(train_data_path, news_clicks_path):

    print 'run news clicks stating...'
    f = open(train_data_path, 'r')
    line = f.readline()
    nid2clicks = {}
    nid2uid = {}
    nid2title = {}
    while line:
        parts = line.strip().split('\t')
        uid = parts[0].strip()
        nid = parts[1].strip()
        title = parts[3].strip()
        nid2clicks[nid] = nid2clicks.get(nid, 0) + 1
        nid2title[nid] = title
        line = f.readline()
    nid_clicks = sorted(nid2clicks.items(), key=lambda d: d[1], reverse=True)
    fw = open(news_clicks_path, 'w+')
    lines = ['%s\t%s\t%s' % (nid, click_count, nid2title.get(nid, '')) for nid, click_count in nid_clicks]
    fw.write('\n'.join(lines))
    fw.close()

if __name__ == '__main__':
    run(train_data_path, news_clicks_path)

