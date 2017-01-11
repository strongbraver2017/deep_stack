#coding:utf-8
"""
@file:      role.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm Mac
@create:    2017/1/11 01:32
@description:
        德州扑克游戏里的各种角色
"""

class Seat:
    '''
        座位
    '''
    index = None
    player = None
    status = 'free'
    table_index = 0
    queue_postion_index = 0

    def __init__(self,index,player=None):
        if player:
            self.player = player
        self.index = index

    def sit(self,player):
        if self.status == 'busy':
            raise IOError('Sorry, the seat has been occupied.')
        self.player = player
        self.player.status = 'Game in table {}, seat {}'.format(
            self.table_index, self.index
        )
        self.status = 'busy'

    def go(self):
        self.status = 'free'
        self.player.status = 'free'
        self.player = None

    def __repr__(self):
        return (
            'Seat [{}]( {} ): ${} \n'
        ).format(
            self.table_index, self.player.name,
            self.player.stack
        )


class Table:
    '''
        牌桌
    '''
    id = 0
    big_blind = 100
    seats = []
    pot_size = 0
    status = 'free'
    seat_size = 12

    def __init__(self,big_blind=100,id=0):
        self.big_blind = big_blind
        self.id = id
        for i in range(self.seat_size):
            seat = Seat(index=i)
            seat.table_index = self.id
            self.seats.append(seat)

    @property
    def max_buyin(self):
        return 200 * self.big_blind

    @property
    def min_buyin(self):
        return 20 * self.big_blind

    def occupy(self):
        self.pot_size = 0
        self.status = 'busy'

    def cancel(self):
        self.status = 'free'
        self.pot_size = 0

    def get_specific_seat(self,seat_index):
        for seat in self.seats:
            if seat.index == seat_index:
                return seat
        return None

    def __repr__(self):
        seat_str = ''
        for seat in self.seats:
            seat_str += seat.__repr__()
        return (
            '______________ Table {} _________________\n'
            '{}'
            '_________________________________________'
        ).format(self.id, seat_str)


class Casino:
    '''
        赌场/平台
    '''
    name = 'Macau'
    tables = []
    table_cot = 100

    def __init__(self,table_cot=100):
        self.table_cot = table_cot
        for i in range(table_cot):
            self.tables.append(Table(id=i))

    def get_free_table(self):
        for table in self.tables:
            if table.status == 'free':
                return table


class Player:
    '''
        玩家
    '''
    import random

    id = random.choice(range(1000))
    name = None
    stack = 0
    level = None
    place = 'BTN'
    status = 'free'
    account_chips = None
    hands = []

    def __init__(self,id=0,name=None,level=100):
        if name==None:
            self.name = 'Robot-{}'.format(self.id)
        else:
            self.name = name
        self.id = id
        self.level = level


class Operation:
    '''
        操作
    '''
    name = "Bet"
    add_size = 0






