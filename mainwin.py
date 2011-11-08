#-*- coding: utf-8 -*-

import sys
import logging

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from widgets.taglistwidget import TaglistPanel
from widgets.tagbar import Tagbar
from widgets.thumbnails import Thumbnails
from widgets.control import Controller


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.control = Controller()

        centralWidget = CentralWidget(self.control)
        self.setCentralWidget(centralWidget)

        self.createActions()
        self.createMenus()

        self.control.start()

    def createActions(self):
        self.exitAct = QAction("E&xit", self)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.setStatusTip("Exit the application")
        self.connect(self.exitAct,
                SIGNAL("triggered()"), self, SLOT("close()"))

        self.openDBAct = QAction("&Open database...", self)
        self.openDBAct.setShortcut("Ctrl+O")
        self.openDBAct.setStatusTip("Open a database file")
        self.connect(self.openDBAct,
                SIGNAL("triggered()"), self.control.loadDB)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openDBAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

class CentralWidget(QFrame):
    def __init__(self, ctrl, parent=None):
        QFrame.__init__(self, parent)

        self.setContentsMargins(0, 0, 0, 0)

        #Create widgets&layouts
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        splitter = QSplitter()
        vboxw = QWidget()

        taglist = TaglistPanel()
        tagbar = Tagbar()
        thumbview = Thumbnails()

        #Connect signals
        self.connect(taglist._tagview, SIGNAL('tagClicked'), ctrl.tagClicked)

        self.connect(ctrl, SIGNAL('updateTags'), taglist.setTaglist)
        self.connect(ctrl, SIGNAL('addPhotos'), thumbview.addImages)
        self.connect(ctrl, SIGNAL('addTag'), tagbar.addTag)
        self.connect(tagbar, SIGNAL('tagRemoved'), ctrl.tagRemoved)

        self.connect(tagbar, SIGNAL('clearTags'), ctrl.reset)
        self.connect(tagbar, SIGNAL('clearTags'), thumbview.clearWidget)

        #Add widgets to layouts
        vboxw.setLayout(vbox)

        splitter.addWidget(taglist)
        splitter.addWidget(vboxw)

        hbox.addWidget(splitter)

        vbox.addWidget(tagbar)
        vbox.addWidget(thumbview)

        self.setLayout(hbox)

        #Start the application

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
    sys.exit()
