#-*- coding: utf-8 -*-

import logging

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from managedb import PhotoDB


class Controller(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.photoDB = None

        self.currentTags = []
        self.currentImages = []

    def start(self):
        self.photoDB = PhotoDB('testdb')  # XXX debug value
        self.loadTags()

    def reset(self):
        self.currentTags = []
        self.filterShownTags()

    def loadDB(self):
        filename = QFileDialog.getOpenFileName()
        if filename:
            logging.info("Loading database: %s", str(filename))
            self.photoDB = PhotoDB(str(filename))
        else:
            return
        self.loadTags()

    def loadTags(self):
        taglist = self.photoDB.getTaglist()
        logging.debug("list of tags: %s", taglist)
        self.emit(SIGNAL("updateTags"), taglist)

    def loadImgs(self):
        # extract the IDs
        tagidlist = [tagid for (tagid, _) in self.currentTags]
        self.currentImages = self.photoDB.getPhotosByTagIDs(tagidlist)
        # extract path from tuple
        imgpathlist = [p for (_, p) in self.currentImages]
        self.emit(SIGNAL('addPhotos'), imgpathlist)

    def filterShownTags(self):
        if not self.currentTags:  # if the list is empty then show all tags
            self.loadTags()
            return
        # extract id from tuple
        imgidList = [i for (i, _) in self.currentImages]
        # extract the IDs
        tagfilter = [tagid for (tagid, _) in self.currentTags]
        filteredtags = self.photoDB.getTagsForImages(imgidList, tagfilter)
        self.emit(SIGNAL("updateTags"), filteredtags)

    def tagClicked(self, tagid, tagname):
        """
        This slot fires when the user clicks a tag in the list
        """
        self.emit(SIGNAL('addTag'), tagid, tagname)  #add tag to strip
        self.currentTags.append((tagid, tagname))  #update state
        self.loadImgs()  #list photos according to state
        self.filterShownTags()  #reduce list of tags according to state

    def tagRemoved(self, tagid):
        """
        This slot fires when a tag is removed
        """
        #remove tag with tagid from the currenttags list
        self.currentTags = filter(
                lambda (tid, tn): tid != tagid, self.currentTags)
        self.loadImgs()  #list photos according to state
        self.filterShownTags()  #reduce list of tags according to state
