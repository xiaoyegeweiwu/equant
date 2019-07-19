import talib

qty = 2

def initialize(context): 
    SetBarInterval('SHFE|F|CU|1908', 'M', 1, 100)


def handle_data(context):
    cb = CurrentBar()
    LogInfo(f"[{cb}][K线{cb}初始持仓情况]: MarketPosition: {MarketPosition()}")
    if cb % 2 == 1:
        if MarketPosition() == -1:
            BuyToCover(qty, Close()[-1])
            LogInfo(f"[{cb}][买入平仓后]: MarketPosition: {MarketPosition()}")
        Buy(2*qty, Close()[-1], needCover=False)
        LogInfo(f"[{cb}][买入开仓后]: 买开手数: {qty+qty}")
        LogInfo(f"[{cb}][买入开仓后]: MarketPosition: {MarketPosition()}")
    else:
        if MarketPosition() == 1:
            Sell(2*qty, Close()[-1])
            LogInfo(f"[{cb}][卖出平仓后]: MarketPosition: {MarketPosition()}")
        SellShort(qty, Close()[-1], needCover=False)
        LogInfo(f"[{cb}][卖出开仓后]: 卖开手数: {qty}")
        LogInfo(f"[{cb}][卖出开仓后]: MarketPosition: {MarketPosition()}")
    
