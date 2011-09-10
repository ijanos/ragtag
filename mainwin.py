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

        tagbar.addTag("kutya")
        tagbar.addTag("cica")
        tagbar.addTag(u"akármi")
        tagbar.addTag(u"árvíz")
        tagbar.addTag(u"tűrő")
        tagbar.addTag(u"foobar")
        for x in xrange(0,20):
            thumbview.addImage('pic/nestor.jpg')
            thumbview.addImage('pic/juv.jpg')
            thumbview.addImage('pic/kili.jpg')
#            thumbview.addImage('pic/DSCF6114.JPG')

        self.connect(taglist._tagview, SIGNAL('tagClicked()'), 
                     tagbar,  SLOT('addTagslot()'))

        hbox.addWidget(taglist)
        hbox.addLayout(vbox)

        vbox.addWidget(ctrl)

        vbox.addWidget(tagbar)
        vbox.addWidget(thumbview)

        self.setLayout(hbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
    sys.exit()
