#coding=utf8
'''
    保存user_profile中的一些util函数
'''

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
    return uid2newsids_map

