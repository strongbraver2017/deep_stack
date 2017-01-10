#coding:utf-8
"""
@file:      judge.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm Mac
@create:    2017/1/10 16:54
@description:
        对于牌型的判定
"""

from patterns import *


class JudgeModel:
    def __init__(self,cards):
        self.cards = cards

    def judge(self,five_cards):
        for pattern in [
            RoyalFlush, StraightFlush, FourOfOneKind,
            FullHouse, Flush, Straight,
            Set, TwoPairs, OnePair, HighCard
        ]:
            test_model = pattern(five_cards)
            if test_model.judge_result:
                print('{}:\t{}'.format(
                    test_model.name,five_cards))
                return test_model.name

