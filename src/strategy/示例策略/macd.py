import talib

fast = 12 # 快周期
slow = 26 # 慢周期
back = 9  # dea周期
qty = 1   # 下单量

def initialize(context): 
    # K线稳定后发单
    SetOrderWay(2)

def handle_data(context):
    # 断判数据是否就绪
    if len(Close()) < slow + back - 1:
        return

    # 计算MACD   
    diff, dea, macd = talib.MACD(Close(), fast, slow, back)

    # 突破下单
    if MarketPosition() != 1 and macd[-1] > 2:
        Buy(qty, Open()[-1]) 
    elif MarketPosition() != -1 and macd[-1] < -2:
        SellShort(qty, Open()[-1]) 

    # 绘制MACD曲线
    PlotNumeric('diff', diff[-1], RGB_Red(), False, False)
    PlotNumeric('dea', dea[-1], RGB_Blue(), False, False)    
    PlotStickLine('macd', 0, macd[-1], RGB_Red() if macd[-1] > 0 else RGB_Blue(), False, False) 
    # 绘制盈亏曲线
    PlotNumeric("profit", NetProfit() + FloatProfit(), 0xcccccc, False, True) 

