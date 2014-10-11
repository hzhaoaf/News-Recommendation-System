#coding=utf8
'''
    这个模块根据训练集生成用户的profile,涉及到的特征
    1,从训练集中生成每个用户的阅读list
    2,根据不同的模型生成用户的keywords
'''

topN = 5
data_dir = '/Users/huanzhao/projects/recommendation-system-contest/data/splited_data/'
train_data_path = data_dir + 'segmented_train_data.txt'
user_topkeywords_path = data_dir + 'uid2top%skeywords.txt' % topN
user_read_list_path = data_dir + 'user_read_list.txt'

from generate_user_keywords_by_title import generate_user_topkeywords

def generate_user_read_list(train_data_path, user_read_list_path):
    '''
        从训练集中生成每个用户的阅读list
        输入：训练集
        输出：输出到文件中,每一行一个用户信息:uid:NUM:newsid1,newsid2,...
    '''
    f = open(train_data_path, 'r')
    line = f.readline()
    users_nids = {}
    while line:
        parts = line.strip().split('\t')
        uid, newsid = parts[0].strip(), parts[1].strip()
        users_nids.setdefault(uid, []).append(newsid)
        line = f.readline()
    users_nids = sorted(users_nids.items(), key=lambda d:len(d[1]), reverse=True)
    fw = open(user_read_list_path, 'w+')
    fw.write('\n'.join(['%s:%s:%s' % (uid, len(nids), ','.join(nids)) for uid, nids in users_nids]))
    fw.close()

def run():
    generate_user_read_list(train_data_path, user_read_list_path)

    generate_user_topkeywords(train_data_path, user_read_list_path, user_topkeywords_path, topN)

def main():
    run()

if __name__ == '__main__':
    main()
