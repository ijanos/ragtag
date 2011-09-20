#-*- coding: utf-8 -*-

import sys
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from widgets.taglistwidget import TaglistPanel
from widgets.tagbar import Tagbar
from widgets.thumbnails import Thumbnails
from widgets.control import Controller

class MainWindow(QFrame):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()


        taglist = TaglistPanel()
        tagbar = Tagbar()
        thumbview = Thumbnails()

        ctrl = Controller()

        self.connect(taglist._tagview, SIGNAL('tagClicked'), ctrl.tagClicked)

        self.connect(ctrl, SIGNAL('updateTags'), taglist.setTaglist)
        self.connect(ctrl, SIGNAL('addPhotos'), thumbview.addImages)
        self.connect(ctrl, SIGNAL('addTag'), tagbar.addTag)
        self.connect(tagbar, SIGNAL('tagRemoved'), ctrl.tagRemoved)

        self.connect(tagbar, SIGNAL('clearTags'), ctrl.reset)
        self.connect(tagbar, SIGNAL('clearTags'), thumbview.clearWidget)

        splitter = QSplitter()
        vboxw = QWidget()
        vboxw.setLayout(vbox)

        splitter.addWidget(taglist)
        splitter.addWidget(vboxw)

        hbox.addWidget(splitter)

        vbox.addWidget(ctrl)

        vbox.addWidget(tagbar)
        vbox.addWidget(thumbview)

        self.setLayout(hbox)

        ctrl.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
    sys.exit()
