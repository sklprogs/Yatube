#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import io
import html
import youtube_dl
import shared    as sh
import sharedGUI as sg
import db
import meta      as mt

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')

pattern1  = 'https://www.youtube.com/watch?v='
pattern2  = '<meta itemprop="channelId" content="'
pattern3a = 'https://www.youtube.com/channel/'
pattern3b = '/videos'
pattern4  = '?flow=list&sort=dd'
pattern5  = 'https://www.youtube.com/'
AllOS     = False


sample_subscribe = '''BostonDynamics	UU7vVhkEfw4nOGp8TyDk7RcQ
Brave Wilderness	UU6E2mP01ZLH_kbAyeazCNdg
Pravda GlazaRezhet	UUgCqhDRyMH1wZBI4OOKLQ8g
Дмитрий ПОТАПЕНКО	UU54SBo5_usXGEoybX1ZVETQ
Мохнатые Друзья	UUqKbBJRz6SGrvUHNoZkpF2w
'''

sample_block = '''Россия 24'''


class Feed:
    
    def __init__(self):
        self._token_prev = 0
        self._token_next = 0
    
    def get_token(self):
        f = '[Yatube] logic.Feed.get_token'
        if mt.objs.videos()._videos:
            self._token_next = mt.objs._videos._videos[-1]._fdtime
            self._token_prev = mt.objs._videos._videos[0]._fdtime
            date_next = sh.Time (_timestamp = self._token_next
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).date()
            date_prev = sh.Time (_timestamp = self._token_prev
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).date()
            sh.log.append (f,_('DEBUG')
                          ,_('Previous page token: %s') % str(date_prev)
                          )
            sh.log.append (f,_('DEBUG')
                          ,_('Next page token: %s') % str(date_next)
                          )
        else:
            sh.com.empty(f)
            ''' This returns correct tokens for the 1st page if we are
                out of bounds.
            '''
            self._token_prev = 0
            self._token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
    
    def fetch(self):
        self._token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
        self.fetch_next()
    
    def fetch_prev(self):
        f = '[Yatube] logic.Feed.fetch_prev'
        ids = objs.db().feed_prev (fdtime = self._token_prev
                                  ,limit  = mt.MAX_VIDEOS
                                  )
        if ids:
            for vid in ids:
                video = mt.Video()
                video._id = vid
                mt.objs._videos.add(video)
        else:
            sh.com.empty(f)
    
    def fetch_next(self):
        f = '[Yatube] logic.Feed.fetch_next'
        ids = objs.db().feed_next (fdtime = self._token_next
                                  ,limit  = mt.MAX_VIDEOS
                                  )
        if ids:
            for vid in ids:
                video = mt.Video()
                video._id = vid
                mt.objs._videos.add(video)
        else:
            sh.com.empty(f)



class Favorites:
    
    def __init__(self):
        self._token_prev = 0
        self._token_next = 0
    
    def get_token(self):
        f = '[Yatube] logic.Favorites.get_token'
        if mt.objs.videos()._videos:
            self._token_next = mt.objs._videos._videos[-1]._ftime
            self._token_prev = mt.objs._videos._videos[0]._ftime
            date_next = sh.Time (_timestamp = self._token_next
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).date()
            date_prev = sh.Time (_timestamp = self._token_prev
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).date()
            sh.log.append (f,_('DEBUG')
                          ,_('Previous page token: %s') % str(date_prev)
                          )
            sh.log.append (f,_('DEBUG')
                          ,_('Next page token: %s') % str(date_next)
                          )
        else:
            sh.com.empty(f)
            ''' This returns correct tokens for the 1st page if we are
                out of bounds.
            '''
            self._token_prev = 0
            self._token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
    
    def fetch(self):
        self._token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
        self.fetch_next()
    
    def fetch_prev(self):
        f = '[Yatube] logic.Favorites.fetch_prev'
        ids = objs.db().fav_prev (ftime = self._token_prev
                                 ,limit = mt.MAX_VIDEOS
                                 )
        if ids:
            for vid in ids:
                video = mt.Video()
                video._id = vid
                mt.objs._videos.add(video)
        else:
            sh.com.empty(f)
    
    def fetch_next(self):
        f = '[Yatube] logic.Favorites.fetch_next'
        ids = objs.db().fav_next (ftime = self._token_next
                                 ,limit = mt.MAX_VIDEOS
                                 )
        if ids:
            for vid in ids:
                video = mt.Video()
                video._id = vid
                mt.objs._videos.add(video)
        else:
            sh.com.empty(f)



