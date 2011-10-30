#-*- coding: utf-8 -*-
"""
A widget for displaying a thumbnail grid
"""

import sys

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from flowlayout import FlowLayout
from thumbnailer import Thumbnailmaker

class Thumbnail(QLabel):
    def __init__(self, image, pool, parent=None):
        QLabel.__init__(self, parent)

        self.setStyleSheet(#"background-color:black;"
                           #"selection-color: yellow;"
                           "border-style: solid;"
                           "border-width: 1px;"
                           "border-color: grey;"
                          )
        self.setMargin(2)

        self.setMaximumSize(QSize(200,200))

        self.setText("loading image...")

        filenamesplit = image.split('/')
        self.setToolTip("File: " + filenamesplit[-1])

        self.thread = Thumbnailmaker(image)
        self.connect(self.thread.obj, SIGNAL("imageDone"), self.setImage)

        pool.start(self.thread)


    def setImage(self, image):
        pixmap = QPixmap()
        pixmap.convertFromImage(image)
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        print "I've been clicked \o/", event


class Thumbnails(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._layout = FlowLayout()
        layout = QHBoxLayout()

        self._threadpool = QThreadPool()

        container = QWidget()
        scrollArea = QScrollArea();
#        scrollArea.setStyleSheet("border-style: none;") # Scrollbar gets wierd
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(container)

        container.setLayout(self._layout)

        layout.addWidget(scrollArea)
        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

    def clearWidget(self):
        # empty the layout
        for i in xrange(0, self._layout.count()):
            item = self._layout.itemAt(0) # always delete the first item
            # because items are being deleted during the loop
            widget = item.widget()
            widget.hide()
            widget.close()
            self._layout.removeItem(item)

    def addImages(self, imagelist):
        self.clearWidget()
        for image in imagelist:
            self.addImage(image)

    def addImage(self, image):
        thumb = Thumbnail(image, self._threadpool)
        self._layout.addWidget(thumb)

    def reset(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Thumbnails()
    w.show()
    app.exec_()
    sys.exit()
