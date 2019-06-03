from capi.com_types import *


class LimitCtl(object):

    def __init__(self, maxConOpenTimes, maxKLineOpenTime, openNotReverse, coverNotOpen):

        # 限制
        self._maxConOpenTime   = maxConOpenTimes      # 最大连续同向开仓次数
        self._maxKLineOpenTime = maxKLineOpenTime     # 最大每根K线同向开仓次数
        self._openNotReverse   = openNotReverse       # 开仓的当前K线不允许平仓
        self._coverNotOpen     = coverNotOpen         # 平仓的当前K线不允许开仓

        self._conOpen          = 0                    # 连续同向开仓次数
        self._kLineOpenTime    = {
            "BuyOpen"  : 0,       #
            "SellOpen" : 0,
            "Open"     : 0,
            "Sell"     : 0,
        }                                            # 每根K线同向开仓次数
        self._hasCover       = False                 # 当前K线是否有平仓单
        self._hasOpen        = False                 # 当前K线是否有开仓单

        self._curBarIndex      = 0                   # 当前bar序号

    def _initKLineOpenTime(self):
        """初始化每根K线同向开仓次数"""
        self._kLineOpenTime = {
            "BuyOpen": 0,
            "SellOpen": 0,
            "Open": 0,
            "Sell": 0,
        }

    def conOpen(self, order, lastOrder):
        """
        判断是否满足连续开仓次数限制
        :param order: 订单
        :param lastOrder: 前一个订单
        :return: 1：订单满足限制条件   -1： 订单不满足限制条件
        """
        # TODO：暂时没有考虑外盘
        if self._maxConOpenTime == -1:
            return 1  #  连续开仓次数不做限制

        if order["Offset"] == oOpen or order["Offset"] == oNone:   # 开仓单或外盘订单
            if lastOrder["Direct"] == order["Direct"] and \
                    lastOrder["Offset"] == order["Offset"]:  # 订单方向相同
                if self._conOpen > self._maxConOpenTime:
                    self._conOpen = 1
                    return -1   # 大于同向开仓次数限制
                else:
                    self._conOpen += 1
                    return 1  # 不大于同向开仓次数限制

        else:
            self._conOpen = 0
            return 1  # 小于同向开仓次数限制

    def CurBarOpen(self, order):
        """
        每根K线同向开仓次数是否满足条件
        :param order: 订单
        :return: 1：订单满足限制条件   -1： 订单不满足限制条件
        """
        # TODO：暂时没有考虑外盘
        if self._maxKLineOpenTime == -1:
            return 1   # 每根K线同向开仓次数不做限制

        if order["CurBarIndex"] == self._curBarIndex:
            if order["Direct"] == dBuy and order["Offset"] == oOpen:  # 买开
                if self._kLineOpenTime["BuyOpen"] > self._maxKLineOpenTime:
                    return -1    # 大于每根K线连续同向开仓次数限制
                else:
                    self._kLineOpenTime["BuyOpen"] += 1
                    return 1     # 订单不大于每根K线连续开仓次数限制

            elif order["Direct"] == dSell and order["Offset"] == oOpen:  # 卖开
                if self._kLineOpenTime["SellOpen"] > self._maxKLineOpenTime:
                    return -1
                else:
                    self._kLineOpenTime["SellOpen"] += 1
                    return 1

            elif order["Direct"] == dBuy and order["Offset"] == oNone:  # 买
                if self._kLineOpenTime["Buy"] > self._maxKLineOpenTime:
                    return -1
                else:
                    self._kLineOpenTime["Buy"] += 1
                    return 1

            elif order["Direct"] == dSell and order["Offset"] == oNone:  # 卖
                if self._kLineOpenTime["Sell"] > self._maxKLineOpenTime:
                    return -1
                else:
                    self._kLineOpenTime["Sell"] += 1
                    return 1

            else:                                                        # 平仓单
                return 1

        else:
            self._curBarIndex = order["CurBarIndex"]
            self._initKLineOpenTime()
            return 1

    def allowCover(self, order):
        """
        开仓的当前K线是否可以平仓判断
        :param order: 订单
        :return:  1：订单满足限制条件   -1： 订单不满足限制条件
        """
        # TODO：暂时没有考虑外盘
        if self._openNotReverse == 0:
            return 1   # 不做限制

        if order["CurBarIndex"] == self._curBarIndex:
            pass
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
                self.hasOpen = True
                return 1
            else:
                return 1

    def allowOpen(self, order):
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

        else:
            if order["Offset"] == oCover:
                self.hasCover = True
                return 1
            else:
                return 1