class Watchlist:
    
    def __init__(self):
        self._token_prev = 0
        self._token_next = 0
    
    def get_token(self):
        f = '[Yatube] logic.Watchlist.get_token'
        if mt.objs.videos()._videos:
            self._token_next = mt.objs._videos._videos[-1]._ltime
            self._token_prev = mt.objs._videos._videos[0]._ltime
            date_next = sh.Time (_timestamp = self._token_next
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).date()
            date_prev = sh.Time (_timestamp = self._token_prev
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).date()
            sh.log.append (f,_('DEBUG')
                          ,_('Previous page token: %s') % str(date_prev)
                          )
            sh.log.append (f,_('DEBUG')
                          ,_('Next page token: %s') % str(date_next)
                          )
        else:
            sh.com.empty(f)
            ''' This returns correct tokens for the 1st page if we are
                out of bounds.
            '''
            self._token_prev = 0
            self._token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
    
    def fetch(self):
        self._token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
        self.fetch_next()
    
    def fetch_prev(self):
        f = '[Yatube] logic.Watchlist.fetch_prev'
        ids = objs.db().watch_prev (ltime = self._token_prev
                                   ,limit = mt.MAX_VIDEOS
                                   )
        if ids:
            for vid in ids:
                video = mt.Video()
                video._id = vid
                mt.objs._videos.add(video)
        else:
            sh.com.empty(f)
    
    def fetch_next(self):
        f = '[Yatube] logic.Watchlist.fetch_next'
        ids = objs.db().watch_next (ltime = self._token_next
                                   ,limit = mt.MAX_VIDEOS
                                   )
        if ids:
            for vid in ids:
                video = mt.Video()
                video._id = vid
                mt.objs._videos.add(video)
        else:
            sh.com.empty(f)



class History:
    
    def __init__(self):
        self._token_next = 0
        self._token_prev = 0
    
    def get_token(self):
        f = '[Yatube] logic.History.get_token'
        if mt.objs.videos()._videos:
            self._token_next = mt.objs._videos._videos[-1]._dtime
            self._token_prev = mt.objs._videos._videos[0]._dtime
            date_next = sh.Time (_timestamp = self._token_next
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).date()
            date_prev = sh.Time (_timestamp = self._token_prev
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).date()
            sh.log.append (f,_('DEBUG')
                          ,_('Previous page token: %s') % str(date_prev)
                          )
            sh.log.append (f,_('DEBUG')
                          ,_('Next page token: %s') % str(date_next)
                          )
        else:
            sh.com.empty(f)
            ''' This returns correct tokens for the 1st page if we are
                out of bounds.
            '''
            self._token_prev = 0
            self._token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
    
    def fetch(self):
        self._token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
        self.fetch_next()
    
    def fetch_prev(self):
        f = '[Yatube] logic.History.fetch_prev'
        ids = objs.db().history_prev (dtime = self._token_prev
                                     ,limit = mt.MAX_VIDEOS
                                     )
        if ids:
            for vid in ids:
                video = mt.Video()
                video._id = vid
                mt.objs._videos.add(video)
        else:
            sh.com.empty(f)
    
    def fetch_next(self):
        f = '[Yatube] logic.History.fetch_next'
        ids = objs.db().history_next (dtime = self._token_next
                                     ,limit = mt.MAX_VIDEOS
                                     )
        if ids:
            for vid in ids:
                video = mt.Video()
                video._id = vid
                mt.objs._videos.add(video)
        else:
            sh.com.empty(f)



class Channel:
    
    def __init__(self,myid=''):
        self.values()
        if myid:
            self.reset(myid)
    
    def run(self):
        f = '[Yatube] logic.Channel.run'
        if self.Success:
            mt.objs.playlist().reset(self._play_id)
            mt.objs._playlist.run()
            for video in mt.objs._videos._videos:
                self._ids.append(video._id)
        else:
            sh.com.cancel(f)
        return self._ids
    
    def reset(self,myid):
        self.autodetect(myid)
    
    def autodetect(self,myid):
        f = '[Yatube] logic.Channel.autodetect'
        if myid:
            #todo: implement autodetection
            self._play_id = myid
        else:
            self.Success = False
            sh.com.empty(f)
    
    def values(self):
        self.Success  = True
        self._ids     = []
        self._play_id = ''



class Time:
    
    def __init__(self):
        self._days   = []
        self._months = []
        self._years  = []
        self._year   = ''
        self._day    = ''
        self._month  = ''
        self.itime = sh.Time(pattern='%d')
    
    def days(self):
        self._days = [str(day+1) for day in range(31)]
        # sh.Time outputs a day number preceded by 0
        self._days = tuple ('0' + day if len(day) == 1 else day \
                            for day in self._days
                           )
        return self._days
        
    def months(self):
        self._months = (_('Jan'),_('Feb'),_('Mar'),_('Apr'),_('May')
                       ,_('Jun'),_('Jul'),_('Aug'),_('Sep'),_('Oct')
                       ,_('Nov'),_('Dec')
                       )
        return self._months
        
    def years(self):
        f = '[Yatube] logic.Time.years'
        # Year of Youtube birth
        first_year = 2005
        last_year  = self.itime.year()
        last_year  = sh.Input (title = f
                              ,value = last_year
                              ).integer()
        if not last_year > first_year:
            sh.log.append (f,_('WARNING')
                          ,_('Wrong input data!')
                          )
            last_year = 2018
        self._years = tuple (str(year) for year in range (first_year
                                                         ,last_year + 1
                                                         )
                            )
        return self._years
        
    def set_date(self,DaysDelta=7):
        self.itime.add_days(days_delta=-DaysDelta)
        self._year = str(self.itime.year())
        self._day = self.itime.date()
        self.itime.month_abbr()
        self._month = self.itime.localize_month_abbr()


