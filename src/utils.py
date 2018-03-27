#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import shared as sh
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')


class DB:
    
    def __init__(self,path,clone):
        self._data   = ()
        self._path   = path
        self._clone  = clone
        self.Success = self._clone and sh.File(file=self._path).Success
    
    def save(self):
        if self.Success:
            try:
                self.dbw.commit()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.save'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._clone
                            )
        else:
            sh.log.append ('DB.save'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        
    def connect(self):
        if self.Success:
            try:
                self.db  = sqlite3.connect(self._path)
                self.dbc = self.db.cursor()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.connect'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('DB.connect'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def connectw(self):
        if self.Success:
            try:
                self.dbw  = sqlite3.connect(self._clone)
                self.dbcw = self.dbw.cursor()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.connectw'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._clone
                            )
        else:
            sh.log.append ('DB.connectw'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def fetch(self):
        if self.Success:
            try:
                # 16 columns for now
                self.dbc.execute ('select URL,AUTHOR,TITLE,DATE,CATEGORY\
                                         ,DESC,DURATION,LENGTH,VIEWS\
                                         ,LIKES,DISLIKES,RATING,IMAGE\
                                         ,BLOCK,IGNORE,READY \
                                   from   VIDEOS'
                                 )
                self._data = self.dbc.fetchall()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.fetch'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('DB.fetch'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def create_table(self):
        if self.Success:
            try:
                # 18 columns by now
                self.dbcw.execute (
                    'create table VIDEOS (\
                     URL       text    \
                    ,AUTHOR    text    \
                    ,TITLE     text    \
                    ,DATE      text    \
                    ,CATEGORY  text    \
                    ,DESC      text    \
                    ,DURATION  text    \
                    ,LENGTH    integer \
                    ,VIEWS     integer \
                    ,LIKES     integer \
                    ,DISLIKES  integer \
                    ,RATING    float   \
                    ,IMAGE     binary  \
                    ,BLOCK     boolean \
                    ,IGNORE    boolean \
                    ,READY     boolean \
                    ,SEARCH    text    \
                    ,TIMESTAMP float   \
                                                       )'
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.create_table'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._clone
                            )
        else:
            sh.log.append ('DB.create_table'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def fill(self):
        if self.Success:
            if self._data:
                sh.log.append ('DB.fill'
                              ,_('INFO')
                              ,_('Copy "%s" to "%s"') % (self._path
                                                        ,self._clone
                                                        )
                              )
                for row in self._data:
                    try:
                        search = row[1].lower() + ' ' + row[2].lower()
                        itime = sh.Time(pattern='%Y-%m-%d %H:%M:%S')
                        itime._date = row[3]
                        timestamp = itime.timestamp()
                        row = (row[0],row[1],row[2],row[3],row[4],row[5]
                              ,row[6],row[7],row[8],row[9],row[10]
                              ,row[11],row[12],row[13],row[14],row[15]
                              ,search,timestamp
                              )
                        self.dbcw.execute ('insert into VIDEOS values \
                                            (?,?,?,?,?,?,?,?,?,?,?,?,?\
                                            ,?,?,?,?,?\
                                            )'
                                          ,row
                                          )
                    except (sqlite3.DatabaseError
                           ,sqlite3.OperationalError
                           ):
                        self.Success = False
                # This must be out of the loop
                if not self.Success:
                    sh.objs.mes ('DB.fill'
                                ,_('WARNING')
                                ,_('Database "%s" has failed!') \
                                % self._clone
                                )
            else:
                sh.log.append ('DB.fill'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('DB.fill'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def close(self):
        if self.Success:
            try:
                self.dbc.close()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.close'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('DB.close'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def closew(self):
        if self.Success:
            try:
                self.dbcw.close()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.closew'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._clone
                            )
        else:
            sh.log.append ('DB.closew'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



class Commands:
    
    def __init__(self):
        self._path  = '/home/pete/bin/Yatube/user/yatube.db'
        self._clone = '/tmp/yatube.db'
        
    def alter(self):
        sh.File(file=self._clone).delete()
        # Alter DB and add new columns 'SEARCH', 'TIMESTAMP'
        idb = DB (path  = self._path
                 ,clone = self._clone
                 )
        idb.connect()
        idb.connectw()
        idb.fetch()
        idb.create_table()
        idb.fill()
        idb.save()
        idb.close()
        idb.closew()
        
    def read_random(self):
        idb = DB (path  = self._path
                 ,clone = self._clone
                 )
        idb.connectw()
        idb.dbcw.execute ('select AUTHOR,TITLE,SEARCH,TIMESTAMP \
                           from VIDEOS where AUTHOR=?\
                          ',('kamikadzedead',)
                         )
        data = idb.dbcw.fetchone()
        if data:
            print('Author: "%s"'    % str(data[0]))
            print('Title: "%s"'     % str(data[1]))
            print('Search: "%s"'    % str(data[2]))
            print('Timestamp: "%s"' % str(data[3]))
        else:
            sh.log.append ('Commands.read_random'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        idb.closew()


if __name__ == '__main__':
    sh.objs.mes(Silent=1)
    commands = Commands()
    commands.read_random()
