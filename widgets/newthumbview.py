#-*- coding: utf-8 -*-
"""
A widget for displaying a thumbnail grid
"""

import sys
import logging

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from thumbnailer import Thumbnailmaker


class ThumbnailCache():
    pass

class Thumbnail(QObject):
    def __init__(self, imagepath, pool):
        QObject .__init__(self)
        self.path = imagepath
        self._thread = None
        self.pool = pool
        self.qimg = None

    def calcThumbnail(self):
        if self._thread:
            # Called during an already running calculation
            return

        thread = Thumbnailmaker(self.path)
        self.connect(thread.obj, SIGNAL("imageDone"), self.imageDone)

        #Hold onto a reference to prevent PyQt from dereferencing
        self._thread = thread

        self.pool.start(thread)

    def imageDone(self, image = None):
        if not image:
            logging.warning("Did not get back image from the resizer thread!")
            return

        self.qimg = image
        self._thread = None #Let the thread die

        #self.emit(SIGNAL("updateUI"))

class ThumbnailDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    def drawImage():
        pass

    def paint(self, painter, option, index):
        painter.save()

        value = index.data(Qt.DisplayRole)

        thumbnail = value.toPyObject() #Convert QVariant to a Thumbnail instance
        if not thumbnail.qimg:
            thumbnail.calcThumbnail()

        option.rect.adjust(0,0,-5,-5)

        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(Qt.red))
        else:
            painter.setBrush(QBrush(Qt.white))
        painter.drawRect(option.rect)

        option.rect.adjust(10,10,-10,-10)

        if thumbnail.qimg:
            imgrect = thumbnail.qimg.rect
            pixmap = QPixmap()
            pixmap.convertFromImage(thumbnail.qimg)
            painter.drawPixmap(option.rect, pixmap)
        else:
            painter.drawText(option.rect, Qt.AlignCenter, "Loading...")

        painter.restore()

    def sizeHint(self, model, index):
        return QSize(200,200)

class ThumbnailsModel(QAbstractListModel):
    def __init__(self, thumbnailpaths, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self._list = thumbnailpaths

    def rowCount(self, parent=QModelIndex()):
        return len(self._list)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self._list[index.row()])
        else:
            return QVariant()

class ThumbnailGridView(QListView):
    def __init__(self, parent=None):
        QListView.__init__(self, parent)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)

class Thumbnails(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._view = ThumbnailGridView()
        d = ThumbnailDelegate()
        self._view.setItemDelegate(d)

        self._threadpool = QThreadPool.globalInstance()

        # Let Qt decide the ideal thread count
        # only override this with good reason, or debug purposes
        ##self._threadpool.setMaxThreadCount(2)

        layout = QHBoxLayout()
        layout.addWidget(self._view)

        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        self.setLayout(layout)


    def addImages(self, imagelist):
        logging.debug("Adding images to thumbview: %s", imagelist)
        m = ThumbnailsModel([Thumbnail(i,self._threadpool) for i in imagelist])
        self._view.setModel(m)

    def clearWidget(self):
        logging.warning("Implement widget clearing")
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Thumbnails()
    w.show()
    app.exec_()
    sys.exit()
