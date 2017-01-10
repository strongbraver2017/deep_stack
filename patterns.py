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
    NameMap = {
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A'
    }

    def __init__(self,val,suit):
        self.value = val   #牌面数值
        self.suit = suit   #花色

    def __repr__(self):
        value = self.value
        if self.value in self.NameMap.keys():
            value = self.NameMap[self.value]
        return (
            "{}{}"
        ).format(value,self.suit[0])


class GameCards:
    '''
        生成德州扑克游戏所用到的52张牌
    '''
    ValueMap = list(range(2, 15))
    # 数值域

    SuitMap = ['heart', 'spade', 'clover', 'diamond']
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
    'One Pair': 2,
    'Two Pairs': 3,
    'Set': 4,
    'Straight': 5,
    'Flush': 6,
    'Full House': 7,
    'Four Of One Kind': 8,
    'Straight Flush': 9,
    'Royal Flush': 10
}


class GroupPattern:
    '''
        组合牌型
    '''
    suit_list = []
    value_list = []
    suit_set = set()    #花色值域
    value_set = set()   #牌面大小值域
    name = 'Basic Pattern'

    def __init__(self,name,five_cards):
        self.name = name     #牌型名称
        self.value = GroupMap[name]     #组合大小权值（用于排序牌力）
        self.five_cards = five_cards
        self.suit_list = [card.suit for card in self.five_cards]
        self.suit_set = set(self.suit_list)
        self.value_list = [card.value for card in self.five_cards]
        self.value_set = set(self.value_list)
        self.value_map = {}
        for uni_val in self.value_set:
            self.value_map[uni_val] = self.value_list.count(uni_val)
        self.judge_result = self.judge()

    def _judge(self):
        if len(self.five_cards) != 5:
            raise ValueError('Just judge pattern of 5 cards group')

    def judge(self):
        print('execute basic judge , pls check it.')

    def raise_TypeError(self):
        raise TypeError(
            'Just {} judged, the function could be executed.' \
                .format(self.name)
        )

    def get_x_value(self,count,list=False,need_check=True):
        if need_check and not self.judge_result:
            self.raise_TypeError()
        keys = []
        for key in self.value_map.keys():
            if self.value_map[key] == count:
                if not list:
                    return key
                else:
                    keys.append(key)
        return keys

    @property
    def max_val(self):
        return max(*self.value_set)

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

    def judge(self):
        self._judge()
        return len(self.value_set)==2 and \
               max(*self.value_map.values())==3
              #四条时最大相同值的键数应为4

    @property
    def the_three_Value(self):
        return self.get_x_value(count=3)

    @property
    def the_two_Value(self):
         return self.get_x_value(count=2)


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

    def judge(self):
        self._judge()
        return len(self.suit_set)==1


class FourOfOneKind(GroupPattern):
    '''
        四条
    '''
    name = 'Four Of One Kind'

    def __init__(self,five_cards):
        GroupPattern.__init__(self,
            name=self.name,
            five_cards=five_cards
          )

    def judge(self):
        self._judge()
        return len(self.value_set) == 2 and \
           max(*self.value_map.values())==4

    @property
    def the_four_Value(self):
        return self.get_x_value(count=4)

    @property
    def the_one_Value(self):
        return self.get_x_value(count=1)


class Straight(GroupPattern):
    '''
        顺子
    '''
    name = 'Straight'

    def __init__(self,five_cards):
        GroupPattern.__init__(self,
            name=self.name,
            five_cards=five_cards
          )

    def judge(self):
        self._judge()
        #一是首尾之差为4，二是无重复元素
        return max(*self.value_set)-min(*self.value_set)==4 and\
                len(self.value_set) == 5


class StraightFlush(GroupPattern):
    '''
        同花顺
    '''
    name = 'Straight Flush'

    def __init__(self,five_cards):
        GroupPattern.__init__(self,
            name=self.name,
            five_cards=five_cards
          )

    def judge(self):
        self._judge()
        return Straight(self.five_cards).judge_result and\
            Flush(self.five_cards).judge_result


class RoyalFlush(GroupPattern):
    '''
        皇家同花顺
    '''
    name = 'Royal Flush'

    def __init__(self,five_cards):
        GroupPattern.__init__(self,
            five_cards = five_cards,
            name=self.name
        )

    def judge(self):
        self._judge()
        return StraightFlush(self.five_cards).judge_result and\
            self.max_val == 14


class Set(GroupPattern):
    '''
        三条
    '''
    name = 'Set'

    def __init__(self,five_cards):
        GroupPattern.__init__(self,
              five_cards=five_cards,
              name=self.name
        )

    def judge(self):
        self._judge()
        return 1 in self.value_map.values() and \
               3 in self.value_map.values()

    @property
    def the_three_Value(self):
        return self.get_x_value(count=3)

    @property
    def the_one_Value(self):
        return max(*self.get_x_value(count=1,list=True))


class TwoPairs(GroupPattern):
    '''
        两对
    '''
    name = 'Two Pairs'

    def __init__(self,five_cards):
        GroupPattern.__init__(self,
              five_cards=five_cards,
              name=self.name
        )

    def judge(self):
        self._judge()
        return len(
            self.get_x_value(count=2,list=True,need_check=False)
        )==2

    @property
    def the_big_pair_Value(self):
        return max(*self.get_x_value(count=2, list=True))

    @property
    def the_small_pair_Value(self):
        return min(*self.get_x_value(count=2, list=True))

    @property
    def the_single_Value(self):
        return self.get_x_value(count=1)


class OnePair(GroupPattern):
    '''
        一对
    '''
    name = 'One Pair'

    def __init__(self,five_cards):
        GroupPattern.__init__(self,
              five_cards=five_cards,
              name=self.name
        )

    def judge(self):
        self._judge()
        return len(self.get_x_value(count=2,list=True,need_check=False))==1 and \
                len(self.get_x_value(count=1,list=True,need_check=False))==3

    @property
    def the_pair_Value(self):
        return self.get_x_value(count=2)

    @property
    def the_single_Values(self):
        return self.get_x_value(count=1,list=True,need_check=False)


class HighCard(GroupPattern):
    '''
        高牌
    '''
    name = 'High Card'

    def __init__(self,five_cards):
        GroupPattern.__init__(self,
              five_cards=five_cards,
              name=self.name
        )

    def judge(self):
        self._judge()
        return len(self.get_x_value(count=1,list=True,need_check=False))==5 and \
            not Straight(self.five_cards).judge_result and \
            not Flush(self.five_cards).judge_result

    @property
    def the_single_Values(self):
        return self.get_x_value(count=1, list=True, need_check=False)