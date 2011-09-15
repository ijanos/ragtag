#-*- coding: utf-8 -*-

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from managedb import PhotoDB

class Controller(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.photoDB = None

        self.currentTags = []

        layout = QHBoxLayout()

        txt = QLabel("Hello World")

        bLoad = QPushButton("Load database")
        bTags = QPushButton("Load tags")
        bImgs = QPushButton("load images")
        bReset = QPushButton("reset")
        bQuit = QPushButton("Quit")

        layout.addWidget(txt)

        layout.insertStretch(-1)

        layout.addWidget(bLoad)
        layout.addWidget(bTags)
        layout.addWidget(bImgs)
        layout.addWidget(bReset)
        layout.addWidget(bQuit)

        self.connect(bQuit, SIGNAL('clicked()'),
                     QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(bLoad, SIGNAL('clicked()'), self.loadDB)
        self.connect(bTags, SIGNAL('clicked()'), self.loadTags)
        self.connect(bImgs, SIGNAL('clicked()'), self.loadImgs)
        self.connect(bReset, SIGNAL('clicked()'), self.reset)

        self.setLayout(layout)

    def reset(self):
        self.currentTags = []

    def createGUI(self):
        pass #TODO

    def loadDB(self):
        filename = QFileDialog.getOpenFileName()
        if filename:
            self.photoDB = PhotoDB(str(filename))

    def loadTags(self):
        taglist = self.photoDB.getTaglist()
        self.emit(SIGNAL("updateTags"), taglist)

    def loadImgs(self):
        tagidlist = [tagid for (tagid, _) in self.currentTags]
        print self.currentTags
        imglist = self.photoDB.getPhotosByTag(tagidlist)
        self.emit(SIGNAL('addPhotos'), imglist)

    def tagClicked(self, tagid, tagname):
        """ 
        This slot fires when the user clicks a tag in the list
        """
        self.emit(SIGNAL('addTag'), tagname) #add tag to strip
        self.currentTags.append((tagid,tagname)) #update state
        self.loadImgs() #list photos according to state
        #TODO reduce list of tags according to state
