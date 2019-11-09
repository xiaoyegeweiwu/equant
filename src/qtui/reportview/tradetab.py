import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


HEADERS = [
    "时间",
    "合约",
    "交易类型",
    "下单类型",
    "成交数量",
    "成交价",
    "成交额",
    "委托数量",
    "平仓盈亏",
    "手续费",
    "滑点损耗"
]


def formatOrderTime(klineType, order):
    """格式化订单数据"""
    t = str(order['DateTimeStamp'])

    if klineType['KLineType'] == 'D':
        time = t[0:8]

    elif klineType["KLineType"] == 'M':
        time = t[0:8] + " " + t[8:10] + ":" + t[10:12]

    elif klineType["KLineType"] == "T":
        time = t[0:8] + " " + t[8:10] + ":" + t[10:12] + ":" + t[12:14] + '.' + t[-3:]

    else:
        time = t

    return time


class BaseCell(QTableWidgetItem):
    def __init__(self, content):
        super(BaseCell, self).__init__()
        self.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setContent(content)

    def setContent(self, content):
        self.setText(str(content))


class TradeTab(QTableWidget):

    def __init__(self, orders, kLineInfo, parent=None):
        super().__init__(parent)
        self._orders = orders
        self._kLineInfo = kLineInfo
        self.initStage()

    def initStage(self):
        self.setColumnCount(len(HEADERS))

        self.setHorizontalHeaderLabels(HEADERS)
        self.horizontalHeader().setSectionsMovable(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setShowGrid(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.horizontalHeader().setFixedHeight(25)

        # 去除边框
        self.setFrameShape(QFrame.NoFrame)

        self.verticalHeader().setVisible(False)

        # -----------增加trade数据---------------
        self.addTradeDatas(self._orders)

    def addTradeDatas(self, orders):
        self.setRowCount(len(orders))
        for eo, row in zip(orders, range(self.columnCount())):
            time = formatOrderTime(self._kLineInfo, eo["Order"])
            direct = eo["Order"]["Direct"]
            offset = eo["Order"]["Offset"]
            cont = eo["Order"]["Cont"]
            tradeType = direct + offset
            orderType = eo["Order"]["OrderPrice"]
            orderQty = eo['Order']['OrderQty']
            orderPrice = '{:.2f}'.format(float(eo['Order']['OrderPrice']))
            turnover =  '{:.1f}'.format(float(eo['Turnover']))
            liqProfit = '{:.1f}'.format(float(eo['LiquidateProfit']))
            cost = '{:.1f}'.format(float(eo['Cost']))
            slippage = '{:.1f}'.format(float(eo["SlippageLoss"]))
            contents = [time, cont, tradeType, orderType, orderQty, orderPrice, turnover, orderQty, liqProfit, cost, slippage]
            for index, content in enumerate(contents):
                cell = BaseCell(content)
                self.setItem(row, index, cell)




