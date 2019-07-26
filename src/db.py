#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import skl_shared.shared as sh
import gettext
import skl_shared.gettext_windows

skl_shared.gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')


class DB:
    
    def __init__(self,path):
        self.Success = True
        self._user   = ''
        self._path   = path
        self.connect()
        self.create_videos()
    
    def update_pause(self,video_id,pause=0):
        f = '[Yatube] db.DB.update_pause'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   PAUSE = ? \
                                                 where ID    = ?'
                                 ,(pause,video_id,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def update_ch_id(self,video_id,channel_id):
        f = '[Yatube] db.DB.update_ch_id'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   CHANID = ? \
                                                 where ID     = ?'
                                 ,(channel_id,video_id,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def feed_next(self,fdtime=0,limit=50):
        f = '[Yatube] db.DB.feed_next'
        if self.Success:
            try:
                self.dbc.execute ('select   ID from VIDEOS \
                                   where    FDTIME < ? \
                                   order by FDTIME desc,PTIME desc \
                                   limit ?'
                                 ,(fdtime,limit,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def feed_prev(self,fdtime=0,limit=50):
        f = '[Yatube] db.DB.feed_prev'
        if self.Success:
            try:
                ''' #note: videos are sorted from newest to oldest
                    (new fdtime > old fdtime), therefore, we cannot use
                    'desc' because otherwise the first page will be
                    returned each time we use 'feed_prev'. Thus, we
                    manually sort the return output.
                '''
                self.dbc.execute ('select   ID from VIDEOS \
                                   where    FDTIME > ? \
                                   order by FDTIME,PTIME limit ?'
                                 ,(fdtime,limit,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result][::-1]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fav_next(self,ftime=0,limit=50):
        f = '[Yatube] db.DB.fav_next'
        if self.Success:
            try:
                self.dbc.execute ('select   ID from VIDEOS \
                                   where    FTIME > ? and FTIME < ? \
                                   order by FTIME desc,PTIME desc \
                                   limit ?'
                                 ,(0,ftime,limit,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fav_prev(self,ftime=0,limit=50):
        f = '[Yatube] db.DB.fav_prev'
        if self.Success:
            try:
                ''' #note: videos are sorted from newest to oldest
                    (new ftime > old ftime), therefore, we cannot use
                    'desc' because otherwise the first page will be
                    returned each time we use 'fav_prev'. Thus, we
                    manually sort the return output.
                    #note: also sort by PTIME everywhere, because DB
                    inherits equal FTIME fields from previous versions,
                    and 'sqlite' may randomize output.
                '''
                self.dbc.execute ('select   ID from VIDEOS \
                                   where    FTIME > ? \
                                   order by FTIME,PTIME limit ?'
                                 ,(ftime,limit,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result][::-1]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def watch_prev(self,ltime=0,limit=50):
        f = '[Yatube] db.DB.watch_prev'
        if self.Success:
            try:
                ''' #note: videos are sorted from newest to oldest
                    (new ltime > old ltime), therefore, we cannot use
                    'desc' because otherwise the first page will be
                    returned each time we use 'watch_prev'. Thus, we
                    manually sort the return output.
                    #note: also sort by PTIME everywhere, because DB
                    inherits equal LTIME fields from previous versions,
                    and 'sqlite' may randomize output.
                '''
                self.dbc.execute ('select   ID from VIDEOS \
                                   where    LTIME > ? \
                                   order by LTIME,PTIME limit ?'
                                 ,(ltime,limit,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result][::-1]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def watch_next(self,ltime=0,limit=50):
        f = '[Yatube] db.DB.watch_next'
        if self.Success:
            try:
                self.dbc.execute ('select   ID from VIDEOS \
                                   where    LTIME > ? and LTIME < ? \
                                   order by LTIME desc,PTIME desc \
                                   limit ?'
                                 ,(0,ltime,limit,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def update_len(self,video_id,length):
        f = '[Yatube] db.DB.update_len'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   LENGTH = ? \
                                                 where ID     = ?'
                                 ,(length,video_id,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def update_play_id(self,video_id,play_id):
        f = '[Yatube] db.DB.update_play_id'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   PLAYID = ? \
                                                 where ID     = ?'
                                 ,(play_id,video_id,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def mark_later(self,video_id,ltime=0):
        f = '[Yatube] db.DB.mark_later'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   LTIME = ? \
                                                 where ID    = ?'
                                 ,(ltime,video_id,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def starred(self):
        f = '[Yatube] db.DB.starred'
        if self.Success:
            try:
                self.dbc.execute ('select   ID from VIDEOS \
                                   where    FTIME > 0 \
                                   order by FTIME desc,PTIME desc'
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def mark_starred(self,video_id,ftime=0):
        f = '[Yatube] db.DB.mark_starred'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   FTIME = ? \
                                                 where ID    = ?'
                                 ,(ftime,video_id,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fail(self,func,error):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self._path,error)
        sh.objs.mes(func,mes).warning()
    
    def ids(self):
        f = '[Yatube] db.DB.ids'
        if self.Success:
            try:
                self.dbc.execute('select ID from VIDEOS')
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def history_prev(self,dtime=0,limit=50):
        f = '[Yatube] db.DB.history_prev'
        if self.Success:
            try:
                ''' #note: videos are sorted from newest to oldest
                    (new dtime > old dtime), therefore, we cannot use
                    'desc' because otherwise the first page will be
                    returned each time we use 'history_prev'. Thus, we
                    manually sort the return output.
                '''
                self.dbc.execute ('select   ID from VIDEOS \
                                   where    DTIME > ? and DTIME > ? \
                                   order by DTIME,PTIME \
                                   limit ?'
                                 ,(0,dtime,limit,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result][::-1]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def history_next(self,dtime=0,limit=50):
        f = '[Yatube] db.DB.history_next'
        if self.Success:
            try:
                self.dbc.execute ('select   ID from VIDEOS \
                                   where    DTIME > ? and DTIME < ? \
                                   order by DTIME desc,PTIME desc \
                                   limit ?'
                                 ,(0,dtime,limit,)
                                 )
                result = self.dbc.fetchall()
                if result:
                    return [item[0] for item in result]
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def _filt1(self,timestamp):
        self.dbc.execute ('select   ID,AUTHOR,TITLE from VIDEOS \
                           where    PTIME >= ? \
                           order by AUTHOR,PTIME',(timestamp,)
                         )
                         
    def _filt2(self,timestamp):
        self.dbc.execute ('select ID,AUTHOR,TITLE from VIDEOS \
                           where DTIME = ? and PTIME >= ? \
                           order by AUTHOR,PTIME',(0,timestamp,)
                         )
    
    def _filt3(self,timestamp):
        self.dbc.execute ('select ID,AUTHOR,TITLE from VIDEOS \
                           where PTIME <= ? \
                           order by AUTHOR,PTIME',(timestamp,)
                         )
                         
    def _filt4(self,timestamp):
        self.dbc.execute ('select ID,AUTHOR,TITLE from VIDEOS \
                           where DTIME = ? and PTIME <= ? \
                           order by AUTHOR,PTIME',(0,timestamp,)
                         )
    
    def date_filter (self,timestamp
                    ,Newer=True,WithReady=False
                    ):
        f = '[Yatube] db.DB.date_filter'
        if self.Success:
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
        f = '[Yatube] db.DB.connect'
        if self.Success:
            try:
                self.db  = sqlite3.connect(self._path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def channel_videos(self,author):
        f = '[Yatube] db.DB.channel_videos'
        if self.Success:
            try:
                self.dbc.execute ('select ID from VIDEOS where AUTHOR=?'
                                 ,(author,)
                                 )
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def mark_downloaded(self,video_id,dtime):
        f = '[Yatube] db.DB.mark_downloaded'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   DTIME = ? \
                                                 where ID    = ?'
                                 ,(dtime,video_id,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_videos(self):
        f = '[Yatube] db.DB.create_videos'
        if self.Success:
            try:
                # 15 columns by now
                self.dbc.execute (
                    'create table if not exists VIDEOS (\
                     ID     text    \
                    ,PLAYID text    \
                    ,CHANID text    \
                    ,AUTHOR text    \
                    ,TITLE  text    \
                    ,DESC   text    \
                    ,SEARCH text    \
                    ,LENGTH integer \
                    ,PAUSE  integer \
                    ,IMAGE  binary  \
                    ,PTIME  float   \
                    ,DTIME  float   \
                    ,FTIME  float   \
                    ,LTIME  float   \
                    ,FDTIME float   \
                                                       )'
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def add_video(self,data):
        f = '[Yatube] db.DB.add_video'
        if self.Success:
            try:
                self.dbc.execute ('insert into VIDEOS values \
                                   (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                                 ,data
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def save(self):
        f = '[Yatube] db.DB.save'
        if self.Success:
            mes = _('Save "{}"').format(self._path)
            sh.objs.mes(f,mes,True).info()
            try:
                self.db.commit()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def get_video(self,video_id):
        ''' This is very slow (~0,28s per a video).
            Use 'self.get_videos' for a batch.
        '''
        f = '[Yatube] db.DB.get_video'
        if self.Success:
            try:
                self.dbc.execute ('select ID,PLAYID,CHANID,AUTHOR,TITLE\
                                         ,DESC,SEARCH,LENGTH,PAUSE\
                                         ,IMAGE,PTIME,DTIME,FTIME,LTIME\
                                         ,FDTIME\
                                   from   VIDEOS\
                                   where  ID = ?',(video_id,)
                                 )
                return self.dbc.fetchone()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_videos(self,ids):
        ''' For some reason, sqlite skips unknown IDs (no empty
            tuples), so we need to return ID as well in order not to
            mix up results.
        '''
        f = '[Yatube] db.DB.get_videos'
        if self.Success:
            if ids:
                try:
                    query = 'select ID,PLAYID,CHANID,AUTHOR,TITLE,DESC\
                                   ,SEARCH,LENGTH,PAUSE,IMAGE,PTIME\
                                   ,DTIME,FTIME,LTIME,FDTIME\
                             from   VIDEOS where ID in (%s)' \
                            % ','.join('?'*len(ids))
                    self.dbc.execute(query,ids)
                    result = self.dbc.fetchall()
                except Exception as e:
                    result = None
                    self.fail(f,e)
                # The data are fetched in a mixed order
                if result:
                    data = []
                    for vid in ids:
                        Found = False
                        for item in result:
                            if item[0] == vid:
                                Found = True
                                break
                        if Found:
                            data.append(item)
                        else:
                            data.append(())
                    return data
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)

    def close(self):
        f = '[Yatube] db.DB.close'
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
        f = '[Yatube] db.DB.print'
        if self.Success:
            ''' 'self.dbc.description' is 'None' without performing 
                'select' first
             '''
            if not Selected:
                self.dbc.execute('select * from VIDEOS limit ?',(5,))
            headers = [cn[0] for cn in self.dbc.description]
            rows    = self.dbc.fetchall()
            sh.lg.Table (headers = headers
                        ,rows    = rows
                        ,Shorten = Shorten
                        ,MaxRow  = MaxRow
                        ,MaxRows = MaxRows
                        ).print()
        else:
            sh.com.cancel(f)


if __name__ == '__main__':
    f = 'db.__main__'
    path = sh.lg.Home('yatube').add_config('yatube.db')
    idb = DB(path)
    ids = ['vjSohj-Iclc','0BXC2-zyujI','0nNrILS7OgE']
    result = idb.get_videos(ids)
    if result:
        dtimes = [item[10] for item in result if item[10]]
        print(dtimes)
    else:
        sh.com.empty(f)
    idb.close()
