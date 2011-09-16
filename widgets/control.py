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
        self.currentImages = []

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

    def start(self):
        self.photoDB = PhotoDB('testdb') #XXX debug value
        self.loadTags()

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
        # TODO empty prevoius images
        tagidlist = [tagid for (tagid, _) in self.currentTags] # extract the IDs
        self.currentImages = self.photoDB.getPhotosByTagIDs(tagidlist)
        imgpathlist = [p for (_, p) in self.currentImages] # extract path from tuple
        self.emit(SIGNAL('addPhotos'), imgpathlist)

    def filterShownTags(self):
        if not self.currentTags: #if the list is empty then show all tags
            self.loadTags()
            return
        imgidList = [i for (i, _) in self.currentImages] # extract id from tuple
        tagfilter = [tagid for (tagid, _) in self.currentTags] # extract the IDs
        filteredtags = self.photoDB.getTagsForImages(imgidList,tagfilter)
        self.emit(SIGNAL("updateTags"), filteredtags)


    def tagClicked(self, tagid, tagname):
        """ 
        This slot fires when the user clicks a tag in the list
        """
        self.emit(SIGNAL('addTag'), tagid, tagname) #add tag to strip
        self.currentTags.append((tagid,tagname)) #update state
        self.loadImgs() #list photos according to state
        self.filterShownTags() #reduce list of tags according to state

    def tagRemoved(self, tagid):
        """
        This slot fires when a tag is removed
        """
        #remove tag with tagid from the currenttags list
        self.currentTags = filter(lambda (tid,tn): tid != tagid,self.currentTags)
        self.loadImgs() #list photos according to state
        self.filterShownTags() #reduce list of tags according to state