class Constants:
    
    def __init__(self):
        self._countries = []
        self._trending  = []
        
    def countries(self):
        self._countries = {_('Algeria')                : 'DZ'
                          ,_('Argentina')              : 'AR'
                          ,_('Australia')              : 'AU'
                          ,_('Austria')                : 'AT'
                          ,_('Azerbaijan')             : 'AZ'
                          ,_('Bahrain')                : 'BH'
                          ,_('Belarus')                : 'BY'
                          ,_('Belgium')                : 'BE'
                          ,_('Bosnia and Herzegovina') : 'BA'
                          ,_('Brazil')                 : 'BR'
                          ,_('Bulgaria')               : 'BG'
                          ,_('Canada')                 : 'CA'
                          ,_('Chile')                  : 'CL'
                          ,_('Colombia')               : 'CO'
                          ,_('Croatia')                : 'HR'
                          ,_('Czechia')                : 'CZ'
                          ,_('Denmark')                : 'DK'
                          ,_('Egypt')                  : 'EG'
                          ,_('Estonia')                : 'EE'
                          ,_('Finland')                : 'FI'
                          ,_('France')                 : 'FR'
                          ,_('Georgia')                : 'GE'
                          ,_('Germany')                : 'DE'
                          ,_('Ghana')                  : 'GH'
                          ,_('Greece')                 : 'GR'
                          ,_('Hong Kong')              : 'HK'
                          ,_('Hungary')                : 'HU'
                          ,_('Iceland')                : 'IS'
                          ,_('India')                  : 'IN'
                          ,_('Indonesia')              : 'ID'
                          ,_('Iraq')                   : 'IQ'
                          ,_('Ireland')                : 'IE'
                          ,_('Israel')                 : 'IL'
                          ,_('Itality')                : 'IT'
                          ,_('Jamaica')                : 'JM'
                          ,_('Japan')                  : 'JP'
                          ,_('Jordan')                 : 'JO'
                          ,_('Kazakhstan')             : 'KZ'
                          ,_('Kenya')                  : 'KE'
                          ,_('Kuwait')                 : 'KW'
                          ,_('Latvia')                 : 'LV'
                          ,_('Lebanon')                : 'LB'
                          ,_('Libya')                  : 'LY'
                          ,_('Lithuania')              : 'LT'
                          ,_('Luxembourg')             : 'LU'
                          ,_('Macedonia')              : 'MK'
                          ,_('Malaysia')               : 'MY'
                          ,_('Mexico')                 : 'MX'
                          ,_('Montenegro')             : 'ME'
                          ,_('Morocco')                : 'MA'
                          ,_('Nepal')                  : 'NP'
                          ,_('Netherlands')            : 'NL'
                          ,_('New Zealand')            : 'NZ'
                          ,_('Nigeria')                : 'NG'
                          ,_('Norway')                 : 'NO'
                          ,_('Oman')                   : 'OM'
                          ,_('Pakistan')               : 'PK'
                          ,_('Peru')                   : 'PE'
                          ,_('Philippines')            : 'PH'
                          ,_('Poland')                 : 'PL'
                          ,_('Portugal')               : 'PT'
                          ,_('Puerto Rico')            : 'PR'
                          ,_('Qatar')                  : 'QA'
                          ,_('Romania')                : 'RO'
                          ,_('Russia')                 : 'RU'
                          ,_('Saudi Arabia')           : 'SA'
                          ,_('Senegal')                : 'SN'
                          ,_('Serbia')                 : 'RS'
                          ,_('Singapore')              : 'SG'
                          ,_('Slovakia')               : 'SK'
                          ,_('Slovenia')               : 'SL'
                          ,_('South Africa')           : 'ZA'
                          ,_('South Korea')            : 'KR'
                          ,_('Spain')                  : 'ES'
                          ,_('Sri Lanka')              : 'LK'
                          ,_('Sweden')                 : 'SE'
                          ,_('Switzerland')            : 'CH'
                          ,_('Taiwan')                 : 'TW'
                          ,_('Tanzania')               : 'TZ'
                          ,_('Thailand')               : 'TH'
                          ,_('Tunisia')                : 'TN'
                          ,_('Turkey')                 : 'TR'
                          ,_('Uganda')                 : 'UG'
                          ,_('Ukraine')                : 'UA'
                          ,_('United Arab Emirates')   : 'AE'
                          ,_('United Kingdom')         : 'GB'
                          ,_('United States')          : 'US'
                          ,_('Vietnam')                : 'VN'
                          ,_('Yemen')                  : 'YE'
                          ,_('Zimbabwe')               : 'ZW'
                          }
        return self._countries
        
    def trending(self):
        self._trending = [_('Trending')] \
                         + sorted(self.countries().keys())
        return self._trending



