from capi.com_types import *


class CalcController:
    def __init__(self, logger, limit):
        self._logger = logger
        self._limit = limit

    def canOrderByVirtualFund(self, availableVirtualFund, qty, price, marginRate, fee=0):
        if availableVirtualFund-qty*price*marginRate < 0:
            return {
                "ErrorCode":OrderFail,
                "LimitSource":OrderLimitFromFund,
            }
        else:
            return {
                "ErrorCode": OrderSuccess,
                "LimitSource": OrderLimitFromFund,
            }