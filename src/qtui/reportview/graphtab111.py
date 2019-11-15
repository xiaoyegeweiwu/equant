from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore
from functools import partial


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


GRAPHTYPE = {
    "Equity"      : "柱状图",
    "NetProfit"   : "立体",
    "Returns"     : "立体",
    "WinRate"     : "柱状图",
    "MeanReturns" : "柱状图",
    "IncSpeed"    : "立体"
}


# class DirTree(QTreeWidget):
#
#     def __init__(self, parent=None):
#         super(DirTree, self).__init__(parent)
#         self._parent = parent
#
#         self._graphDatas = None
#
#         self.setColumnCount(1)
#         self.setHeaderHidden(True)
#         self._addTreeItem()
#         self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
#         self.setColumnWidth(0, 50)
#         self.setFixedWidth(140)
#         self._initPlotWidget()
#
#     def _initPlotWidget(self):
#         self.stringaxis = pg.AxisItem(orientation='bottom')
#         self.mYAxis = pg.AxisItem(orientation='left')
#         self.pw = pg.PlotWidget(name="master", axisItem={'bottom': self.stringaxis, 'left': self.mYAxis},
#                                 enableMenu=False, border=(150, 150, 150))
#         self.pw.showGrid(x=True, y=True)
#         # self.pw.setLimits(xMin=0, xMax=-1, yMin=0, yMax=-1)
#
#         self.pw.getAxis('left').setWidth(60)
#         self.pw.getAxis('left').setStyle(tickFont=QFont("Roman times", 10, QFont.Bold))
#         self.pw.getAxis('left').setPen(color=(255, 255, 255, 255), width=0.8)
#         self.pw.hideButtons()
#
#     def _addTreeItem(self):
#         for key in DIR.keys():
#             root = QTreeWidgetItem(self)
#             root.setText(0, key)
#             for item in DIR[key]:
#                 child = QTreeWidgetItem(root)
#                 child.setText(0, item[0])  # 设置文本
#                 child.setText(1, item[1])
#
#             self.addTopLevelItem(root)
#
#         self.itemClicked.connect(self.itemClickedCallback)
#
#     def getPlotData(self, key, tag):
#         x, y = [], []
#         for sd in self._graphDatas[key]:
#             x.append(sd.get('Time'))
#             y.append(sd.get(tag))
#         return x, y
#
#     def itemClickedCallback(self, item):
#         if item.parent():
#             rootKey = item.parent().text(0)
#             key = item.text(0)
#             flag = item.text(1)
#             x, y = self.getPlotData(rootKey, flag)
#
#             self.pw.plot(title="testing")
#             self.pw.clear()
#             self.pw.plot(x, y)
#
#     def setInitialGraph(self, data):
#         self._graphDatas = data
#         self.pw.clear()
#         x, y = self.getPlotData("年度分析", 'Equity')
#
#         self.pw.plot(x, y)
#         self._parent.layout().addWidget(self.pw)
#
#     def showGraphDatas(self, datas):
#         self._graphDatas = datas
#         self.pw.clear()
#         x, y = self.getPlotData("年度分析", 'Equity')
#
#         self.pw.plot(x, y)
#         self._parent.layout().addWidget(self.pw)


class DirTree(QTreeWidget):

    def __init__(self, graph, parent=None):
        super(DirTree, self).__init__(parent)
        self._parent = parent

        self._graph = graph
        self._graphDatas = None

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self._addTreeItem()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setColumnWidth(0, 50)
        self.setFixedWidth(140)

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

            self._graph.plot(title="testing")
            # self._graph.clear()
            self._graph.loadData(y)

    def setInitialGraph(self, data):
        self._graphDatas = data
        # self._graph.clear()
        x, y = self.getPlotData("年度分析", 'Equity')

        self._graph.loadData(y)
        self._parent.layout().addWidget(self._graph)

    def showGraphDatas(self, datas):
        self._graphDatas = datas
        # self._graph.clear()
        x, y = self.getPlotData("年度分析", 'Equity')

        self._graph.loadData(y)
        self._parent.layout().addWidget(self._graph)


class BarGraph(pg.GraphicsObject):
    """柱状图"""
    def __init__(self, datas):
        super(BarGraph, self).__init__()
        self.data = datas
        self.generatePicture(self.data)

    def generatePicture(self, datas=None):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = 0.4
        for i, data in enumerate(datas):
            if data >= 0:
                p.setPen(pg.mkPen('r'))
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setPen(pg.mkPen('g'))
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QtCore.QRectF(i-w, 0, w * 2, data))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