class Extractor:
       
    def __init__(self):
        self.values()
    
    def url(self):
        f = '[Yatube] logic.Extractor.url'
        if self.Success:
            ''' Owing to parser peculiarities, if the link is
                a non-conventional link to a Youtube video, it should be
                first converted to a conventional link (see 'pattern1').
                Youtube playlists, search results and links from
                external sites may be preserved in the original form.
                #todo: Fix the parser to get rid of this.
            '''
            vid = URL(self._url).video_id()
            if len(vid) == 11 and not 'https:' in vid \
            and not 'http:' in vid and not 'www.' in vid:
                self._url = URL(vid).video_full()
        else:
            sh.com.cancel(f)
        
    def reset(self,url=''):
        f = '[Yatube] logic.Extractor.reset'
        self.values()
        if url:
            self._url = url
        else:
            self.Success = False
            sh.com.empty(f)
        
    def values(self):
        self.Success = True
        self._url    = ''
        self._html   = ''
        self._urls   = []
    
    def page(self):
        f = '[Yatube] logic.Extractor.page'
        if self.Success:
            if self._html or self._urls:
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
            else:
                response = sh.Get(url=self._url).run()
                if response:
                    self._html = response
                else:
                    sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def urls(self):
        f = '[Yatube] logic.Extractor.urls'
        if self.Success:
            if self._urls:
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
            else:
                ilinks = sh.Links (text = self._html
                                  ,root = 'href="'
                                  )
                ilinks.poses()
                old = list(ilinks._links)
                ilinks = sh.Links (text = self._html
                                  ,root = 'src="'
                                  )
                ilinks.poses()
                ''' #note: if links from both root elements are present,
                    their order may be desynchronized.
                '''
                ilinks._links += old
                if 'youtube' in self._url or 'youtu.be' in self._url:
                    ilinks._links = ['https://www.youtube.com' + link \
                                     for link in ilinks._links \
                                     if link.startswith('/watch?v=')
                                    ]
                else:
                    ilinks.redirection()
                    ''' We should do our best here to ensure that
                        the URL will refer to a Youtube video. There
                        could be links to 'youtube.com', e.g., from
                        'account.google.com' that will not refer to
                        videos. We need a slash here because there can
                        be links like
                        .../uploads/youtu.be-bv2OGph5Kec-330x225.jpg.
                    '''
                    ilinks._links = [link for link in ilinks._links 
                                     if 'youtu.be/' in link 
                                     or 'youtube.com/watch?v=' in link 
                                     or 'youtube.com/embed/' in link
                                    ]
                    ilinks.valid()
                old = list(ilinks._links)
                ''' Previous algorithms consider a link as valid if it has
                    'youtu(be)' in its tag, and we have just ID there, so
                    this should be put after those algorithms.
                '''
                ilinks = sh.Links (text = self._html
                                  ,root = 'data-pe-videoid="'
                                  )
                ilinks.poses()
                ilinks._links += old
                ilinks._links = [URL(url=link).video_id() \
                                 for link in ilinks._links
                                ]
                ilinks.duplicates()
                self._urls = ilinks._links
                sh.log.append (f,_('INFO')
                              ,_('Fetched %d links') % len(self._urls)
                              )
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.url()
        self.page()
        self.urls()
        return self._urls



class Lists:
    
    def __init__(self):
        self.values()
        
    def reset(self):
        self.values()
        self.idefault = objs.default()
        self.Success  = self.idefault.Success
        self.load()
    
    def values(self):
        self._block       = ''
        self._blockw      = ''
        self._subsc       = ''
        self._block_auth  = []
        self._block_words = []
        self._subsc_auth  = []
        self._subsc_ids  = []
    
    def match_blocked_word(self,word):
        f = '[Yatube] logic.Lists.match_blocked_word'
        if self.Success:
            word = word.lower()
            for item in self._block_words:
                ''' Contents of 'self._block_words' should already be
                    lower-cased.
                '''
                if item in word:
                    return True
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[Yatube] logic.Lists.load'
        if self.Success:
            # Blocked authors
            text = sh.ReadTextFile(file=self.idefault._fblock).get()
            text = sh.Text(text=text).delete_comments()
            # We should allow empty files
            self._block      = text
            self._block_auth = text.splitlines()
            # Blocked words
            text = sh.ReadTextFile(file=self.idefault._fblockw).get()
            text = sh.Text(text=text).delete_comments()
            # We should allow empty files
            self._blockw      = text
            self._block_words = text.splitlines()
            self._block_words = [item.lower() for item \
                                 in self._block_words
                                ]
            # Suppress errors on empty text
            if os.path.exists(self.idefault._fsubsc):
                dic = sh.Dic (file     = self.idefault._fsubsc
                             ,Sortable = False
                             )
                self.Success = dic.Success
                if self.Success:
                    self._subsc      = dic.text
                    self._subsc_auth = dic.orig
                    self._subsc_ids  = dic.transl
            if self._subsc_auth:
                self._subsc_auth, self._subsc_ids = (list(x) for x \
                in zip (*sorted (zip (self._subsc_auth, self._subsc_ids)
                                ,key = lambda x:x[0].lower()
                                )
                       )
                                                     )
        else:
            sh.com.cancel(f)



