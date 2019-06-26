from collections import defaultdict
from capi.com_types import *


class LimitCtl(object):

    def __init__(self, maxConOpenTimes, maxKLineOpenTime, openNotReverse, coverNotOpen):

        # 限制
        self._maxConOpenTime   = maxConOpenTimes      # 最大连续同向开仓次数
        self._maxKLineOpenTime = maxKLineOpenTime     # 最大每根K线同向开仓次数
        self._openNotReverse   = openNotReverse       # 开仓的当前K线不允许平仓
        self._coverNotOpen     = coverNotOpen         # 平仓的当前K线不允许开仓

        # self._conOpen          = defaultdict(int)   # 连续同向开仓次数(多合约字典)
        self._conOpen          = 0                    # 连续同向开仓次数

        self._kLineOpenTime    = 0                    # 每根K线同向开仓次数

        self._hasCover         = False                # 当前K线是否有平仓单
        self._hasOpen          = False                # 当前K线是否有开仓单

        self._curBarIndex      = 0                    # 当前bar序号


    def _setCurBarIndex(self, index):
        if index == self._curBarIndex:
            return
        self._curBarIndex = index

    def _allowConOpen(self, order, lastOrder):
        """
        判断是否满足连续同向开仓次数限制，连续同向开仓次数是对策略限制的
        :param order: 订单
        :param lastOrder: 前一个订单
        :return: 1：订单满足限制条件   -1： 订单不满足限制条件
        """
        # TODO：暂时没有考虑外盘(外盘通过订单无法判断)
        if self._maxConOpenTime == -1:
            return 1  #  连续开仓次数不做限制

        if len(lastOrder) < 1:
            if order["Offset"] == oOpen or order["Offset"] == oNone:
                self._conOpen += 1

            return 1

        if order["Offset"] == oOpen or order["Offset"] == oNone:   # 开仓单或外盘订单
            if lastOrder["Direct"] == order["Direct"] and \
                    lastOrder["Offset"] == order["Offset"]:  # 订单方向相同
                if self._conOpen >= self._maxConOpenTime:
                    # self._conOpen[order["Cont"]] = 1
                    return -1   # 大于同向开仓次数限制
                else:
                    self._conOpen += 1
                    return 1  # 不大于同向开仓次数限制
            else:
                self._conOpen = 0
                return 1  # 不同向

        else:
            self._conOpen = 0
            return 1  # 小于同向开仓次数限制

    def _allowCurBarOpen(self, order, lastOrder):
        """
        每根K线同向开仓次数是否满足条件
        :param order: 订单
        :param lastOrder: 前一个订单
        :return: 1：订单满足限制条件   -1： 订单不满足限制条件
        """
        # TODO：暂时没有考虑外盘
        if self._maxKLineOpenTime == -1:
            return 1   # 每根K线同向开仓次数不做限制

        if len(lastOrder) < 1:
            if order["Offset"] == oOpen or order["Offset"] == oNone:
                self._kLineOpenTime += 1
            return 1

        if order["CurBarIndex"] == self._curBarIndex:
            if order["Offset"] == oOpen or order["Offset"] == oNone:  # 开仓单
                if lastOrder["Direct"] == order["Direct"] and \
                        lastOrder["Offset"] == order["Offset"]:  # 订单方向相同
                    if self._kLineOpenTime >= self._maxKLineOpenTime:
                        return -1
                    else:
                        self._kLineOpenTime += 1
                        return 1
                else:   # 开仓不同向
                    self._kLineOpenTime = 1
                    return 1
            else:      # 不是开仓单
                return 1

        else:
            if order["Direct"] == oOpen or order["Direct"] == oNone:
                self._kLineOpenTime = 1
                return 1
            else:
                self._kLineOpenTime = 0
                return 1

    def _allowCover(self, order):
        """
        开仓的当前K线是否可以平仓判断
        :param order: 订单
        :return:  1：订单满足限制条件   -1： 订单不满足限制条件
        """
        # TODO：暂时没有考虑外盘
        if self._openNotReverse == 0:
            return 1   # 不做限制

        if order["CurBarIndex"] == self._curBarIndex:
            if self._hasOpen:
                if order["Offset"] == oCover:
                    return -1
                else:
                    return 1
            else:
                if order["Offset"] == oOpen:
                    self._hasOpen = True
                    return 1
                else:
                    return 1

        else:
            if order["Offset"] == oOpen:
                self._hasOpen = True
                return 1
            else:
                self._hasOpen = False
                return 1

    def _allowOpen(self, order):
        """
        平仓的当前K线是否可以开仓判断
        :param order: 订单
        :return:  1：订单满足限制条件   -1： 订单不满足限制条件
        """
        # TODO：暂时没有考虑外盘
        if self._coverNotOpen == 0:
            return 1   # 不做限制

        if order["CurBarIndex"] == self._curBarIndex:
            if self._hasCover:     # 当前K线存在平仓单
                if order["Offset"] == oOpen:
                    return -1
                else:
                    return 1
            else:                                # 当前K线不存在平仓单
                if order["Offset"] == oCover:
                    self._hasCover = True
                    return 1
                else:
                    return 1

        else:
            if order["Offset"] == oCover:
                self._hasCover = True
                return 1
            else:
                self._hasCover = False
                return 1

    def allowOrder(self, order, lastOrder):
        """
        判断是否可以下单
        :param order:
        :param lastOrder:
        :return: 0: 可以下单， -1: 不能下单
        """

        ret1 = self._allowConOpen(order, lastOrder)
        ret2 = self._allowCurBarOpen(order, lastOrder)
        ret3 = self._allowCover(order)
        ret4 = self._allowOpen(order)

        self._setCurBarIndex(order["CurBarIndex"])

        if ret1 == 1 and ret2 == 1 and ret3 == 1 and ret4 == 1:
            return 1
        else:
            return 0








