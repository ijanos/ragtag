#-*- coding: utf-8 -*-
"""
A widget for displaying a single image
"""

import sys
import logging

from PyQt4 import QtCore
from PyQt4 import QtGui


class ImageViewerPopup(QtGui.QLabel):
    def __init__(self):
        QtGui.QLabel.__init__(self, flags = QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle('Image Viewer')

        self.setAlignment(QtCore.Qt.AlignCenter)

        MARGIN = 40

        desktopGeo = QtGui.QDesktopWidget().availableGeometry()

        self.resize(desktopGeo.width() - MARGIN,
                    desktopGeo.height() - MARGIN)

        #move the window to the center of the screen
        frect = self.frameGeometry();
        frect.moveCenter(desktopGeo.center());
        self.move(frect.topLeft())

        self.installEventFilter(self);

    def setImage(self, imagepath):
        title = "Image Viewer - " + imagepath
        self.setWindowTitle(title)
        pixmap = QtGui.QPixmap(imagepath).scaled(
                    self.width(), self.height(),
                    QtCore.Qt.KeepAspectRatio
                )
        self.setPixmap(pixmap)

    def eventFilter(self, obj, event):
        """
        Override eventFilter to be able to catch when the window loses focus
        """
        if (event.type() == QtCore.QEvent.WindowDeactivate):
            self.hide()
        if (event.type() == QtCore.QEvent.KeyRelease and
            (event.key() == QtCore.Qt.Key_Escape or
             event.key() == QtCore.Qt.Key_Q)):
            self.hide()
        return False

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = ImageViewerPopup()
    w.show()
    app.exec_()
    sys.exit()
