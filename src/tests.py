#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared as sh
import logic  as lg
import db


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
    idb.dbc.execute('select TITLE,DTIME,TIMESTAMP from VIDEOS where DTIME > ? order by DTIME desc,TIMESTAMP desc limit ?',(0,5))
    result = idb.dbc.fetchall()
    if result:
        sh.Table (headers = ['TITLE','DTIME','TIMESTAMP']
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
    idb.dbc.execute('select URL from VIDEOS where length(URL) > 11')
    result = idb.dbc.fetchall()
    if result:
        result = list(result)
        result = [item[0] for item in result]
        print('\n'.join(result))
    idb.close()


if __name__ == '__main__':
    f = '[Yatube] tests.__main__'
    '''
    urls = ['OFP5rzaOCfw','taRRpqX0CmA','MYXjO5TJqjw','f2gX4K5AndM'
           ,'vDP804SHKGg','jJfXOpQuxU4','E8QB5oxtoYE','9ZWmJcAi_OI'
           ,'WVNlMYYY-XX','c_2baGSBlxg','WVNlMBpS-eE'
           ]
    '''
    urls = ('WVNlMYYY-XX','WVNlMBpS-eE')
    path = sh.Home('yatube').add_config('yatube.db')
    #invalid_urls()
    idb = db.DB(path)
    '''
    idb.dbc.execute ('select AUTHOR,TITLE,DATE,CATEGORY,DESC,DURATION\
                            ,LENGTH,VIEWS,LIKES,DISLIKES,RATING,IMAGE\
                            ,SEARCH,TIMESTAMP,DTIME from VIDEOS \
                      where URL = ?',(video_id,)
                    )
    '''
    '''
    idb.dbc.execute ('select TITLE from VIDEOS where URL like ?'
                    ,('%' + ','.join(urls) + '%',)
                    )
    '''
    idb.dbc.execute ('select URL,AUTHOR,TITLE,DATE from VIDEOS where URL in %s' % str(tuple(urls))
                    )
    result = idb.dbc.fetchall()
    if result:
        #result = [item[0] for item in result]
        #print('\n'.join(result))
        print(result)
        '''
        authors = [item[0] for item in result]
        titles  = [item[1] for item in result]
        dates   = [item[2] for item in result]
        mes = ''
        for i in range(len(authors)):
            mes += '%d: %s; ' % (i,authors[i])
        mes += '\n'
        for i in range(len(titles)):
            mes += '%d: %s; ' % (i,titles[i])
        mes += '\n'
        for i in range(len(dates)):
            mes += '%d: %s; ' % (i,dates[i])
        mes += '\n'
        print(mes)
        '''
    else:
        sh.com.empty(f)
    idb.close()
