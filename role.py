#coding:utf-8
"""
@file:      role.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm Mac
@create:    2017/1/11 01:32
@description:
        牌桌上的各种角色
"""

class Seat:
    name = None
    index = None
    player = None
    status = 'free'


class Table:
    id = 0
    is_open = True
    big_blind = None
    seats = []
    pot_size = None
    status = None


class Player:
    id = 0
    name = None
    stack = None
    level = None
    place = 'BTN'


class Operation:
    name = "Bet"
    add_size = 0


class Game:
    table = None    #table->seat->player
    status = None
    cards_machine = None
