# -*- coding: utf-8 -*- 
#用户编号 新闻编号 浏览时间 新闻标题 新闻详细内容 新闻发表时间

import datetime
dateC = datetime.datetime(1970,1,1)
print dateC


FILE_PATH = '../../data/data.txt'
f = open(FILE_PATH,'r')

content = f.readlines()

user_set = set()
article_set = set()

read_time_list = list()
for c in content:
    c = c[:-1]
    items = c.split('\t')
    user_set.add(items[0])
    article_set.add(items[1])
    read_time_list.append(int(items[2]))

print '用户数量 %s' % len(user_set)
print '文章数量 %s' % len(article_set)

read_time_list = sorted(read_time_list)

print read_time_list[:30]
print read_time_list[-30:]

