#-*- coding: utf-8 -*-
"""
A widget for displaying a thumbnail grid
"""

import sys
import subprocess
import logging

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from thumbnailer import Thumbnailmaker


class ThumbnailCache():
    pass

class Thumbnail(QObject):
    def __init__(self, imagepath, pool, listview):
        QObject .__init__(self)
        self.path = imagepath
        self._thread = None

        self.qimg = None

        self.pool = pool
        self._qlistview = listview
        self._index = None

    def calcThumbnail(self, index, w, h):
        if self._thread:
            # Called during an already running calculation
            return

        self._index = index

        thread = Thumbnailmaker(self.path, w, h)
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

        # Tell the QListView widget to update the item that will
        # hold the freshly calculated thumbnail
        self._qlistview.update(self._index)

class ThumbnailDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    def drawImage():
        pass

    def paint(self, painter, option, index):
        painter.save()

        border = True

        option.rect.adjust(0,0,-2,-2)

        painter.setPen(QColor(200,200,200))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(Qt.red))
        else:
            painter.setBrush(QBrush(Qt.white))

        option.rect.adjust(2,2,-2,-2)

        value = index.data(Qt.DisplayRole)

        thumbnail = value.toPyObject() #Convert QVariant to a Thumbnail instance

        if not thumbnail.qimg:
            thumbnail.calcThumbnail(index, option.rect.width(), option.rect.height())
            painter.setPen(QColor(0,0,0))
            painter.drawText(option.rect, Qt.AlignCenter, "Loading...")
        else:
            imgrect = thumbnail.qimg.rect()
            pixmap = QPixmap()
            pixmap.convertFromImage(thumbnail.qimg)

            # Adjust the image to the center both vertically and horizontally
            adj_w = (option.rect.width() - imgrect.width()) / 2
            adj_h = (option.rect.height() - imgrect.height()) / 2

            option.rect.adjust(adj_w, adj_h, -adj_w, -adj_h)
            if border:
                option.rect.adjust(-2, -2, 2, 2)
                painter.drawRect(option.rect)
                option.rect.adjust(2, 2, -2, -2)
            painter.drawPixmap(option.rect, pixmap)


        painter.restore()

    def sizeHint(self, model, index):
        return QSize(180,180)

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

        self.connect(self, SIGNAL("activated (const QModelIndex&)"), self.click)

        # This does not seem to do anything
        # most likely because of QTBUG-7232
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def click(self, index):
        value = index.data(Qt.DisplayRole)
        thumbnail = value.toPyObject() #Convert QVariant to a Thumbnail instance

        logging.info("Thumbnail clicked %s", thumbnail.path)

        # TODO get my own image viewer, till then why not use feh
        subprocess.call(["/usr/bin/feh", "-F", thumbnail.path])

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
        m = ThumbnailsModel([Thumbnail(i, self._threadpool, self._view) for i in imagelist])
        self._view.setModel(m)

    def clearWidget(self):
        m = ThumbnailsModel([])
        self._view.setModel(m)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Thumbnails()
    w.show()
    app.exec_()
    sys.exit()
