#-*- coding: utf-8 -*-
"""
A widget to show active tags
"""

import sys
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Tagbar(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)

        hbox = QHBoxLayout()
        self._buttons = QHBoxLayout()
        self._buttons.setContentsMargins(0,0,0,0)
        self._buttons.setMargin(0)
        self._buttons.setSpacing(1)
#        self.setStyleSheet("background-color:yellow;"
#                           "selection-color: red;"
#                           "border-style: outset;"
#                           "border-width: 2px;"
#                           "border-color: black;"
#                          )

        hbox.addLayout(self._buttons)
        hbox.insertStretch(-1)
        self.setLayout(hbox)

    @pyqtSlot()
    def addTagslot(self):
        self.addTag("omg")

    def addTag(self,tagname):
        tagbutton = QPushButton(tagname)
     #   tagbutton.setFlat(True)

        def clickfun():
            self.emit(SIGNAL('tagRemoved()'))
            tagbutton.hide()

        self.connect(tagbutton, SIGNAL('clicked()'), clickfun)
        self._buttons.addWidget(tagbutton)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Tagbar()

    w.addTag("kutya")
    w.addTag("cica")
    w.addTag(u"akármi")
    w.addTag(u"árvíz")
    w.addTag(u"tűrő")
    w.addTag(u"foobar")

    w.show()
    app.exec_()
    sys.exit()
