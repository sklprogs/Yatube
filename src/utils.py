#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sqlite3
import html
import skl_shared.shared as sh
from skl_shared.localize import _


class DB:
    
    def __init__(self,path,clone):
        self.data = ()
        self.path = path
        self.clone = clone
        self.Success = self.clone and sh.File(self.path).Success
    
    def get_dtime(self):
        f = '[Yatube] utils.DB.get_dtime'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'select DTIME from VIDEOS where DTIME > 0 order by DTIME'
        try:
            self.dbc.execute(query)
            return self.dbc.fetchall()
        except Exception as e:
            self.fail(f, e)
    
    def get_videos(self):
        f = '[Yatube] utils.DB.get_videos'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'select ID from VIDEOS'
        try:
            self.dbc.execute(query)
            return self.dbc.fetchall()
        except Exception as e:
            self.fail(f, e)
    
    def get_older(self,dtime):
        f = '[Yatube] utils.DB.get_older'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'select ID from VIDEOS where DTIME > 0 and DTIME < ?'
        try:
            self.dbc.execute(query, (dtime,))
            return self.dbc.fetchall()
        except Exception as e:
            self.fail(f, e)
    
    def get_watched(self):
        f = '[Yatube] utils.DB.get_watched'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'select LENGTH from VIDEOS where DTIME > 0'
        try:
            self.dbc.execute(query)
            return self.dbc.fetchall()
        except Exception as e:
            self.fail(f, e)
    
    def vacuumize(self):
        f = '[Yatube] utils.DB.vacuumize'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.dbcw.execute('vacuum')
        except Exception as e:
            self.fail_clone(f, e)
    
    def update_unescape(self,id_,author,title,search):
        f = '[Yatube] utils.DB.update_unescape'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'update VIDEOS set AUTHOR = ?,TITLE = ?,SEARCH = ? where ID = ?'
        try:
            self.dbcw.execute(query, (author, title, search, id_))
        except Exception as e:
            self.fail_clone(f, e)
    
    def get_unescape(self):
        f = '[Yatube] utils.DB.get_unescape'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'select ID,AUTHOR,TITLE,SEARCH from VIDEOS'
        try:
            self.dbcw.execute(query)
            return self.dbcw.fetchall()
        except Exception as e:
            self.fail_clone(f, e)
    
    def del_author(self,author):
        f = '[Yatube] utils.DB.del_author'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'delete from VIDEOS where AUTHOR = ?'
        try:
            self.dbcw.execute(query, (author,))
        except Exception as e:
            self.fail_clone(f, e)
    
    def fetch_ftime(self):
        f = '[Yatube] utils.DB.fetch_ftime'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'select ID,FTIME from VIDEOS where FTIME > ? \
                 order by FTIME desc,PTIME desc'
        try:
            self.dbcw.execute(query, (0,))
            return self.dbcw.fetchall()
        except Exception as e:
            self.fail_clone(f, e)
    
    def update_ftime(self, id_, ftime):
        f = '[Yatube] utils.DB.update_ftime'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'update VIDEOS set FTIME = ? where ID = ?'
        try:
            self.dbcw.execute(query, (ftime, id_,))
        except Exception as e:
            self.fail_clone(f, e)
    
    def update_ltime(self, id_, ltime):
        f = '[Yatube] utils.DB.update_ltime'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'update VIDEOS set LTIME = ? where ID = ?'
        try:
            self.dbcw.execute(query, (ltime, id_,))
        except Exception as e:
            self.fail_clone(f, e)
    
    def fetch_ltime(self):
        f = '[Yatube] utils.DB.fetch_ltime'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'select ID,LTIME from VIDEOS where LTIME > ? \
                 order by LTIME desc,PTIME desc'
        try:
            self.dbcw.execute(query, (0,))
            return self.dbcw.fetchall()
        except Exception as e:
            self.fail_clone(f, e)
    
    def fail(self, f, e):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.path, e)
        sh.objs.get_mes(f, mes).show_warning()
    
    def fail_clone(self, f, e):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.clone, e)
        sh.objs.get_mes(f, mes).show_warning()
    
    def down_markw(self):
        f = '[Yatube] utils.DB.down_markw'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'update VIDEOS set DTIME = ? where DTIME > ?'
        try:
            self.dbcw.execute(query, (0, 0,))
        except Exception as e:
            self.fail_clone(f, e)
    
    def savew(self):
        f = '[Yatube] utils.DB.savew'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.dbw.commit()
        except Exception as e:
            self.fail_clone(f, e)
        
    def connect(self):
        f = '[Yatube] utils.DB.connect'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.db = sqlite3.connect(self.path)
            self.dbc = self.db.cursor()
        except Exception as e:
            self.fail(f, e)
                          
    def connectw(self):
        f = '[Yatube] utils.DB.connectw'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.dbw = sqlite3.connect(self.clone)
            self.dbcw = self.dbw.cursor()
        except Exception as e:
            self.fail_clone(f, e)
    
    def fetch(self):
        f = '[Yatube] utils.DB.fetch'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = _('Fetch data')
        sh.objs.get_mes(f, mes, True).show_info()
        # 12 columns
        query = 'select ID,PLAYID,CHANID,AUTHOR,TITLE,LENGTH,PAUSE,PTIME,DTIME\
                ,FTIME,LTIME,FDTIME from VIDEOS'
        try:
            self.dbc.execute(query)
            self.data = self.dbc.fetchall()
        except Exception as e:
            self.fail(f, e)
    
    def create_table(self):
        f = '[Yatube] utils.DB.create_table'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            # Create 13 columns
            self.dbcw.execute (
                'create table VIDEOS (\
                 ID     text    \
                ,PLAYID text    \
                ,CHANID text    \
                ,AUTHOR text    \
                ,TITLE  text    \
                ,SEARCH text    \
                ,LENGTH integer \
                ,PAUSE  integer \
                ,PTIME  float   \
                ,DTIME  float   \
                ,FTIME  float   \
                ,LTIME  float   \
                ,FDTIME float   \
                                     )'
                              )
        except Exception as e:
            self.fail_clone(f, e)
    
    def fill(self):
        f = '[Yatube] utils.DB.fill'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.data:
            sh.com.rep_empty(f)
            return
        mes = _('Copy "{}" to "{}"').format(self.path, self.clone)
        sh.objs.get_mes(f, mes, True).show_info()
        query = 'insert into VIDEOS values (?,?,?,?,?,?,?,?,?,?,?,?,?)'
        for row in self.data:
            try:
                id_ = row[0]
                playid = row[1]
                chanid = row[2]
                author = row[3]
                title = row[4]
                length = row[5]
                pause = row[6]
                ptime = row[7]
                dtime = row[8]
                ftime = row[9]
                ltime = row[10]
                fdtime = row[11]
                search = author.lower() + ' ' + title.lower()
                row = (id_,playid,chanid,author,title,search,length,pause
                      ,ptime,dtime,ftime,ltime,fdtime
                      )
                self.dbcw.execute(query, row)
            except Exception as e:
                self.Success = False
                self.fail(f, e)
                break
                          
    def close(self):
        f = '[Yatube] utils.DB.close'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.dbc.close()
        except Exception as e:
            self.fail(f, e)
                          
    def closew(self):
        f = '[Yatube] utils.DB.closew'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.dbcw.close()
        except Exception as e:
            self.fail_clone(f, e)
                          
    def repair_urls(self):
        f = '[Yatube] utils.DB.repair_urls'
        if not self.Success:
            sh.com.cancel(f)
            return
        query = 'select URL from VIDEOS where length(URL) > 11'
        uquery = 'update VIDEOS set URL = ? where URL = ?'
        self.dbcw.execute(query)
        result = self.dbcw.fetchall()
        if not result:
            sh.com.rep_lazy(f)
            return
        result = list(result)
        result = [item[0] for item in result]
        for item in result:
            old_item = item
            item = item.replace('ttps://www.youtube.com/watch?v=', '')
            item = item.replace('https://youtu.be/', '')
            item = item.replace('https://m.youtube.com/', '')
            item = item.replace('youtube.com/watch?v=', '')
            item = item.replace('watch?v=', '')
            item = item.replace('?t=118', '')
            mes = f'"{old_item}" -> "{item}"'
            sh.objs.get_mes(f, mes, True).show_info()
            try:
                self.dbcw.execute(uquery, (item, old_item,))
            except Exception as e:
                self.fail_clone(f, e)



