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

        clearbutton = QPushButton("Clear")

        self.connect(clearbutton, SIGNAL('clicked()'), self.clearTags)

        hbox.addLayout(self._buttons)
        hbox.insertStretch(-1)
        hbox.addWidget(clearbutton)
        self.setLayout(hbox)

    def clearTags(self):
        self.emit(SIGNAL('clearTags'))
        for i in xrange(0, self._buttons.count()):
            item = self._buttons.itemAt(0) # always delete the first item
            # because items are being deleted during the loop
            widget = item.widget()
            widget.hide()
            widget.close()
            self._buttons.removeItem(item)

    def addTag(self, tagid, tagname):
        tagbutton = QPushButton(unicode(tagname, encoding='utf-8'))
        tagbutton.setFlat(True)

        def clickfun():
            self.emit(SIGNAL('tagRemoved'), tagid)
            tagbutton.hide()
            #TODO remove the button entirely

        self.connect(tagbutton, SIGNAL('clicked()'), clickfun)
        self._buttons.addWidget(tagbutton)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Tagbar()

    w.addTag(u"foobar")

    w.show()
    app.exec_()
    sys.exit()
