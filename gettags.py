#-*- coding: utf-8 -*-
"""
Parse image files and store their metadata in the database
"""

import sys
import os
import os.path
import logging

import pyexiv2

from widgets.managedb import PhotoDB

photos = PhotoDB('testdb')
photos.create_tables()

def getMetadata(f):
    metadata = pyexiv2.ImageMetadata(f)
    metadata.read()
    # get the tags from the image
    if 'Iptc.Application2.Keywords' in metadata.iptc_keys:
        tags = metadata['Iptc.Application2.Keywords'].value
    else:
        tags = []

    # try to get a proper date/time from the image
    datetime = None
    for dateattr in ['Exif.Image.DateTimeOriginal', 'Exif.Image.DateTime']:
        try:
            datetime = metadata[dateattr].value
            break
        except KeyError:
            pass
    if not datetime:
        logging.debug("Could not find datetime in file")
    return (datetime, tags)

def traverseDir(directory, extfilter, fun):
    """
    Walk the directory and its subdirectories and look for files
    ending with extfilter and call fun on them
    """
    for root, dirs, files in os.walk(directory):
        for name in files:
            ext = name.split('.')[-1].lower()
            if  ext in extfilter:
                f = os.path.join(root, name)
                f = "/".join(f.split('/')[1:])
                fun(f)

def processDir(pathtodir):
    fullpath = os.path.abspath(pathtodir)
    os.chdir(fullpath)
    dirid = photos.lookupDir(fullpath)
    extfilter = ['jpg', 'jpeg']
    def f(filepath):
        (datetime, taglist) = getMetadata(filepath)
        photos.storePhoto(dirid, filepath, datetime, taglist)
    traverseDir(".", extfilter, f)

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    dir1 = sys.argv[1]
    processDir(dir1)
