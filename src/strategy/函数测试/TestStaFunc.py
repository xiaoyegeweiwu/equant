import talib

rd=0

def initialize(context): 
    SetBarInterval('SHFE|F|CU|1907', 'M',1, 100)


def handle_data(context):
    global rd
    close = Close()
    ret, sma = SMA(close, 12, 2)
    LogInfo("round:%d, len:%d, sma:%f, cl:%f\n" %(rd, len(close), sma, close[-1]))

    opc, opo, opos, otran = ParabolicSAR(High(), Low(), 0.02, 0.2)
    LogInfo("round:%d, opc:%f, opo:%f, opos:%d, otran:%d\n" %(rd, opc, opo, opos, otran))
    rd = rd+1
