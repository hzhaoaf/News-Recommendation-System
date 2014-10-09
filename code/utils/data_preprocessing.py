#coding=utf8
'''
    这个模块用来保存一些预处理的方法
'''

data_dir = '/Users/huanzhao/projects/recommendation-system-contest/data/'
train_data_path = data_dir + 'train_data.txt'
splited_train_data_path = data_dir + 'splited_train_data.txt'
splited_test_data_path = data_dir + 'splited_test_data.txt'

def split_train_data(train_data_path, splited_train_data_path, splited_test_data_path):
    '''
        将训练数据拆分成两部分，每个用户的最后一条阅读记录作为我们
        自己的测试集，用来对推荐系统进行验证
        输入：原始训练数据
        输出：拆分后的训练集，拆分后的测试集（和官方测试集保持一致）
    '''
    print 'run split_train_data...'
    f = open(train_data_path, 'r')
    line = f.readline()
    users_news = {}#uid: [和训练集结构一样的数据集]
    while line:
        parts = line.strip().split('\t')
        uid = parts[0].strip()
        users_news.setdefault(uid, []).append(parts)
        line = f.readline()

    for uid, news in users_news.items():
        users_news[uid] = sorted(news, key=lambda d: int(d[2]), reverse=True)#d[2]即为时间戳

    splited_train_data, splited_test_data = [], []
    for uid, news in users_news.items():
        splited_train_data.extend(news[1:])
        splited_test_data.append((news[0][0], news[0][1]))#测试集只需要uid,newsid

    fw1 = open(splited_train_data_path, 'w+')
    #import pdb;pdb.set_trace()
    fw1.write('\n'.join(['\t'.join(r) for r in splited_train_data]))
    fw1.close()

    fw2 = open(splited_test_data_path, 'w+')
    fw2.write('userid,newsid\n')
    fw2.write('\n'.join([','.join(r) for r in splited_test_data]))
    fw2.close()
    print 'finish spliting, splited_train_data saved in %s\nsplited_test_data saved in %s' % (splited_train_data_path, splited_test_data_path)

def main():
    split_train_data(train_data_path, splited_train_data_path, splited_test_data_path)

if __name__ == '__main__':
    main()
