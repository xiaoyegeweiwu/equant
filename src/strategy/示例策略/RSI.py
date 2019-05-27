#-*-coding:utf-8
import talib

def initialize(context):
    SetBenchmark("NYMEX|F|CL|1907")
    SetBarInterval('M',1)

def handle_data(context):
    rsi = talib.RSI(Close(), timeperiod=20)
    
    #记录指标
    PlotNumeric('RSI', rsi[-1], color=Enum_Color_Red(), axis=True)
















