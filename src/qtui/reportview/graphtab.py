from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg

from qtui.reportview.fundtab import KeyWraper, MyStringAxis, CustomViewBox


DIR = {
    "年度分析": [["年度权益", "Equity"], ["年度净利润", "NetProfit"], ["年度盈利率", "Returns"],
             ["年度胜率", "WinRate"], ["年度平均盈亏", "MeanReturns"], ["年度权益增长", "IncSpeed"]],
    "季度分析": [["季度权益", "Equity"], ["季度净利润", "NetProfit"], ["季度盈利率", "Returns"],
             ["季度胜率", "WinRate"], ["季度平均盈亏", "MeanReturns"], ["季度权益增长", "IncSpeed"]],
    "月度分析": [["月度权益", "Equity"], ["月度净利润", "NetProfit"], ["月度盈利率", "Returns"],
             ["月度胜率", "WinRate"], ["月度平均盈亏", "MeanReturns"], ["月度权益增长", "IncSpeed"]],
    "周分析"  : [["周权益", "Equity"], ["周净利润", "NetProfit"], ["周盈利率", "Returns"],
              ["周胜率", "WinRate"], ["周平均盈亏", "MeanReturns"], ["周权益增长", "IncSpeed"]],
    "日分析"  : [["日权益", "Equity"], ["日净利润", "NetProfit"], ["日盈利率", "Returns"],
              ["日胜率", "WinRate"], ["日平均盈亏", "MeanReturns"], ["日权益增长", "IncSpeed"]]
}


class DirTree(QTreeWidget):

    def __init__(self, parent=None):
        super(DirTree, self).__init__(parent)
        self._parent = parent

        self._graphDatas = None

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self._addTreeItem()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setColumnWidth(0, 50)
        self.setFixedWidth(140)
        self._initPlotWidget()

    def _initPlotWidget(self):
        self.stringaxis = pg.AxisItem(orientation='bottom')
        self.mYAxis = pg.AxisItem(orientation='left')
        self.pw = pg.PlotWidget(name="master", axisItem={'bottom': self.stringaxis, 'left': self.mYAxis},
                                enableMenu=False, border=(150, 150, 150))
        self.pw.showGrid(x=True, y=True)
        self.pw.setLimits(xMin=0, xMax=-1, yMin=0, yMax=-1)

    def _addTreeItem(self):
        for key in DIR.keys():
            root = QTreeWidgetItem(self)
            root.setText(0, key)
            for item in DIR[key]:
                child = QTreeWidgetItem(root)
                child.setText(0, item[0])  # 设置文本
                child.setText(1, item[1])

            self.addTopLevelItem(root)

        self.itemClicked.connect(self.itemClickedCallback)

    def getPlotData(self, key, tag):
        x, y = [], []
        for sd in self._graphDatas[key]:
            x.append(sd.get('Time'))
            y.append(sd.get(tag))
        return x, y

    def itemClickedCallback(self, item):
        if item.parent():
            rootKey = item.parent().text(0)
            key = item.text(0)
            flag = item.text(1)
            x, y = self.getPlotData(rootKey, flag)

            self.pw.plot(title="testing")
            self.pw.clear()
            self.pw.plot(x, y)

    def setInitialGraph(self, data):
        self._graphDatas = data
        self.pw.clear()
        x, y = self.getPlotData("年度分析", 'Equity')

        self.pw.plot(x, y)
        self._parent.layout().addWidget(self.pw)

    def showGraphDatas(self, datas):
        self._graphDatas = datas
        self.pw.clear()
        x, y = self.getPlotData("年度分析", 'Equity')

        self.pw.plot(x, y)
        self._parent.layout().addWidget(self.pw)


class GraphTab(KeyWraper):

    def __init__(self, parent=None):
        super(GraphTab, self).__init__(parent)

        self._initUI()

    def _initUI(self):
        qLayout = QHBoxLayout()
        qLayout.setContentsMargins(0, 0, 0, 0)
        self.dir = DirTree(self)
        qLayout.addWidget(self.dir,  0, Qt.AlignLeft)
        self.setLayout(qLayout)

    def addGraphDatas(self, datas):
        self.dir.showGraphDatas(datas)
