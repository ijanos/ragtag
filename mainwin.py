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
        centralWidget = CentralWidget()
        self.setCentralWidget(centralWidget)


class CentralWidget(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        #Create widgets&layouts
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        splitter = QSplitter()
        vboxw = QWidget()

        taglist = TaglistPanel()
        tagbar = Tagbar()
        thumbview = Thumbnails()

        ctrl = Controller()

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

        vbox.addWidget(ctrl)

        vbox.addWidget(tagbar)
        vbox.addWidget(thumbview)

        self.setLayout(hbox)

        #Start the application
        ctrl.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
    sys.exit()
