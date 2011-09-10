#-*- coding: utf-8 -*-

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Controller(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QHBoxLayout()

        txt = QLabel("Hello World")

        bLoad = QPushButton("Load images")
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

        self.setLayout(layout)
