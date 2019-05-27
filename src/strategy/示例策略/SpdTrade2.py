# 套利策略，盘实运行

import talib

usr="DDY"
code1="ZCE|F|TA|909"
code2="ZCE|F|AT|001"
p1=20
dot=2
qty=1

bar=0

def initialize(context):
    SetBarInterval(code1, 'M', 10, "20190310")
    SetBarInterval(code2, 'M', 10, "20190310")
    SetActual()

def handle_data(context):
    if len(Close()) < p1:
        return;
    ma1 = talib.MA(Close(code1), timeperiod=p1, matype=0)
    ma2 = talib.MA(Close(code2), timeperiod=p1, matype=0)
    LogInfo('ma1', Close(code1)[-1], '  ma2', Close(code2)[-1])

    ma= ma1[-1] - ma2[-1]
    prc = Close(code1)[-1] - Close(code2)[-1]       
    
    PlotNumeric("ma1", ma1[-1], color=0xFF00FF)
    PlotNumeric("ma2", ma2[-1], color=0x0008FF)
    
    PlotNumeric("prc", prc, 0xFF0000, False)
    PlotNumeric("high", ma + dot * PriceTick(), 0x00aa00, False)
    PlotNumeric("low", ma - dot * PriceTick(), 0x0000FF, False)
    PlotNumeric("fit", A_TotalProfitLoss(), 0xFF0000, False) 
    
    if context.strategyStatus() !='C':
        return;
    
    global bar    
    #同一根K线上只做一笔交易
    if bar == CurrentBar():
        return

    offset = Enum_Entry()
    if prc > ma + dot * PriceTick():
        # 不允许多笔多仓
        if A_TotalPosition() > 0:
            return
        if A_SellPosition(code1) > 0 or A_SellPosition(code2) > 0:
            offset = Enum_ExitToday()
        A_SendOrder(usr, code1, '2', '0', Enum_Buy() , offset, 'T', Q_BidPrice(code1) + PriceTick(), qty)
        A_SendOrder(usr, code2, '2', '0', Enum_Sell(), offset, 'T', Q_AskPrice(code2) - PriceTick(), qty)
    elif prc < ma - dot * PriceTick():
        # 不允许多笔空仓
        if A_TotalPosition() < 0:
            return
        if A_BuyPosition(code1) > 0 or A_BuyPosition(code2) > 0:
            offset = Enum_ExitToday()
        A_SendOrder(usr, code1, '2', '0', Enum_Sell(), offset, 'T', Q_AskPrice(code2) - PriceTick(), qty)
        A_SendOrder(usr, code2, '2', '0', Enum_Buy() , offset, 'T', Q_BidPrice(code1) + PriceTick(), qty)
        
    bar == CurrentBar()















