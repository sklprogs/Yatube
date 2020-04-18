#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import io
import html
import youtube_dl
import skl_shared2.shared as sh
import meta              as mt
import db
from skl_shared2.localize import _

pattern1 = 'https://www.youtube.com/watch?v='
pattern2 = 'https://www.youtube.com/channel/'
pattern3 = 'https://www.youtube.com/'
AllOS    = False


sample_subscribe = '''BostonDynamics	UU7vVhkEfw4nOGp8TyDk7RcQ
Brave Wilderness	UU6E2mP01ZLH_kbAyeazCNdg
Pravda GlazaRezhet	UUgCqhDRyMH1wZBI4OOKLQ8g
Дмитрий ПОТАПЕНКО	UU54SBo5_usXGEoybX1ZVETQ
Мохнатые Друзья	UUqKbBJRz6SGrvUHNoZkpF2w
'''

sample_block = '''Россия 24'''


class Config(sh.Config):

    def __init__(self):
        super().__init__()
        self.Success = objs.get_default().Success
        
    def run(self):
        f = '[Yatube] logic.Config.run'
        if self.Success:
            self.sections = [sh.lg.SectionIntegers
                            ,sh.lg.SectionVariables
                            ]
            self.sections_abbr = [sh.lg.SectionIntegers_abbr
                                 ,sh.lg.SectionVariables_abbr
                                 ]
            self.sections_func = [sh.lg.config_parser.getint
                                 ,sh.lg.config_parser.get
                                 ]
            self.message = _('The following sections and/or keys are missing:') + '\n'
            self.total_keys = 0
            self.changed_keys = 0
            self.missing_keys = 0
            self.missing_sections = 0
            # Create these keys before reading the config
            self.path = objs.get_default().ihome.add_config('yatube.cfg')
            self.reset()
            iread = sh.ReadTextFile(self.path)
            self.text = iread.get()
            self.Success = iread.Success
            self.load_default()
            if os.path.exists(self.path):
                self.open()
            else:
                self.Success = False
            self.check()
            self.load()
        else:
            sh.com.cancel(f)

    # Do not rename, this procedure is called by 'shared'
    def load_default(self):
        self._load_default_int()
        self._load_default_var()
    
    def _load_default_int(self):
        sh.lg.globs['int'].update ({
            'max_videos' :50
                                  })
    
    def _load_default_var(self):
        sh.lg.globs['var'].update ({
            'resolution' :'auto'
           ,'quality'    :'best'
                                  })

    def reset(self):
        sh.lg.globs['bool']  = {}
        sh.lg.globs['float'] = {}
        sh.lg.globs['int']   = {}
        sh.lg.globs['var']   = {}



class Commands:
    
    def extract_resolution(self,text):
        # '<=1080p' -> '1080'
        match = re.match('<=(\d+)p',text)
        if match:
            return match.group(1)
        else:
            return ''



