#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import skl_shared.shared as sh
from skl_shared.localize import _


class DB:
    
    def __init__(self,path):
        self.Success = True
        self.user = ''
        self.path = path
        self.connect()
        self.create_videos()
    
    def update_pause(self,videoid,pause=0):
        f = '[Yatube] db.DB.update_pause'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   PAUSE = ? \
                                                 where ID = ?'
                                 ,(pause,videoid,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def update_ch_id(self,videoid,channel_id):
        f = '[Yatube] db.DB.update_ch_id'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   CHANID = ? \
                                                 where ID = ?'
                                 ,(channel_id,videoid,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_feed_next(self,fdtime=0,limit=50):
        f = '[Yatube] db.DB.get_feed_next'
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
    
    def get_feed_prev(self,fdtime=0,limit=50):
        f = '[Yatube] db.DB.get_feed_prev'
        if self.Success:
            try:
                ''' #NOTE: videos are sorted from newest to oldest
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
    
    def get_fav_next(self,ftime=0,limit=50):
        f = '[Yatube] db.DB.get_fav_next'
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
    
    def get_fav_prev(self,ftime=0,limit=50):
        f = '[Yatube] db.DB.get_fav_prev'
        if self.Success:
            try:
                ''' #NOTE: videos are sorted from newest to oldest
                    (new ftime > old ftime), therefore, we cannot use
                    'desc' because otherwise the first page will be
                    returned each time we use 'fav_prev'. Thus, we
                    manually sort the return output.
                    #NOTE: also sort by PTIME everywhere, because DB
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
    
    def get_watch_prev(self,ltime=0,limit=50):
        f = '[Yatube] db.DB.get_watch_prev'
        if self.Success:
            try:
                ''' #NOTE: videos are sorted from newest to oldest
                    (new ltime > old ltime), therefore, we cannot use
                    'desc' because otherwise the first page will be
                    returned each time we use 'watch_prev'. Thus, we
                    manually sort the return output.
                    #NOTE: also sort by PTIME everywhere, because DB
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
    
    def get_watch_next(self,ltime=0,limit=50):
        f = '[Yatube] db.DB.get_watch_next'
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
    
    def update_len(self,videoid,length):
        f = '[Yatube] db.DB.update_len'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   LENGTH = ? \
                                                 where ID = ?'
                                 ,(length,videoid,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def update_playid(self,videoid,playid):
        f = '[Yatube] db.DB.update_playid'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   PLAYID = ? \
                                                 where ID = ?'
                                 ,(playid,videoid,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def mark_later(self,videoid,ltime=0.0):
        f = '[Yatube] db.DB.mark_later'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   LTIME = ? \
                                                 where ID = ?'
                                 ,(ltime,videoid,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_starred(self):
        f = '[Yatube] db.DB.get_starred'
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
    
    def mark_starred(self,videoid,ftime=0.0):
        f = '[Yatube] db.DB.mark_starred'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   FTIME = ? \
                                                 where ID = ?'
                                 ,(ftime,videoid,)
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fail(self,func,error):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.path,error)
        sh.objs.get_mes(func,mes).show_warning()
    
    def get_ids(self):
        f = '[Yatube] db.DB.get_ids'
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
    
    def get_history_prev(self,dtime=0,limit=50):
        f = '[Yatube] db.DB.get_history_prev'
        if self.Success:
            try:
                ''' #NOTE: videos are sorted from newest to oldest
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
    
    def get_history_next(self,dtime=0,limit=50):
        f = '[Yatube] db.DB.get_history_next'
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
    
    def _run_filt1(self,timestamp):
        self.dbc.execute ('select   ID,AUTHOR,TITLE from VIDEOS \
                           where    PTIME >= ? \
                           order by AUTHOR,PTIME',(timestamp,)
                         )
                         
    def _run_filt2(self,timestamp):
        self.dbc.execute ('select ID,AUTHOR,TITLE from VIDEOS \
                           where DTIME = ? and PTIME >= ? \
                           order by AUTHOR,PTIME',(0,timestamp,)
                         )
    
    def _run_filt3(self,timestamp):
        self.dbc.execute ('select ID,AUTHOR,TITLE from VIDEOS \
                           where PTIME <= ? \
                           order by AUTHOR,PTIME',(timestamp,)
                         )
                         
    def _run_filt4(self,timestamp):
        self.dbc.execute ('select ID,AUTHOR,TITLE from VIDEOS \
                           where DTIME = ? and PTIME <= ? \
                           order by AUTHOR,PTIME',(0,timestamp,)
                         )
    
    def filter_date (self,timestamp
                    ,Newer=True,WithReady=False
                    ):
        f = '[Yatube] db.DB.filter_date'
        if self.Success:
            try:
                if Newer:
                    if WithReady:
                        self._run_filt1(timestamp)
                    else:
                        self._run_filt2(timestamp)
                else:
                    if WithReady:
                        self._run_filt3(timestamp)
                    else:
                        self._run_filt4(timestamp)
                return self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def connect(self):
        f = '[Yatube] db.DB.connect'
        if self.Success:
            try:
                self.db = sqlite3.connect(self.path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def get_channel_videos(self,author):
        f = '[Yatube] db.DB.get_channel_videos'
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
    
    def mark_downloaded(self,videoid,dtime):
        f = '[Yatube] db.DB.mark_downloaded'
        if self.Success:
            try:
                self.dbc.execute ('update VIDEOS set   DTIME = ? \
                                                 where ID = ?'
                                 ,(dtime,videoid,)
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
            mes = _('Save "{}"').format(self.path)
            sh.objs.get_mes(f,mes,True).show_info()
            try:
                self.db.commit()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def get_video(self,videoid):
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
                                   where  ID = ?',(videoid,)
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
                sh.com.rep_empty(f)
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
                'select' first.
             '''
            if not Selected:
                self.dbc.execute('select * from VIDEOS limit ?',(5,))
            headers = [cn[0] for cn in self.dbc.description]
            rows = self.dbc.fetchall()
            sh.Table (headers = headers
                     ,rows = rows
                     ,Shorten = Shorten
                     ,MaxRow = MaxRow
                     ,MaxRows = MaxRows
                     ).print()
        else:
            sh.com.cancel(f)


if __name__ == '__main__':
    f = 'db.__main__'
    path = sh.Home('yatube').add_config('yatube.db')
    idb = DB(path)
    ids = ['vjSohj-Iclc','0BXC2-zyujI','0nNrILS7OgE']
    result = idb.get_videos(ids)
    if result:
        dtimes = [item[10] for item in result if item[10]]
        print(dtimes)
    else:
        sh.com.rep_empty(f)
    idb.close()
