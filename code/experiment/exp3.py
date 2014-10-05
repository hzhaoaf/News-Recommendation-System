# -*- coding: utf-8 -*-

__author__ = 'wangjz'

from CONSTANT import *

with open(ORIGIN_DATA_PATH, 'r') as f:
    lines = f.readlines()[1:]

dict = {}

for l in lines:
    items = l.split('\t')
    user_id = int(items[0])
    item_id = int(items[1])
    if user_id in dict:
        if len(dict[user_id]) == 1:
            dict[user_id].append(item_id)
    else:
        dict[user_id] = [item_id]

result = []
for u,v in dict.items():
    result.append((u,v[0]))
    result.append((u,v[1]))

data = sorted(result, key=lambda x:x[0])

print "ok"
with open(COMMIT_RESULT_PATH, 'w') as f:
    for (u, v) in data:
        f.write(str(u) + ',' + str(v) + '\n')
