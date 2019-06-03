import talib

rd=0

def initialize(context): 
    SetBarInterval('SHFE|F|CU|1907', 'M',1, 100)


def handle_data(context):
    global rd
    close = Close()
    ret, smas = SMA(close, 12, 2)
    LogInfo("round:%d, len:%d, sma:%f, cl:%f\n" %(rd, len(close), smas[-1], close[-1]))

    opcs, opos, oposs, otrans = ParabolicSAR(High(), Low(), 0.02, 0.2)
    LogInfo("round:%d, opc:%f, opo:%f, opos:%d, otran:%d\n" %(rd, opcs[-1], opos[-1], oposs[-1], otrans[-1]))
    rd = rd+1

