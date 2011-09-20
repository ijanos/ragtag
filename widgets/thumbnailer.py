#-*- coding: utf-8 -*-

from PyQt4 import *
from PyQt4.QtCore import *

from PIL import Image, ImageQt

class Thumbnailmaker(QRunnable):
    def __init__(self, filename, parent = None):
        QRunnable.__init__(self)
        self.filename = filename
        # Need a QObject to emit signals from a QRunnable
        self.obj = QObject()

    def run(self):
        img = Image.open(self.filename)
        img.thumbnail( (200,200), Image.ANTIALIAS )
        thumb = ImageQt.ImageQt(img)
        self.obj.emit(SIGNAL("imageDone"), thumb)

if __name__ == "__main__":
    pass
