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
    """ 座位 """
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
    '''
        牌桌
    '''
    id = 0
    big_blind = 100
    seats = []
    pots = []
    status = 'free'
    seat_size = 12
    sb_allin_just_now = False
    previous_allin_value = 0

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
    id = 0
    name = 'argo'
    stack = 0
    game_init_stack = 0
    level = None
    status = 'free'
    account_chips = 1000000
    hands = []
    join_pots = []
    last_bet_quantity = 0

    def __init__(self,id=None,name=None,level=100):
        import random
        if id==None:
            self.id = random.choice(range(1000))
        if name==None:
            self.name = 'Robot-{}'.format(self.id)
        else:
            self.name = name
        self.id = id
        self.level = level

    def cmd_operate(self):
        operation_index = input('operation_index: ?')
        quantity = input('quantity: ?')
        return (operation_index,quantity)

    def cmd_if_call(self,quantity):
        call = input('if call {}?'.format(quantity))
        return call



class Pot:
    """  底池   """
    players = []
    size = 0
    total_size = 0
    unit_size = 0

    def liquidate(self):
        winners = [self.players[0], ]
        for seat in self.players[1:]:
            self.dealer.get(
                five_cards_A=seat.player.hands,
                five_cards_B=winners[0].hands
            )
            if self.dealer.A_stronger_than_B == 'draw':
                winners.append(seat.player)
            if self.dealer.A_stronger_than_B == True:
                winners = [seat.player,]

        for winner in winners:
            if winner not in self.players:
                raise AssertionError('Not pot player: {}'.format(winner))
        for winner in winners:
            winner.stack += self.size / len(winners)


class RingNode:
    """ 环形列表单位节点 """
    index = 0
    object = None
    parent_ring = None

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
                parent_ring=self,obj=node_object)
        )

    @property
    def length(self):
        return len(self.nodes)

    def assign(self,index,obj):
        self.nodes[index].object = obj

    def remove(self,obj):
        self.nodes.remove(
            self.get_node_by(obj=obj)
        )

    def get_node_by(self,index=None,obj=None):
        if index:
            return self.nodes[index]
        if obj:
            for node in self.nodes:
                if node.object == obj:
                    return node

    def to_list(self):
        return [ node.object for node in self.nodes ]




