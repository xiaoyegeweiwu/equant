import talib

sentOrder = True
localIdList = []

cnt = 0

def initialize(context): 
    SetBarInterval("NYMEX|F|CL|1910", 'M', 1, 200)
    #SetBarInterval("ZCE|F|CF|001", 'M', 1, 200)    SetActual()


def handle_data(context):
    global sentOrder, localIdList
    global cnt
    if context.triggerType() == 'H':
        return

    #LogInfo('ac:', A_AccountID())

    if sentOrder:
    #if cnt < 100:
        for i in range(50):
            ret, localId = A_SendOrder(Enum_Buy(), Enum_Entry(), 1, Q_Last())
            if ret == 0: 
                localIdList.append(localId)
                cnt = cnt + 1
        sentOrder = False
    
    #LogInfo("lst:%s, len:%d, ac:%s" %(str(localIdList), len(localIdList), A_AccountID()))

    if not A_AccountID():
        return
    
    for lid in localIdList:
        LogInfo("ORDER", lid, A_GetOrderNo(lid), A_OrderStatus(lid), A_FirstOrderNo())
    
