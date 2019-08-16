import talib

sendtimes = 0
code2 = 'ZCE|F|SR|001'

def initialize(context): 
    SetBarInterval(code2, 'M', 1, 1)
    SetActual()

def handle_data(context):
    global sendtimes
    if context.triggerType == 'H':
        return
    if sendtimes < 2:
        A_SendOrder(Enum_Buy(), Enum_Entry(), 1, Q_UpperLimit(), code2)
        sendtimes += 1

    queueOrders = A_AllQueueOrderNo()
    LogInfo("AAAAAA", queueOrders)

    if len(queueOrders) > 0:
        DeleteAllOrders()
