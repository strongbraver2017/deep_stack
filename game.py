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
    pot_players = []                #底池中的玩家，缓冲区
    public_pot_cards = []           #公共牌缓冲区
    game_queue = None               #游戏逻辑的队列
    small_blind_seat_index = None   #游戏队列头（小盲）的seat坐标
    dealer = CompareModel()

    def __init__(self,casino,big_blind,small_blind_seat_index):
        self.table = casino.get_free_table()
        self.table.big_blind = big_blind
        self.full_cards = self.cards_machine.to_arr()
        self.game_queue = []

    def shuffle_cards(self):
        self.used_cards_buffer = []
        self.public_pot_cards = []
        self.game_queue = []
        self.table.pot_size = 0

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
        self.table.pot_size += quantity

    def fold(self,player):
        self.pot_players.remove(player)

    def call(self,player,last_quantity,raise_to):
        self.bet(player,raise_to-last_quantity)

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
            self.game_queue.append(seat)

    def open(self):
        self.status = 'open'
        self.send_cards(count=2,to_players=True)

    def flop(self):
        self.status = 'flop'
        self.send_cards(count=3, to_public_area=True)

    def turn(self):
        self.status = 'turn'
        self.send_cards(count=1, to_public_area=True)

    def river(self):
        self.status = 'river'
        self.send_cards(count=1,to_public_area=True)

    def liquidate(self,winners):
        """ 瓜分底池 """
        self.table.pot_size
        pass

    def get_ones_max_pattern(self,player):
        """ 得到某玩家5-7张牌中的最大牌型 """
        self.public_pot_cards
        pass

    def end(self):
        """ 以下可得到所有的赢家列表，后交于荷官清算 """
        winners = [self.game_queue[0],]
        for seat in self.game_queue[1:]:
            self.dealer.get(
                five_cards_A=seat.player.hands,
                five_cards_B=winners[0].hands
            )
            if self.dealer.A_stronger_than_B in ['draw',True]:
                winners.append(seat.player)
            if self.dealer.A_stronger_than_B == True:
                winners.remove(winners[0])
                vvvvvv
        self.liquidate(winners)

        self.table.cancel()
        self.status = 'free'