class Objects:
    
    def __init__(self):
        ''' Do not put here instances that do not require input because
            of using meta objects and need to be constantly reset owing
            to possible 'Success' fails (e.g., 'logic.Video').
        '''
        self._online = self._lists = self._const = self._default \
                     = self._db = self._channels = self._channel \
                     = self._extractor = self._history \
                     = self._watchlist = self._favorites = self._feed \
                     = None
    
    def feed(self):
        if self._feed is None:
            self._feed = Feed()
        return self._feed
    
    def favorites(self):
        if self._favorites is None:
            self._favorites = Favorites()
        return self._favorites
    
    def watchlist(self):
        if self._watchlist is None:
            self._watchlist = Watchlist()
        return self._watchlist
    
    def history(self):
        if self._history is None:
            self._history = History()
        return self._history
    
    def extractor(self):
        if not self._extractor:
            self._extractor = Extractor()
        return self._extractor
    
    def channel(self):
        if not self._channel:
            self._channel = Channel()
        return self._channel
    
    def db(self):
        f = '[Yatube] logic.Objects.db'
        if not self._db:
            path = self.default(product='yatube')._fdb
            if self._default.Success:
                self._db = db.DB(path=path)
            else:
                sh.log.append (f,_('WARNING')
                              ,_('Wrong input data!')
                              )
                self._db = db.DB()
        return self._db
    
    def default(self,product='yatube'):
        if not self._default:
            self._default = DefaultConfig(product='yatube')
            self._default.run()
        return self._default
    
    def const(self):
        if not self._const:
            self._const = Constants()
            self._const.countries()
            self._const.trending()
        return self._const
    
    def online(self):
        if not self._online:
            self._online = sh.Online(MTSpecific=False)
        return self._online
        
    def lists(self):
        if not self._lists:
            self._lists = Lists()
        return self._lists
    
    def channels(self):
        if not self._channels:
            self._channels = ChannelHistory()
        return self._channels



