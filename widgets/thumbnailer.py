#-*- coding: utf-8 -*-

import logging

from PyQt4 import *
from PyQt4.QtCore import *

from PIL import Image, ImageQt

class Thumbnailmaker(QRunnable):
    def __init__(self, filename, parent = None):
        logging.debug("Starting Thumbnailmaker constructor")
        QRunnable.__init__(self)
        self.filename = filename
        # Need a QObject to emit signals from a QRunnable
        self.obj = QObject()
        logging.debug("Starting Thumbnailmaker constructor DONE")

    def run(self):
        logging.debug("Starting Thumbnailmaker RUN")
        img = Image.open(self.filename)

        logging.info("creating thumbnail image")
        img.thumbnail( (200,200), Image.ANTIALIAS )

        logging.info("creating thumbnail image DONE %s", img)
        thumb = ImageQt.ImageQt(img)

        logging.info("creating ImageQT DONE, emitting signal %s", thumb)
        self.obj.emit(SIGNAL("imageDone"), thumb)

        logging.debug("thread finished")

if __name__ == "__main__":
    pass
