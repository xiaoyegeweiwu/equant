# 套利策略 历史回测

import talib

code1="ZCE|F|TA|909"
code2="ZCE|F|TA|001"
tp = 'M'
p = 10

p1=5
p1=20
dot=1
qty=1

bar=0

def initialize(context):
    SetBarInterval(code1, tp, p, 2000)
    SetBarInterval(code2, tp, p, 2000)
    
def handle_data(context):
    if len(Close(code1, tp, p)) < p1 or len(Close(code2, tp, p)) < p2:
        return;
    
    ma1 = talib.MA(Close(code1, tp, p), timeperiod=p1, matype=0)
    ma2 = talib.MA(Close(code2, tp, p), timeperiod=p1, matype=0)
    sma1= ma1[-1] - ma2[-1]
    ma1 = talib.MA(Close(code1, tp, p), timeperiod=p2, matype=0)
    ma2 = talib.MA(Close(code2, tp, p), timeperiod=p2, matype=0)
    sma2= ma1[-1] - ma2[-1]     
    
    PlotNumeric("sma1", sma1, 0x0000FF, False)
    PlotNumeric("sma2", sma2, 0xFF0000, False)
    PlotNumeric("profit", A_TotalProfitLoss(), 0x808080, False, True) 
    
    global bar    
    #同一根K线上只做一笔交易
    if bar == CurrentBar(code1, tp, p):
        return

    if sma1 > sma2 + dot * PriceTick():
        if MarketPosition(code1) == 0:
            Buy(qty, Close(code1, tp, p)[-1], code1)
            SellShort(qty, Close(code2, tp, p)[-1], code2)
        elif MarketPosition() < 0:
            BuyToCover(qty, Close(code1, tp, p)[-1], code1)
            Sell(qty, Close(code2, tp, p)[-1], code2)
        else:
            return
    elif sma1 < sma2 - dot * PriceTick():
        if MarketPosition(code1) == 0:
            SellShort(qty, Close(code1, tp, p)[-1], code1)
            Buy(qty, Close(code2, tp, p)[-1], code2)
        elif MarketPosition(code1) > 0:
            Sell(qty, Close(code1, tp, p)[-1], code1)
            BuyToCover(qty, Close(code2, tp, p)[-1], code2)
        else:
            return
        
    bar = CurrentBar(code1, tp, p)
    




















