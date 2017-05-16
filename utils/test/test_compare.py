# coding:utf-8
"""
@file:      test_compare
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm Mac
@create:    2017/1/10 23:27
@description:
        测试二元牌型的牌力比较
"""

import time

from compare import CompareModel
from patterns import GameCards

cards_machine = GameCards()
all_cards = GameCards().to_arr()

while (1):
    cardsA = cards_machine.get_random_x(
        x=5, ext_cards=all_cards)
    cardsB = cards_machine.get_random_x(
        x=5, ext_cards=all_cards)

    cp = CompareModel()

    cp.get(cardsA, cardsB)

    st = cp.A_stronger_than_B

    if st == 'draw':
        res = '='
    else:
        if st:
            res = '>'
        else:
            res = '<'

    print('{} {} {}'.format(
        cardsA, res, cardsB))

    time.sleep(0.1)

    print('----------')
