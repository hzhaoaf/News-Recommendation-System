# -*- coding: utf-8 -*-
__author__ = 'wangjz'


from generate_translate_dic import generate_translate_dic
from generate_sim_and_clk import generate_sim_and_clk
from commit_cf import commit_cf
from generate_result import generate_result

"""使用CF计算的整体流程，请每行分别执行"""
"""在CONSTANT里面设置好相应的输入文件路径"""
#输入输出定义在CONSTANS，输入包括 data.txt文件和user_candidate_hot_news.txt
#最终的输出是final_result.csv

#[1]generate_translate_dic 读取文件，生成user<->order 和 news<->order 双向翻译字典 序列化到文件里
# generate_translate_dic()

#[2]generate_sim_and_clk 计算i2i 相似度，直接序列化,生成点击矩阵，稀疏表示后进行序列化
# generate_sim_and_clk()

#[3]commit_cf 执行CF计算
# commit_cf()

# #[4]generate_result 结合热门新闻，给出每个用户最终的推荐结果
# generate_result()