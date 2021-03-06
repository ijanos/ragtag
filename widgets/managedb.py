# -*- coding: utf-8 -*-
"""
Database absctraction
"""

import os.path
import sqlite3
import logging


class PhotoDB():
    def __init__(self, filename):
        (self.cursor, self.connection) = self.initDB(filename)
        #XXX check if tables are available

    def __del__(self):
        logging.debug("Destroying photo database object")
        self.connection.commit()

    def initDB(self, filename):
        '''Initialize the database'''
        db_connection = sqlite3.connect(filename)
        db_connection.text_factory = str  # be unicode friendly
        return (db_connection.cursor(), db_connection)

    def create_tables(self):
        '''
        Create the tables in the database.
        This will erease any previous data!
        '''
        sqlscript = '''
            DROP TABLE IF EXISTS tags;
            DROP TABLE IF EXISTS xtagimg;
            DROP TABLE IF EXISTS images;
            DROP TABLE IF EXISTS dirs;

            CREATE TABLE tags (
                "id" INTEGER PRIMARY KEY,
                "name" TEXT
            );

            CREATE TABLE dirs (
                "id" INTEGER PRIMARY KEY,
                "path" TEXT
            );

            CREATE TABLE xtagimg (
                tagid INTEGER,
                imgid INTEGER,
                FOREIGN KEY(tagid) REFERENCES tags(id),
                FOREIGN KEY(imgid) REFERENCES images(id)
            );

            CREATE TABLE images (
                "id" INTEGER PRIMARY KEY,
                "dirid" INTEGER,
                "path" TEXT,
                "datetime" DATETIME,
                FOREIGN KEY(dirid) REFERENCES dirs(id)
            );
        '''
        self.cursor.executescript(sqlscript)

    def lookupDir(self, path):
        """
        Look up a given path in the database and return its ID.
        Create a new entry if the path was not in the DB.
        """
        self.cursor.execute('SELECT id FROM dirs WHERE path = ?', (path,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute("INSERT INTO dirs(path) VALUES (?)", (path,))
            return self.cursor.lastrowid

    def lookupTag(self, tagname):
        self.cursor.execute('SELECT id FROM tags WHERE name = ?', (tagname,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute(''' INSERT INTO tags(name) VALUES (?); ''',
                    (tagname,))
            return self.cursor.lastrowid

    def storePhoto(self, dirid, filepath, datetime, tags):
        '''Store a photo with tags into the database'''
        self.cursor.execute('INSERT INTO images(dirid, datetime, path) VALUES (?,?,?);',
                (dirid, datetime, filepath))
        imgid = self.cursor.lastrowid
        logging.info("processing tags, imgeid: %s, path: %s", imgid, filepath)
        for tag in tags:
            tagid = self.lookupTag(tag)
            self.cursor.execute(
                'INSERT OR REPLACE INTO xtagimg(tagid,imgid) VALUES (?,?)',
                (tagid, imgid))

    def getPhotosByTagIDs(self, tagidlist):
        idlist = ','.join([str(x) for x in tagidlist])
        idlistlen = len(tagidlist)
        sqlquery = '''
          SELECT images.id, dirs.path, images.path
            FROM images,
                 xtagimg ON xtagimg.imgid = images.id,
                 dirs ON dirs.id = images.dirid
          WHERE tagid IN (%s)
          GROUP BY imgid
          HAVING COUNT( imgid ) = %s
          ORDER BY datetime
        ''' % (idlist, idlistlen)
        # prepare statement cannot really work here, but no problem
        # the user has direct access to the databse anyways.
        self.cursor.execute(sqlquery)
        result = []
        for (imgid, path1, path2) in self.cursor:
            result.append((imgid, os.path.join(path1, path2)))
        return result

    def getTaglist(self):
        '''Return tag id, tagname and the usage frequency'''
        # TODO specify different orders: frequency/lexical
        sqlquery = '''
            SELECT id,name,count(id) as used
               FROM tags, xtagimg on xtagimg.tagid = id
            GROUP BY id
            ORDER BY count(id) DESC
        '''
        self.cursor.execute(sqlquery)
        result = []
        for row in self.cursor:
            result.append(row)
        return result

    def getTagsForImages(self, imgIDlist, tagfilter):
        ''' which tags are used with the images '''
        idlist = ','.join([str(x) for x in imgIDlist])
        filterlist = ','.join([str(x) for x in tagfilter])
        sqlquery = '''
          SELECT id,name,count(id) as used
              FROM tags, xtagimg on xtagimg.tagid = id
          WHERE xtagimg.imgid IN (%s)
          AND xtagimg.tagid NOT IN (%s)
          GROUP BY id
          ORDER BY count(id) DESC
        ''' % (idlist, filterlist)
        # TODO modify this to not show any if no new picture can be added
        self.cursor.execute(sqlquery)
        result = []
        for row in self.cursor:
            result.append(row)
        return result

if __name__ == "__main__":
    photos = PhotoDB('testdb')
    for p in photos.getPhotos([2]):
        print p
    #photos.create_tables()
    #photos.addDir('pic')
