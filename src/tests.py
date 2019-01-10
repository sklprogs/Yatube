#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg
import logic     as lg
import db


class ImageViewer:
    
    def __init__(self):
        self.gui()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def bindings(self):
        sg.bind (obj      = self.parent
                ,bindings = ['<Escape>','<Control-w>','<Control-q>'
                            ,'<ButtonRelease-1>'
                            ]
                ,action   = self.close
                )
    
    def title(self,arg=None):
        if not arg:
            arg = _('Image:')
        self.parent.title(arg)
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon (sh.objs.pdir().add ('..','resources'
                                                 ,'unmusic.gif'
                                                 )
                             )
    
    def gui(self):
        self.parent = sg.Top(sg.objs.root())
        self.lbl    = sg.Label (parent = self.parent
                               ,text   = _('Image:')
                               ,Close  = False
                               ,expand = True
                               ,fill   = 'both'
                               )
        self.title()
        self.icon()
        self.bindings()


def time():
    itime = lg.Time()
    itime.set_date(DaysDelta=0)
    print('Current time:')
    print('Year:',itime._year)
    print('Month:',itime._month)
    print('Day:',itime._day)
    itime.set_date(DaysDelta=7)
    print()
    print('A week ago:')
    print('Year:',itime._year)
    print('Month:',itime._month)
    print('Day:',itime._day)
    
def constants():
    cs = lg.Constants()
    print('Countries:')
    print(cs.countries())
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
    print(lists._subsc_auth)
    print('URLs:')
    print(lists._subsc_urls)
    print('Block authors:')
    print(lists._block_auth)
    
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
    itime._date = '2007-09-01'
    result = itime.timestamp()
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


if __name__ == '__main__':
    f = '[Yatube] tests.__main__'
    sg.objs.start()
    import yatube as ct
    import meta   as mt
    mt.objs.stat()
    add = ct.objs.add_id()
    add.reset()
    add.show()
    mt.objs._stat.report()
    sg.objs.end()
