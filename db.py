#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import shared    as sh
import sharedGUI as sg
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','./locale')


class DB:
    
    def __init__(self):
        self.Success = True
        self._user   = ''
        self._path   = sh.objs.pdir().add('yatube.db')
        self.db      = sqlite3.connect(self._path)
        self.dbc     = self.db.cursor()
        self.create_channels()
        self.create_videos()
    
    def create_channels(self):
        if self.Success:
            try:
                # 3 columns by now
                self.dbc.execute (
                    'create table if not exists CHANNELS (\
                     USER      text    \
                    ,AUTHOR    text    \
                    ,BLOCK     boolean \
                                                         )'
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sg.Message ('DB.create_channels'
                           ,_('WARNING')
                           ,_('Database "%s" has failed!') % self._path
                           )
        else:
            sh.log.append ('DB.create_channels'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def create_videos(self):
        if self.Success:
            try:
                # 14 columns by now
                self.dbc.execute (
                    'create table if not exists VIDEOS (\
                     ROOTURL   text    \
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
                    ,BLOCK     boolean \
                    ,IGNORE    boolean \
                                                       )'
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sg.Message ('DB.create_videos'
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
                                  (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sg.Message ('DB.add_video'
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
                sg.Message ('DB.save'
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
                                    ,DISLIKES,RATING from VIDEOS \
                              where ROOTURL = ?',(url,))
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
                sg.Message ('DB.close'
                           ,_('WARNING')
                           ,_('Database "%s" has failed!') % self._path
                           )
        else:
            sh.log.append ('DB.close'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def print (self,Selected=False,Shorten=False
              ,MaxRow=20,MaxRows=20,mode='VIDEOS'
              ):
        if self.Success:
            ''' 'self.dbc.description' is 'None' without performing 
                'select' first
             '''
            if not Selected:
                if mode == 'VIDEOS':
                    self.dbc.execute('select * from VIDEOS')
                elif mode == 'CHANNELS':
                    self.dbc.execute('select * from CHANNELS')
                else:
                    sg.Message (func    = 'DB.print'
                               ,level   = _('ERROR')
                               ,message = _('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') % (str(mode),'VIDEOS, CHANNELS')
                               )
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
