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
import random


class Seat:
    """ 座位 """

    def __init__(self,index,player=None):
        self.player = player
        self.index = index
        self.status = 'free'
        self.table_index = 0
        self.queue_postion_index = 0

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
        if self.player:
            return (
                'Seat [{}]( {} ): ${} \n'
            ).format(
                self.index, self.player.name,
                self.player.stack
            )
        else:
            return (
                'Seat [{}]: None \n'
            ).format(
                self.index
            )


class Table:
    """
        牌桌
    """
    def __init__(self,big_blind=2,id=0,seat_size=9):
        self.big_blind = big_blind
        self.seat_size = seat_size
        self.id = id

        self.seats = []
        self.pots = []
        self.status = 'free'
        self.sb_allin_just_now = False
        self.previous_allin_value = 0

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
        self.pots.append(Pot())
        self.status = 'busy'

    def cancel(self):
        self.status = 'free'
        self.pots = []

    def clear_just_now_buffer(self):
        self.sb_allin_just_now = False
        self.previous_allin_value = 0

    def get_specific_seat(self,seat_index):
        for seat in self.seats:
            if seat.index == seat_index:
                return seat
        return None

    def get_free_seat(self):
        for seat in self.seats:
            if seat.status == 'free':
                return seat
        return None

    def __repr__(self):
        seat_str = ''
        for seat in self.seats:
            seat_str += seat.__repr__()
        return (
            '______________ Table {} _________________\n{}'
        ).format(self.id, seat_str)


class Casino:
    """
        赌场/平台
    """

    def __init__(self,table_cot=100,table_seat_size=9,name=None):
        self.name = name
        self.tables = []
        self.table_cot = table_cot
        for i in range(table_cot):
            self.tables.append(
                Table(id=i,seat_size=table_seat_size)
            )

    def get_free_table(self):
        for table in self.tables:
            if table.status == 'free':
                return table


class Player:
    """
        玩家
    """

    def __init__(self,id=None,name=None,level=100):
        self.id = id
        self.name = name
        self.level = level
        self.stack = 0
        self.game_init_stack = 0
        self.status = 'free'
        self.account_chips = 1000000
        self.hands = []
        self.join_pots = []
        self.last_bet_quantity = 0
        if id is None:
            self.id = random.choice(range(1000))
        if name is None:
            self.name = 'Robot-{}'.format(self.id)

    def cmd_operate(self):
        while True:
            operation_index = input('operation_index: ')
            if operation_index in ['ca','ch','f']:
                quantity = None
                break
            elif operation_index in ['b','r']:
                quantity = int(input('quantity: '))
                break
            else:
                print('No such index.Again:')
        return operation_index, quantity

    def cmd_if_call(self,quantity):
        call = input('if call {}?(y or n)\n'.format(quantity))
        return call

    def __repr__(self):
        return (
            '\n________  Player {}:  {}   ___________\n'
            'stack: ${}\n'
            'join_pots: {}\n'
            'last_bet_quantity: ${}\n'
        ).format(self.name, self.hands, self.stack,
                 self.join_pots, self.last_bet_quantity)


class Pot:
    """  底池   """
    def __init__(self):
        self.players = []
        self.size = 0
        self.index = random.choice(['a', 'b', 'c', 'd', 'e'])

    def liquidate(self):
        winners = [self.players[0], ]
        for seat in self.players[1:]:
            self.dealer.get(
                five_cards_A=seat.player.hands,
                five_cards_B=winners[0].hands
            )
            if self.dealer.A_stronger_than_B == 'draw':
                winners.append(seat.player)
            if self.dealer.A_stronger_than_B is True:
                winners = [seat.player, ]

        for winner in winners:
            if winner not in self.players:
                raise AssertionError('Not pot player: {}'.format(winner))
        for winner in winners:
            winner.stack += self.size / len(winners)

    def __repr__(self):
        return '<Pot {}: ${} >'.format(self.index,self.size)


class RingNode:
    """ 环形列表单位节点 """

    def __init__(self, index, parent_ring=None,obj=None):
        self.index = index
        self.object = obj
        self.parent_ring = parent_ring

    @property
    def next(self):
        if self.index == self.parent_ring.length-1:
            return self.parent_ring.nodes[0]
        else:
            return self.parent_ring.nodes[self.index+1]

    @property
    def prev(self):
        if self.index == 0:
            return self.parent_ring.nodes[self.parent_ring.length-1]
        else:
            return self.parent_ring.nodes[self.index-1]


class RingList:
    """ 环形列表 """

    nodes = []

    def __init__(self,size):
        for i in range(size):
            self.append(node_object=None)

    def append(self,node_object=None):
        self.nodes.append(
            RingNode(index=self.length,
                     parent_ring=self,
                     obj=node_object)
        )

    @property
    def length(self):
        return len(self.nodes)

    def assign(self, index,obj):
        self.nodes[index].object = obj

    def remove(self, obj):
        self.nodes.remove(
            self.get_node_by(obj=obj)
        )

    def get_node_by(self,index=None,obj=None):
        if index is not None:
            return self.nodes[index]
        if obj is not None:
            for node in self.nodes:
                if node.object == obj:
                    return node
        return None

    def to_list(self):
        return [node.object for node in self.nodes]




