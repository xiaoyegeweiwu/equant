import talib

code1 = 'ZCE|F|TA|001'
code2 = 'ZCE|F|TA|005'
scode = 'SPD|s|TA|001|005'

def initialize(context): 
    SetBarInterval(scode, 'T', 0, 300)
    SetBarInterval(code1, 'T', 0, 300)
    SetBarInterval(code2, 'T', 0, 300)

def handle_data(context):
    LogInfo('quote time:', context.contractNo(), Q_UpdateTime())  

