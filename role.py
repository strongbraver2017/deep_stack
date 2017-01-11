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


class Table:
    '''
        牌桌
    '''
    id = 0
    big_blind = 100
    seats = []
    pot_size = None
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
        self.status = 'busy'

    def cancel(self):
        self.status = 'free'

    def get_specific_seat(self,seat_index):
        for seat in self.seats:
            if seat.index == seat_index:
                return seat
        return None

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
    stack = None
    level = None
    place = 'BTN'
    status = 'free'
    chose_seat_index = 0
    chose_buyin = 100

    def __init__(self,chose_seat_index,chose_buyin,
                    id=0,name=None,level=100,
                 ):
        self.name = 'Robot-{}'.format(self.id)
        self.chose_buyin = chose_buyin
        self.chose_seat_index = chose_seat_index


class Operation:
    '''
        操作
    '''
    name = "Bet"
    add_size = 0


class Game:
    '''
        德州牌局
    '''
    table = None    #table->seat->player
    status = None
    cards_machine = None

    def __init__(self,casino,big_blind):
        self.table = casino.get_free_table()
        self.table.big_blind = big_blind

    def add_player(self,player,chose_seat_index):
        seat = self.table.get_specific_seat(chose_seat_index)
        seat.sit(player)

    def rm_seat(self,seat_index):
        seat = self.table.get_specific_seat(seat_index)
        seat.go()

    def begin(self):
        self.table.occupy()

    def end(self):
        self.table.cancel()