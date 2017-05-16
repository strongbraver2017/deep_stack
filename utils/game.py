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

from role import Pot, RingList, Player
from patterns import GameCards
from compare import CompareModel
from itertools import combinations
from judge import JudgeModel
import time


class Game:
    """
    brief:
            德州扑克游戏核心逻辑
    params:
        table = None                    #table->seat->player
        cards_machine = GameCards()     #发牌机
        full_cards = []                 #完整的两副牌
        used_cards_buffer = []          #保存已发出的牌，缓冲区
        public_pot_cards = []           #公共牌缓冲区
        players_queue = RingList(size=0)#游戏逻辑的玩家队列
        small_blind_seat_index = None   #游戏队列头（小盲）的seat坐标
        dealer = CompareModel()         #荷官，比较牌力
        stage_max_bet = 0               #某个阶段的最大下注
    """
    def __init__(self, casino,big_blind, small_blind_seat_index):
        self.table = casino.get_free_table()
        self.table.big_blind = big_blind
        self.cards_machine = GameCards()
        self.full_cards = self.cards_machine.to_arr()
        self.small_blind_seat_index = small_blind_seat_index

        self.used_cards_buffer = []
        self.public_pot_cards = []
        self.players_queue = RingList(size=0)
        self.dealer = CompareModel()
        self.stage_max_bet = 0
        self.status = None

    def shuffle_cards(self):
        self.used_cards_buffer = []
        self.public_pot_cards = []
        self.players_queue = RingList(size=0)
        self.table.pots = [Pot(),]

    def card_is_in_buffer(self,card):
        for used_card in self.used_cards_buffer:
            if used_card.suit == card.suit and \
               used_card.value == card.value:
                    return True
        return False

    def get_x_free_cards(self,count):
        cards = self.cards_machine.get_random_x(
            x = count,
            ext_cards = self.full_cards,
            except_cards = self.used_cards_buffer
        )
        self.used_cards_buffer.extend(cards)
        return cards

    def add_player(self,player,chose_buyin,chose_seat_index=None):
        if chose_seat_index:
            seat = self.table.get_specific_seat(chose_seat_index)
        else:
            # 未指定index则随机分配空闲座位
            seat = self.table.get_free_seat()
            if seat==None:
                raise EnvironmentError('No seat could be allocated.')
        seat.sit(player)
        self.add_ones_chips(player, chose_buyin)

    def add_AI(self,size):
        import random
        for i in range(size):
            try:
                self.add_player(
                    player=Player(),
                    chose_buyin= random.choice(
                        range(self.table.min_buyin,self.table.max_buyin)
                    )
                )
            except EnvironmentError:
                break
        return

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

    @staticmethod
    def return_ones_chips(player, quantity):
        player.account_chips += quantity
        player.stack -= quantity

    def send_cards(self, count, to_players=False, to_public_area=False):
        if to_players:
            for seat in self.table.seats:
                if seat.player is None:
                    continue
                seat.player.hands.extend(self.get_x_free_cards(count))
        if to_public_area:
            self.public_pot_cards.extend(self.get_x_free_cards(count))

    def bet(self,player,quantity):
        player.stack -= quantity
        player.last_bet_quantity += quantity
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

    @staticmethod
    def bet_is_allin(player, quantity):
        return quantity >= player.stack

    def fold(self, player, cuba=None):
        self.players_queue.remove(player)

    def call(self, player, cuba=None):
        self.bet(player,self.stage_max_bet)

    def raise_(self,player,raise_to):
        self.call(player)
        delta = raise_to-self.stage_max_bet
        self.bet(player,delta)

    def check(self, player, cuba=None):
        pass

    @property
    def big_blind(self):
        return self.table.big_blind

    def operate(self):
        operation_map = {
            'b': self.bet,
            'ca': self.call,
            'ch': self.check,
            'f': self.fold,
            'r': self.raise_,
        }

        """ 开牌由UTG说话 """
        first_node = self.players_queue.get_node_by(index=2)
        node = first_node
        while True:
            """ 轮询列表里的所有玩家，表态 """
            player = node.object
            print(player)
            try:
                his_max_cards = self.get_ones_max_pattern(player)
                cards_model = JudgeModel().get_type(his_max_cards)
                print(cards_model)
            except LookupError:
                pass
            """ 检测是否是待call状态 """
            if self.stage_max_bet>0:
                delta = self.stage_max_bet - player.last_bet_quantity
                print('you have to agree someones bet: {} or fold.'.format(delta))
            operation_index, quantity = player.cmd_operate()
            operation_map[operation_index](player,quantity)
            if operation_index == 'r':
                # 如果有人raise表示不服，则重新开启进程环，直到他上家表态完成
                first_node = node
            node = node.next
            if node==first_node:
                print('AgreeMent Achieved!')
                break

    def basic_process(self, stage_name, status_name,count,
                      cards_to_players=False, cards_to_area=False):
        print('\n___________  {}  _____________'.format(stage_name))
        self.table.clear_just_now_buffer()
        self.status = status_name
        self.send_cards(
            count=count,
            to_players=cards_to_players,
            to_public_area=cards_to_area
        )
        print('public_cards: {}'.format(self.public_pot_cards))
        self.operate()
        self.stage_max_bet = 0
        for player in self.players_queue.to_list():
            player.last_bet_quantity = 0
        if self.players_queue.length<=1:
            # 其余玩家都fo牌，直接清算结束游戏
            self.end()
            return 'game over'

    def preflop(self):
        self.basic_process(
            stage_name='Pre Flop',
            status_name='preflop',
            count=2,
            cards_to_players=True
        )

    def flop(self):
        self.basic_process(
            stage_name='Flop',
            status_name='flop',
            count=3,
            cards_to_area=True
        )

    def turn(self):
        self.basic_process(
            stage_name='Turn',
            status_name='turn',
            count=1,
            cards_to_area=True
        )

    def river(self):
        self.basic_process(
            stage_name='River',
            status_name='river',
            count=1,
            cards_to_area=True
        )

    def get_ones_max_pattern(self,player):
        """ 得到某玩家5-7张牌中的最大牌型 """
        temp_cards = []
        temp_cards.extend(self.public_pot_cards)
        temp_cards.extend(player.hands)
        print('temp_cards: ',temp_cards)

        if len(temp_cards)<5:
            raise LookupError('Cards < 5')
        all_cards = list(combinations(
            iterable=temp_cards,
            r=5
        ))
        max_cards = all_cards[0]
        for cards in all_cards:
            # 5-7张中选五张组合（python内建的迭代工具）
            self.dealer.get(
                five_cards_A=cards,
                five_cards_B=max_cards
            )
            if self.dealer.A_stronger_than_B:
                max_cards = cards
        return max_cards

    def end(self):
        """ 清算所有底池 """
        for pot in self.table.pots:
            pot.liquidate()
        self.table.cancel()
        self.status = 'free'

    def begin(self):
        self.table.occupy()
        self.status = 'preflop'
        self.shuffle_cards()

        """  按照指定的小盲位顺时针取出玩家，并扣除大小盲入池   """
        seat_indexs = list(range(
            self.small_blind_seat_index,
            self.table.seat_size
        ))
        seat_indexs.extend(list(range(
            self.small_blind_seat_index
        )))
        small_blind = self.table.get_specific_seat(
            seat_index=self.small_blind_seat_index
        ).player
        big_blind = self.table.get_specific_seat(
            seat_index=seat_indexs[1]
        ).player
        self.bet(player=small_blind,quantity=0.5*self.big_blind)
        self.bet(player=big_blind, quantity=1*self.big_blind)
        """  将玩家全部置入游戏队列   """
        for seat_index in seat_indexs:
            seat = self.table.get_specific_seat(seat_index)
            if seat.player is None:
                continue
            seat.player.game_init_stack = seat.player.stack
            self.players_queue.append(seat.player)

        print(self.table)

        while self.players_queue.length<2:
            print('waiting for players join...')
            print(self.table)
            time.sleep(1)

        for stage in [self.preflop, self.flop, self.turn, self.river]:
            if stage() == 'game over':
                return
