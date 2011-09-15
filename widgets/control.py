#-*- coding: utf-8 -*-

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from managedb import PhotoDB

class Controller(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.photoDB = None

        layout = QHBoxLayout()

        txt = QLabel("Hello World")

        bLoad = QPushButton("Load database")
        bTags = QPushButton("Load tags")
        bReset = QPushButton("reset")
        bQuit = QPushButton("Quit")

        layout.addWidget(txt)
        layout.addWidget(bLoad)
        layout.addWidget(bTags)
        layout.addWidget(bReset)
        layout.addWidget(bQuit)

        self.connect(bQuit, SIGNAL('clicked()'),
                     QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(bLoad, SIGNAL('clicked()'), self.loadDB)
        self.connect(bTags, SIGNAL('clicked()'), self.loadTags)

        self.setLayout(layout)

    def loadDB(self):
        filename = QFileDialog.getOpenFileName()
        self.photoDB = PhotoDB(str(filename))

    def loadTags(self):
        taglist = self.photoDB.getTaglist()
        self.emit(SIGNAL("updateTags"), taglist)


