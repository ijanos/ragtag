#-*- coding: utf-8 -*-
"""
A widget for displaying a thumnail grid
"""

import sys

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from flowlayout import FlowLayout

class Thumbnail(QLabel):
    def __init__(self, image,parent=None):
        QLabel.__init__(self, parent)

        self.setStyleSheet(#"background-color:black;"
                           #"selection-color: yellow;"
                           "border-style: solid;"
                           "border-width: 1px;"
                           "border-color: grey;"
                          )
        self.setMargin(2)

        self.setMaximumSize(QSize(200,200))

        filenamesplit = image.split('/')
        self.setToolTip("File: " + filenamesplit[-1])

        img = QPixmap(image)

        thumb = img.scaled(200,200,Qt.KeepAspectRatio)#,Qt.SmoothTransformation) # slooooooow :(

        self.setPixmap(thumb)

    def mousePressEvent(self, event):
        print "I've been clicked \o/", event


class Thumbnails(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._layout = FlowLayout()
        layout = QHBoxLayout()

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
        thumb = Thumbnail(image)
        self._layout.addWidget(thumb)

    def reset(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Thumbnails()
    w.show()
    app.exec_()
    sys.exit()
