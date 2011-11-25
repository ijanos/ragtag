#-*- coding: utf-8 -*-

import sys

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyListItem(QListWidgetItem):
    """ Extend QListWidgetItem with some information about the tag"""
    def __init__(self, tagid, name, weight, parent=None):
        QListWidgetItem.__init__(self, parent)
        self._name = name
        self._tagid = tagid
        self._wight = weight

        self.setText(unicode(name, encoding='utf-8'))


class MyTaglistWidget(QListWidget):
    """
    QListWidget extended with filter capabilites and it can read
    my tagdata tuple
    """
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        self.setAlternatingRowColors(True)
        self.connect(self, SIGNAL('itemClicked (QListWidgetItem *)'), self.clicked)

    def clicked(self, item):
        self.emit(SIGNAL('tagClicked'), item._tagid, item._name)

    def filterList(self, text):
        # TODO allow user to toggle case-sensitvity
        text = unicode(text).lower() # lower for case insesitivity
        for idx in xrange(0,self.count()):
            item = self.item(idx)
            itemtext = unicode(item.text()).lower() #here too
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

        vbox.addWidget(self._tagview)

        self.setLayout(vbox)
        self.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

    def setTaglist(self, taglist):
        self._itemedit.clear()
        self._tagview.setTaglist(taglist)

    def sizeHint(self):
        return QSize(35,16777215)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TaglistPanel()
    w.show()
    app.exec_()
    sys.exit()
