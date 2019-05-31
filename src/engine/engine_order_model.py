import copy
from capi.com_types import *


class EngineOrderModel:
    def __init__(self, strategyOrder={}):

        self._localOrder = {}
        self._epoleStarOrder = {}
        # 从文件中恢复的对应关系
        self._orderNo2OtherMap = {}

        if strategyOrder:
            # self._localOrder = strategyOrder["LocalOrder"]
            # self._epoleStarOrder = strategyOrder["EpoleStarOrder"]
            self._orderNo2OtherMap = strategyOrder["EpoleStarOrder2LocalOrderMap"]

        strategyId = 0
        self._localOrder.update({strategyId:SingleStrategyLocalOrder(strategyId)})
        self._epoleStarOrder.update({strategyId:EpoleStarOrder(strategyId)})

    def updateLocalOrder(self, event):
        strategyId = event.getStrategyId()
        if strategyId not in self._localOrder:
            self._localOrder[strategyId] = SingleStrategyLocalOrder(strategyId)
        record = event.getData()
        record['StrategyId'] = strategyId; record['ESessionId'] = event.getESessionId()
        self._localOrder[strategyId].updateLocalOrder(record)

    # response and notice
    def updateEpoleStarOrder(self, apiEvent):
        eventCode = apiEvent.getEventCode()
        if eventCode == EEQU_SRVEVENT_TRADE_ORDERQRY:
            self._updateEpoleStarOrderResponse(apiEvent)
        elif eventCode == EEQU_SRVEVENT_TRADE_ORDER:
            self._updateEpoleStarOrderNotice(apiEvent)
        elif eventCode == EEQU_SRVEVENT_TRADE_MATCHQRY:
            self._updateEpoleStarOrderResponse(apiEvent)
        elif eventCode == EEQU_SRVEVENT_TRADE_MATCH:
            self._updateEpoleStarOrderNotice(apiEvent)
        else:
            raise NotImplementedError

    #
    def _updateEpoleStarOrderResponse(self, event):
        for record in event.getData():
            if record["OrderNo"] and record["OrderNo"] in self._orderNo2OtherMap:
                strategyIdAndOrderId = self._orderNo2OtherMap[record["OrderNo"]]
                record["StrategyId"] = strategyIdAndOrderId["StrategyId"]
                record["ESessionId"] = strategyIdAndOrderId["ESessionId"]
            else:
                record['StrategyId'] = 0
                record["ESessionId"] = 0

            if record["StrategyId"] not in self._epoleStarOrder:
                self._epoleStarOrder.update({record["StrategyId"]:EpoleStarOrder(record["StrategyId"])})
            self._epoleStarOrder[record["StrategyId"]].updateEpoleOrderResponse(record)

    def _updateEpoleStarOrderNotice(self, apiEvent):
        assert len(apiEvent.getData()) == 1, "error"
        record = apiEvent.getData()[0]
        strategyId, eSessionId = apiEvent.getStrategyId(), apiEvent.getESessionId()
        record["StrategyId"] = strategyId; record["ESessionId"] = eSessionId
        if strategyId not in self._epoleStarOrder:
            self._epoleStarOrder.update({strategyId: EpoleStarOrder(strategyId)})
        self._epoleStarOrder[strategyId].updateEpoleStarOrderNotice(record)
        self._localOrder[strategyId].updateLocalOrder(record)
        if strategyId > 0 and record["OrderNo"]:
            self._orderNo2OtherMap[record["OrderNo"]] = {"StrategyId":strategyId, "ESessionId":eSessionId}

    def getLocalOrderData(self):
        data = {}
        for strategyId, obj in self._localOrder.items():
            data[strategyId] = obj.getLocalOrder()
        return data

    def getEpoleStarOrder(self):
        data = {}
        for strategyId, obj in self._epoleStarOrder.items():
            data[strategyId] = obj.getEpoleStarOrder()
        return data

    def getData(self):
        result = {
            "LocalOrder":self.getLocalOrderData(),
            "EpoleStarOrder":self.getEpoleStarOrder(),
            "EpoleStarOrder2LocalOrderMap":self._orderNo2OtherMap
        }
        return result


# 实盘本地订单
class SingleStrategyLocalOrder:
    def __init__(self, strategyId):
        self._strategyId = strategyId
        self._localOrder = {}
        self._localOrderFlow = []

    def updateLocalOrder(self, record):
        self._localOrder[record["ESessionId"]] = record
        self._localOrderFlow.append({record["ESessionId"]:record})

    def getLocalOrder(self):
        return self._localOrder

    def removeLocalOrder(self, event):
        pass


class EpoleStarOrder:
    def __init__(self, strategyId):
        self._strategyId = strategyId
        self._epoleStarOrder = {}
        self._epoleStarOrderFlow = []

        if self._strategyId == 0:
            self._eSessionId = 1

    def updateEpoleOrderResponse(self, record):
        self.resetESessionId(record)
        self._epoleStarOrder[record["ESessionId"]] = record
        self._epoleStarOrderFlow.append(record)

    def updateEpoleStarOrderNotice(self, record):
        self.resetESessionId(record)
        self._epoleStarOrder[record["ESessionId"]] = record
        self._epoleStarOrderFlow.append(record)

    def resetESessionId(self, record):
        if self._strategyId == 0 and record["ESessionId"] == 0:
            eSessionId = str(self._strategyId)+'-'+str(self._eSessionId)
            record["ESessionId"] = eSessionId
            self._eSessionId += 1

    def getEpoleStarOrder(self):
        return self._epoleStarOrder

    def clear(self):
        self._epoleStarOrder = {}
        self._epoleStarOrderFlow = []



