#coding:utf-8
"""
@file:      run_game
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2017-01-12 15:44
@description:
            游戏主线程
"""
from game import Game
from role import *


macau = Casino(table_cot=2)

game = Game(casino=macau, big_blind=2, small_blind_seat_index=0)

game.add_AI(size=3)

game.begin()
