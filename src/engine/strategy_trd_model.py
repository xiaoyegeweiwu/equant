import numpy as np
from capi.com_types import *
from .engine_model import *
import time, sys, datetime
from .trade_model import TradeModel

class StrategyTrade(TradeModel):
    '''交易数据模型'''
    def __init__(self, strategy, config):
        self.logger = strategy.logger
        self._strategy = strategy
        TradeModel.__init__(self, self.logger)
        self._config = config
        #self._selectedUserNo = self._config._metaData['Money']['UserNo']
        # print("===== StrategyTrade ====", self._config._metaData)
        
    def initialize(self):
        self._selectedUserNo = self._config.getUserNo()

    def reqTradeData(self):
        event = Event({
            'EventCode': EV_ST2EG_STRATEGYTRADEINFO,
            'StrategyId': self._strategy.getStrategyId(),
            'Data': '',
        })

        self._strategy.sendEvent2Engine(event)

    def getAccountId(self):
        '''
        :return:当前公式应用的交易帐户ID
        '''
        if not self._selectedUserNo:
            return ''
        
        user = self._userInfo[self._selectedUserNo]
        if not user.isReady():
            return ''
        
        return self._selectedUserNo
        
    def getAllAccountId(self):
        '''
        获取所有登录账号ID
        '''
        accList = []
        for k, v in self._userInfo.items():
            if not v.isReady():
                continue
            accList.append(k)
        return accList

    def getAllPositionSymbol(self, userNo):
        '''
        :return:所有持仓合约
        ''' 
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if len(self._userInfo) == 0 or userNo not in self._userInfo:
            raise Exception("请确保您的账号已经在客户端登录")

        tUserInfoModel = self._userInfo[userNo]
        if not tUserInfoModel.isReady():
            return []
        
        if len(tUserInfoModel._position) == 0:
            return []

        contList = []
        for positionNo in list(tUserInfoModel._position.keys()):
            position = tUserInfoModel._position[positionNo]
            contNo = position._metaData['Cont']
            if contNo not in contList:
                contList.append(contNo)
        return contList

    def getDataFromTMoneyModel(self, key, userNo):
        '''
        获取self._userInfo中当前账户指定的资金信息
        :param key:需要的资金信息的key
        :return:资金信息
        '''       
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo       
        
        if len(self._userInfo) == 0 or userNo not in self._userInfo:
            raise Exception("请确保您的账号已经在客户端登录")

        tUserInfoModel = self._userInfo[userNo]
        if not tUserInfoModel.isReady():
            return 0
        
        if len(tUserInfoModel._money) == 0:
            return 0

        tMoneyModel = None
        if 'Base' in tUserInfoModel._money:
            tMoneyModel = tUserInfoModel._money['Base']

        if len(tUserInfoModel._money) > 0:
            tMoneyModelList = list(tUserInfoModel._money.values())
            tMoneyModel = tMoneyModelList[0]

        if not tMoneyModel or key not in tMoneyModel._metaData:
            return 0

        return tMoneyModel._metaData[key]
        
    def getSign(self, userNo):
        '''
        :return: 获取当前账户的服务器标识
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo

        if userNo not in self._userInfo:
            return None
        return self._userInfo[userNo].getSign()

    def getCost(self, userNo):
        '''
        :return: 当前公式应用的交易帐户的手续费
        '''  
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
        
        return self.getDataFromTMoneyModel('Fee', userNo)

    def getCurrentEquity(self, userNo):
        '''
        :return:当前公式应用的交易帐户的动态权益
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return self.getDataFromTMoneyModel('Equity', userNo)

    def getFreeMargin(self, userNo):
        '''
        :return:当前公式应用的交易帐户的可用资金
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return self.getDataFromTMoneyModel('Available', userNo)

    def getAMargin(self, userNo):
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return self.getDataFromTMoneyModel('Deposit', userNo)

    def getProfitLoss(self, userNo):
        '''
        :return:当前公式应用的交易帐户的浮动盈亏
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return self.getDataFromTMoneyModel('FloatProfitTBT', userNo)

    def getCoverProfit(self, userNo):
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return self.getDataFromTMoneyModel('CoverProfitTBT', userNo)

    def getTotalFreeze(self, userNo):
        '''
        :return:当前公式应用的交易帐户的冻结资金
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return self.getDataFromTMoneyModel('FrozenFee', userNo) + self.getDataFromTMoneyModel('FrozenDeposit', userNo)

    def getItemSumFromPositionModel(self, direct, contNo, key, userNo):
        '''
        获取某个账户下所有指定方向、指定合约的指标之和
        :param direct: 买卖方向，为空时表示所有方向
        :param contNo: 合约编号
        :param key: 指标名称
        :return:
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if len(self._userInfo) == 0 or userNo not in self._userInfo:
            return 0

        tUserInfoModel = self._userInfo[userNo]
        if len(tUserInfoModel._position) == 0:
            return 0

        contractNo = self._config.getBenchmark() if not contNo else contNo
        itemSum = 0.0
        for orderNo in list(tUserInfoModel._position.keys()):
            tPositionModel = tUserInfoModel._position[orderNo]
            if tPositionModel._metaData['Cont'] == contractNo and key in tPositionModel._metaData:
                if not direct or tPositionModel._metaData['Direct'] == direct:
                    itemSum += tPositionModel._metaData[key]

        return itemSum

    def getBuyAvgPrice(self, contNo, userNo):
        '''
        :return:当前公式应用的帐户下当前商品的买入持仓均价
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if len(self._userInfo) == 0 or userNo not in self._userInfo:
            raise Exception("请确保您的账号已经在客户端登录")

        tUserInfoModel = self._userInfo[userNo]
        if len(tUserInfoModel._position) == 0:
            return 0

        contNo = self._config.getBenchmark() if not contNo else contNo
        priceSum = 0.0
        posSum = 0
        for orderNo in list(tUserInfoModel._position.keys()):
            tPositionModel = tUserInfoModel._position[orderNo]
            if tPositionModel._metaData['Cont'] == contNo and tPositionModel._metaData['Direct'] == 'B':
                priceSum += tPositionModel._metaData['PositionPrice'] * tPositionModel._metaData['PositionQty']
                posSum += tPositionModel._metaData['PositionQty']

        return priceSum / posSum if posSum > 0 else 0.0

    def getBuyPosition(self, contNo, userNo):
        '''
        :return:当前公式应用的帐户下当前商品的买入持仓
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return int(self.getItemSumFromPositionModel('B', contNo,  'PositionQty', userNo))

    def getBuyPositionCanCover(self, contNo, userNo):
        '''买仓可平数量'''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if not contNo:
            contNo = self._config.getBenchmark()
        buyPos = self.getBuyPosition(contNo, userNo) - self.getQueueSumFromOrderModel( 'S', contNo, ('C', 'T'), userNo)
        return int(buyPos)

    def getQueueSumFromOrderModel(self, direct, contNo, offset, userNo):
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if len(self._userInfo) == 0 or userNo not in self._userInfo:
            raise Exception("请确保您的账号已经在客户端登录")
        tUserInfoModel = self._userInfo[userNo]

        if len(tUserInfoModel._order) == 0:
            return 0

        queueSum = 0
        for orderKey in list(tUserInfoModel._order.keys()):
            orderModel = tUserInfoModel._order[orderKey]
            if contNo == orderModel._metaData['Cont'] and direct == orderModel._metaData['Direct'] and orderModel._metaData['Offset'] in offset:
                if orderModel._metaData['OrderState'] == '4':
                    # 已排队
                    queueSum += orderModel._metaData['OrderQty']
                elif orderModel._metaData['OrderState'] == '5':
                    # 部分成交
                    queueSum += orderModel._metaData['OrderQty'] - orderModel._metaData['MatchQty']

        return queueSum

    def getBuyProfitLoss(self, contNo, userNo):
        '''
        :return:当前公式应用的帐户下当前商品的买入持仓盈亏
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return self.getItemSumFromPositionModel('B', contNo, 'FloatProfitTBT', userNo)

    def getSellAvgPrice(self, contNo, userNo):
        '''
        :return: 当前公式应用的帐户下当前商品的卖出持仓均价
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if len(self._userInfo) == 0 or userNo not in self._userInfo:
            raise Exception("请确保您的账号已经在客户端登录")

        tUserInfoModel = self._userInfo[userNo]
        if len(tUserInfoModel._position) == 0:
            return 0

        contNo = self._config.getBenchmark() if not contNo else contNo
        priceSum = 0.0
        posSum = 0
        for orderNo in list(tUserInfoModel._position.keys()):
            tPositionModel = tUserInfoModel._position[orderNo]
            if tPositionModel._metaData['Cont'] == contNo and tPositionModel._metaData['Direct'] == 'S':
                priceSum += tPositionModel._metaData['PositionPrice'] * tPositionModel._metaData['PositionQty']
                posSum += tPositionModel._metaData['PositionQty']

        return priceSum / posSum if posSum > 0 else 0.0

    def getSellPosition(self, contNo, userNo):
        '''
        :return: 当前公式应用的帐户下当前商品的卖出持仓
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return int(self.getItemSumFromPositionModel('S', contNo, 'PositionQty', userNo))

    def getSellPositionCanCover(self, contNo, userNo):
        '''卖仓可平数量'''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if not contNo:
            contNo = self._config.getBenchmark()
        sellPos = self.getSellPosition(contNo, userNo) - self.getQueueSumFromOrderModel('B', contNo, ('C', 'T'), userNo)
        return int(sellPos)


    def getSellProfitLoss(self, contNo, userNo):
        '''
        :return: 当前公式应用的帐户下当前商品的卖出持仓盈亏
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return self.getItemSumFromPositionModel('S', contNo, 'FloatProfitTBT', userNo)

    def getTotalAvgPrice(self, contNo, userNo):
        '''
        :return: 当前公式应用的帐户下当前商品的持仓均价
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if len(self._userInfo) == 0 or userNo not in self._userInfo:
            raise Exception("请确保您的账号已经在客户端登录")

        tUserInfoModel = self._userInfo[userNo]
        if len(tUserInfoModel._position) == 0:
            return 0

        contNo = self._config.getBenchmark() if not contNo else contNo
        priceSum = 0.0
        posSum = 0
        for orderNo in list(tUserInfoModel._position.keys()):
            tPositionModel = tUserInfoModel._position[orderNo]
            if tPositionModel._metaData['Cont'] == contNo:
                priceSum += tPositionModel._metaData['PositionPrice'] * tPositionModel._metaData['PositionQty']
                posSum += tPositionModel._metaData['PositionQty']

        return priceSum / posSum if posSum > 0 else 0.0

    def getTotalPosition(self, contNo, userNo):
        '''
        :return: 当前公式应用的帐户下当前商品的总持仓
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        totalPos = int(self.getItemSumFromPositionModel('B', contNo, 'PositionQty'), userNo) - int(self.getItemSumFromPositionModel('S', contNo, 'PositionQty', userNo))
        return totalPos

    def getTotalProfitLoss(self, contNo, userNo):
        '''
        :return: 当前公式应用的帐户下当前商品的总持仓盈亏
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        return self.getItemSumFromPositionModel('', contNo, 'FloatProfit', userNo)

    def getTodayBuyPosition(self, contNo, userNo):
        '''
        :return: 当前公式应用的帐户下当前商品的当日买入持仓
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        todayBuyPos = self.getItemSumFromPositionModel('B', contNo, 'PositionQty', userNo) - self.getItemSumFromPositionModel('B', contNo, 'PrePositionQty', userNo)
        return int(todayBuyPos)

    def getTodaySellPosition(self, contNo, userNo):
        '''
        :return: 当前公式应用的帐户下当前商品的当日卖出持仓
        '''
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        todaySellPos = self.getItemSumFromPositionModel('S', contNo, 'PositionQty', userNo) - self.getItemSumFromPositionModel('S', contNo, 'PrePositionQty', userNo)
        return int(todaySellPos)


    def getFirstOrderNo(self, contNo1, contNo2, userNo):
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if userNo not in self._userInfo:
            raise Exception("请先在极星客户端登录您的交易账号")

        tUserInfoModel = self._userInfo[userNo]
        if len(tUserInfoModel._order) == 0:
            return -1

        orderId = -1
        for orderKey in list(tUserInfoModel._order.keys()):
            orderModel = tUserInfoModel._order[orderKey]
            if not contNo1 or contNo1 == orderModel._metaData['Cont']:
                if orderId == -1 or orderId > orderModel._metaData['OrderId']:
                    orderId = orderModel._metaData['OrderId']

        return orderId

    def getNextOrderNo(self, orderId, contNo1, contNo2, userNo):
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if userNo not in self._userInfo:
            raise Exception("请先在极星客户端登录您的交易账号")

        tUserInfoModel = self._userInfo[userNo]
        if len(tUserInfoModel._order) == 0:
            return -1

        minOrderId = -1
        for orderKey in list(tUserInfoModel._order.keys()):
            orderModel = tUserInfoModel._order[orderKey]
            if not contNo1 or contNo1 == orderModel._metaData['Cont']:
                if orderModel._metaData['OrderId'] <= orderId:
                    continue
                # 获取大于orderId的值
                if minOrderId == -1:
                    minOrderId = orderModel._metaData['OrderId']
                # 找到大于orderId并最接近orderId的值
                if orderModel._metaData['OrderId'] < minOrderId:
                    minOrderId = orderModel._metaData['OrderId']

        return minOrderId

    def getLastOrderNo(self, contNo1, contNo2, userNo):
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if userNo not in self._userInfo:
            raise Exception("请先在极星客户端登录您的交易账号")

        tUserInfoModel = self._userInfo[userNo]
        if len(tUserInfoModel._order) == 0:
            return -1

        orderId = -1
        insertSeconds = -1
        for orderKey in list(tUserInfoModel._order.keys()):
            orderModel = tUserInfoModel._order[orderKey]
            if not contNo1 or contNo1 == orderModel._metaData['Cont']:
                timeDateStr = orderModel._metaData['InsertTime']
                time1 = datetime.datetime.strptime(timeDateStr, "%Y-%m-%d %H:%M:%S")
                seconds = float(time.mktime(time1.timetuple()))
                if seconds >= insertSeconds and orderModel._metaData['OrderId'] > orderId:
                    orderId = orderModel._metaData['OrderId']

        return orderId

    def getFirstQueueOrderNo(self, contNo1, contNo2, userNo):
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if userNo not in self._userInfo:
            raise Exception("请先在极星客户端登录您的交易账号")

        tUserInfoModel = self._userInfo[userNo]
        if len(tUserInfoModel._order) == 0:
            return -1

        orderId = -1
        for orderKey in list(tUserInfoModel._order.keys()):
            orderModel = tUserInfoModel._order[orderKey]
            if not contNo1 or contNo1 == orderModel._metaData['Cont']:
                # 待触发,排队中,部分成交
                if orderModel._metaData['OrderState'] not in (osTriggering, osQueued, osFillPart):
                    continue
                if orderId == -1 or orderId > orderModel._metaData['OrderId']:
                    orderId = orderModel._metaData['OrderId']

        return orderId

    def getNextQueueOrderNo(self, orderId, contNo1, contNo2, userNo):
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if userNo not in self._userInfo:
            raise Exception("请先在极星客户端登录您的交易账号")

        tUserInfoModel = self._userInfo[userNo]
        if len(tUserInfoModel._order) == 0:
            return -1

        minOrderId = -1
        for orderKey in list(tUserInfoModel._order.keys()):
            orderModel = tUserInfoModel._order[orderKey]
            if not contNo1 or contNo1 == orderModel._metaData['Cont']:
                # 待触发,排队中,部分成交
                if orderModel._metaData['OrderState'] not in (osTriggering, osQueued, osFillPart):
                    continue
                if orderModel._metaData['OrderId'] <= orderId:
                    continue
                # 获取大于orderId的值
                if minOrderId == -1:
                    minOrderId = orderModel._metaData['OrderId']
                # 找到大于orderId并最接近orderId的值
                if orderModel._metaData['OrderId'] < minOrderId:
                    minOrderId = orderModel._metaData['OrderId']

        return minOrderId

    def getALatestFilledTime(self, contNo, userNo):
        # 默认usrNo为空字符串（''），此时取当前用户
        if not userNo:
            userNo = self._selectedUserNo
            
        if userNo not in self._userInfo:
            raise Exception("请先在极星客户端登录您的交易账号")

        tUserInfoModel = self._userInfo[userNo]
        latestTime = -1
        for orderId in list(tUserInfoModel._order.keys()):
            tOrderModel = tUserInfoModel._order[orderId]
            if not contNo or tOrderModel._metaData['Cont'] == contNo:
                if tOrderModel._metaData['OrderState'] == osFilled:
                    updateTime = tOrderModel._metaData['UpdateTime']
                    struct_time = time.strptime(updateTime, "%Y-%m-%d %H:%M:%S")
                    timeStamp = time.strftime("%Y%m%d.%H%M%S", struct_time)
                    if float(timeStamp) > latestTime:
                        latestTime = float(timeStamp)
        return latestTime

