DATA
=====================
放数据的文件夹

###官方数据

1. data.txt 训练数据
2. demo.csv 提交的样例
 
###翻译字典

generate_translate_dic.py的输出

1. i2o.pickle
2. o2i.pickle
3. o2u.pickle
4. u2o.pickle

###训练集的全集

generate_clk_matrix.py 的输出

1. clk_matrix.pickle 

###训练集和测试集

以每个用户最后阅读的一条新闻做为测试集，之前的全作为训练集
generate_one_out_clk_matrix_and_test.py 的输出

1. one_out_clk_matrix.pickle
2. one_out_test_data.pickle
