# 德州扑克模拟程序

### patterns.py 
> 对各种牌型的现实描述及逻辑描述

### judge.py
> 对某五张组合的牌型判断
> 通过 test_patterns_judge 模块测试

![](http://wx1.sinaimg.cn/large/a0695fdfly1fblq5tmwpbj20xy1bstp4.jpg)


### compare.py
> 二元判断牌力
> 通过 test_compare 模块测试

![](http://ww2.sinaimg.cn/large/a0695fdfgw1fbmz3e6e2uj20lo154qfg.jpg)

### roles.py
> 抽象出关于德州赌局的各种角色

### game.py
> 精准描绘游戏逻辑，从发牌前下大小盲，到最后的清算。
至于本模块是否为主体，得看老子怎样看待这份程序，如果是为了模拟游戏交互的流程，那么是。如果是为了探究AI的算法，这模块包括之后的建库，webserver响应，前台UI的绘制，都是side part。