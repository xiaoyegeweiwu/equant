import talib

qty2    = 2
AllBuy  = 0   # 多头持仓数
AllSell = 0   # 空头持仓数

def initialize(context): 
    SetBarInterval('SHFE|F|CU|1908', 'M', 1, 100)

def handle_data(context):
    global AllBuy
    global AllSell

    cb = CurrentBar()
    LogInfo(f"[{cb}][K线{cb}初始持仓情况]: MarketPosition: {MarketPosition()}")
    if cb % 2 == 1:
        if MarketPosition() == -1:
            Buy(qty2, Close()[-1], needCover=False)
            TotalBuy = BuyPosition()
            if TotalBuy - AllBuy == qty2:
                AllBuy += qty2
                LogInfo(f"[{cb}][买入开仓后]: 买开手数: {qty2}")
                LogInfo(f"[{cb}][买入开仓后]: 多头数量: {AllBuy}, 空头数量: {AllSell}")
                LogInfo(f"[{cb}][买入开仓后]: MarketPosition: {MarketPosition()}")
            else:
                LogInfo(f"[{cb}][买入开仓失败]，当前多头数量: {AllBuy}, 空头数量: {AllSell}")
                LogInfo(f"[{cb}][买入开仓失败]，当前MarketPosition: {MarketPosition()}")
            BuyToCover(qty2, Close()[-1])
            TotalSell = SellPosition()
            if TotalSell - AllSell == -qty2:
                AllSell -= qty2
                LogInfo(f"[{cb}][买入平仓后]: 买平手数: {qty2}")
                LogInfo(f"[{cb}][买入平仓后]: 多头数量: {AllBuy}, 空头数量: {AllSell}")
                LogInfo(f"[{cb}][买入平仓后]: MarketPosition: {MarketPosition()}")
            else:
                LogInfo(f"[{cb}][买入平仓失败]，当前多头数量: {AllBuy}, 空头数量: {AllSell}")
                LogInfo(f"[{cb}][买入平仓失败]，当前MarketPosition: {MarketPosition()}")
        Buy(qty2, Close()[-1], needCover=False)
        TotalBuy = BuyPosition()
        if TotalBuy - AllBuy == qty2:
            AllBuy += qty2
            LogInfo(f"[{cb}][买入开仓后]: 买开手数: {qty2}")
            LogInfo(f"[{cb}][买入开仓后]: 多头数量: {AllBuy}, 空头数量: {AllSell}")
            LogInfo(f"[{cb}][买入开仓后]: MarketPosition: {MarketPosition()}")
        else:
            LogInfo(f"[{cb}][买入开仓失败]，当前多头数量: {AllBuy}, 空头数量: {AllSell}")
            LogInfo(f"[{cb}][买入开仓失败]，当前MarketPosition: {MarketPosition()}")
    else:
        if MarketPosition() == 1:
            SellShort(qty2, Close()[-1], needCover=False)
            TotalSell = SellPosition()
            if TotalSell - AllSell == qty2:
                AllSell += qty2
                LogInfo(f"[{cb}][卖出开仓后]: 卖开手数: {qty2}")
                LogInfo(f"[{cb}][卖出开仓后]: 多头数量: {AllBuy}, 空头数量: {AllSell}")
                LogInfo(f"[{cb}][卖出开仓后]: MarketPosition: {MarketPosition()}")
            else:
                LogInfo(f"[{cb}][卖出开仓失败]，当前多头数量: {AllBuy}, 空头数量: {AllSell}")
                LogInfo(f"[{cb}][卖出开仓失败]，当前MarketPosition: {MarketPosition()}")
            Sell(qty2, Close()[-1])
            TotalBuy = BuyPosition()
            if TotalBuy - AllBuy == -qty2:
                AllBuy -= qty2
                LogInfo(f"[{cb}][卖出平仓后]: 卖平手数: {qty2}")
                LogInfo(f"[{cb}][卖出平仓后]: 多头数量: {AllBuy}, 空头数量: {AllSell}")
                LogInfo(f"[{cb}][卖出平仓后]: MarketPosition: {MarketPosition()}")
            else:
                LogInfo(f"[{cb}][卖出平仓失败]，当前多头数量: {AllBuy}, 空头数量: {AllSell}")
                LogInfo(f"[{cb}][卖出平仓失败]，当前MarketPosition: {MarketPosition()}")
        SellShort(qty2, Close()[-1], needCover=False)
        TotalSell = SellPosition()
        if TotalSell - AllSell == qty2:
            AllSell += qty2
            LogInfo(f"[{cb}][卖出开仓后]: 卖开手数: {qty2}")
            LogInfo(f"[{cb}][卖出开仓后]: 多头数量: {AllBuy}, 空头数量: {AllSell}")
            LogInfo(f"[{cb}][卖出开仓后]: MarketPosition: {MarketPosition()}")
        else:
            LogInfo(f"[{cb}][卖出开仓失败]，当前多头数量: {AllBuy}, 空头数量: {AllSell}")
            LogInfo(f"[{cb}][卖出开仓失败]，当前MarketPosition: {MarketPosition()}")
    
