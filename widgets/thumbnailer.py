#-*- coding: utf-8 -*-

import logging

from PyQt4 import *
from PyQt4.QtCore import *

from PIL import Image, ImageQt


class Thumbnailmaker(QRunnable):
    def __init__(self, filename, width, height, parent=None):
        QRunnable.__init__(self)
        self.filename = filename
        self._w = width
        self._h = height

        # Need a QObject to emit signals from a QRunnable
        self.obj = QObject()

    def run(self):
        img = Image.open(self.filename)

        img.thumbnail((self._w, self._h), Image.ANTIALIAS)

        thumb = ImageQt.ImageQt(img)

        logging.info("creating thumbnail image for %s is done", self.filename)
        self.obj.emit(SIGNAL("imageDone"), thumb)

if __name__ == "__main__":
    pass
