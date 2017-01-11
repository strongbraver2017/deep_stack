#coding:utf-8
"""
@file:      game
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

    table = None                    #table->seat->player
    status = None                   #游戏进度
    cards_machine = GameCards()     #发牌机
    full_cards = []                 #完整的两副牌
    used_cards_buffer = []          #保存已发出的牌，缓冲区
    pot_players = []                #底池中的玩家，缓冲区
    public_pot_cards = []           #公共牌缓冲区

    def __init__(self,casino,big_blind):
        self.table = casino.get_free_table()
        self.table.big_blind = big_blind
        self.full_cards = self.cards_machine.to_arr()

    def shuffle_cards(self):
        self.used_cards_buffer = []

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

    def send_cards(self,count):
        for seat in self.table.seats:
            if seat.player == None:
                continue
            seat.player.hands = self.get_x_free_cards(2)

    def open(self):
        self.table.occupy()
        self.status = 'open'
        self.send_cards(2)


    def flop(self):
        self.status = 'flop'


    def turn(self):
        self.status = 'turn'

    def river(self):
        self.status = 'river'

    def end(self):

        self.table.cancel()
        self.status = 'free'