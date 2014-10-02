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

