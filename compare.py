#coding:utf-8
"""
@file:      compare
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm Mac
@create:    2017/1/10 22:22
@description:
        二元牌型比较牌力
"""

from judge import JudgeModel
from patterns import GroupMap

class CompareModel:
    def __init__(self,five_cards_A,five_cards_B):
        if len(five_cards_A)!=5 or\
                len(five_cards_B)!=5:
            raise ValueError('Just support five cards compared.')
        engine = JudgeModel()
        self.A = engine.get_type(five_cards_A)
        self.B = engine.get_type(five_cards_B)

    def A_stronger_than_B(self):
        if None not in [self.A, self.B]:
            if self.A.name != self.B.name:
                return GroupMap[self.A.name] > GroupMap[self.B.name]
            else:
                public_type = self.A.name
                if public_type in [
                    'High Card',
                    'Straight',
                    'Flush',
                    'Straight Flush',
                    'Royal Flush'
                ]:
                    if self.A.max_val==self.B.max_val:
                        return 'draw'
                    else:
                        return self.A.max_val > self.B.max_val

                if public_type=='One Pair':
                    if self.A.the_pair_Value != self.B.the_pair_Value:
                        return self.A.the_pair_Value > self.B.the_pair_Value
                    for i in range(len(self.A.the_single_Values)):
                        if self.A.the_single_Values[i] != self.B.the_single_Values[i]:
                             return self.A.the_single_Values[i] > self.B.the_single_Values[i]
                    return 'draw'

                if public_type=='Two Pairs':
                    if self.A.the_big_pair_Value != self.B.the_big_pair_Value:
                        return self.A.the_big_pair_Value > self.B.the_big_pair_Value
                    if self.A.the_small_pair_Value != self.B.the_small_pair_Value:
                        return self.A.the_small_pair_Value > self.B.the_small_pair_Value
                    if self.A.the_small_pair_Value != self.B.the_small_pair_Value:
                        return self.A.the_single_Value > self.B.the_single_Value
                    else:
                        return 'draw'

                if public_type=='Full House':
                    if self.A.the_three_Value != self.B.the_three_Value:
                        return self.A.the_three_Value > self.B.the_three_Value
                    if self.A.the_two_Value != self.B.the_two_Value:
                        return self.A.the_two_Value > self.B.the_two_Value
                    else:
                        return 'draw'

                if public_type=='Four Of One Kind':
                    if self.A.the_four_Value != self.B.the_four_Value:
                        return self.A.the_four_Value > self.B.the_four_Value
                    if self.A.the_one_Value != self.B.the_one_Value:
                        return self.A.the_one_Value > self.B.the_one_Value
                    else:
                        return 'draw'

                if public_type=='Set':
                    if self.A.the_three_Value != self.B.the_three_Value:
                        return self.A.the_three_Value > self.B.the_three_Value
                    for i in range(len(self.A.the_single_Values)):
                        if self.A.the_single_Values[i] != self.B.the_single_Values[i]:
                             return self.A.the_single_Values[i] > self.B.the_single_Values[i]
                    return 'draw'
        else:
            raise TypeError('At least One of A or B cant be judged which group belongs to.')