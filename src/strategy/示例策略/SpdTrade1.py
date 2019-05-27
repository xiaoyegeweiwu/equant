# 套利策略 历史回测

import talib

code1="ZCE|F|TA|909"
code2="ZCE|F|AT|001"
p1=20
dot=2
qty=1

bar=0

def initialize(context):
    SetBarInterval(code1, 'M', 1, "20190510")
    SetBarInterval(code2, 'M', 1, "20190510")
    
def handle_data(context):
    if len(Close()) < p1:
        return;
    ma1 = talib.MA(Close(code1, 'M', 1), timeperiod=p1, matype=0)
    ma2 = talib.MA(Close(code2, 'M', 1), timeperiod=p1, matype=0)    
    LogInfo('ma1', Close(code1, 'M', 1)[-1], '  ma2', Close(code2, 'M', 1)[-1])

    ma= ma1[-1] - ma2[-1]
    prc = Close(code1)[-1] - Close(code2)[-1]       
    
    PlotNumeric("ma1", ma1[-1], color=0xFF00FF)
    PlotNumeric("ma2", ma2[-1], color=0x0008FF)
    
    print(ma1[-1], ma2[-1])
    PlotNumeric("prc", prc, 0xFF0000, False)
    PlotNumeric("high", ma + dot * PriceTick(), 0x00aa00, False)
    PlotNumeric("low", ma - dot * PriceTick(), 0x0000FF, False)    
    PlotNumeric("fit", NetProfit(), 0xFF0000, False)
    
    global bar    
    #同一根K线上只做一笔交易
    if bar == CurrentBar():
        return

    if prc > ma + dot * PriceTick():
        if MarketPosition() == 0:
            Buy(qty, Close()[-1])
            Buy(qty, Close()[-1])
        elif MarketPosition() < 0:
            BuyToCover(qty, Close()[-1])
            BuyToCover(qty, Close()[-1])
        else:
            return
    elif prc < ma - dot * PriceTick():
        if MarketPosition() == 0:
            SellShort(qty, Close()[-1])
            SellShort(qty, Close()[-1])
        elif MarketPosition() > 0:
            Sell(qty, Close()[-1])
            Sell(qty, Close()[-1])
        else:
            return
        
    bar == CurrentBar()
    




















