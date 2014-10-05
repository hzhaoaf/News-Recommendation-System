# -*- coding: utf-8 -*-

__author__ = 'wangjz'

import cPickle
from CONSTANT import *


with open(ONE_OUT_TEST_DATA_PATH, 'r') as f:
    test_data = cPickle.load(f)

test_data = sorted(test_data, key=lambda x:x[0])

print test_data[0]

with open(COMMIT_RESULT_PATH, 'w') as f:
    for (u, v) in test_data:
        f.write(str(u) + ',' + str(v) + '\n')



