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
        self.Success = self.clone and sh.File(file=self.path).Success
    
    def vacuumize(self):
        f = '[Yatube] utils.DB.vacuumize'
        if self.Success:
            try:
                self.dbcw.execute('vacuum')
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def update_unescape(self,id_,author,title,desc,search):
        f = '[Yatube] utils.DB.update_unescape'
        if self.Success:
            try:
                self.dbcw.execute ('update VIDEOS set AUTHOR = ?\
                                                     ,TITLE = ?\
                                                     ,DESC = ?\
                                                     ,SEARCH = ?\
                                    where  ID = ?'
                                  ,(author,title,desc,search,id_)
                                  )
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def get_unescape(self):
        f = '[Yatube] utils.DB.get_unescape'
        if self.Success:
            try:
                self.dbcw.execute ('select ID,AUTHOR,TITLE,DESC,SEARCH \
                                    from VIDEOS'
                                  )
                return self.dbcw.fetchall()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def del_author(self,author):
        f = '[Yatube] utils.DB.del_author'
        if self.Success:
            try:
                self.dbcw.execute ('delete from VIDEOS \
                                    where AUTHOR = ?',(author,)
                                  )
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def fetch_ftime(self):
        f = '[Yatube] utils.DB.fetch_ftime'
        if self.Success:
            try:
                self.dbcw.execute ('select  ID,FTIME\
                                   from     VIDEOS \
                                   where    FTIME > ?\
                                   order by FTIME desc,PTIME desc',(0,)
                                 )
                return self.dbcw.fetchall()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def update_ftime(self,id_,ftime):
        f = '[Yatube] utils.DB.update_ftime'
        if self.Success:
            try:
                self.dbcw.execute ('update VIDEOS set FTIME = ? \
                                    where  ID = ?',(ftime,id_,)
                                  )
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def update_ltime(self,id_,ltime):
        f = '[Yatube] utils.DB.update_ltime'
        if self.Success:
            try:
                self.dbcw.execute ('update VIDEOS set LTIME = ? \
                                    where  ID = ?',(ltime,id_,)
                                  )
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def fetch_ltime(self):
        f = '[Yatube] utils.DB.fetch_ltime'
        if self.Success:
            try:
                self.dbcw.execute ('select  ID,LTIME\
                                   from     VIDEOS \
                                   where    LTIME > ?\
                                   order by LTIME desc,PTIME desc',(0,)
                                 )
                return self.dbcw.fetchall()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def fail(self,f,e):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.path,e)
        sh.objs.get_mes(f,mes).show_warning()
    
    def fail_clone(self,f,e):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.clone,e)
        sh.objs.get_mes(f,mes).show_warning()
    
    def down_markw(self):
        f = '[Yatube] utils.DB.down_markw'
        if self.Success:
            try:
                self.dbcw.execute ('update VIDEOS set DTIME = ? \
                                    where  DTIME > ?',(0,0,)
                                  )
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def savew(self):
        f = '[Yatube] utils.DB.savew'
        if self.Success:
            try:
                self.dbw.commit()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
        
    def connect(self):
        f = '[Yatube] utils.DB.connect'
        if self.Success:
            try:
                self.db = sqlite3.connect(self.path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def connectw(self):
        f = '[Yatube] utils.DB.connectw'
        if self.Success:
            try:
                self.dbw = sqlite3.connect(self.clone)
                self.dbcw = self.dbw.cursor()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def fetch(self):
        f = '[Yatube] utils.DB.fetch'
        if self.Success:
            mes = _('Fetch data')
            sh.objs.get_mes(f,mes,True).show_info()
            try:
                # 12 columns
                query = 'select ID,PLAYID,CHANID,AUTHOR,TITLE,DESC,SEARCH,LENGTH,PAUSE,PTIME,DTIME,FTIME,LTIME,FDTIME'
                self.dbc.execute ('select ID,PLAYID,CHANID,AUTHOR,TITLE\
                                         ,LENGTH,PAUSE,PTIME,DTIME \
                                         ,FTIME,LTIME,FDTIME \
                                   from VIDEOS'
                                 )
                self.data = self.dbc.fetchall()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_table(self):
        f = '[Yatube] utils.DB.create_table'
        if self.Success:
            try:
                # Create 12 columns
                self.dbcw.execute (
                    'create table VIDEOS (\
                     ID     text    \
                    ,PLAYID text    \
                    ,CHANID text    \
                    ,AUTHOR text    \
                    ,TITLE  text    \
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
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
    
    def fill(self):
        f = '[Yatube] utils.DB.fill'
        if self.Success:
            if self.data:
                mes = _('Copy "{}" to "{}"').format (self.path
                                                    ,self.clone
                                                    )
                sh.objs.get_mes(f,mes,True).show_info()
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
                        row = (id_,playid,chanid,author,title,length
                              ,pause,ptime,dtime,ftime,ltime,fdtime
                              )
                        self.dbcw.execute ('insert into VIDEOS values \
                                          (?,?,?,?,?,?,?,?,?,?,?,?)',row
                                          )
                    except Exception as e:
                        self.Success = False
                        self.fail(f,e)
                        break
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
                          
    def close(self):
        f = '[Yatube] utils.DB.close'
        if self.Success:
            try:
                self.dbc.close()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
                          
    def closew(self):
        f = '[Yatube] utils.DB.closew'
        if self.Success:
            try:
                self.dbcw.close()
            except Exception as e:
                self.fail_clone(f,e)
        else:
            sh.com.cancel(f)
                          
    def repair_urls(self):
        f = '[Yatube] utils.DB.repair_urls'
        if self.Success:
            self.dbcw.execute('select URL from VIDEOS where length(URL) > 11')
            result = self.dbcw.fetchall()
            if result:
                result = list(result)
                result = [item[0] for item in result]
                for item in result:
                    old_item = item
                    item = item.replace('ttps://www.youtube.com/watch?v=','')
                    item = item.replace('https://youtu.be/','')
                    item = item.replace('https://m.youtube.com/','')
                    item = item.replace('youtube.com/watch?v=','')
                    item = item.replace('watch?v=','')
                    item = item.replace('?t=118','')
                    mes = '"{}" -> "{}"'.format(old_item,item)
                    sh.objs.get_mes(f,mes,True).show_info()
                    try:
                        self.dbcw.execute ('update VIDEOS set URL = ? where URL = ?'
                                          ,(item,old_item,)
                                          )
                    except Exception as e:
                        self.fail_clone(f,e)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)



class Commands:
    
    def __init__(self):
        self.path = '/home/pete/.config/yatube/yatube.db'
        self.clone = '/tmp/yatube.db'
        
    def unescape(self):
        f = '[Yatube] utils.Commands.unescape'
        sh.File(self.path,self.clone).copy()
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connectw()
        data = idb.get_unescape()
        if data:
            ids = []
            authors = []
            titles = []
            desc = []
            search = []
            mes = _('Get data')
            sh.objs.get_mes(f,mes,True).show_info()
            for item in data:
                ids.append(item[0])
                authors.append(item[1])
                titles.append(item[2])
                desc.append(item[3])
                search.append(item[4])
            mes = _('Process data')
            sh.objs.get_mes(f,mes,True).show_info()
            for i in range(len(ids)):
                if authors[i] != html.unescape(authors[i]) \
                or titles[i] != html.unescape(titles[i]) \
                or desc[i] != html.unescape(desc[i]) \
                or search[i] != html.unescape(search[i]):
                    mes = _('Update {}').format(ids[i])
                    sh.objs.get_mes(f,mes,True).show_info()
                    tauthor = html.unescape(authors[i])
                    ttitle = html.unescape(titles[i])
                    tdesc = html.unescape(desc[i])
                    tsearch = html.unescape(search[i])
                    idb.update_unescape (ids[i],tauthor,ttitle,tdesc
                                        ,tsearch
                                        )
            idb.savew()
        else:
            sh.com.rep_empty(f)
        idb.closew()
    
    def del_author(self,author):
        sh.File(self.path,self.clone).copy()
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
        if Success:
            idb = DB (path = self.path
                     ,clone = self.clone
                     )
            idb.connectw()
            idb.repair_urls()
            idb.savew()
            idb.closew()
        else:
            sh.com.cancel(f)
    
    def down_markw(self):
        f = '[Yatube] utils.Commands.down_markw'
        Success = sh.File (file = self.path
                          ,dest = self.clone
                          ,Rewrite = True
                          ).copy()
        if Success:
            idb = DB (path = self.path
                     ,clone = self.clone
                     )
            idb.connectw()
            idb.down_markw()
            idb.savew()
            idb.closew()
        else:
            sh.com.cancel(f)
    
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
        idb.dbc.execute ('select AUTHOR,TITLE,SEARCH,TIMESTAMP \
                          from VIDEOS where SEARCH like ?\
                         ',('%стихийный митинг%',)
                         )
        data = idb.dbc.fetchone()
        if data:
            print('Author: "%s"'    % str(data[0]))
            print('Title: "%s"'     % str(data[1]))
            print('Search: "%s"'    % str(data[2]))
            print('Timestamp: "%s"' % str(data[3]))
        else:
            sh.com.rep_empty(f)
        idb.close()
        
    def _get_empty(self,idb):
        f = '[Yatube] utils.Commands._get_empty'
        idb.dbcw.execute ('select AUTHOR from VIDEOS \
                           where  AUTHOR = ? or TITLE = ?',('','',)
                         )
        data = idb.dbcw.fetchall()
        mes = _('{} records have been found.').format(len(data))
        sh.objs.get_mes(f,mes,True).show_info()
    
    def get_empty(self):
        f = '[Yatube] utils.Commands.get_empty'
        idb = DB (path = self.path
                 ,clone = self.clone
                 )
        idb.connect()
        idb.dbc.execute ('select AUTHOR from VIDEOS \
                          where  AUTHOR = ? or TITLE = ?',('','',)
                         )
        data = idb.dbc.fetchall()
        mes = _('{} records have been found.').format(len(data))
        sh.objs.get_mes(f,mes,True).show_info()
        idb.close()
    
    def empty_author(self):
        f = '[Yatube] utils.Commands.empty_author'
        Success = sh.File (file = self.path
                          ,dest = self.clone
                          ,Rewrite = True
                          ).copy()
        if Success:
            idb = DB (path = self.path
                     ,clone = self.clone
                     )
            idb.connectw()
            self._get_empty(idb)
            idb.dbcw.execute ('delete from VIDEOS \
                               where AUTHOR = ? or TITLE = ?',('','',)
                             )
            self._get_empty(idb)
            idb.savew()
            idb.closew()
        else:
            sh.com.cancel(f)


com = Commands()


if __name__ == '__main__':
    sh.objs.get_mes(Silent=1)
    com.alter()
