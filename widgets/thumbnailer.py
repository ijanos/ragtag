#-*- coding: utf-8 -*-

from PyQt4 import *
from PyQt4.QtCore import *

from PIL import Image, ImageQt

class Thumbnailmaker(QThread):
    def __init__(self, filename, parent = None):
        QThread.__init__(self, parent)
        self.filename = filename

    def run(self):
        img = Image.open(self.filename)
        img.thumbnail( (200,200), Image.ANTIALIAS )
        thumb = ImageQt.ImageQt(img)
        self.emit(SIGNAL("imageDone"), thumb)

if __name__ == "__main__":
    pass
