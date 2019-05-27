import talib

code1 = "SHFE|F|ZN|1907"
code2 = "SHFE|F|ZN|1908"
bar = 0
#时间以小数方式返回 ？

def initialize(context): 
    SetBarInterval(code1, 'M', 5, "20190520")
    SetActual()

def handle_data(context):            
    #bid = Q_BidPrice()
    #ask = Q_AskPrice()
    bid = ask = Close()
    PlotNumeric("bid", bid, 0x00FF00)    
    PlotNumeric("ask", ask, 0xFF0000)    
     
    
    global bar
    if bar == CurrentBar():
        return
        
    if MarketPosition() != 1:
        Buy(1, bid)
    elif MarketPosition() != -1:
        SellShort(1, ask)

    bar = CurrentBar()









































