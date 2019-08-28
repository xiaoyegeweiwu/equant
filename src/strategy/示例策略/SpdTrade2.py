# 套利策略，盘实运行

import talib
import numpy as np

code1="ZCE|F|TA|909"
code2="ZCE|F|TA|001"

bt = 'M'    #barType
bi = 1      #barLength

p1=5
p2=20
dot=1
qty=1

spds = []

def initialize(context):
    SetBarInterval(code1, bt, bi, 1)
    SetBarInterval(code2, bt, bi, 1)
    SetTriggerType(code1, 1)
    SetTriggerType(code2, 1)
    SetOrderWay(2)
    SetActual()

def handle_data(context):  
    # 仅限实盘阶段运行
    if context.strategyStatus() !='C':
        return 

    if len(spd_c) < p1:
        return

    prc_lst1 = Close(code1, bt, bi)
    prc_lst2 = Close(code2, bt, bi)

    # 生成价差序列
    spd_c = prc_lst1[-1] - prc_lst2[-1];
    global spds
    if len(prc_lst1) > len(spds):
        spds.append(spd_c)
    else:
        spds[-1] = spd_c

    # 计算价差ma
    sma1 = talib.MA(np.array(spds), p1, 2, 2)  
    sma2 = talib.MA(np.array(spds), p2, 2, 2)         

    # 根据两根ma的交叉关系下单
    offset = Enum_Entry()
    if sma1 > sma2 + dot * PriceTick() and A_TotalPosition() <= 0: # 不允许多笔多仓
        if A_SellPosition(code1) > 0 or A_SellPosition(code2) > 0:
            offset = Enum_ExitToday()
        A_SendOrder(Enum_Buy() , offset, qty, Q_BidPrice(code1) + PriceTick(code1), code1)
        A_SendOrder(Enum_Sell(), offset, qty, Q_AskPrice(code2) - PriceTick(code2), code2)
    elif sma1 < sma2 - dot * PriceTick() and A_TotalPosition() = 0: # 不允许多笔空仓
        if A_BuyPosition(code1) > 0 or A_BuyPosition(code2) > 0:
            offset = Enum_ExitToday()
        A_SendOrder(Enum_Sell(), offset, qty, Q_AskPrice(code1) - PriceTick(code1), code1)
        A_SendOrder(Enum_Buy() , offset, qty, Q_BidPrice(code2) + PriceTick(code2), code2)

    # 绘制指标线   
    PlotNumeric("sma1", sma1, 0x0000FF, False)
    PlotNumeric("sma2", sma2, 0xFF0000, False)
    PlotNumeric("profit", A_TotalProfitLoss() + A_ProfitLoss() - A_Cost(), 0x808080, False, True)   

