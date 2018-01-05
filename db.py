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
                          
    def reset(self,user):
        self._user = user
    
    def add_video(self,data):
        if self.Success:
            try:
                self.dbc.execute ('insert into VIDEOS values \
                                  (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data
                                 )
            except sqlite3.OperationalError:
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
                          
    def close(self):
        if self.Success:
            try:
                self.dbc.close()
            except sqlite3.OperationalError:
                self.Success = False
                sg.Message ('DB.create_videos'
                           ,_('WARNING')
                           ,_('Database "%s" has failed!') % self._path
                           )
        else:
            sh.log.append ('DB.close'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )


if __name__ == '__main__':
    db = DB()
    '''
    ROOTURL   text    \
                    ,AUTHOR    text    \
                    ,TITLE     text    \
                    ,DATE      text    \
                    ,CATEGORY  text    \
                    ,DESC      text    \
                    ,DURATION  text    \
                    ,VIEWS     integer \
                    ,LIKES     integer \
                    ,DISLIKES  integer \
                    ,RATING    float   \
                    ,BLOCK     boolean \
                    ,IGNORE    boolean \
    '''
    rooturl = 
    user = ''
    db.add_video(data)
    db.close()
