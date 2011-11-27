#-*- coding: utf-8 -*-

import logging

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QRunnable, QObject, SIGNAL


class Thumbnailmaker(QRunnable):
    def __init__(self, filename, width, height, parent=None):
        QRunnable.__init__(self)
        self.filename = filename
        self._w = width
        self._h = height

        # Need a QObject to emit signals from a QRunnable
        self.obj = QObject()

    def run(self):
        """
        Method run by the worker thread, responsible for downscaling
        one image to thumbnail size
        """
        # Use two way scaling of the image.
        # The result will be calculated faster than a one-way
        # SmoothTransformation but will be as nice.
        thumb = QtGui.QImage(self.filename)\
                .scaled(self._w * 4, self._h * 4,
                        Qt.KeepAspectRatio,
                        Qt.FastTransformation)\
                .scaled(self._w, self._h,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation)

        logging.info("creating thumbnail image for %s is done", self.filename)
        self.obj.emit(SIGNAL("imageDone"), thumb)

if __name__ == "__main__":
    pass
