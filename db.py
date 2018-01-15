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
                ''' 2 columns by now
                    Other potentially needed columns:
                    AUTHOR, text
                    IMAGE, binary: channel's image
                '''
                self.dbc.execute (
                    'create table if not exists CHANNELS (\
                     USER      text    \
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
                # 15 columns by now
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
                    ,IMAGE     binary  \
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
                                  (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data
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
                                    ,DISLIKES,RATING,IMAGE from VIDEOS \
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
                               ,message = _('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                                          % (str(mode)
                                            ,'VIDEOS, CHANNELS'
                                            )
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
    
    def get_channels(self,block=0):
        if self.Success:
            try:
                if block == -1:
                    self.dbc.execute ('select USER from CHANNELS')
                elif block == 0 or block == 1:
                    self.dbc.execute ('select USER from CHANNELS \
                                       where BLOCK = ?',(block,)
                                     )
                else:
                    self.Success = False
                    sg.Message ('DB.get_channels'
                               ,_('ERROR')
                               ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                               % (str(block),'-1, 0, 1')
                               )
                if self.Success:
                    result = self.dbc.fetchall()
                    if result:
                        return [item[0] for item in result if item]
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sg.Message ('DB.get_channels'
                           ,_('WARNING')
                           ,_('Database "%s" has failed!') % self._path
                           )
        else:
            sh.log.append ('DB.get_channels'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def add_channel(self,data):
        if self.Success:
            try:
                self.dbc.execute ('insert into CHANNELS values (?,?)'
                                 ,data
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sg.Message ('DB.add_channel'
                           ,_('WARNING')
                           ,_('Database "%s" has failed!') % self._path
                           )
        else:
            sh.log.append ('DB.add_channel'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def block_channels(self,channels,block=1):
        if self.Success:
            try:
                self.dbc.execute ('update CHANNELS set BLOCK = ? \
                                   where USER in ?',(block,channels,)
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sg.Message ('DB.block_channels'
                           ,_('WARNING')
                           ,_('Database "%s" has failed!') % self._path
                           )
        else:
            sh.log.append ('DB.block_channels'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def zzz(self):
        pass


if __name__ == '__main__':
    pass
