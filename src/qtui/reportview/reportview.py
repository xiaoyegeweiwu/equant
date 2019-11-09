import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from dir import Dir
from tab import Tab
from commonhelper import CommonHelper


class ReportView(QWidget):

    def __init__(self):
        super(ReportView, self).__init__()
        self._windowTitle = "回测报告"
        self._objName = "Report"
        self._iconPath = r"./epolestar ix0.ico"
        self.styleFile = r"./style.qss"

        self.setWindowTitle(self._windowTitle)
        self.setWindowIcon(QIcon(self._iconPath))
        self.resize(1000, 600)
        self.setMinimumSize(600, 600)
        self.setMaximumSize(1000, 600)
        self.setObjectName(self._objName)

        self._initUI()

    def _initUI(self):
        style = CommonHelper.readQss(self.styleFile)
        self.setStyleSheet(style)

        vLayout = QHBoxLayout()
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)

        dir = Dir()
        tab = Tab()
        vLayout.addSpacing(0)
        vLayout.addWidget(dir)
        vLayout.setSpacing(1)
        vLayout.addWidget(tab)
        vLayout.setSpacing(2)

        self.setLayout(vLayout)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ReportView()
    win.show()
    sys.exit(app.exec_())
