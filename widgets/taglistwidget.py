#-*- coding: utf-8 -*-

import sys
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MyListItem(QListWidgetItem):
    def __init__(self, tagid, name, weight, parent = None):
        QListWidgetItem.__init__(self, parent)
        self._name = name
        self._tagid = tagid
        self._wight = weight

        self.setText(name)

class MyTaglistWidget(QListWidget):
    def __init__(self, parent = None):
        QListWidget.__init__(self, parent)
        self.setAlternatingRowColors(True)
        self.connect(self, SIGNAL('itemClicked (QListWidgetItem *)'), self.clicked)

    @pyqtSlot()
    def clicked(self, item):
        self.emit(SIGNAL('tagClicked'))
        print "click ", item

    @pyqtSlot()
    def filterList(self, text):
        text = unicode(text)
        matched = self.findItems(text, Qt.MatchContains)
        for idx in xrange(0,self.count()):
            item = self.item(idx)
            itemtext = unicode(item.text())
            if (text in itemtext):
                self.setItemHidden(item, False)
            else:
                self.setItemHidden(item, True)

    def setTaglist(self, tags):
        self.clear()
        for (tid, tname, tw) in tags:
            self.addItem(MyListItem(tid, tname, tw))


class TaglistPanel(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)

        vbox = QVBoxLayout()

        self._itemedit = QLineEdit()

        vbox.addWidget(self._itemedit)

        self._tagview = MyTaglistWidget()

        self.connect(self._itemedit, SIGNAL('textChanged(QString)'), self._tagview.filterList)
                    # self._tagview, SLOT('filterList()'))

        vbox.addWidget(self._tagview)

        self.setLayout(vbox)
        self.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

    def setTaglist(self, taglist):
        self._tagview.setTaglist(taglist)

    def sizeHint(self):
        return QSize(90,16777215)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TaglistPanel()
    w.show()
    app.exec_()
    sys.exit()
