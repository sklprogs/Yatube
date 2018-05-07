#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import shared as sh
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')


class DB:
    
    def __init__(self):
        self.values()
        self.connect()
        self.create_videos()
        
    def downloaded(self,limit=50):
        if self.Success:
            try:
                self.dbc.execute ('select URL from VIDEOS \
                                   where READY = ?\
                                   order by TIMESTAMP desc limit ?'
                                 ,(True,limit,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.downloaded'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('DB.downloaded'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def new_videos(self,timestamp,authors):
        if self.Success:
            try:
                query = 'select   URL from VIDEOS \
                         where    AUTHOR in (%s) and TIMESTAMP >= %f\
                         order by AUTHOR,TIMESTAMP' \
                        % (','.join('?'*len(authors)),timestamp)
                self.dbc.execute(query,authors)
                result = self.dbc.fetchall()
                if result:
                    #todo: should we return a list or a tuple?
                    return [row[0] for row in result]
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.new_videos'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('DB.new_videos'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def _filt1(self,timestamp):
        self.dbc.execute ('select URL,AUTHOR,TITLE,DATE from VIDEOS \
                           where TIMESTAMP >= ? \
                           order by AUTHOR,TIMESTAMP',(timestamp,)
                         )
                         
    def _filt2(self,timestamp):
        self.dbc.execute ('select URL,AUTHOR,TITLE,DATE from VIDEOS \
                           where READY = ? and TIMESTAMP >= ? \
                           order by AUTHOR,TIMESTAMP',(False,timestamp,)
                         )
    
    def _filt3(self,timestamp):
        self.dbc.execute ('select URL,AUTHOR,TITLE,DATE from VIDEOS \
                           where TIMESTAMP <= ? \
                           order by AUTHOR,TIMESTAMP',(timestamp,)
                         )
                         
    def _filt4(self,timestamp):
        self.dbc.execute ('select URL,AUTHOR,TITLE,DATE from VIDEOS \
                           where READY = ? and TIMESTAMP <= ? \
                           order by AUTHOR,TIMESTAMP',(False,timestamp,)
                         )
    
    def date_filter (self,timestamp
                    ,Newer=True,WithReady=False
                    ):
        if self.Success:
            #todo (?): BLOCK, IGNORE
            try:
                if Newer:
                    if WithReady:
                        self._filt1(timestamp)
                    else:
                        self._filt2(timestamp)
                else:
                    if WithReady:
                        self._filt3(timestamp)
                    else:
                        self._filt4(timestamp)
                return self.dbc.fetchall()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.date_filter'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('DB.date_filter'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def values(self):
        self.Success = True
        self._user   = ''
        self._path   = sh.objs.pdir().add('..','user','yatube.db')
        
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
    
    def channel_videos(self,author):
        if self.Success:
            try:
                self.dbc.execute ('select URL from VIDEOS where AUTHOR=?'
                                 ,(author,)
                                 )
                return self.dbc.fetchall()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.channel_videos'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('DB.channel_videos'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def mark_downloaded(self,url,Ready=True):
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set READY=? where URL=?'
                                 ,(Ready,url,)
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.mark_downloaded'
                            ,_('WARNING')
                            ,_('Database "%s" has failed!') % self._path
                            )
        else:
            sh.log.append ('DB.mark_downloaded'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def create_videos(self):
        if self.Success:
            try:
                # 18 columns by now
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
                    ,SEARCH    text    \
                    ,TIMESTAMP float   \
                                                       )'
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.create_videos'
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
                                  (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                                 ,data
                                 )
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.add_video'
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
            sh.log.append ('DB.save'
                          ,_('INFO')
                          ,_('Save "%s"') % self._path
                          )
            try:
                self.db.commit()
            except (sqlite3.DatabaseError,sqlite3.OperationalError):
                self.Success = False
                sh.objs.mes ('DB.save'
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
                                    ,DISLIKES,RATING,IMAGE,READY,SEARCH\
                                    ,TIMESTAMP \
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
                sh.objs.mes ('DB.close'
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
    idb = DB()
    urls = idb.downloaded()
    urls = list(urls)
    for i in range(len(urls)):
        urls[i] = str(i) + ': ' + urls[i]
    print('\n'.join(urls))
    idb.close()
