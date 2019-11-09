import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class FileSystemModel(QFileSystemModel):
    """Overwrite columnCount"""
    def columnCount(self, parent: QModelIndex = ...):
        return 1


class Dir(QTreeView):
    """The directory of report data"""
    def __init__(self):
        super(Dir, self).__init__()
        self._dirPath = r"./reportdata"
        self._initUI()
        self.setHeaderHidden(True)
        self.sizeHint()

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setMaximumWidth(200)

    def _initUI(self):
        self.model = FileSystemModel()
        self.model.setRootPath(self._dirPath)

        self.setAnimated(False)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

        self.setModel(self.model)
        # 需要加上这句setRootPath才生效
        self.setRootIndex(self.model.index(self._dirPath))
