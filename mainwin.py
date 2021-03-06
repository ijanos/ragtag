#-*- coding: utf-8 -*-

import sys
import logging

# Use the new, more pythonic PyQt4 API
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore
from PyQt4 import QtGui

from widgets.taglistwidget import TaglistPanel
from widgets.tagbar import Tagbar
from widgets.thumbnails import Thumbnails
from widgets.control import Controller


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Expanding)

        self.control = Controller()

        self.centralWidget = CentralWidget(self.control)
        self.setCentralWidget(self.centralWidget)

        self.createActions()
        self.createMenus()

        self.control.start()

    def createActions(self):
        self.exitAct = QtGui.QAction("E&xit", self)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.setStatusTip("Exit the application")
        self.connect(self.exitAct, QtCore.SIGNAL("triggered()"),
                     self, QtCore.SLOT("close()"))

        self.openDBAct = QtGui.QAction("&Open database...", self)
        self.openDBAct.setShortcut("Ctrl+O")
        self.openDBAct.setStatusTip("Open a database file")
        self.connect(self.openDBAct, QtCore.SIGNAL("triggered()"),
                     self.control.loadDB)

        self.actionSortByAlpha = QtGui.QAction("Sort tags alphabetically", self)
        self.actionSortByAlpha.setCheckable(True)
        self.connect(self.actionSortByAlpha, QtCore.SIGNAL("triggered()"),
                        self.centralWidget.taglist.sortModeChanged)

        self.actionOpenWith = QtGui.QAction("Open with...", self)

        self.actionCopyImagePath = QtGui.QAction("Copy image path", self)
        self.actionCopyImagePath.setShortcut("Ctrl+C")

        self.actionAbout = QtGui.QAction("About", self)
        self.actionAbout.setStatusTip("Show an about box.")
        self.connect(self.actionAbout, QtCore.SIGNAL("activated()"),
                     self.slotAbout)

        self.actionAboutQt = QtGui.QAction("About &Qt", self)
        self.actionAboutQt.setStatusTip("Show an about box for Qt.")
        self.connect(self.actionAboutQt, QtCore.SIGNAL("activated()"),
                     self.slotAboutQt)

    def createMenus(self):
        # File menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openDBAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        # Edit menu
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.actionOpenWith)
        self.editMenu.addAction(self.actionCopyImagePath)
        self.editMenu.addAction(self.actionSortByAlpha)


        # Help menu
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actionAboutQt)
        self.helpMenu.addAction(self.actionAbout)

    def slotAbout(self):
        QtGui.QMessageBox.about(self,
                            "ragtag",
                            "<h1>Ragtag</h1>"
                            "A simple, tag-based image collection browser<br/>"
                            "<a href='https://github.com/ijanos/ragtag'>"
                            "https://github.com/ijanos/ragtag</a>")

    def slotAboutQt(self):
        QtGui.QMessageBox.aboutQt(self)

    def sizeHint(self):
        return QtCore.QSize(1900,700)


class CentralWidget(QtGui.QWidget):
    def __init__(self, ctrl, parent=None):
        QtGui.QWidget.__init__(self, parent)

        #Create widgets&layouts
        mainLayout = QtGui.QHBoxLayout()
        rightPanelLayout = QtGui.QVBoxLayout()

        mainLayout.setContentsMargins(0,0,0,0)
        rightPanelLayout.setContentsMargins(0,0,0,0)

        splitter = QtGui.QSplitter()

        rightPanelWidget = QtGui.QWidget()

        self.taglist = TaglistPanel()
        tagbar = Tagbar()
        thumbview = Thumbnails()

        #Connect signals
        self.connect(self.taglist._tagview, QtCore.SIGNAL('tagClicked'),
                     ctrl.tagClicked)

        self.connect(ctrl, QtCore.SIGNAL('updateTags'),
                     self.taglist.setTaglist)
        self.connect(ctrl, QtCore.SIGNAL('addPhotos'),
                     thumbview.addImages)
        self.connect(ctrl, QtCore.SIGNAL('addTag'),
                     tagbar.addTag)
        self.connect(tagbar, QtCore.SIGNAL('tagRemoved'),
                     ctrl.tagRemoved)

        self.connect(tagbar, QtCore.SIGNAL('clearTags'),
                     ctrl.reset)
        self.connect(tagbar, QtCore.SIGNAL('clearTags'),
                     thumbview.clearWidget)

        #Add widgets to layouts
        rightPanelWidget.setLayout(rightPanelLayout)

        splitter.addWidget(self.taglist)
        splitter.addWidget(rightPanelWidget)

        mainLayout.addWidget(splitter)

        rightPanelLayout.addWidget(tagbar)
        rightPanelLayout.addWidget(thumbview)

        self.setLayout(mainLayout)

        #Start the application

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
    sys.exit()