class Commands:
    
    def __init__(self):
        self.path = '/home/pete/.config/yatube/yatube.db'
        self.clone = '/tmp/yatube.db'

    def _count(self, videos):
        if not videos:
            return 0
        videos = len(videos)
        return sh.com.set_figure_commas(videos)
    
    def show_stat(self):
        f = '[Yatube] utils.Commands.show_stat'
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connect()
        videos = idb.get_videos()
        watched = idb.get_watched()
        idb.close()
        mes = []
        sub = _('Number of videos: {}')
        sub = sub.format(self._count(videos))
        mes.append(sub)
        sub = _('Number of watched videos: {}')
        sub = sub.format(self._count(watched))
        mes.append(sub)
        if watched:
            length = sum([item[0] for item in watched])
            length = sh.com.get_human_time(length)
        else:
            length = 0
        sub = _('Total length of watched videos: {}').format(length)
        mes.append(sub)
        mes = '\n'.join(mes)
        sh.objs.get_mes(f, mes).show_info()
        
    def unescape(self):
        f = '[Yatube] utils.Commands.unescape'
        sh.File(self.path,self.clone).copy()
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connectw()
        data = idb.get_unescape()
        if not data:
            sh.com.rep_empty(f)
            idb.closew()
            return
        ids = []
        authors = []
        titles = []
        search = []
        mes = _('Get data')
        sh.objs.get_mes(f, mes, True).show_info()
        for item in data:
            ids.append(item[0])
            authors.append(item[1])
            titles.append(item[2])
            search.append(item[3])
        mes = _('Process data')
        sh.objs.get_mes(f,mes,True).show_info()
        for i in range(len(ids)):
            if authors[i] != html.unescape(authors[i]) \
            or titles[i] != html.unescape(titles[i]) \
            or search[i] != html.unescape(search[i]):
                mes = _('Update {}').format(ids[i])
                sh.objs.get_mes(f, mes, True).show_info()
                tauthor = html.unescape(authors[i])
                ttitle = html.unescape(titles[i])
                tsearch = html.unescape(search[i])
                idb.update_unescape(ids[i], tauthor, ttitle, tsearch)
        idb.savew()
        idb.closew()
    
    def del_author(self, author):
        sh.File(self.path, self.clone).copy()
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connectw()
        idb.del_author(author)
        idb.savew()
        idb.closew()
    
    def repair_urls(self):
        f = '[Yatube] utils.Commands.repair_urls'
        Success = sh.File (file = self.path
                          ,dest = self.clone
                          ,Rewrite = True
                          ).copy()
        if not Success:
            sh.com.cancel(f)
            return
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connectw()
        idb.repair_urls()
        idb.savew()
        idb.closew()
    
    def down_markw(self):
        f = '[Yatube] utils.Commands.down_markw'
        Success = sh.File (file = self.path
                          ,dest = self.clone
                          ,Rewrite = True
                          ).copy()
        if not Success:
            sh.com.cancel(f)
            return
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connectw()
        idb.down_markw()
        idb.savew()
        idb.closew()
    
    def alter(self):
        if os.path.exists(self.clone):
            sh.File(self.clone).delete()
        # Alter DB and add/remove some columns
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connect()
        idb.connectw()
        idb.fetch()
        idb.create_table()
        idb.fill()
        idb.savew()
        idb.close()
        idb.closew()
        
    def read_random(self):
        f = '[Yatube] utils.Commands.read_random'
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connect()
        query = 'select AUTHOR,TITLE,SEARCH,TIMESTAMP from VIDEOS \
                 where SEARCH like ?'
        pattern = '%радиационная опасность%'
        idb.dbc.execute(query, (pattern,))
        data = idb.dbc.fetchone()
        if not data:
            sh.com.rep_empty(f)
            idb.close()
            return
        print('Author: "{}"'.format(data[0]))
        print('Title: "{}"'.format(data[1]))
        print('Search: "{}"'.format(data[2]))
        print('Timestamp: "{}"'.format(data[3]))
        idb.close()
        
    def _get_empty(self,idb):
        f = '[Yatube] utils.Commands._get_empty'
        query = 'select AUTHOR from VIDEOS where AUTHOR = ? or TITLE = ?'
        idb.dbcw.execute(query,('', '',))
        data = idb.dbcw.fetchall()
        mes = _('{} records have been found.').format(len(data))
        sh.objs.get_mes(f, mes, True).show_info()
    
    def get_empty(self):
        f = '[Yatube] utils.Commands.get_empty'
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connect()
        query = 'select AUTHOR from VIDEOS where AUTHOR = ? or TITLE = ?'
        idb.dbc.execute(query, ('', '',))
        data = idb.dbc.fetchall()
        mes = _('{} records have been found.').format(len(data))
        sh.objs.get_mes(f, mes, True).show_info()
        idb.close()
    
    def empty_author(self):
        f = '[Yatube] utils.Commands.empty_author'
        Success = sh.File (file = self.path
                          ,dest = self.clone
                          ,Rewrite = True
                          ).copy()
        if not Success:
            sh.com.cancel(f)
            return
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connectw()
        self._get_empty(idb)
        query = 'delete from VIDEOS where AUTHOR = ? or TITLE = ?'
        idb.dbcw.execute(query, ('', '',))
        self._get_empty(idb)
        idb.savew()
        idb.closew()


com = Commands()


if __name__ == '__main__':
    sh.objs.get_mes(Silent=1)
    #com.alter()
    #com.show_stat()
    com.unescape()
