# -*- coding: utf-8 -*-

__author__ = 'wangjz'


def calculate_F(recommend, reality):
    """
    计算调和均值F

    【recommend】 userid,newsid 一对多
    [(35,100647112),
    (35,100647132),
    (107,100647132),
    ……]

    【reality】 userid,newsid 一对一
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
        if item in reality: #疑问，这样的查询效率怎样？
            sum_hitu += 1

    precision = 1.0 * sum_hitu / sum_Lu
    recall = 1.0 * sum_hitu / sum_Tu
    F = 2.0 / (1.0 / precision + 1.0 / recall)

    return (precision, recall,F)




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