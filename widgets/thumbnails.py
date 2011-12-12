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
from ImageViewerPopup import ImageViewerPopup


class ThumbnailCache():
    pass


class Thumbnail(QObject):
    def __init__(self, imagepath, listview):
        QObject .__init__(self)
        self.path = imagepath
        self._thread = None

        self.qimg = None

        self.pool = QThreadPool.globalInstance()

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

    def imageDone(self, image=None):
        if not image:
            logging.warning("Did not get back image from the resizer thread!")
            return

        self.qimg = image
        self._thread = None  # Let the thread die

        # Tell the QListView widget to update the item that will
        # hold the freshly calculated thumbnail
        self._qlistview.update(self._index)


class ThumbnailDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    def paint(self, painter, option, index):
        painter.save()

        border = True

        option.rect.adjust(0, 0, -2, -2)

        painter.setPen(QColor(200, 200, 200))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(Qt.red))
        else:
            painter.setBrush(QBrush(Qt.white))

        option.rect.adjust(2, 2, -2, -2)

        value = index.data(Qt.DisplayRole)

        # Convert QVariant to a Thumbnail instance
        thumbnail = value.toPyObject()

        if not thumbnail.qimg:
            thumbnail.calcThumbnail(index,
                                    option.rect.width(),
                                    option.rect.height())
            painter.setPen(QColor(0, 0, 0))
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
        return QSize(160, 160)


class ThumbnailsModel(QAbstractListModel):
    def __init__(self, thumbnailpaths, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self._list = thumbnailpaths

    def rowCount(self, parent=QModelIndex()):
        return len(self._list)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self._list[index.row()])
        elif index.isValid() and role == Qt.ToolTipRole:
            # Show the path of the image as tooltip when the thumbnails is hovered
            return "<b>Image path:</b>\n" + self._list[index.row()].path
        else:
            return QVariant()


class ThumbnailGridView(QListView):
    def __init__(self, parent=None):
        QListView.__init__(self, parent)

        self.setViewMode(QListView.IconMode)

        # Reflow the image grid after resize
        self.setResizeMode(QListView.Adjust)

        # All items uses the same size, this supposedly improves performance
        self.setUniformItemSizes(True)

        # Generate images from left to right
        self.setFlow(QListView.LeftToRight)

        self.imageviewpopup = ImageViewerPopup()

        self.connect(self,
                     SIGNAL("activated (const QModelIndex&)"), self.click)

        # TODO enable this
        #self.addContextMenu()

        # This does not seem to do anything
        # most likely because of QTBUG-7232
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def addContextMenu(self):
        """
        Create & connect the QActions of the right-click menu
        """
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.action1 = QAction("Menu item1", self)
        self.addAction(self.action1)
        self.connect(self.action1, SIGNAL("triggered()"), self.rightClick)

    def click(self, index):
        """
        Handle the click event on a thumbnail.
        Show the imageviewer popup
        """
        value = index.data(Qt.DisplayRole)
        thumbnail = value.toPyObject()

        logging.info("Thumbnail clicked %s", thumbnail.path)

        self.imageviewpopup.setImage(thumbnail.path)
        self.imageviewpopup.show()

    def rightClick(self):
        photo = self.currentIndexToPhoto()
        print photo.path

    def currentIndexToPhoto(self):
        """
        Convert current QModelIndex object to Photo
        """
        # Get the index of the currently selected photo
        index = self.currentIndex()
        # get the object of the currently selected photo
        value = index.data(Qt.DisplayRole)
        # Convert QVariant to a Photo instance
        photo = value.toPyObject()

        return photoobj


class Thumbnails(QWidget):
    """
    This widget can display a list of images in a thumbnail grid

    has two slots:
        addImages: takes a list of strings, paths to images
        clearWidget: remove the thumbnals, show empty the widget

    emits no signals
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._view = ThumbnailGridView()
        d = ThumbnailDelegate()
        self._view.setItemDelegate(d)


        # Let Qt decide the ideal thread count
        # only override this with good reason, or debug purposes
        ##self._threadpool = QThreadPool.globalInstance()
        ##self._threadpool.setMaxThreadCount(2)

        layout = QHBoxLayout()
        layout.setMargin(1)

        layout.addWidget(self._view)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setLayout(layout)

    def addImages(self, imagelist):
        logging.debug("Adding images to thumbview: %s", imagelist)
        m = ThumbnailsModel(
               [Thumbnail(i, self._view) for i in imagelist])
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
