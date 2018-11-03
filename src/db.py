#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import shared as sh
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')


class DB:
    
    def __init__(self,path):
        self.Success = True
        self._user   = ''
        self._path   = path
        self.connect()
        self.create_videos()
        
    def feed(self):
        f = 'db.DB.feed'
        if self.Success:
            try:
                self.dbc.execute ('select   URL from VIDEOS \
                                   where    IGNORE = ? \
                                   order by TIMESTAMP desc'
                                 ,(False,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def mark_later(self,video_id,Later=True):
        f = 'db.DB.mark_later'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   LATER = ? \
                                                 where URL   = ?'
                                 ,(Later,video_id,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def watchlist(self):
        f = 'db.DB.watchlist'
        if self.Success:
            try:
                self.dbc.execute ('select   URL from VIDEOS \
                                   where    LATER = ? \
                                   order by TIMESTAMP desc'
                                 ,(True,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def starred(self):
        f = 'db.DB.starred'
        if self.Success:
            try:
                self.dbc.execute ('select   URL from VIDEOS \
                                   where    FAV = ? \
                                   order by DTIME desc, \
                                            TIMESTAMP desc'
                                 ,(True,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def mark_starred(self,video_id,Starred=True):
        f = 'db.DB.mark_starred'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   FAV = ? \
                                                 where URL = ?'
                                 ,(Starred,video_id,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fail(self,func,error):
        self.Success = False
        sh.objs.mes (func
                    ,_('WARNING')
                    ,_('Database "%s" has failed!\n\nDetails: %s') \
                    % (self._path,str(error))
                    )
    
    def urls(self):
        f = 'db.DB.urls'
        if self.Success:
            try:
                self.dbc.execute('select URL from VIDEOS')
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def downloaded(self):
        f = 'db.DB.downloaded'
        if self.Success:
            try:
                self.dbc.execute ('select   URL from VIDEOS \
                                   where    DTIME > ? \
                                   order by DTIME desc, \
                                            TIMESTAMP desc'
                                 ,(0,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def new_videos(self,timestamp,authors):
        f = 'db.DB.new_videos'
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
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def _filt1(self,timestamp):
        self.dbc.execute ('select URL,AUTHOR,TITLE,DATE from VIDEOS \
                           where TIMESTAMP >= ? \
                           order by AUTHOR,TIMESTAMP',(timestamp,)
                         )
                         
    def _filt2(self,timestamp):
        self.dbc.execute ('select URL,AUTHOR,TITLE,DATE from VIDEOS \
                           where DTIME = ? and TIMESTAMP >= ? \
                           order by AUTHOR,TIMESTAMP',(0,timestamp,)
                         )
    
    def _filt3(self,timestamp):
        self.dbc.execute ('select URL,AUTHOR,TITLE,DATE from VIDEOS \
                           where TIMESTAMP <= ? \
                           order by AUTHOR,TIMESTAMP',(timestamp,)
                         )
                         
    def _filt4(self,timestamp):
        self.dbc.execute ('select URL,AUTHOR,TITLE,DATE from VIDEOS \
                           where DTIME = ? and TIMESTAMP <= ? \
                           order by AUTHOR,TIMESTAMP',(0,timestamp,)
                         )
    
    def date_filter (self,timestamp
                    ,Newer=True,WithReady=False
                    ):
        f = 'db.DB.date_filter'
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
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def connect(self):
        f = 'db.DB.connect'
        if self.Success:
            try:
                self.db  = sqlite3.connect(self._path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def channel_videos(self,author):
        f = 'db.DB.channel_videos'
        if self.Success:
            try:
                self.dbc.execute ('select URL from VIDEOS where AUTHOR=?'
                                 ,(author,)
                                 )
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def mark_downloaded(self,video_id,dtime):
        f = 'db.DB.mark_downloaded'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   DTIME = ? \
                                                 where URL   = ?'
                                 ,(dtime,video_id,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_videos(self):
        f = 'db.DB.create_videos'
        if self.Success:
            try:
                # 20 columns by now
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
                    ,SEARCH    text    \
                    ,TIMESTAMP float   \
                    ,DTIME     float   \
                    ,FAV       boolean \
                    ,LATER     boolean \
                                                       )'
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def add_video(self,data):
        f = 'db.DB.add_video'
        if self.Success:
            try:
                self.dbc.execute ('insert into VIDEOS values \
                                   (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?\
                                   ,?,? \
                                   )'
                                 ,data
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def save(self):
        f = 'db.DB.save'
        if self.Success:
            sh.log.append (f,_('INFO')
                          ,_('Save "%s"') % self._path
                          )
            try:
                self.db.commit()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def get_video(self,video_id):
        ''' This is very slow (~0,28s per a video => ~3s per a channel).
            Use 'self.get_videos' for a batch.
        '''
        f = 'db.DB.get_video'
        if self.Success:
            try:
                self.dbc.execute ('select AUTHOR,TITLE,DATE,CATEGORY,DESC \
                                         ,DURATION,LENGTH,VIEWS,LIKES \
                                         ,DISLIKES,RATING,IMAGE,SEARCH\
                                         ,TIMESTAMP,DTIME \
                                   from   VIDEOS \
                                   where  URL = ?',(video_id,)
                                 )
                return self.dbc.fetchone()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_videos(self,urls):
        ''' For some reason, sqlite skips unknown URLs (no empty
            tuples), so we need to return URL as well in order not to
            mix up results.
        '''
        f = 'db.DB.get_videos'
        if self.Success:
            if urls:
                try:
                    self.dbc.execute ('select URL,AUTHOR,TITLE,DATE\
                                             ,CATEGORY,DESC,DURATION\
                                             ,LENGTH,VIEWS,LIKES\
                                             ,DISLIKES,RATING,IMAGE\
                                             ,SEARCH,TIMESTAMP,DTIME\
                                       from   VIDEOS \
                                       where  URL in %s' \
                                     % str(tuple(urls))
                                     )
                    result = self.dbc.fetchall()
                except Exception as e:
                    result = None
                    self.fail(f,e)
                # The data are fetched in a mixed order
                if result:
                    data = []
                    for url in urls:
                        Found = False
                        for item in result:
                            if item[0] == url:
                                Found = True
                                break
                        if Found:
                            data.append(item[1:])
                        else:
                            data.append(())
                    return data
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)

    def close(self):
        f = 'db.DB.close'
        if self.Success:
            try:
                self.dbc.close()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def print (self,Selected=False,Shorten=False
              ,MaxRow=20,MaxRows=20
              ):
        f = 'db.DB.print'
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
            sh.com.cancel(f)


if __name__ == '__main__':
    path = sh.Home('yatube').add_config('yatube.db')
    idb = DB(path)
    urls = idb.downloaded()
    urls = list(urls)
    for i in range(len(urls)):
        urls[i] = str(i) + ': ' + urls[i]
    print('\n'.join(urls))
    idb.close()
