# -*- coding: utf-8 -*-

__author__ = 'wangjz'

import cPickle
from CONSTANT import *
from CF.user_based_CF import UBCFilter
import numpy as np

with open(ONE_OUT_CLK_MATRIX_PATH, 'r') as f:
    clk_matrix = cPickle.load(f)

with open(ONE_OUT_COS_U2U_SIM_MATRIX_PATH, 'r') as f:
    u2u_sim_mat = cPickle.load(f)

clk_matrix = np.int16(clk_matrix.todense()).tolist()
u2u_sim_mat = np.float16(u2u_sim_mat.todense()).tolist()

ubc_filter = UBCFilter(u2u_sim_mat, clk_matrix, k_nearest=30, l_top=5)
ubc_filter.start_cf()
res = ubc_filter.result

with open(REC_RESULT,'wb') as f:
    cPickle.dump(res, f)

