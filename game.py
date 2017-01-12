#coding:utf-8
"""
@file:      game.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm Mac
@create:    2017/1/11 20:00
@description:
        保存德州扑克游戏逻辑
"""
from role import Pot


class Game:
    '''
        德州牌局
    '''
    from patterns import GameCards
    from compare import CompareModel

    table = None                    #table->seat->player
    status = None                   #游戏进度
    cards_machine = GameCards()     #发牌机
    full_cards = []                 #完整的两副牌
    used_cards_buffer = []          #保存已发出的牌，缓冲区
    public_pot_cards = []           #公共牌缓冲区
    game_queue = []                 #游戏逻辑的队列
    small_blind_seat_index = None   #游戏队列头（小盲）的seat坐标
    dealer = CompareModel()         #荷官

    def __init__(self,casino,big_blind,small_blind_seat_index):
        self.table = casino.get_free_table()
        self.table.big_blind = big_blind
        self.full_cards = self.cards_machine.to_arr()

    def shuffle_cards(self):
        self.used_cards_buffer = []
        self.public_pot_cards = []
        self.game_queue = []
        self.table.pots = [Pot(),]

    def card_is_in_buffer(self,card):
        for used_card in self.used_cards_buffer:
            if used_card.suit == card.suit and \
                used_card.value == card.value:
                    return True
        return False

    def get_x_free_cards(self,count):
        cards = []
        for i in range(count):
            card = self.cards_machine.get_random_x(
                x=1,ext_cards=self.full_cards)
            while(1):
                if not self.card_is_in_buffer(card):
                    cards.append(card)
                    self.used_cards_buffer.append(card)
                    break
        return cards

    def add_player(self,player,chose_seat_index,chose_buyin):
        seat = self.table.get_specific_seat(chose_seat_index)
        seat.sit(player)
        self.add_ones_chips(player, chose_buyin)

    def rm_seat(self,seat_index):
        seat = self.table.get_specific_seat(seat_index)
        self.return_ones_chips(
            player = seat.player,
            quantity = seat.player.stack
        )
        seat.go()

    def add_ones_chips(self,player,quantity):
        player.account_chips -= quantity
        player.stack += quantity
        if player.stack > self.table.max_buyin:
            delta = player.stack - self.table.max_buyin
            self.return_ones_chips(player,delta)

    def return_ones_chips(self,player,quantity):
        player.account_chips += quantity
        player.stack -= quantity

    def send_cards(self,count,
            to_players=False,to_public_area=False):
        if to_players:
            for seat in self.table.seats:
                if seat.player == None:
                    continue
                seat.player.hands = self.get_x_free_cards(count)
        if to_public_area:
            self.public_pot_cards = self.get_x_free_cards(count)

    def bet(self,player,quantity):
        player.stack -= quantity
        self.last_quantity = quantity
        if self.table.sb_allin_just_now and\
                self.table.previous_allin_value < quantity:
            """ 新建底池,并添加该玩家入池 """
            new_pot = Pot()
            new_pot.players.append(player)
            self.table.pots.append(new_pot)
            player.join_pots.append(new_pot)
            """ 计算玩家两个底池的下注量 """
            call_val = self.table.previous_allin_value
            raise_delta = quantity - call_val
            """ 对最新的两个底池下注 """
            self.table.pots[-2].size += call_val
            self.table.pots[-1].size += raise_delta
            return 'raise'
        if self.bet_is_allin(player,quantity):
            player.status = 'allin'
            self.table.sb_allin_just_now = True
            self.table.previous_allin_value = quantity
        self.table.pots[-1].size += quantity
        old_pot = self.table.pots[-1]
        if player not in old_pot.players:
            old_pot.players.append(player)
            player.join_pots.append(old_pot)
        return 'bet or call'

    def bet_is_allin(self,player,quantity):
        return quantity >= player.stack

    def fold(self,player):
        self.game_queue.remove(player)

    def call(self,player,quantity):
        self.bet(player,quantity)

    def raise_(self,player,raise_to):
        self.bet(player,raise_to)
        delta = raise_to-self.last_quantity
        call = player.cmd_if_call(delta)
        if call:
            self.call(player,delta)

    def before_open(self):
        self.table.occupy()
        self.status = 'before open'
        self.shuffle_cards()

        """  按照指定的小盲位顺时针取出玩家，并扣除大小盲入池   """
        seat_indexs = list(range(
            self.small_blind_seat_index,self.table.seat_size))
        seat_indexs.extend(list(range(
            self.small_blind_seat_index)))
        small_blind = self.table.get_specific_seat(
            self.small_blind_seat_index).player
        big_blind = self.table.get_specific_seat(
            seat_indexs[1]).player
        self.bet(player=small_blind,quantity=0.5*big_blind)
        self.bet(player=big_blind, quantity=1*big_blind)

        """  将玩家全部置入游戏队列   """
        for seat_index in seat_indexs:
            seat = self.table.get_specific_seat(seat_index)
            if seat.player == None:
                continue
            seat.player.game_init_stack = seat.player.stack
            self.game_queue.append(seat)

    def bet_process(self):
        operation_map = {
            'b': self.bet,
            'c': self.call,
            'f': self.fold,
            'r': self.raise_,
        }
        for player in self.game_queue:
            operation_index, quantity = player.operate()
            operate = operation_map[operation_index]
            operate(*[player,quantity])

    def basic_process(self,status_name,count,
            cards_to_players=False,cards_to_area=False):
        self.table.clear_just_now_buffer()
        self.status = status_name
        self.send_cards(
            count = count,
            to_players = cards_to_players,
            to_public_area = cards_to_area
        )
        self.bet_process()

    def open(self):
        self.basic_process(
            status_name = 'open',
            count = 2,
            cards_to_players = True
        )

    def flop(self):
        self.basic_process(
            status_name = 'flop',
            count = 3,
            cards_to_area = True
        )

    def turn(self):
        self.basic_process(
            status_name = 'turn',
            count = 1,
            cards_to_players = True
        )

    def river(self):
        self.basic_process(
            status_name = 'river',
            count = 1,
            cards_to_players = True
        )

    def get_ones_max_pattern(self,player):
        """ 得到某玩家5-7张牌中的最大牌型 """
        self.public_pot_cards
        pass

    def end(self):
        """ 清算所有底池 """
        for pot in self.table.pots:
            pot.liquidate()
        self.table.cancel()
        self.status = 'free'

    def begin(self):
        self.before_open()
        self.end()
