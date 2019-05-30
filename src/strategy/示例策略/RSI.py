#-*-coding:utf-8
import talib

def initialize(context):
    SetBarInterval("NYMEX|F|CL|1907", 'M', 1, '20190510')

def handle_data(context):
    rsi = talib.RSI(Close(), timeperiod=20)
    
    #记录指标
    PlotNumeric('RSI', rsi[-1], RGB_Red(), True, True)
    
