#-*- coding: utf-8 -*-

import sys
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
  
class MyTaglistWidget(QListWidget):
    def __init__(self, parent = None):
        QListWidget.__init__(self, parent)
        self.setAlternatingRowColors(True)
        self.connect(self, SIGNAL('itemClicked (QListWidgetItem *)'), self.clicked)
        #self.connect(self, SIGNAL('itemSelectionChanged()'), self.clicked)

    @pyqtSlot()
    def clicked(self, item):
        self.emit(SIGNAL('tagClicked()'))
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
#        for item in matched:
#            self.setItemHidden(item, False)

class TaglistPanel(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)

        vbox = QVBoxLayout()

        self._itemedit = QLineEdit()

        vbox.addWidget(self._itemedit)

        self._tagview = MyTaglistWidget()
        self._tagview.addItems(["recece1","recece2","@kutya","@cica",u"ősz","tanya","pest",u"árívíz"])
        ###############
        tmplist = []
        for tmp in xrange(0,200):
            tmplist.append("foobar"+str(tmp))
        self._tagview.addItems(tmplist)
       ###############

        self.connect(self._itemedit, SIGNAL('textChanged(QString)'), self._tagview.filterList)
                    # self._tagview, SLOT('filterList()'))

        self.setMaximumSize(QtCore.QSize(150, 16777215))
        vbox.addWidget(self._tagview)

        self.setLayout(vbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TaglistPanel()
    w.show()
    app.exec_()
    sys.exit()
