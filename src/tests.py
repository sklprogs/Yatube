#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared2.shared as sh
import logic             as lg
import gui               as gi
import db
from skl_shared2.localize import _


class ImageViewer:
    
    def __init__(self):
        self.set_gui()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def set_bindings(self):
        sh.com.bind (obj      = self.parent
                    ,bindings = ('<Escape>','<Control-w>','<Control-q>'
                                ,'<ButtonRelease-1>'
                                )
                    ,action   = self.close
                    )
    
    def set_title(self,arg=None):
        if not arg:
            arg = _('Image:')
        self.parent.set_title(arg)
    
    def set_icon(self,path=None):
        if path:
            self.parent.set_icon(path)
        else:
            self.parent.set_icon (sh.objs.get_pdir().add ('..','resources'
                                                         ,'unmusic.gif'
                                                         )
                                 )
    
    def set_gui(self):
        self.parent = sh.Top()
        self.lbl    = sh.Label (parent = self.parent
                               ,text   = _('Image:')
                               ,expand = True
                               ,fill   = 'both'
                               )
        self.set_title()
        self.set_icon()
        self.set_bindings()


def time():
    itime = lg.Time()
    itime.set_date(DaysDelta=0)
    print('Current time:')
    print('Year:',itime.year)
    print('Month:',itime.month)
    print('Day:',itime.day)
    itime.set_date(DaysDelta=7)
    print()
    print('A week ago:')
    print('Year:',itime.year)
    print('Month:',itime.month)
    print('Day:',itime.day)
    
def constants():
    cs = lg.Constants()
    print('Countries:')
    print(cs.get_countries())
    print()
    print('Trending:')
    print(cs.trending())
    
def delimiter():
    input('Press Return')
    print('--------------------------------------------')
    
def lists():
    lists = lg.Lists()
    lists.load()
    print('Subscribe to authors:')
    print(lists.subauth)
    print('URLs:')
    print(lists.subsc_urls)
    print('Block authors:')
    print(lists.blauth)
    
def all():
    print('Run all tests')
    time()
    delimiter()
    constants()
    delimiter()
    
def author():
    idb = db.DB()
    result = idb.channel_videos(author='Алексей Навальный')
    if result:
        print(len(result))
    idb.close()
    
def timestamp():
    itime = sh.Time()
    itime.date = '2007-09-01'
    result = itime.get_timestamp()
    idb = db.DB()
    result = idb.date_filter (timestamp = result
                             ,Newer     = False
                             )
    if result:
        sh.Table (headers = ['AUTHOR','TITLE','DATE','TIMESTAMP']
                 ,rows    = result
                 ).print()
    idb.close()
    
def dtime():
    idb = db.DB()
    idb.dbc.execute('select TITLE,DTIME,PTIME from VIDEOS where DTIME > ? order by DTIME desc,PTIME desc limit ?',(0,5))
    result = idb.dbc.fetchall()
    if result:
        sh.Table (headers = ['TITLE','DTIME','PTIME']
                 ,rows    = result
                 ).print()
    idb.close()
    
def url():
    print(lg.URL(url='https://youtu.be/vjSohj-Iclc').video_full())
    print(lg.URL(url='https://m.youtube.com/watch?v=vjSohj-Iclc').video_full())
    print(lg.URL(url='https://www.youtube.com/embed/vjSohj-Iclc').video_full())
    print(lg.URL(url='vjSohj-Iclc').video_full())
    
def invalid_urls():
    idb = db.DB()
    idb.dbc.execute('select ID from VIDEOS where length(ID) > 11')
    result = idb.dbc.fetchall()
    if result:
        result = list(result)
        result = [item[0] for item in result]
        print('\n'.join(result))
    idb.close()

def search_field():
    # An example of a complex search in the DB
    idb = db.DB(path='/home/pete/.config/yatube/yatube.db')
    itime = sh.Time(pattern='%Y-%m-%d %H:%M:%S')
    itime.add_days(-7)
    idb.dbc.execute ('select ID,AUTHOR,TITLE from VIDEOS \
                      where SEARCH like ? and DTIME > ? and FDTIME < ?'
                    ,('%дерев%',0,itime.get_timestamp(),)
                    )
    result = idb.dbc.fetchall()
    if result:
        import io
        tmp = io.StringIO()
        for i in range(len(result)):
            tmp.write(str(i))
            tmp.write(' : ')
            tmp.write(result[i][0])
            tmp.write('\n')
            tmp.write(result[i][1])
            tmp.write('\n')
            tmp.write(result[i][2])
            tmp.write('\n\n')
        text = tmp.getvalue()
        tmp.close()
        sh.com.fast_txt(text)
    idb.close()


if __name__ == '__main__':
    f = 'tests.__main__'
    sh.com.start()
    
    sh.com.end()
