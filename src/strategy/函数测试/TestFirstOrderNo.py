import talib


def initialize(context): 
    SetUserNo('Q437104345')
    SetBarInterval("SHFE|F|AL|1908", 'M', 1, 200)


def handle_data(context):
    orderNo = A_FirstOrderNo()
    while orderNo != -1:
        orderStatus = A_OrderStatus(orderNo)
        contNo = A_OrderContractNo(orderNo)
        LogInfo("contNo=", contNo, "orderNo=", orderNo, "orderStatus=", orderStatus)
        orderNo = A_NextOrderNo(orderNo)