class Video:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.values()
        self.check()
    
    def unsupported(self):
        video         = mt.objs.videos().current()
        video._author = sh.Text(video._author).delete_unsupported()
        video._title  = sh.Text(video._title).delete_unsupported()
        video._desc   = sh.Text(video._desc).delete_unsupported()
        video._search = sh.Text(video._search).delete_unsupported()
        video._author = html.unescape(video._author)
        video._title  = html.unescape(video._title)
        video._desc   = html.unescape(video._desc)
        video._search = html.unescape(video._search)
    
    def length(self):
        f = '[Yatube] logic.Video.length'
        video = mt.objs.videos().current()
        if not video._len:
            if mt.VideoInfo().length():
                objs.db().update_len(video._id,video._len)
            else:
                sh.com.empty(f)
        return video._len
    
    def statistics(self):
        f = '[Yatube] logic.Video.statistics'
        video = mt.objs.videos().current()
        ''' Likes/dislikes/number of comments can be 0, so we shoud rely
            on 'video._views' only.
        '''
        if not video._views:
            # Return True if metadata were fetched successfully
            return mt.VideoInfo().statistics()
        return True
    
    def play_id(self):
        f = '[Yatube] logic.Video.play_id'
        video = mt.objs.videos().current()
        if not video._play_id:
            channel_id = self.channel_id()
            if channel_id:
                mt.objs.playid().reset(channel_id)
                play_id = mt.objs._playid.by_channel_id()
                if play_id:
                    video._play_id = play_id
                    objs.db().update_play_id(video._id,video._play_id)
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        return video._play_id
    
    def channel_id(self):
        f = '[Yatube] logic.Video.channel_id'
        video = mt.objs.videos().current()
        if not video._ch_id:
            channel_id = mt.VideoInfo().channel_id()
            if channel_id:
                video._ch_id = channel_id
                objs.db().update_ch_id(video._id,video._ch_id)
            else:
                sh.com.empty(f)
        return video._ch_id
    
    def check(self):
        f = '[Yatube] logic.Video.check'
        if mt.objs.videos().current():
            video_id = mt.objs._videos.current()._id
            if len(video_id) == 11 and not 'http:' in video_id \
            and not 'https:' in video_id and not 'www.' in video_id:
                return True
            else:
                self.Success = False
                sh.objs.mes (f,_('WARNING')
                            ,_('Wrong input data: "%s"!') \
                            % str(video_id)
                            )
        else:
            self.Success = False
            sh.com.empty(f)
        
    def url(self):
        f = '[Yatube] logic.Video.url'
        if self.Success:
            video = mt.objs.videos().current()
            if not video._url:
                video._url = URL(video._id).video_full()
            return video._url
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success = True

    def delete(self):
        f = '[Yatube] logic.Video.delete'
        if self.Success:
            if self.path():
                video = mt.objs.videos().current()
                # Do not warn about missing files
                if os.path.exists(video._path):
                    Success = sh.File(file=video._path).delete()
                    idir = sh.Directory(path=video._dir)
                    if not idir.files():
                        idir.delete()
                    return Success
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def page(self):
        f = '[Yatube] logic.Video.page'
        if self.Success:
            video = mt.objs.videos().current()
            if not video._page:
                if video._url:
                    video._page = sh.Get(url=video._url).run()
                else:
                    sh.com.empty(f)
            return video._page
        else:
            sh.com.cancel(f)
    
    def assign_online(self):
        f = '[Yatube] logic.Video.assign_online'
        if self.Success:
            video = mt.objs.videos().current()
            if not video._author:
                ''' Do not use 'self.channel_id' or 'self.play_id' here
                    since we do not want unnecessary DB updates.
                '''
                mt.VideoInfo().channel_id()
            video._search = video._author.lower() + ' ' \
                            + video._title.lower()
            video._fdtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
        else:
            sh.com.cancel(f)
                          
    def dump(self):
        f = '[Yatube] logic.Video.dump'
        if self.Success:
            ''' Do no write default data.
                Do not forget to commit where necessary.
            '''
            video = mt.objs.videos().current()
            data = (video._id,video._play_id,video._ch_id,video._author
                   ,video._title,video._desc,video._search,video._len
                   ,video._bytes,video._ptime,video._dtime,video._ftime
                   ,video._ltime,video._fdtime
                   )
            if video._author and video._title:
                objs.db().add_video(data)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
        
    def assign_offline(self,data):
        f = '[Yatube] logic.Video.assign_offline'
        if self.Success:
            if data:
                data_len = 14
                if len(data) == data_len:
                    video          = mt.objs.videos().current()
                    video._id      = data[0]
                    video._play_id = data[1]
                    video._ch_id   = data[2]
                    video._author  = data[3]
                    video._title   = data[4]
                    video._desc    = data[5]
                    video._search  = data[6]
                    video._len     = data[7]
                    video._bytes   = data[8]
                    video._ptime   = data[9]
                    video._dtime   = data[10]
                    video._ftime   = data[11]
                    video._ltime   = data[12]
                    video._fdtime  = data[13]
                else:
                    sh.objs.mes (f,_('ERROR')
                                ,_('The condition "%s" is not observed!')\
                                % '%d == %d' % (len(data),data_len)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def load_image(self):
        ''' We need this code as a separate function since we should be
            able to assign offline data, and 'self.image' is run only
            for online data. Indeed, this function uses 'sharedGUI', but
            it seems easier and more appropriate to use this code in
            the logic, not in the controller. After all, these are
            GUI data that are still data.
        '''
        f = '[Yatube] logic.Video.load_image'
        if self.Success:
            video = mt.objs.videos().current()
            if video._bytes:
                img = sg.Image()
                img._bytes = video._bytes
                img.loader()
                video._image = img.image()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def image(self):
        f = '[Yatube] logic.Video.image'
        if self.Success:
            video = mt.objs.videos().current()
            image = sh.Get (url      = video._thumb
                           ,encoding = None
                           ,Verbose  = False
                           ).run()
            if image:
                video._bytes = image
                self.load_image()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def get(self):
        f = '[Yatube] logic.Video.get'
        if self.Success:
            video = mt.objs.videos().current()
            video.Saved = objs.db().get_video(video._id)
            ''' We use 'self.unsupported' for both online and offline
                value assigning. Do not put it in the end - we want
                DB to be clean of unsupported symbols, because we may
                want to use separate methods instead of the whole
                'self.get' (for example, see
                'yatube.Commands.fill_known').
            '''
            if video.Saved:
                self.assign_offline(video.Saved)
                self.unsupported()
            else:
                sh.log.append (f,_('INFO')
                              ,_('Get new video info: %s') \
                              % str(video._id)
                              )
                self.assign_online()
                self.unsupported()
                self.image()
                self.dump()
        else:
            sh.com.cancel(f)
    
    def summary(self):
        f = '[Yatube] logic.Video.summary'
        if self.Success:
            video = mt.objs.videos().current()
            logic = Video()
            logic.length()
            logic.statistics()
            tmp = io.StringIO()
            tmp.write(_('Author'))
            tmp.write(': ')
            tmp.write(video._author)
            tmp.write('\n')
            tmp.write(_('Title'))
            tmp.write(': ')
            tmp.write(video._title)
            tmp.write('\n')
            tmp.write(_('Length'))
            tmp.write(': ')
            tmp.write(sh.com.human_time(video._len))
            tmp.write('\n')
            tmp.write(_('Views'))
            tmp.write(': ')
            tmp.write(str(video._views))
            tmp.write('\n')
            tmp.write(_('Likes'))
            tmp.write(': ')
            tmp.write(str(video._likes))
            tmp.write('\n')
            tmp.write(_('Dislikes'))
            tmp.write(': ')
            tmp.write(str(video._dislikes))
            tmp.write('\n')
            # ':' is right here to provide a different localization item
            tmp.write(_('Comments:'))
            tmp.write(' ')
            tmp.write(str(video._com_num))
            tmp.write('\n\n')
            tmp.write(_('Description'))
            tmp.write(':\n')
            tmp.write(video._desc)
            tmp.write('\n')
            result = tmp.getvalue()
            tmp.close()
            return result
        else:
            sh.com.cancel(f)
        
    def path(self):
        f = '[Yatube] logic.Video.path'
        if self.Success:
            video = mt.objs.videos().current()
            if not video._path:
                author = sh.FixBaseName (basename = video._author
                                        ,AllOS    = AllOS
                                        ,max_len  = 100
                                        ).run()
                title  = sh.FixBaseName (basename = video._title
                                        ,AllOS    = AllOS
                                        ,max_len  = 100
                                        ).run()
                ''' For some reason, 'youtube_dl' does not screen
                    correctly characters such as '%' and throws an error
                    when downloading videos containing such characters
                    in their path. We delete '%' instead of replacing
                    with '%%' since 'mpv' also seems to have such
                    problems.
                '''
                title = title.replace('%','')
                video._dir  = objs.default().ihome.add_config ('Youtube'
                                                              ,author
                                                              )
                video._path = objs._default.ihome.add_config ('Youtube'
                                                             ,author
                                                             ,title
                                                             )
                video._pathsh = sh.Text (text = sh.Path(video._path).basename()
                                        ,Auto = False
                                        ).shorten (max_len = 20
                                                  ,FromEnd = False
                                                  ,ShowGap = True
                                                  )
                video._path += '.mp4'
            return video._path
        else:
            sh.com.cancel(f)
    
    def make_dir(self):
        f = '[Yatube] logic.Video.make_dir'
        if self.Success:
            video = mt.objs.videos().current()
            if video._dir:
                self.Success = sh.Path(path=video._dir).create()
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def download(self,callback=None):
        f = '[Yatube] logic.Video.download'
        self.make_dir()
        if self.Success:
            video = mt.objs.videos().current()
            if video._path:
                sh.log.append (f,_('INFO')
                              ,_('Download "%s"') % video._path
                              )
                #todo: select format & quality
                options = {'outtmpl'           :video._path
                          ,'format'            :'mp4'
                          ,'ignoreerrors'      :True
                          ,'nooverwrites'      :True
                          ,'noplaylist'        :True
                          ,'nocheckcertificate':True
                          ,'socket_timeout'    :7
                          ,'progress_hooks'    :[callback]
                          }
                try:
                    with youtube_dl.YoutubeDL(options) as ydl:
                        ydl.download([video._id])
                    # Tell other functions the operation was a success
                    return True
                except Exception as e:
                    mt.com.error(f,e)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def stream(self):
        f = '[Yatube] logic.Video.stream'
        if self.Success:
            video = mt.objs.videos().current()
            if video._id:
                #todo: select quality
                ''' If we do not set 'format', then 'youtube_dl'
                    will not provide info_dict['url']. Instead, it will
                    generate 'url' for each available format.
                '''
                options = {'format'            :'best'
                          ,'ignoreerrors'      :True
                          ,'nocheckcertificate':True
                          ,'socket_timeout'    :7
                          }
                try:
                    with youtube_dl.YoutubeDL(options) as ydl:
                        info_dict = ydl.extract_info(video._id,download=False)
                        if 'url' in info_dict:
                            ''' Since the stream url will expire, we do
                                not create a permanent variable.
                            '''
                            return info_dict['url']
                        else:
                            sh.objs.mes (f,_('WARNING')
                                        ,_('Wrong input data!')
                                        )
                except Exception as e:
                    mt.com.error(f,e)
            else:
                sh.com.empty(f)



class URL:
    
    def __init__(self,url):
        f = '[Yatube] logic.URL.__init__'
        self._url = url
        self._url = sh.Input (title = f
                             ,value = self._url
                             ).not_none()
        self._url = str(self._url)
        self._url = self._url.strip()
    
    def video_id(self):
        self.video_full()
        return self._url.replace(pattern1,'')
    
    def video_full(self):
        f = '[Yatube] logic.URL.video_full'
        if self._url:
            self.trash()
            self.trash_v()
            self._url = self._url.replace('/embed/','/watch?v=')
            self.prefixes()
            if not pattern1 in self._url:
                self._url = pattern1 + self._url
        else:
            sh.com.empty(f)
        return self._url
    
    def channel_full(self):
        f = '[Yatube] logic.URL.channel_full'
        if self._url:
            self.trash()
            self.prefixes()
            self.prefixes_ch()
            self.suffixes_ch()
        else:
            sh.com.empty(f)
        return self._url
        
    def trash(self):
        if self._url.endswith('/'):
            self._url = self._url[:-1]

    def trash_v(self):
        ''' There is no need to adjust channel URLs. Using this method
            will corrupt playlist URLs.
        '''
        self._url = self._url.replace ('watch?feature=player_detailpage&v'
                                      ,'watch?v'
                                      )
        self._url = re.sub('#t=\d+','',self._url)
        if 'watch?v' in self._url:
            search = sh.Search (text   = self._url
                               ,search = '?'
                               )
            search.next()
            i = search.next()
            # 'search.i' is updated only on a successful search
            if i and i > 0:
                self._url = self._url[i::]
        else:
            self._url = re.sub('\?.*','',self._url)
        self._url = re.sub('\&.*','',self._url)
        return self._url
    
    def prefixes(self):
        if self._url.startswith('youtube.com'):
            self._url = 'https://www.' + self._url
        elif self._url.startswith('youtu.be'):
            self._url = 'https://' + self._url
        self._url = self._url.replace('http://','https://')
        self._url = self._url.replace('m.youtube.com','youtube.com')
        self._url = self._url.replace('https://youtube.com','https://www.youtube.com')
        self._url = self._url.replace('https://youtu.be/',pattern1)
            
    def prefixes_ch(self):
        if not pattern5 in self._url:
            self._url = pattern5 + self._url
        if '/user/' in self._url or '/channel/' in self._url \
        or '/c/' in self._url:
            pass
        else:
            self._url += '/user'
        
    def suffixes_ch(self):
        if not '/videos' in self._url:
            self._url += '/videos'
        if not pattern4 in self._url:
            self._url += pattern4



class DefaultConfig:
    
    def __init__(self,product='yatube'):
        self.values()
        self.ihome   = sh.Home(app_name=product)
        self.Success = self.ihome.create_conf()
    
    def values(self):
        self._fsubsc  = ''
        self._fblock  = ''
        self._fblockw = ''
        self._fdb     = ''
    
    def db(self):
        f = '[Yatube] logic.DefaultConfig.db'
        if self.Success:
            self._fdb = self.ihome.add_config('yatube.db')
            if self._fdb:
                if os.path.exists(self._fdb):
                    self.Success = sh.File(file=self._fdb).Success
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def block_words(self):
        f = '[Yatube] logic.DefaultConfig.block_words'
        if self.Success:
            self._fblockw = self.ihome.add_config('block words.txt')
            if self._fblockw:
                if os.path.exists(self._fblockw):
                    self.Success = sh.File(file=self._fblockw).Success
                else:
                    iwrite = sh.WriteTextFile (file    = self._fblockw
                                              ,Rewrite = True
                                              )
                    iwrite.write('# ' + _('Put here words to block in titles (case is ignored)'))
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def block_channels(self):
        f = '[Yatube] logic.DefaultConfig.block_channels'
        if self.Success:
            self._fblock = self.ihome.add_config('block channels.txt')
            if self._fblock:
                if os.path.exists(self._fblock):
                    self.Success = sh.File(file=self._fblock).Success
                else:
                    iwrite = sh.WriteTextFile (file    = self._fblock
                                              ,Rewrite = True
                                              )
                    iwrite.write(sample_block)
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def subscribe(self):
        f = '[Yatube] logic.DefaultConfig.subscribe'
        if self.Success:
            self._fsubsc = self.ihome.add_config('subscribe.txt')
            if self._fsubsc:
                if os.path.exists(self._fsubsc):
                    self.Success = sh.File(file=self._fsubsc).Success
                else:
                    iwrite = sh.WriteTextFile (file    = self._fsubsc
                                              ,Rewrite = True
                                              )
                    iwrite.write(sample_subscribe)
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        f = '[Yatube] logic.DefaultConfig.run'
        if self.Success:
            self.subscribe()
            self.block_channels()
            self.block_words()
            self.db()
        else:
            sh.com.cancel(f)



class ChannelHistory:
    
    def __init__(self):
        self.values()
    
    def values(self):
        self._no      = 0
        self._authors = []
        self._urls    = []
    
    def reset(self):
        self.values()
    
    def add(self,author,urls):
        f = '[Yatube] logic.ChannelHistory.add'
        if author and urls:
            if not urls in self._urls:
                self._authors.append(author)
                self._urls.append(urls)
                self._no = len(self._urls) - 1
        else:
            sh.com.empty(f)
    
    def inc(self):
        if self._no == len(self._urls) - 1:
            self._no = 0
        elif self._urls:
            self._no += 1
    
    def dec(self):
        if self._no == 0:
            if self._urls:
                self._no = len(self._urls) - 1
        else:
            self._no -= 1
    
    def prev(self):
        f = '[Yatube] logic.ChannelHistory.prev'
        self.dec()
        cond1 = self._no == 0 and len(self._authors) == 0 \
                              and len(self._urls) == 0
        cond2 = 0 <= self._no < len(self._authors) \
            and 0 <= self._no < len(self._urls)
        if cond1:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
        elif cond2:
            return (self._authors[self._no]
                   ,self._urls[self._no]
                   )
        else:
            min_val = min(len(self._authors),len(self._urls))
            sh.objs.mes (f,_('ERROR')
                        ,_('The condition "%s" is not observed!') \
                        % '%d <= %d < %d' % (0,self._no,min_val)
                        )
    
    def next(self):
        f = '[Yatube] logic.ChannelHistory.next'
        self.inc()
        cond1 = self._no == 0 and len(self._authors) == 0 \
                              and len(self._urls) == 0
        cond2 = 0 <= self._no < len(self._authors) \
            and 0 <= self._no < len(self._urls)
        if cond1:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
        elif cond2:
            return (self._authors[self._no]
                   ,self._urls[self._no]
                   )
        else:
            min_val = min(len(self._authors),len(self._urls))
            sh.objs.mes (f,_('ERROR')
                        ,_('The condition "%s" is not observed!') \
                        % '%d <= %d < %d' % (0,self._no,min_val)
                        )


objs = Objects()
mt.objs.stat()


if __name__ == '__main__':
    url = 'https://www.youtube.com/embed/1jjSSXr5J7A?hl=ru_RU'
    print(URL(url).video_id())
