# -*- coding: utf-8 -*-
"""
Database absctraction
"""

import sqlite3

class PhotoDB():
    def __init__(self, filename):
        (self.cursor, self.connection) = self.initDB(filename)
        #XXX check if tables are available

    def initDB(self, filename):
        '''Initialize the database'''
        db_connection = sqlite3.connect(filename)
        db_connection.text_factory = str #be unicode friendly
        return (db_connection.cursor(), db_connection)

    def create_tables(self):
        '''Create the tables in the database. This will erease any previous data!'''
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
                FOREIGN KEY(dirid) REFERENCES dirs(id)
            );
        '''
        self.cursor.executescript(sqlscript)


    def lookupDir(self,path):
        self.connection.commit()
        self.cursor.execute('SELECT id FROM dirs WHERE path = ?', (path,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute("INSERT INTO dirs(path) VALUES (?)", (path,))
            self.connection.commit()
            return self.cursor.lastrowid


    def lookupTag(self, tagname):
        self.cursor.execute('SELECT id FROM tags WHERE name = ?', (tagname,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute(''' INSERT INTO tags(name) VALUES (?); ''', (tagname,))
            self.connection.commit()
            return self.cursor.lastrowid

    def storePhoto(self, dirid, filepath, tags):
        '''Store a photo with tags into the database'''
        print "recece", dirid, filepath, tags
        self.cursor.execute('INSERT INTO images(dirid, path) VALUES (?,?);',
                (dirid,filepath))
        imgid = self.cursor.lastrowid
        for tag in tags:
            tagid = self.lookupTag(tag)
            self.cursor.execute(
                'INSERT OR REPLACE INTO xtagimg(tagid,imgid) VALUES (?,?)',
                (tagid, imgid))

if __name__ == "__main__":
    photos = PhotoDB('testdb')
    photos.create_tables()
    photos.addDir('pic')
