#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import shared as sh
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','./locale')


class DB:
    
    def __init__(self,Silent=False):
        if Silent:
            self.mesfc = sh.Log().append
        else:
            import sharedGUI as sg
            self.mesfc = sg.Message
        self.Success = True
        self._user   = ''
        self._path   = sh.objs.pdir().add('yatube.db')
        self.db      = sqlite3.connect(self._path)
        self.dbc     = self.db.cursor()
        self.create_videos()
    
    def create_videos(self):
        if self.Success:
            try:
                # 16 columns by now
                self.dbc.execute (
                    'create table if not exists VIDEOS (\
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
                                                       )'
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                self.mesfc ('DB.create_videos'
                           ,_('WARNING')
                           ,_('Database "%s" has failed!') % self._path
                           )
        else:
            sh.log.append ('DB.create_videos'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def add_video(self,data):
        if self.Success:
            try:
                self.dbc.execute ('insert into VIDEOS values \
                                  (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                                 ,data
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                self.mesfc ('DB.add_video'
                           ,_('WARNING')
                           ,_('Database "%s" has failed!') % self._path
                           )
        else:
            sh.log.append ('DB.add_video'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def save(self):
        if self.Success:
            try:
                self.db.commit()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                self.mesfc ('DB.save'
                           ,_('WARNING')
                           ,_('Database "%s" has failed!') % self._path
                           )
        else:
            sh.log.append ('DB.save'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def get_video(self,url):
        if self.Success:
            self.dbc.execute('select AUTHOR,TITLE,DATE,CATEGORY,DESC \
                                    ,DURATION,LENGTH,VIEWS,LIKES \
                                    ,DISLIKES,RATING,IMAGE,READY \
                              from   VIDEOS \
                              where  URL = ?',(url,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.get_video'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def close(self):
        if self.Success:
            try:
                self.dbc.close()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                self.mesfc ('DB.close'
                           ,_('WARNING')
                           ,_('Database "%s" has failed!') % self._path
                           )
        else:
            sh.log.append ('DB.close'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def print (self,Selected=False,Shorten=False
              ,MaxRow=20,MaxRows=20
              ):
        if self.Success:
            ''' 'self.dbc.description' is 'None' without performing 
                'select' first
             '''
            if not Selected:
                self.dbc.execute('select * from VIDEOS')
            headers = [cn[0] for cn in self.dbc.description]
            rows    = self.dbc.fetchall()
            sh.Table (headers = headers
                     ,rows    = rows
                     ,Shorten = Shorten
                     ,MaxRow  = MaxRow
                     ,MaxRows = MaxRows
                     ).print()
        else:
            sh.log.append ('DB.print'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )


if __name__ == '__main__':
    pass
