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
        QtGui.QLabel.__init__(self, flags = QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle('Image Viewer')

        self._imagepath = None

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
        self._imagepath = imagepath
        self.fitImage()

    def fitImage(self):
        pixmap = QtGui.QPixmap(self._imagepath).scaled(
                    self.width(), self.height(),
                    QtCore.Qt.KeepAspectRatio
                )
        self.setPixmap(pixmap)

    def eventFilter(self, obj, event):
        """
        Override eventFilter to be able to catch when the window loses focus
        """
        # Hide the window when focus is lost or Esc or Q keys are pressed
        if (event.type() == QtCore.QEvent.WindowDeactivate):
            self.hide()
        if (event.type() == QtCore.QEvent.KeyRelease and
            (event.key() == QtCore.Qt.Key_Escape or
             event.key() == QtCore.Qt.Key_Q)):
            self.hide()

        # Toggle fullscreen mode if F key is pressed
        if (event.type() == QtCore.QEvent.KeyRelease and
                event.key() == QtCore.Qt.Key_F):
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        # Update the image when the size of the window changes
        if (event.type() == QtCore.QEvent.Resize):
            self.fitImage()

        return False

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = ImageViewerPopup()
    w.show()
    app.exec_()
    sys.exit()