class Feed:
    
    def __init__(self):
        self.token_prev = 0
        self.token_next = 0
    
    def get_token(self):
        f = '[Yatube] logic.Feed.get_token'
        if mt.objs.get_videos().videos:
            self.token_next = mt.objs.videos.videos[-1].fdtime
            self.token_prev = mt.objs.videos.videos[0].fdtime
            date_next = sh.Time (tstamp = self.token_next
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            date_prev = sh.Time (tstamp = self.token_prev
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            mes = _('Previous page token: {}').format(date_prev)
            sh.objs.get_mes(f,mes,True).show_debug()
            mes = _('Next page token: {}').format(date_next)
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.rep_empty(f)
            ''' This returns correct tokens for the 1st page if we are
                out of bounds.
            '''
            self.token_prev = 0
            self.token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
    
    def fetch(self):
        self.token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
        self.fetch_next()
    
    def fetch_prev(self):
        f = '[Yatube] logic.Feed.fetch_prev'
        ids = objs.get_db().feed_prev (fdtime = self.token_prev
                                  ,limit  = mt.MAX_VIDEOS
                                  )
        if ids:
            for vid in ids:
                video = mt.Video()
                video.id_ = vid
                mt.objs.videos.add(video)
        else:
            sh.com.rep_empty(f)
    
    def fetch_next(self):
        f = '[Yatube] logic.Feed.fetch_next'
        ids = objs.get_db().feed_next (fdtime = self.token_next
                                  ,limit  = mt.MAX_VIDEOS
                                  )
        if ids:
            for vid in ids:
                video = mt.Video()
                video.id_ = vid
                mt.objs.videos.add(video)
        else:
            sh.com.rep_empty(f)



class Favorites:
    
    def __init__(self):
        self.token_prev = 0
        self.token_next = 0
    
    def get_token(self):
        f = '[Yatube] logic.Favorites.get_token'
        if mt.objs.get_videos().videos:
            self.token_next = mt.objs.videos.videos[-1].ftime
            self.token_prev = mt.objs.videos.videos[0].ftime
            date_next = sh.Time (tstamp  = self.token_next
                                ,pattern = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            date_prev = sh.Time (tstamp  = self.token_prev
                                ,pattern = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            mes = _('Previous page token: {}').format(date_prev)
            sh.objs.get_mes(f,mes,True).show_debug()
            mes = _('Next page token: {}').format(date_next)
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.rep_empty(f)
            ''' This returns correct tokens for the 1st page if we are
                out of bounds.
            '''
            self.token_prev = 0
            self.token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
    
    def fetch(self):
        self.token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
        self.fetch_next()
    
    def fetch_prev(self):
        f = '[Yatube] logic.Favorites.fetch_prev'
        ids = objs.get_db().get_fav_prev (ftime = self.token_prev
                                         ,limit = mt.MAX_VIDEOS
                                         )
        if ids:
            for id_ in ids:
                video = mt.Video()
                video.id_ = id_
                mt.objs.videos.add(video)
        else:
            sh.com.rep_empty(f)
    
    def fetch_next(self):
        f = '[Yatube] logic.Favorites.fetch_next'
        ids = objs.get_db().get_fav_next (ftime = self.token_next
                                         ,limit = mt.MAX_VIDEOS
                                         )
        if ids:
            for vid in ids:
                video = mt.Video()
                video.id_ = vid
                mt.objs.videos.add(video)
        else:
            sh.com.rep_empty(f)



class Watchlist:
    
    def __init__(self):
        self.token_prev = 0
        self.token_next = 0
    
    def get_token(self):
        f = '[Yatube] logic.Watchlist.get_token'
        if mt.objs.get_videos().videos:
            self.token_next = mt.objs.videos.videos[-1].ltime
            self.token_prev = mt.objs.videos.videos[0].ltime
            date_next = sh.Time (tstamp = self.token_next
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            date_prev = sh.Time (tstamp = self.token_prev
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            mes = _('Previous page token: {}').format(date_prev)
            sh.objs.get_mes(f,mes,True).show_debug()
            mes = _('Next page token: {}').format(date_next)
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.rep_empty(f)
            ''' This returns correct tokens for the 1st page if we are
                out of bounds.
            '''
            self.token_prev = 0
            self.token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
    
    def fetch(self):
        self.token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
        self.fetch_next()
    
    def fetch_prev(self):
        f = '[Yatube] logic.Watchlist.fetch_prev'
        ids = objs.get_db().get_watch_prev (ltime = self.token_prev
                                           ,limit = mt.MAX_VIDEOS
                                           )
        if ids:
            for id_ in ids:
                video = mt.Video()
                video.id_ = id_
                mt.objs.videos.add(video)
        else:
            sh.com.rep_empty(f)
    
    def fetch_next(self):
        f = '[Yatube] logic.Watchlist.fetch_next'
        ids = objs.get_db().get_watch_next (ltime = self.token_next
                                           ,limit = mt.MAX_VIDEOS
                                           )
        if ids:
            for id_ in ids:
                video = mt.Video()
                video.id_ = id_
                mt.objs.videos.add(video)
        else:
            sh.com.rep_empty(f)



class History:
    
    def __init__(self):
        self.token_next = 0
        self.token_prev = 0
    
    def get_token(self):
        f = '[Yatube] logic.History.get_token'
        if mt.objs.get_videos().videos:
            self.token_next = mt.objs.videos.videos[-1].dtime
            self.token_prev = mt.objs.videos.videos[0].dtime
            date_next = sh.Time (tstamp = self.token_next
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            date_prev = sh.Time (tstamp = self.token_prev
                                ,pattern    = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            mes = _('Previous page token: {}').format(date_prev)
            sh.objs.get_mes(f,mes,True).show_debug()
            mes = _('Next page token: {}').format(date_next)
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.rep_empty(f)
            ''' This returns correct tokens for the 1st page if we are
                out of bounds.
            '''
            self.token_prev = 0
            self.token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
    
    def fetch(self):
        self.token_next = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
        self.fetch_next()
    
    def fetch_prev(self):
        f = '[Yatube] logic.History.fetch_prev'
        ids = objs.get_db().get_history_prev (dtime = self.token_prev
                                             ,limit = mt.MAX_VIDEOS
                                             )
        if ids:
            for vid in ids:
                video = mt.Video()
                video.id_ = vid
                mt.objs.videos.add(video)
        else:
            sh.com.rep_empty(f)
    
    def fetch_next(self):
        f = '[Yatube] logic.History.fetch_next'
        ids = objs.get_db().get_history_next (dtime = self.token_next
                                             ,limit = mt.MAX_VIDEOS
                                             )
        if ids:
            for vid in ids:
                video = mt.Video()
                video.id_ = vid
                mt.objs.videos.add(video)
        else:
            sh.com.rep_empty(f)



class Channel:
    
    def __init__(self,myid=''):
        self.set_values()
        if myid:
            self.reset(myid)
    
    def run(self):
        f = '[Yatube] logic.Channel.run'
        if self.Success:
            mt.objs.get_playlist().reset(self.playid)
            mt.objs.playlist.run()
            for video in mt.objs.videos.videos:
                self.ids.append(video.id_)
        else:
            sh.com.cancel(f)
        return self.ids
    
    def reset(self,myid):
        self.autodetect(myid)
    
    def autodetect(self,myid):
        f = '[Yatube] logic.Channel.autodetect'
        if myid:
            #TODO: implement autodetection
            self.playid = myid
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_values(self):
        self.Success = True
        self.ids     = []
        self.playid  = ''



class Time:
    
    def __init__(self):
        self.days   = []
        self.months = []
        self.years  = []
        self.year   = ''
        self.day    = ''
        self.month  = ''
        self.itime = sh.Time(pattern='%d')
    
    def get_days(self):
        self.days = [str(day+1) for day in range(31)]
        # 'sh.Time' outputs a day number preceded by 0
        self.days = tuple ('0' + day if len(day) == 1 else day \
                           for day in self.days
                          )
        return self.days
        
    def get_months(self):
        self.months = (_('Jan'),_('Feb'),_('Mar'),_('Apr'),_('May')
                      ,_('Jun'),_('Jul'),_('Aug'),_('Sep'),_('Oct')
                      ,_('Nov'),_('Dec')
                      )
        return self.months
        
    def get_years(self):
        f = '[Yatube] logic.Time.get_years'
        # Year of Youtube birth
        first_year = 2005
        last_year  = self.itime.get_year()
        last_year  = sh.Input(f,last_year).get_integer()
        if not last_year > first_year:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes,True).show_warning()
            last_year = 2018
        self.years = tuple (str(year) for year in range (first_year
                                                        ,last_year + 1
                                                        )
                           )
        return self.years
        
    def set_date(self,DaysDelta=7):
        self.itime.add_days(days_delta=-DaysDelta)
        self.year = str(self.itime.get_year())
        self.day = self.itime.get_date()
        self.itime.get_month_abbr()
        self.month = self.itime.localize_month_abbr()


class Constants:
    
    def __init__(self):
        self.countries = []
        self.trending  = []
        
    def get_countries(self):
        self.countries = {_('Algeria')                : 'DZ'
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
        return self.countries
        
    def get_trending(self):
        self.trending = [_('Trending')] \
                         + sorted(self.get_countries().keys())
        return self.trending



class Extractor:
       
    def __init__(self):
        self.set_values()
    
    def set_url(self):
        f = '[Yatube] logic.Extractor.set_url'
        if self.Success:
            ''' Owing to parser peculiarities, if the link is
                a non-conventional link to a Youtube video, it should be
                first converted to a conventional link (see 'pattern1').
                Youtube playlists, search results and links from
                external sites may be preserved in the original form.
                #TODO: Fix the parser to get rid of this.
            '''
            id_ = URL(self.url).get_videoid()
            if len(id_) == 11 and not 'https:' in id_ \
            and not 'http:' in id_ and not 'www.' in id_:
                self.url = URL(id_).get_video_full()
        else:
            sh.com.cancel(f)
        
    def reset(self,url=''):
        f = '[Yatube] logic.Extractor.reset'
        self.set_values()
        if url:
            self.url = url
        else:
            self.Success = False
            sh.com.rep_empty(f)
        
    def set_values(self):
        self.Success = True
        self.url  = ''
        self.htm  = ''
        self.urls = []
    
    def set_page(self):
        f = '[Yatube] logic.Extractor.set_page'
        if self.Success:
            if self.htm or self.urls:
                sh.com.rep_lazy(f)
            else:
                response = sh.Get(url=self.url).run()
                if response:
                    self.htm = response
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_urls(self):
        f = '[Yatube] logic.Extractor.set_urls'
        if self.Success:
            if self.urls:
                sh.com.rep_lazy(f)
            else:
                ilinks = sh.Links (text = self.htm
                                  ,root = 'href="'
                                  )
                ilinks.get_poses()
                old = list(ilinks.links)
                ilinks = sh.Links (text = self.htm
                                  ,root = 'src="'
                                  )
                ilinks.get_poses()
                ''' #NOTE: if links from both root elements are present,
                    their order may be desynchronized.
                '''
                ilinks.links += old
                if 'youtube' in self.url or 'youtu.be' in self.url:
                    ilinks.links = ['https://www.youtube.com' + link \
                                    for link in ilinks.links \
                                    if link.startswith('/watch?v=')
                                   ]
                else:
                    ilinks.redirec()
                    ''' We should do our best here to ensure that
                        the URL will refer to a Youtube video. There
                        could be links to 'youtube.com', e.g., from
                        'account.google.com' that will not refer to
                        videos. We need a slash here because there can
                        be links like
                        .../uploads/youtu.be-bv2OGph5Kec-330x225.jpg.
                    '''
                    ilinks.links = [link for link in ilinks.links 
                                    if 'youtu.be/' in link 
                                    or 'youtube.com/watch?v=' in link 
                                    or 'youtube.com/embed/' in link
                                   ]
                    ilinks.get_valid()
                old = list(ilinks.links)
                ''' Previous algorithms consider a link as valid if it has
                    'youtu(be)' in its tag, and we have just ID there, so
                    this should be put after those algorithms.
                '''
                ilinks = sh.Links (text = self.htm
                                  ,root = 'data-pe-videoid="'
                                  )
                ilinks.get_poses()
                ilinks.links += old
                ilinks.links = [URL(url=link).get_videoid() \
                                for link in ilinks.links
                               ]
                ilinks.delete_duplicates()
                self.urls = ilinks.links
                mes = _('Fetched {} links').format(len(self.urls))
                sh.objs.get_mes(f,mes,True).show_info()
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.set_url()
        self.set_page()
        self.set_urls()
        return self.urls



class Lists:
    
    def __init__(self):
        self.set_values()
        
    def reset(self):
        self.set_values()
        self.idefault = objs.get_default()
        self.Success  = self.idefault.Success
        self.load()
    
    def set_values(self):
        self.block   = ''
        self.blockw  = ''
        self.subsc   = ''
        self.blauth  = []
        self.blwords = []
        self.subauth = []
        self.subids  = []
    
    def match_blocked_word(self,word):
        f = '[Yatube] logic.Lists.match_blocked_word'
        if self.Success:
            word = word.lower()
            for item in self.blwords:
                ''' Contents of 'self.blwords' should already be
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
            text = sh.ReadTextFile(file=self.idefault.fblock).get()
            text = sh.Text(text=text).delete_comments()
            # We should allow empty files
            self.block  = text
            self.blauth = text.splitlines()
            # Blocked words
            text = sh.ReadTextFile(file=self.idefault.fblockw).get()
            text = sh.Text(text=text).delete_comments()
            # We should allow empty files
            self.blockw  = text
            self.blwords = text.splitlines()
            self.blwords = [item.lower() for item in self.blwords]
            # Suppress errors on empty text
            if os.path.exists(self.idefault.fsubsc):
                dic = sh.Dic (file     = self.idefault.fsubsc
                             ,Sortable = False
                             )
                self.Success = dic.Success
                if self.Success:
                    self.subsc   = dic.text
                    self.subauth = dic.orig
                    self.subids  = dic.transl
            if self.subauth:
                self.subauth, self.subids = (list(x) for x \
                in zip (*sorted (zip (self.subauth, self.subids)
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
        self.online = self.lists = self.const = self.default \
                    = self.db = self.channels = self.channel \
                    = self.extractor = self.history \
                    = self.watchlist = self.favorites = self.feed \
                    = self.config = None
    
    def get_config(self):
        if self.config is None:
            self.config = Config()
            self.config.run()
        return self.config
    
    def get_feed(self):
        if self.feed is None:
            self.feed = Feed()
        return self.feed
    
    def get_favorites(self):
        if self.favorites is None:
            self.favorites = Favorites()
        return self.favorites
    
    def get_watchlist(self):
        if self.watchlist is None:
            self.watchlist = Watchlist()
        return self.watchlist
    
    def get_history(self):
        if self.history is None:
            self.history = History()
        return self.history
    
    def get_extractor(self):
        if self.extractor is None:
            self.extractor = Extractor()
        return self.extractor
    
    def get_channel(self):
        if self.channel is None:
            self.channel = Channel()
        return self.channel
    
    def get_db(self):
        f = '[Yatube] logic.Objects.get_db'
        if self.db is None:
            path = self.get_default(product='yatube').fdb
            if self.default.Success:
                self.db = db.DB(path=path)
            else:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f,mes,True).show_warning()
                self.db = db.DB()
        return self.db
    
    def get_default(self,product='yatube'):
        if not self.default:
            self.default = DefaultConfig(product=product)
            self.default.run()
        return self.default
    
    def get_const(self):
        if not self.const:
            self.const = Constants()
            self.const.get_countries()
            self.const.get_trending()
        return self.const
    
    def get_online(self):
        if not self.online:
            self.online = sh.Online()
        return self.online
        
    def get_lists(self):
        if not self.lists:
            self.lists = Lists()
        return self.lists
    
    def get_channels(self):
        if not self.channels:
            self.channels = ChannelHistory()
        return self.channels



class Video:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.set_values()
        self.check()
    
    def delete_unsupported(self):
        video        = mt.objs.get_videos().get_current()
        video.author = sh.Text(video.author).delete_unsupported()
        video.title  = sh.Text(video.title).delete_unsupported()
        video.desc   = sh.Text(video.desc).delete_unsupported()
        video.search = sh.Text(video.search).delete_unsupported()
        video.author = html.unescape(video.author)
        video.title  = html.unescape(video.title)
        video.desc   = html.unescape(video.desc)
        video.search = html.unescape(video.search)
    
    def get_length(self):
        f = '[Yatube] logic.Video.get_length'
        video = mt.objs.get_videos().get_current()
        if not video.len_:
            if mt.VideoInfo().get_length():
                objs.get_db().update_len(video.id_,video.len_)
            else:
                sh.com.rep_empty(f)
        return video.len_
    
    def get_stat(self):
        f = '[Yatube] logic.Video.get_stat'
        video = mt.objs.get_videos().get_current()
        ''' Likes/dislikes/number of comments can be 0, so we shoud rely
            on 'video.views' only.
        '''
        if not video.views:
            # Return True if metadata were fetched successfully
            return mt.VideoInfo().get_stat()
        return True
    
    def get_playid(self):
        f = '[Yatube] logic.Video.get_playid'
        video = mt.objs.get_videos().get_current()
        if not video.playid:
            channel_id = self.get_channel_id()
            if channel_id:
                mt.objs.get_playid().reset(channel_id)
                playid = mt.objs.playid.get_by_channel_id()
                if playid:
                    video.playid = playid
                    objs.get_db().update_playid(video.id_,video.playid)
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        return video.playid
    
    def get_channel_id(self):
        f = '[Yatube] logic.Video.get_channel_id'
        video = mt.objs.get_videos().get_current()
        if not video.chid:
            channel_id = mt.VideoInfo().get_channel_id()
            if channel_id:
                video.chid = channel_id
                objs.get_db().update_ch_id(video.id_,video.chid)
            else:
                sh.com.rep_empty(f)
        return video.chid
    
    def check(self):
        f = '[Yatube] logic.Video.check'
        if mt.objs.get_videos().get_current():
            videoid = mt.objs.videos.get_current().id_
            if len(videoid) == 11 and not 'http:' in videoid \
            and not 'https:' in videoid and not 'www.' in videoid:
                return True
            else:
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(videoid)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            self.Success = False
            sh.com.rep_empty(f)
        
    def get_url(self):
        f = '[Yatube] logic.Video.get_url'
        if self.Success:
            video = mt.objs.get_videos().get_current()
            if not video.url:
                video.url = URL(video.id_).get_video_full()
            return video.url
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True

    def delete(self):
        f = '[Yatube] logic.Video.delete'
        if self.Success:
            if self.get_path():
                video = mt.objs.get_videos().get_current()
                # Do not warn about missing files
                if os.path.exists(video.path):
                    Success = sh.File(file=video.path).delete()
                    idir = sh.Directory(path=video.dir_)
                    if not idir.get_files():
                        idir.delete()
                    return Success
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_page(self):
        f = '[Yatube] logic.Video.get_page'
        if self.Success:
            video = mt.objs.get_videos().get_current()
            if not video.page:
                if video.url:
                    video.page = sh.Get(url=video.url).run()
                else:
                    sh.com.rep_empty(f)
            return video.page
        else:
            sh.com.cancel(f)
    
    def assign_online(self):
        f = '[Yatube] logic.Video.assign_online'
        if self.Success:
            video = mt.objs.get_videos().get_current()
            if not video.author:
                ''' Do not use 'self.channel_id' or 'self.playid' here
                    since we do not want unnecessary DB updates.
                '''
                mt.VideoInfo().get_channel_id()
            video.search = video.author.lower() + ' ' \
                         + video.title.lower()
            video.fdtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
        else:
            sh.com.cancel(f)
                          
    def dump(self):
        f = '[Yatube] logic.Video.dump'
        if self.Success:
            ''' Do no write default data.
                Do not forget to commit where necessary.
            '''
            video = mt.objs.get_videos().get_current()
            data = (video.id_,video.playid,video.chid,video.author
                   ,video.title,video.desc,video.search,video.len_
                   ,video.pause,video.bytes_,video.ptime,video.dtime
                   ,video.ftime,video.ltime,video.fdtime
                   )
            if video.author and video.title:
                objs.get_db().add_video(data)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        
    def assign_offline(self,data):
        f = '[Yatube] logic.Video.assign_offline'
        if self.Success:
            if data:
                data_len = 15
                if len(data) == data_len:
                    video        = mt.objs.get_videos().get_current()
                    video.id_    = data[0]
                    video.playid = data[1]
                    video.chid   = data[2]
                    video.author = data[3]
                    video.title  = data[4]
                    video.desc   = data[5]
                    video.search = data[6]
                    video.len_   = data[7]
                    video.pause  = data[8]
                    video.bytes_ = data[9]
                    video.ptime  = data[10]
                    video.dtime  = data[11]
                    video.ftime  = data[12]
                    video.ltime  = data[13]
                    video.fdtime = data[14]
                else:
                    sub = '{} == {}'.format(len(data),data_len)
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                sh.com.rep_empty(f)
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
            video = mt.objs.get_videos().get_current()
            if video.bytes_:
                img = sh.Image()
                img.bytes_ = video.bytes_
                img.get_loader()
                video.image = img.get_image()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_image(self):
        f = '[Yatube] logic.Video.set_image'
        if self.Success:
            video = mt.objs.get_videos().get_current()
            image = sh.Get (url     = video.thumb
                           ,coding  = None
                           ,Verbose = False
                           ).run()
            if image:
                video.bytes_ = image
                self.load_image()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_new(self):
        ''' Separating this code allows to skip a slow 'get_video'
            procedure when we are processing videos not known by the DB.
        '''
        f = '[Yatube] logic.Video.set_new'
        if self.Success:
            mes = _('Get new video info: {}')
            mes = mes.format(mt.objs.get_videos().get_current().id_)
            sh.objs.get_mes(f,mes,True).show_info()
            self.assign_online()
            self.delete_unsupported()
            self.set_image()
            self.dump()
        else:
            sh.com.cancel(f)
    
    def get(self):
        f = '[Yatube] logic.Video.get'
        if self.Success:
            video = mt.objs.get_videos().get_current()
            video.Saved = objs.get_db().get_video(video.id_)
            ''' We use 'self.unsupported' for both online and offline
                value assigning. Do not put it in the end - we want
                DB to be clean of unsupported symbols, because we may
                want to use separate methods instead of the whole
                'self.get' (for example, see
                'yatube.Commands.fill_known').
            '''
            if video.Saved:
                self.assign_offline(video.Saved)
                self.delete_unsupported()
            else:
                self.set_new()
        else:
            sh.com.cancel(f)
    
    def show_summary(self):
        f = '[Yatube] logic.Video.show_summary'
        if self.Success:
            video = mt.objs.get_videos().get_current()
            logic = Video()
            logic.get_length()
            logic.get_stat()
            tmp = io.StringIO()
            tmp.write(_('Author'))
            tmp.write(': ')
            tmp.write(video.author)
            tmp.write('\n')
            tmp.write(_('Title'))
            tmp.write(': ')
            tmp.write(video.title)
            tmp.write('\n')
            tmp.write(_('Date'))
            tmp.write(': ')
            tmp.write(str(sh.Time(tstamp=video.ptime).get_date()))
            tmp.write('\n')
            tmp.write(_('Length'))
            tmp.write(': ')
            tmp.write(sh.com.get_human_time(video.len_))
            tmp.write('\n')
            tmp.write(_('Views'))
            tmp.write(': ')
            tmp.write(sh.com.set_figure_commas(video.views))
            tmp.write('\n')
            tmp.write(_('Likes'))
            tmp.write(': ')
            if video.likes < 0:
                tmp.write(_('Disabled'))
            else:
                tmp.write(sh.com.set_figure_commas(video.likes))
            tmp.write('\n')
            tmp.write(_('Dislikes'))
            tmp.write(': ')
            if video.dislikes < 0:
                tmp.write(_('Disabled'))
            else:
                tmp.write(sh.com.set_figure_commas(video.dislikes))
            tmp.write('\n')
            # ':' is right here to provide a different localization item
            tmp.write(_('Comments:'))
            tmp.write(' ')
            if video.com_num < 0:
                tmp.write(_('Disabled'))
            else:
                tmp.write(sh.com.set_figure_commas(video.com_num))
            tmp.write('\n\n')
            tmp.write(_('Description'))
            tmp.write(':\n')
            tmp.write(video.desc)
            tmp.write('\n')
            result = tmp.getvalue()
            tmp.close()
            return result
        else:
            sh.com.cancel(f)
        
    def get_path(self):
        f = '[Yatube] logic.Video.get_path'
        if self.Success:
            video = mt.objs.get_videos().get_current()
            if not video.path:
                author = sh.FixBaseName (basename = video.author
                                        ,AllOS    = AllOS
                                        ,max_len  = 100
                                        ).run()
                title  = sh.FixBaseName (basename = video.title
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
                video.dir_ = objs.get_default().ihome.add_config ('Youtube'
                                                                 ,author
                                                                 )
                video.path = objs.default.ihome.add_config ('Youtube'
                                                           ,author
                                                           ,title
                                                           )
                video.pathsh = sh.Text (text = sh.Path(video.path).get_basename()
                                       ,Auto = False
                                       ).shorten (max_len = 20
                                                 ,FromEnd = False
                                                 ,ShowGap = True
                                                 )
                ''' #NOTE: youtube_dl may try to use ffmpeg to merge
                    audio and video, but ffmpeg reacts to file
                    extentions rather than to magic numbers and that
                    causes files with a wrong extension to be
                    unplayable.
                '''
                video.path += '.mp4'
            return video.path
        else:
            sh.com.cancel(f)
    
    def make_dir(self):
        f = '[Yatube] logic.Video.make_dir'
        if self.Success:
            video = mt.objs.get_videos().get_current()
            if video.dir_:
                self.Success = sh.Path(path=video.dir_).create()
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def download(self,callback=None,format_='mp4'):
        f = '[Yatube] logic.Video.download'
        self.make_dir()
        if self.Success:
            video = mt.objs.get_videos().get_current()
            if video.path:
                mes = _('Download "{}"').format(video.path)
                sh.objs.get_mes(f,mes,True).show_info()
                #TODO: select quality
                ''' There was a video for which 'webm' downloaded
                    successfully, but 'mp4' failed.
                '''
                options = {'outtmpl'           :video.path
                          ,'format'            :format_
                          ,'nooverwrites'      :True
                          ,'noplaylist'        :True
                          ,'nocheckcertificate':True
                          ,'socket_timeout'    :7
                          ,'progress_hooks'    :[callback]
                          }
                try:
                    with youtube_dl.YoutubeDL(options) as ydl:
                        ydl.download([video.id_])
                    # Tell other functions the operation was a success
                    return True
                except Exception as e:
                    mt.com.show_error(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def generate_url(self,videoid,quality='best'):
        f = '[Yatube] logic.Video.generate_url'
        if self.Success:
            if videoid:
                ''' If we do not set 'format', then 'youtube_dl'
                    will not provide info_dict['url']. Instead, it will
                    generate 'url' for each available format.
                '''
                options = {'format'            :quality
                          ,'ignoreerrors'      :True
                          ,'nocheckcertificate':True
                          ,'socket_timeout'    :7
                          }
                try:
                    ydl = youtube_dl.YoutubeDL(options)
                    info_dict = ydl.extract_info(videoid,download=False)
                    if info_dict:
                        if 'url' in info_dict:
                            ''' Since the stream url will expire, we
                                do not create a permanent variable.
                            '''
                            return info_dict['url']
                        else:
                            mes = _('Wrong input data!')
                            sh.objs.get_mes(f,mes).show_warning()
                except Exception as e:
                    mt.com.show_error(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def stream(self,quality='best'):
        ''' Stream a video with preset parameters. Examples of 'quality'
            settings: 'best', 'worst', 'worst[height<=1080]',
            'best[height<=480]'.
        '''
        f = '[Yatube] logic.Video.stream'
        if self.Success:
            video   = mt.objs.get_videos().get_current()
            gen_url = self.generate_url(video.id_,quality)
            if gen_url:
                return gen_url
            else:
                gen_url = self.generate_url(video.id_)
                if gen_url:
                    mes = _('Selected quality is not available, using default quality.')
                    sh.objs.get_mes(f,mes).show_warning()
                    return gen_url
                else:
                    mes = _('This video is not available.')
                    sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.cancel(f)



class URL:
    
    def __init__(self,url):
        f = '[Yatube] logic.URL.__init__'
        self.url = url
        self.url = sh.Input(f,self.url).get_not_none()
        self.url = str(self.url)
        self.url = self.url.strip()
    
    def get_videoid(self):
        self.get_video_full()
        return self.url.replace(pattern1,'')
    
    def get_video_full(self):
        f = '[Yatube] logic.URL.get_video_full'
        if self.url:
            self.trash()
            self.trash_v()
            self.url = self.url.replace('/embed/','/watch?v=')
            self.set_prefixes()
            if not pattern1 in self.url:
                self.url = pattern1 + self.url
        else:
            sh.com.rep_empty(f)
        return self.url
    
    def get_channel_full(self):
        f = '[Yatube] logic.URL.get_channel_full'
        if self.url:
            self.trash()
            self.set_prefixes()
            self.set_prefixes_ch()
            self.set_suffixes_ch()
        else:
            sh.com.rep_empty(f)
        return self.url
        
    def trash(self):
        if self.url.endswith('/'):
            self.url = self.url[:-1]

    def trash_v(self):
        ''' There is no need to adjust channel URLs. Using this method
            will corrupt playlist URLs.
        '''
        self.url = self.url.replace ('watch?feature=player_detailpage&v'
                                    ,'watch?v'
                                    )
        self.url = re.sub('#t=\d+','',self.url)
        if 'watch?v' in self.url:
            search = sh.Search (text    = self.url
                               ,pattern = '?'
                               )
            search.get_next()
            i = search.get_next()
            # 'search.i' is updated only on a successful search
            if i and i > 0:
                self.url = self.url[i::]
        else:
            self.url = re.sub('\?.*','',self.url)
        self.url = re.sub('\&.*','',self.url)
        return self.url
    
    def set_prefixes(self):
        if self.url.startswith('youtube.com'):
            self.url = 'https://www.' + self.url
        elif self.url.startswith('youtu.be'):
            self.url = 'https://' + self.url
        self.url = self.url.replace('http://','https://')
        self.url = self.url.replace('m.youtube.com','youtube.com')
        self.url = self.url.replace('https://youtube.com','https://www.youtube.com')
        self.url = self.url.replace('https://youtu.be/',pattern1)
            
    def set_prefixes_ch(self):
        if not pattern3 in self.url:
            self.url = pattern3 + self.url
        if '/user/' in self.url or '/channel/' in self.url \
        or '/c/' in self.url:
            pass
        else:
            self.url += '/user'
        
    def set_suffixes_ch(self):
        if not '/videos' in self.url:
            self.url += '/videos'



class DefaultConfig:
    
    def __init__(self,product='yatube'):
        self.set_values()
        self.ihome   = sh.Home(app_name=product)
        self.Success = self.ihome.create_conf()
    
    def set_values(self):
        self.fsubsc  = ''
        self.fblock  = ''
        self.fblockw = ''
        self.fdb     = ''
        self.fdconf  = ''
        self.fconf   = ''
        self.api_key = ''
    
    def get_api_key(self):
        f = '[MClient] logic.DefaultConfig.get_api_key'
        if self.Success:
            if not self.api_key:
                file = self.ihome.add_config('api-key.txt')
                self.api_key = sh.ReadTextFile(file).get()
                self.api_key = self.api_key.strip()
        else:
            sh.com.cancel(f)
        return self.api_key
    
    def get_config(self):
        f = '[MClient] logic.DefaultConfig.get_config'
        if self.Success:
            if not self.fconf:
                self.fconf = self.ihome.add_config('yatube.cfg')
                if os.path.exists(self.fconf):
                    self.Success = sh.File(file=self.fconf).Success
                else:
                    self.get_default_config()
                    if self.Success:
                        self.Success = sh.File (file = self.fdconf
                                               ,dest = self.fconf
                                               ).copy()
                    else:
                        sh.com.cancel(f)
            return self.fconf
        else:
            sh.com.cancel(f)
    
    def get_default_config(self):
        f = '[Yatube] logic.DefaultConfig.get_default_config'
        if self.Success:
            if not self.fdconf:
                self.fdconf = sh.objs.get_pdir().add ('..','resources'
                                                  ,'default.cfg'
                                                  )
                self.Success = sh.File(file=self.fdconf).Success
            return self.fdconf
        else:
            sh.com.cancel(f)
    
    def set_db(self):
        f = '[Yatube] logic.DefaultConfig.set_db'
        if self.Success:
            self.fdb = self.ihome.add_config('yatube.db')
            if self.fdb:
                if os.path.exists(self.fdb):
                    self.Success = sh.File(file=self.fdb).Success
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_block_words(self):
        f = '[Yatube] logic.DefaultConfig.set_block_words'
        if self.Success:
            self.fblockw = self.ihome.add_config('block words.txt')
            if self.fblockw:
                if os.path.exists(self.fblockw):
                    self.Success = sh.File(file=self.fblockw).Success
                else:
                    iwrite = sh.WriteTextFile (file    = self.fblockw
                                              ,Rewrite = True
                                              )
                    iwrite.write('# ' + _('Put here words to block in titles (case is ignored)'))
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_block_channels(self):
        f = '[Yatube] logic.DefaultConfig.set_block_channels'
        if self.Success:
            self.fblock = self.ihome.add_config('block channels.txt')
            if self.fblock:
                if os.path.exists(self.fblock):
                    self.Success = sh.File(file=self.fblock).Success
                else:
                    iwrite = sh.WriteTextFile (file    = self.fblock
                                              ,Rewrite = True
                                              )
                    iwrite.write(sample_block)
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def subscribe(self):
        f = '[Yatube] logic.DefaultConfig.subscribe'
        if self.Success:
            self.fsubsc = self.ihome.add_config('subscribe.txt')
            if self.fsubsc:
                if os.path.exists(self.fsubsc):
                    self.Success = sh.File(file=self.fsubsc).Success
                else:
                    iwrite = sh.WriteTextFile (file    = self.fsubsc
                                              ,Rewrite = True
                                              )
                    iwrite.write(sample_subscribe)
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        f = '[Yatube] logic.DefaultConfig.run'
        if self.Success:
            self.get_default_config()
            self.get_config()
            self.subscribe()
            self.set_block_channels()
            self.set_block_words()
            self.set_db()
        else:
            sh.com.cancel(f)



class ChannelHistory:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.no      = 0
        self.authors = []
        self.urls    = []
    
    def reset(self):
        self.set_values()
    
    def add(self,author,urls):
        f = '[Yatube] logic.ChannelHistory.add'
        if author and urls:
            if not urls in self.urls:
                self.authors.append(author)
                self.urls.append(urls)
                self.no = len(self.urls) - 1
        else:
            sh.com.rep_empty(f)
    
    def inc(self):
        if self.no == len(self.urls) - 1:
            self.no = 0
        elif self.urls:
            self.no += 1
    
    def dec(self):
        if self.no == 0:
            if self.urls:
                self.no = len(self.urls) - 1
        else:
            self.no -= 1
    
    def get_prev(self):
        f = '[Yatube] logic.ChannelHistory.get_prev'
        self.dec()
        cond1 = self.no == 0 and len(self.authors) == 0 \
                             and len(self.urls) == 0
        cond2 = 0 <= self.no < len(self.authors) \
            and 0 <= self.no < len(self.urls)
        if cond1:
            sh.com.rep_lazy(f)
        elif cond2:
            return (self.authors[self.no]
                   ,self.urls[self.no]
                   )
        else:
            min_val = min(len(self.authors),len(self.urls))
            sub = '0 <= {} < {}'.format(self.no,min_val)
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_error()
    
    def get_next(self):
        f = '[Yatube] logic.ChannelHistory.get_next'
        self.inc()
        cond1 = self.no == 0 and len(self.authors) == 0 \
                             and len(self.urls) == 0
        cond2 = 0 <= self.no < len(self.authors) \
            and 0 <= self.no < len(self.urls)
        if cond1:
            sh.com.rep_lazy(f)
        elif cond2:
            return (self.authors[self.no]
                   ,self.urls[self.no]
                   )
        else:
            min_val = min(len(self.authors),len(self.urls))
            sub = '0 <= {} < {}' % (self.no,min_val)
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_error()


objs = Objects()
com  = Commands()
Config()
mt.API_KEY = objs.get_default().get_api_key()
mt.objs.get_stat()


if __name__ == '__main__':
    url = 'https://www.youtube.com/embed/1jjSSXr5J7A?hl=ru_RU'
    print(URL(url).get_videoid())
