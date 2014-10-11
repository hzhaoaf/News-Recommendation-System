# -*- coding: utf-8 -*-
'''
    这个模块对推荐结果进行评测，计算F值；
    输入: recommend_res_file, golden_test
    输出: (precision, recall, F)
'''
import sys

__author__ = 'wangjz'

def calculate_F(recommend, reality):
    """
    计算precision,recall,调和均值F

    【recommend】 userid,newsid 一对多
    [(35,100647112),
    (35,100647132),
    (107,100647132),
    ……]

    【reality】为set类型， userid,newsid 一对一
    [(35,100647112),
    (107,100647112),
    (111,100647112),]
    """
    #ΣL(ui) 推荐给所有用户的列表总长度
    sum_Lu = len(recommend)

    #测试集中用户浏览新闻的数目，本次比赛中T(ui) = 1,所以ΣT(u) = 10000
    sum_Tu = len(reality)

    #命中总次数，对于每个用户而言hit(ui) 要么是1，要么是0
    sum_hitu = 0

    for item in recommend:
        if item in reality: #疑问，这样的查询效率怎样？ 回答: 将reality的类型改为set即可
            sum_hitu += 1

    precision = 1.0 * sum_hitu / sum_Lu
    recall = 1.0 * sum_hitu / sum_Tu
    F = 2.0 / (1.0 / precision + 1.0 / recall)

    return (precision, recall,F)

def test():
    rec = [(1,2),
           (1,3),
           [1,4],
           [2,1],
           [2,2],
           [3,2]]

    rel = [(1,1),
           [2,2],
           [3,2]]

    ans = calculate_F(rec,rel)
    print ans

def run(recommend_res_file, golden_test_file):
    '''
        读入recommend_res_file, golden_test_file两个文件，生成计算F值需要的格式
    '''

    def load_items(items_file):
        lines = open(items_file, 'r').readlines()
        return [l.strip() for l in lines if not l.startswith('#')]

    rec_items = load_items(recommend_res_file)
    gt_items = set(load_items(golden_test_file))
    print 'res is(Precision, Recall, F)\n', calculate_F(rec_items, gt_items)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'please input valid parameters, valid example is:\n python calculate_F.py recommmend_res_file golden_test_file'
        sys.exit(0)
    recommend_res_file = sys.argv[1]
    golden_test_file = sys.argv[2]
    run(recommend_res_file, golden_test_file)

