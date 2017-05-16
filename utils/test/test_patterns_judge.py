#coding:utf-8
"""
@file:      test_patterns_judge
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm Mac
@create:    2017/1/10 16:27
@description:
            本模块用于测试牌型的判断是否准确
"""
import random,time
from patterns import *

cards = GameCards().to_arr()

'''
for card in cards:
    print(card)
'''
cot = 0
rf = 0
sf = 0
ff = 0
while(1):
    cot += 1
    time.sleep(0.01)
    random_five_cards = []

    for i in range(5):
        while(1):
            card = random.choice(cards)
            if card not in random_five_cards:
                random_five_cards.append(card)
                #print(card)
                break
            #print('{} is in queue...'.format(card))


    #print(random_five_cards)

    for pattern in [
        RoyalFlush, StraightFlush, FourOfOneKind,
        FullHouse, Flush, Straight,
        Set, TwoPairs, OnePair, HighCard
    ]:
        test_model = pattern(random_five_cards)
        if test_model.judge_result:
            if pattern==FourOfOneKind:
                ff += 1
                print('[{}]\t {}:\t{}\t{}'.format(
                    cot, test_model.name,
                    random_five_cards,ff
                ))
            elif pattern==StraightFlush:
                sf += 1
                print('[{}]\t {}:\t{}\t{}'.format(
                    cot, test_model.name,
                    random_five_cards, sf
                ))
            elif pattern==RoyalFlush:
                rf += 1
                print('-----------------------------------------------------')
                print('[{}]\t {}:\t{}\t{}'.format(
                    cot, test_model.name,
                    random_five_cards, rf
                ))
            else:
                print('[{}]\t {}:\t{}\t'.format(
                    cot, test_model.name,
                    random_five_cards
                ))
                break
    #print('------')
