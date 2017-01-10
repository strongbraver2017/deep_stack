#coding:utf-8
"""
@file:      patterns.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm Mac
@create:    2017/1/10 13:05
@description:
            各大单元牌型和组合牌型
"""



class CardPattern:
    '''
        单元牌型
    '''
    def __init__(self,val,suit):
        self.value = val   #牌面数值
        self.suit = suit   #花色

    def __repr__(self):
        return (
            "<UnitCard(value={},suit={})>"
        ).format(self.value,self.suit)


class GameCards:
    '''
        生成德州扑克游戏所用到的52张牌
    '''
    ValueMap = list(range(2, 15))
    # 数值域

    SuitMap = ['heart', 'heart', 'clover', 'diamond']
    # 花色域

    def to_arr(self):
        cards = []
        for val in self.ValueMap:
            for suit in self.SuitMap:
                card = CardPattern(val,suit)
                cards.append(card)
        return cards



GroupMap = {
    'High Card': 1,
    'Two Pairs': 2,
    'Set': 3,
    'Straight': 4,
    'Flush': 5,
    'Full House': 6,
    'Four Of One Kind': 7,
    'Straight Flush': 8,
    'Royal Flush': 9
}


class GroupPattern:
    '''
        组合牌型
    '''
    suit_list = []
    value_list = []
    suit_set = set()    #花色值域
    value_set = set()   #牌面大小值域
    value_map = {}


    def __init__(self,name,five_cards):
        self.name = name     #牌型名称
        self.value = GroupMap[name]     #组合大小权值（用于排序牌力）
        self.five_cards = five_cards
        self.suit_list = [card.suit for card in self.five_cards]
        self.suit_set = set(self.suit_list)
        self.value_list = [card.value for card in self.five_cards]
        self.value_set = set(self.value_list)
        for uni_val in self.value_set:
            self.value_map[uni_val] = self.value_list.count(uni_val)

    def _judge(self):
        if len(self.five_cards) != 5:
            raise ValueError('Just judge pattern of 5 cards group')

    def judge(self):
        pass



'''
    以下为具体牌型
'''


class FullHouse(GroupPattern):
    '''
        葫芦，满堂红
    '''

    name = 'Full House'

    def __init__(self,five_cards):
        GroupPattern.__init__(self,
            name = self.name,
            five_cards = five_cards
        )
        self.judge_result = self.judge()

    def judge(self):
        self._judge()
        return len(self.value_set)==2 and \
               max(*self.value_map.values())==3
              #四条时最大相同键数应为4

    @property
    def the_three_Value(self):
        if self.judge_result:
            return max(*self.value_set)
        else:
            raise TypeError(
                'Just {} judged, the function could be executed.' \
                    .format(self.name)
            )

    @property
    def the_two_Value(self):
        if self.judge_result:
            return min(*self.value_set)
        else:
            raise TypeError(
                'Just {} judged, the function could be executed.' \
                    .format(self.name)
            )


class Flush(GroupPattern):
    '''
        同花
    '''
    name = 'Flush'

    def __init__(self,five_cards):
        GroupPattern.__init__(self,
            name = self.name,
            five_cards = five_cards
        )
        self.judge_result = self.judge()

    def judge(self):
        self._judge()
        return len(self.suit_set)==1

    @property
    def max_val(self):
        if not self.judge_result:
            raise TypeError(
                'Just {} judged, the function could be executed.'\
                    .format(self.name)
            )
        return max(*self.value_set)