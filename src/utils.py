#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import shared as sh
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')


class Clone:
    
    def __init__(self,path,clone):
        self._data   = ()
        self._path   = path
        self._clone  = clone
        self.Success = self._clone and sh.File(file=self._path).Success
        self.connect()
        self.connectw()
        
    def connect(self):
        if self.Success:
            try:
                self.db  = sqlite3.connect(self._path)
                self.dbc = self.db.cursor()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('Clone.connect'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('Clone.connect'
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
                sh.objs.mes ('Clone.connectw'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._clone
                            )
        else:
            sh.log.append ('Clone.connectw'
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
                sh.objs.mes ('Clone.fetch'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('Clone.fetch'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def create_table(self):
        if self.Success:
            try:
                # 17 columns by now
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
                                                       )'
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('Clone.create_table'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._clone
                            )
        else:
            sh.log.append ('Clone.create_table'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def copy(self):
        if self.Success:
            if self._data:
                sh.log.append ('Clone.copy'
                              ,_('INFO')
                              ,_('Copy "%s" to "%s"') % (self._path
                                                        ,self._clone
                                                        )
                              )
                for row in self._data:
                    try:
                        row = (row[0],row[1],row[2],row[3],row[4],row[5]
                              ,row[6],row[7],row[8],row[9],row[10]
                              ,row[11],row[12],row[13],row[14],row[15]
                              ,''
                              )
                        self.dbcw.execute ('insert into VIDEOS values \
                                            (?,?,?,?,?,?,?,?,?,?,?,?,?\
                                            ,?,?,?,?\
                                            )'
                                          ,row
                                          )
                    except (sqlite3.DatabaseError
                           ,sqlite3.OperationalError
                           ):
                        self.Success = False
                # This must be out of the loop
                if not self.Success:
                    sh.objs.mes ('Clone.copy'
                                ,_('WARNING')
                                ,_('Database "%s" has failed!') \
                                % self._clone
                                )
            else:
                sh.log.append ('Clone.copy'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Clone.copy'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def close(self):
        if self.Success:
            try:
                self.dbc.close()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('Clone.close'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('Clone.close'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def closew(self):
        if self.Success:
            try:
                self.dbcw.close()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('Clone.closew'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._clone
                            )
        else:
            sh.log.append ('Clone.closew'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )


if __name__ == '__main__':
    sh.objs.mes(Silent=1)
    path  = '/home/pete/bin/Yatube/user/yatube.db'
    clone = '/tmp/yatube.db'
    sh.File(file=clone).delete()
    # Clone DB and add new column 'SEARCH'
    clone = Clone(path=path,clone=clone)
    clone.fetch()
    clone.create_table()
    clone.copy()
    clone.close()
    clone.closew()