class GraphWidget(KeyWraper):

    def __init__(self, parent=None):
        super(GraphWidget, self).__init__(parent)
        self.parent = parent
        self.name = None

        self.countK = 60

        self.initUI()

    def initUI(self):
        """初始化图表控件"""
        self.pw = pg.PlotWidget()
        self.layGraph = pg.GraphicsLayout(border=(100, 100, 100))
        self.layGraph.setContentsMargins(10, 10, 10, 10)
        self.layGraph.setSpacing(0)
        self.layGraph.setBorder(color=(255, 255, 255, 255), width=0.8)
        self.layGraph.setZValue(0)
        self.layGraph.setMinimumHeight(140)
        # self.gTitle = self.layGraph.addLabel(u"")
        self.pw.setCentralWidget(self.layGraph)

        # 设置横坐标
        xdict = {}
        self.axisTime = MyStringAxis(xdict, orientation='bottom')
        # 初始化图
        self.initGraph()

        self.vb = QVBoxLayout()
        self.vb.addWidget(self.pw)
        self.setLayout(self.vb)

    def makeBarPI(self, name):
        """plotItem 对象"""
        vb = CustomViewBox(self)
        #TODO: 作用？？
        barItem = pg.PlotItem(viewBox=vb, name=name, axisItems={'bottom': self.axisTime})
        barItem.setMenuEnabled(False)
        barItem.setClipToView(True)
        barItem.setDownsampling(mode='peak')
        barItem.setRange(xRange=(0, 1), yRange=(0, 1))
        barItem.getAxis('left').setWidth(60)
        barItem.getAxis('left').setStyle(tickFont=QFont("Roman times", 10, QFont.Bold))
        barItem.getAxis('left').setPen(color=(255, 255, 255, 255), width=0.8)
        barItem.showGrid(True, True)
        barItem.hideButtons()

        return barItem

    def initGraph(self):
        self.pwBar = self.makeBarPI("Testing")
        self.barGraph = BarGraph([1, 2, 3, 4, 5, 4, 3, 2, 1])
        self.pwBar.setMaximumHeight((self.rect().height() - 30) / 4)
        self.pwBar.setMinimumHeight(20)

        self.layGraph.nextRow()
        self.layGraph.addItem(self.pwBar)

    def plotBar(self, xmin=0, xmax=-1):
        print("AAAA: ", self.datas)
        self.barGraph.setData(self.datas[xmin:xmax] + [0], name="Bar")

    def updateGraph(self):
        #TODO:
        datas = self.datas
        self.pwBar.update()

        def update(view, low, high):
            vRange = view.viewRange()
            xmin = max(0, int(vRange[0][0]))
            xmax = max(0, int(vRange[0][1]))
            xmax = min(xmax, len(datas))
            if len(datas) > 0 and xmax > xmin:
                ymin = min(datas[xmin:xmax][low])
                ymax = max(datas[xmin:xmax][high])
                if  ymin and ymax:
                   view.setRange(yRange=(ymin, ymax))
            else:
                view.setRange(yRange=(0, 1))

        update(self.pwBar.getViewBox(), 'a', 'b')

    def plotAll(self, redraw=True, xMin=0, xMax=-1):
        if redraw:
            xmax = len(self.datas) if xMax < 0 else xMax
            xmin = max(0, xmax - self.countK)
            self.index = int((xmax + xmin) / 2)

        self.pwBar.setLimits(xMin=xMin, xMax=xMax)
        self.plotBar(xMin, xMax)
        self.refresh()

    def refresh(self):
        datas = self.datas
        minutes = int(self)
        xmin = max(0, self.indexe - minutes)
        xmax = xmin + 2 * minutes

        self.pwBar.setRange(xRange=(xmin, xmax))

    def onPaint(self):
        """界面刷新回调"""
        view = self.pwBar.getViewBox()
        vRange = view.viewRange()

    def resignData(self, datas):
        #TODO:
        # self.crosshair.datas = datas
        def viewXRangeChanged(low, high, self):
            vRange = self.viewRange()
            xmin = max(0, int(vRange[0][0]))
            xmax = max(0, int(vRange[0][1]))
            xmax = min(xmax, len(datas))
            if len(datas) > 0 and xmax > xmin:
                ymin = min(datas[xmin:xmax])
                ymax = max(datas[xmin:xmax])
                if ymin and ymax:
                   self.setRange(yRange=(ymin, ymax))
            else:
                self.setRange(yRange=(0, 1))

        view = self.pwBar.getViewBox()
        view.sigXRangeChanged.connect(partial(viewXRangeChanged, 'low', 'high'))

    def loadData(self, datas):
        """载入数据"""
        self.index = 0

        self.datas = datas

        self.axisTime.xdict = {}
        xdict = dict(enumerate(datas))
        self.axisTime.update_xdict(xdict)
        self.resignData(self.datas)

        self.plotAll(True, 0, len(self.datas))



class GraphTab(QWidget):

    def __init__(self, parent=None):
        super(GraphTab, self).__init__(parent)

        self._initUI()

    def _initUI(self):
        qLayout = QHBoxLayout()
        qLayout.setContentsMargins(0, 0, 0, 0)

        self.graph = GraphWidget(self)
        self.dir = DirTree(self.graph, self)

        qLayout.addWidget(self.dir,  0, Qt.AlignLeft)
        qLayout.addWidget(self.graph, 0, Qt.AlignRight)
        self.setLayout(qLayout)

    def addGraphDatas(self, datas):
        self.dir.showGraphDatas(datas)
