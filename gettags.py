import sys
import os

import pyexiv2

def getMetadata(f):
    metadata = pyexiv2.ImageMetadata(f)
    metadata.read()
    if 'Iptc.Application2.Keywords' in metadata.iptc_keys:
        tags = metadata['Iptc.Application2.Keywords'].value
    else:
        tags = []
    return (metadata, tags)

def getTagList(filepath):
    (_, taglist) = getMetadata(filepath)
    print filepath, taglist

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
                fun(f)

def processFile(pathtofile):
    os.path.basename(pathtofile)
    os.path.dirname(pathtofile)

if __name__=="__main__":
    dir1 = "/mnt/data/Documents/photo/2011/"
    extfilter = ['jpg', 'jpeg']
    traverseDir(dir1, extfilter, getTagList)
