#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import io
#import youtube_dl
import yt_dlp as youtube_dl
from skl_shared.localize import _
import skl_shared.shared as sh
import skl_shared.image.controller as im
import meta as mt
import db

pattern1 = 'https://www.youtube.com/watch?v='
pattern2 = 'https://www.youtube.com/channel/'
pattern3 = 'https://www.youtube.com/'
AllOS = False


sample_subscribe = '''BostonDynamics    UU7vVhkEfw4nOGp8TyDk7RcQ
Brave Wilderness    UU6E2mP01ZLH_kbAyeazCNdg
Pravda GlazaRezhet  UUgCqhDRyMH1wZBI4OOKLQ8g
Дмитрий ПОТАПЕНКО   UU54SBo5_usXGEoybX1ZVETQ
Мохнатые Друзья UUqKbBJRz6SGrvUHNoZkpF2w
'''

sample_block = '''Россия 24'''


class SearchDB:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.token_prev = 0
        self.token_next = 0
        self.pattern = ''
    
    def reset(self,pattern):
        self.set_values()
        self.pattern = pattern
    
    def get_token(self):
        f = '[Yatube] logic.SearchDB.get_token'
        if mt.objs.get_videos().videos:
            self.token_next = mt.objs.videos.videos[-1].ptime
            self.token_prev = mt.objs.videos.videos[0].ptime
            date_next = sh.Time (tstamp = self.token_next
                                ,pattern = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            date_prev = sh.Time (tstamp = self.token_prev
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
        f = '[Yatube] logic.SearchDB.fetch_prev'
        ids = objs.get_db().get_search_prev (pattern = self.pattern
                                            ,ptime = self.token_prev
                                            ,limit = mt.MAX_VIDEOS
                                            )
        if not ids:
            sh.com.rep_empty(f)
            return
        for id_ in ids:
            video = mt.Video()
            video.id_ = id_
            mt.objs.videos.add(video)
    
    def fetch_next(self):
        f = '[Yatube] logic.SearchDB.fetch_next'
        ids = objs.get_db().get_search_next (pattern = self.pattern
                                            ,ptime = self.token_next
                                            ,limit = mt.MAX_VIDEOS
                                            )
        if not ids:
            sh.com.rep_empty(f)
            return
        for id_ in ids:
            video = mt.Video()
            video.id_ = id_
            mt.objs.videos.add(video)



class Image:
    
    def __init__(self):
        self.dir = sh.Home('yatube').add_share(_('Images'))
        self.Success = sh.Path(self.dir).create()
        self.path = ''
        self.video = None
    
    def get_online(self):
        f = '[Yatube] logic.Image.get_online'
        if not self.Success:
            sh.com.cancel(f)
            return
        Video().set_desc_thumb()
        if not self.video.thumb:
            sh.com.rep_empty(f)
            return
        bytes_ = sh.Get (url = self.video.thumb
                        ,coding = None
                        ,Verbose = False
                        ).run()
        iimage = im.Image()
        iimage.bytes_ = bytes_
        iimage.get_loader()
        self.video.image = iimage.get_image()
        #NOTE: comply with a default Youtube thumb format
        iimage.save(self.path, 'JPEG')
        return self.video.image
    
    def get_offline(self):
        f = '[Yatube] logic.Image.get_offline'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.path:
            sh.com.rep_empty(f)
            return
        if not os.path.exists(self.path):
            sh.com.rep_lazy(f)
            return
        self.video.image = im.Image().open(self.path)
        return self.video.image
    
    def load(self):
        f = '[Yatube] logic.Image.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.get_offline():
            self.get_online()
    
    def set_path(self):
        f = '[Yatube] logic.Image.set_path'
        if not self.Success:
            sh.com.cancel(f)
            return
        name = sh.FixBaseName(self.video.id_,True).run()
        if not name:
            sh.com.rep_empty(f)
            return
        name += '.jpg'
        self.path = os.path.join(self.dir,name)
    
    def set_cur(self):
        self.path = ''
        # This function always returns a non-empty value
        self.video = mt.objs.get_videos().get_current()
    
    def run(self):
        self.set_cur()
        self.set_path()
        self.load()



class CreateConfig(sh.CreateConfig):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def fill_bool(self):
        section = _('Booleans')
        self.add_section(section)
        section_abbr = self.sections[-1].abbr
        
        key = 'SlowPC'
        comment = _('[Autosave] Use special mpv options for slow PCs')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'DateActive'
        comment = _('[Autosave] Activate filtering by date')
        self.add_key(section, section_abbr, key, comment)
    
    def fill_int(self):
        section = _('Integers')
        self.add_section(section)
        section_abbr = self.sections[-1].abbr
        
        key = 'max_videos'
        comment = _('[Autosave] Number of videos per screen (5, 10, 15, 30, 50)')
        self.add_key(section, section_abbr, key, comment)
    
    def fill_str(self):
        section = _('Strings')
        self.add_section(section)
        section_abbr = self.sections[-1].abbr
        
        key = 'resolution'
        comment = _('[Autosave] Default video resolution')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'quality'
        comment = _('[Autosave] Default video quality')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'DateChoice'
        comment = _('[Autosave] Date filtering option')
        self.add_key(section, section_abbr, key, comment)



class DefaultKeys(sh.DefaultKeys):

    def __init__(self):
        super().__init__()
        self.load()
    
    def load(self):
        self._load_bool()
        self._load_int()
        self._load_str()
    
    def _load_bool(self):
        sh.lg.globs['bool'].update ({
            'DateActive' :False
           ,'SlowPC'     :True
                                  })
    
    def _load_int(self):
        sh.lg.globs['int'].update ({
            'max_videos' :50
                                  })
    
    def _load_str(self):
        sh.lg.globs['str'].update ({
            'DateChoice' :_('Newer than')
           ,'quality'    :_('Best qual.')
           ,'resolution' :_('Auto')
                                  })



class Commands:
    
    def extract_resolution(self, text):
        # '<=1080p' -> '1080'
        match = re.match('<=(\d+)p',text)
        if not match:
            return ''
        return match.group(1)



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
                                ,pattern = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            date_prev = sh.Time (tstamp = self.token_prev
                                ,pattern = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            mes = _('Previous page token: {}').format(date_prev)
            sh.objs.get_mes(f, mes, True).show_debug()
            mes = _('Next page token: {}').format(date_next)
            sh.objs.get_mes(f, mes, True).show_debug()
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
        ids = objs.get_db().get_feed_prev (fdtime = self.token_prev
                                          ,limit = mt.MAX_VIDEOS
                                          )
        if not ids:
            sh.com.rep_empty(f)
            return
        for id_ in ids:
            video = mt.Video()
            video.id_ = id_
            mt.objs.videos.add(video)
    
    def fetch_next(self):
        f = '[Yatube] logic.Feed.fetch_next'
        ids = objs.get_db().get_feed_next (fdtime = self.token_next
                                          ,limit = mt.MAX_VIDEOS
                                          )
        if not ids:
            sh.com.rep_empty(f)
            return
        for id_ in ids:
            video = mt.Video()
            video.id_ = id_
            mt.objs.videos.add(video)



class Favorites:
    
    def __init__(self):
        self.token_prev = 0
        self.token_next = 0
    
    def get_token(self):
        f = '[Yatube] logic.Favorites.get_token'
        if mt.objs.get_videos().videos:
            self.token_next = mt.objs.videos.videos[-1].ftime
            self.token_prev = mt.objs.videos.videos[0].ftime
            date_next = sh.Time (tstamp = self.token_next
                                ,pattern = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            date_prev = sh.Time (tstamp = self.token_prev
                                ,pattern = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            mes = _('Previous page token: {}').format(date_prev)
            sh.objs.get_mes(f, mes, True).show_debug()
            mes = _('Next page token: {}').format(date_next)
            sh.objs.get_mes(f, mes, True).show_debug()
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
        if not ids:
            sh.com.rep_empty(f)
            return
        for id_ in ids:
            video = mt.Video()
            video.id_ = id_
            mt.objs.videos.add(video)
    
    def fetch_next(self):
        f = '[Yatube] logic.Favorites.fetch_next'
        ids = objs.get_db().get_fav_next (ftime = self.token_next
                                         ,limit = mt.MAX_VIDEOS
                                         )
        if not ids:
            sh.com.rep_empty(f)
            return
        for vid in ids:
            video = mt.Video()
            video.id_ = vid
            mt.objs.videos.add(video)



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
                                ,pattern = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            date_prev = sh.Time (tstamp = self.token_prev
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
        f = '[Yatube] logic.Watchlist.fetch_prev'
        ids = objs.get_db().get_watch_prev (ltime = self.token_prev
                                           ,limit = mt.MAX_VIDEOS
                                           )
        if not ids:
            sh.com.rep_empty(f)
            return
        for id_ in ids:
            video = mt.Video()
            video.id_ = id_
            mt.objs.videos.add(video)
    
    def fetch_next(self):
        f = '[Yatube] logic.Watchlist.fetch_next'
        ids = objs.get_db().get_watch_next (ltime = self.token_next
                                           ,limit = mt.MAX_VIDEOS
                                           )
        if not ids:
            sh.com.rep_empty(f)
            return
        for id_ in ids:
            video = mt.Video()
            video.id_ = id_
            mt.objs.videos.add(video)



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
                                ,pattern = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            date_prev = sh.Time (tstamp = self.token_prev
                                ,pattern = '%Y-%m-%d %H:%M:%S'
                                ).get_date()
            mes = _('Previous page token: {}').format(date_prev)
            sh.objs.get_mes(f, mes, True).show_debug()
            mes = _('Next page token: {}').format(date_next)
            sh.objs.get_mes(f, mes, True).show_debug()
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
        if not ids:
            sh.com.rep_empty(f)
            return
        for vid in ids:
            video = mt.Video()
            video.id_ = vid
            mt.objs.videos.add(video)
    
    def fetch_next(self):
        f = '[Yatube] logic.History.fetch_next'
        ids = objs.get_db().get_history_next (dtime = self.token_next
                                             ,limit = mt.MAX_VIDEOS
                                             )
        if not ids:
            sh.com.rep_empty(f)
            return
        for vid in ids:
            video = mt.Video()
            video.id_ = vid
            mt.objs.videos.add(video)



class Channel:
    
    def __init__(self, myid=''):
        self.set_values()
        if myid:
            self.reset(myid)
    
    def run(self):
        f = '[Yatube] logic.Channel.run'
        if not self.Success:
            sh.com.cancel(f)
            return self.ids
        mt.objs.get_playlist().reset(self.playid)
        mt.objs.playlist.run()
        for video in mt.objs.videos.videos:
            self.ids.append(video.id_)
        return self.ids
    
    def reset(self, myid):
        self.autodetect(myid)
    
    def autodetect(self, myid):
        f = '[Yatube] logic.Channel.autodetect'
        if not myid:
            self.Success = False
            sh.com.rep_empty(f)
            return
        #TODO: implement autodetection
        self.playid = myid
    
    def set_values(self):
        self.Success = True
        self.ids = []
        self.playid = ''



class Time:
    
    def __init__(self):
        self.days = []
        self.months = []
        self.years = []
        self.year = ''
        self.day = ''
        self.month = ''
        self.itime = sh.Time(pattern='%d')
    
    def get_days(self):
        self.days = [str(day+1) for day in range(31)]
        # 'sh.Time' outputs a day number preceded by 0
        self.days = tuple ('0' + day if len(day) == 1 else day \
                           for day in self.days
                          )
        return self.days
        
    def get_months(self):
        self.months = (_('Jan'), _('Feb'), _('Mar'), _('Apr'), _('May')
                      ,_('Jun'), _('Jul'), _('Aug'), _('Sep'), _('Oct')
                      ,_('Nov'), _('Dec')
                      )
        return self.months
        
    def get_years(self):
        f = '[Yatube] logic.Time.get_years'
        # Year of Youtube birth
        first_year = 2005
        last_year = self.itime.get_year()
        last_year = sh.Input(f, last_year).get_integer()
        if not last_year > first_year:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes,True).show_warning()
            last_year = 2018
        self.years = tuple (str(year) for year in range (first_year
                                                        ,last_year + 1
                                                        )
                           )
        return self.years
        
    def set_date(self, DaysDelta=7):
        self.itime.add_days(days_delta=-DaysDelta)
        self.year = str(self.itime.get_year())
        self.day = self.itime.get_date()
        self.itime.get_month_abbr()
        self.month = self.itime.localize_month_abbr()


class Constants:
    
    def __init__(self):
        self.countries = []
        self.trending = []
        
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
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' Owing to parser peculiarities, if the link is a non-conventional
            link to a Youtube video, it should be first converted to
            a conventional link (see 'pattern1'). Youtube playlists, search
            results and links from external sites may be preserved in
            the original form.
            #TODO: Fix the parser to get rid of this.
        '''
        id_ = URL(self.url).get_videoid()
        if len(id_) == 11 and not 'https:' in id_ and not 'http:' in id_ \
        and not 'www.' in id_:
            self.url = URL(id_).get_video_full()
        
    def reset(self, url=''):
        f = '[Yatube] logic.Extractor.reset'
        self.set_values()
        if not url:
            self.Success = False
            sh.com.rep_empty(f)
            return
        self.url = url
        
    def set_values(self):
        self.Success = True
        self.url = ''
        self.htm = ''
        self.urls = []
    
    def set_page(self):
        f = '[Yatube] logic.Extractor.set_page'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.htm or self.urls:
            sh.com.rep_lazy(f)
            return
        response = sh.Get(url=self.url).run()
        if not response:
            sh.com.rep_empty(f)
            return
        self.htm = response
    
    def set_urls(self):
        f = '[Yatube] logic.Extractor.set_urls'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.urls:
            sh.com.rep_lazy(f)
            return
        ilinks = sh.Links (text = self.htm
                          ,root = 'href="'
                          )
        ilinks.get_poses()
        old = list(ilinks.links)
        ilinks = sh.Links (text = self.htm
                          ,root = 'src="'
                          )
        ilinks.get_poses()
        ''' #NOTE: if links from both root elements are present, their order
            may be desynchronized.
        '''
        ilinks.links += old
        if 'youtube' in self.url or 'youtu.be' in self.url:
            ilinks.links = ['https://www.youtube.com' + link \
                            for link in ilinks.links \
                            if link.startswith('/watch?v=')
                           ]
        else:
            ilinks.redirect()
            ''' We should do our best here to ensure that the URL will refer to
                a Youtube video. There could be links to 'youtube.com', e.g.,
                from 'account.google.com' that will not refer to videos. We
                need a slash here because there can be links like
                .../uploads/youtu.be-bv2OGph5Kec-330x225.jpg.
            '''
            ilinks.links = [link for link in ilinks.links \
                            if 'youtu.be/' in link \
                            or 'youtube.com/watch?v=' in link \
                            or 'youtube.com/embed/' in link
                           ]
            ilinks.get_valid()
        old = list(ilinks.links)
        ''' Previous algorithms consider a link as valid if it has 'youtu(be)'
            in its tag, and we have just ID there, so this should be put after
            those algorithms.
        '''
        ilinks = sh.Links (text = self.htm
                          ,root = 'data-pe-videoid="'
                          )
        ilinks.get_poses()
        ilinks.links += old
        ilinks.links = [URL(link).get_videoid() for link in ilinks.links]
        ilinks.delete_duplicates()
        self.urls = ilinks.links
        mes = _('Fetched {} links').format(len(self.urls))
        sh.objs.get_mes(f, mes, True).show_info()
    
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
        self.Success = self.idefault.Success
        self.load()
    
    def set_values(self):
        self.block = ''
        self.blockw = ''
        self.subsc = ''
        self.blauth = []
        self.blwords = []
        self.subauth = []
        self.subids = []
        self.freq = []
    
    def match_blocked_word(self, word):
        f = '[Yatube] logic.Lists.match_blocked_word'
        if not self.Success:
            sh.com.cancel(f)
            return
        word = word.lower()
        for item in self.blwords:
            # Contents of 'self.blwords' should already be lower-cased
            if item in word:
                return True
    
    def load(self):
        f = '[Yatube] logic.Lists.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        # Blocked authors
        text = sh.ReadTextFile(self.idefault.fblock).get()
        text = sh.Text(text).delete_comments()
        # We should allow empty files
        self.block = text
        self.blauth = text.splitlines()
        # Blocked words
        text = sh.ReadTextFile(self.idefault.fblockw).get()
        text = sh.Text(text).delete_comments()
        # We should allow empty files
        self.blockw = text
        self.blwords = text.splitlines()
        self.blwords = [item.lower() for item in self.blwords]
        # Suppress errors on empty text
        if os.path.exists(self.idefault.fsubsc):
            dic = sh.Dic (file = self.idefault.fsubsc
                         ,Sortable = False
                         )
            self.Success = dic.Success
            if self.Success:
                self.subsc = dic.text
                self.subauth = dic.orig
                self.subids = dic.transl
        if self.subauth:
            self.subauth, self.subids = (list(x) for x \
            in zip (*sorted (zip (self.subauth, self.subids)
                            ,key = lambda x:x[0].lower()
                            )
                   )
                                        )
        text = sh.ReadTextFile(self.idefault.ffreq).get()
        text = sh.Text(text).delete_comments()
        self.freq = text.splitlines()



class Objects:
    
    def __init__(self):
        ''' Do not put here instances that depend on meta objects and
            that need to be constantly reset owing to possible 'Success'
            fails (e.g., 'logic.Video').
        '''
        self.online = self.lists = self.const = self.default = self.db \
                    = self.channels = self.channel = self.extractor \
                    = self.history = self.watchlist = self.favorites \
                    = self.feed = self.config = self.image = self.search_db \
                    = None
    
    def get_search_db(self):
        if self.search_db is None:
            self.search_db = SearchDB()
        return self.search_db
    
    def get_image(self):
        if self.image is None:
            self.image = Image()
        return self.image
    
    def get_config(self):
        if self.config is None:
            self.config = sh.Config(self.get_default().get_config())
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
            path = self.get_default('yatube').fdb
            if self.default.Success:
                self.db = db.DB(path)
            else:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f, mes, True).show_warning()
                self.db = db.DB()
        return self.db
    
    def get_default(self, product='yatube'):
        if not self.default:
            self.default = DefaultConfig(product)
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
    
    def set_desc_thumb(self):
        # Set fields that are space-consuming and should not be stored in DB
        f = '[Yatube] logic.Video.set_desc_thumb'
        video = mt.objs.get_videos().get_current()
        if video.desc:
            return
        data = mt.VideoInfo().get_channel_id()
        if not data:
            sh.com.rep_empty(f)
            return
        # Other fields should already be processed and stored in DB
        video.desc = data.desc
        video.thumb = data.thumb
    
    def get_length(self):
        f = '[Yatube] logic.Video.get_length'
        video = mt.objs.get_videos().get_current()
        if video.len_:
            return video.len_
        if mt.VideoInfo().get_length():
            objs.get_db().update_len(video.id_, video.len_)
        else:
            sh.com.rep_empty(f)
        return video.len_
    
    def set_stat(self):
        f = '[Yatube] logic.Video.set_stat'
        video = mt.objs.get_videos().get_current()
        ''' Likes/dislikes/number of comments can be 0, so we shoud rely
            on 'video.views' only.
        '''
        # Return True if metadata were fetched successfully
        if video.views:
            return True
        return mt.VideoInfo().set_stat()
    
    def get_playid(self):
        f = '[Yatube] logic.Video.get_playid'
        video = mt.objs.get_videos().get_current()
        if video.playid:
            return video.playid
        channel_id = self.get_channel_id()
        if not channel_id:
            sh.com.rep_empty(f)
            return video.playid
        mt.objs.get_playid().reset(channel_id)
        playid = mt.objs.playid.get_by_channel_id()
        if not playid:
            sh.com.rep_empty(f)
            return video.playid
        video.playid = playid
        objs.get_db().update_playid(video.id_,video.playid)
        return video.playid
    
    def get_channel_id(self):
        f = '[Yatube] logic.Video.get_channel_id'
        video = mt.objs.get_videos().get_current()
        if video.chid:
            return video.chid
        data = mt.VideoInfo().get_channel_id()
        if not data:
            sh.com.rep_empty(f)
            return video.chid
        video.chid = data.chid
        objs.get_db().update_ch_id(video.id_, video.chid)
        return video.chid
    
    def check(self):
        f = '[Yatube] logic.Video.check'
        if not mt.objs.get_videos().get_current():
            self.Success = False
            sh.com.rep_empty(f)
            return
        videoid = mt.objs.videos.get_current().id_
        if len(videoid) == 11 and not 'http:' in videoid \
        and not 'https:' in videoid and not 'www.' in videoid:
            return True
        self.Success = False
        mes = _('Wrong input data: "{}"!').format(videoid)
        sh.objs.get_mes(f, mes).show_warning()
        
    def get_url(self):
        f = '[Yatube] logic.Video.get_url'
        if not self.Success:
            sh.com.cancel(f)
            return
        video = mt.objs.get_videos().get_current()
        if not video.url:
            video.url = URL(video.id_).get_video_full()
        return video.url
    
    def set_values(self):
        self.Success = True

    def delete(self):
        f = '[Yatube] logic.Video.delete'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.get_path():
            sh.com.rep_empty(f)
            return
        video = mt.objs.get_videos().get_current()
        # Do not warn about missing files
        if not os.path.exists(video.path):
            return
        Success = sh.File(video.path).delete()
        idir = sh.Directory(video.dir_)
        if not idir.get_files():
            idir.delete()
        return Success
    
    def get_page(self):
        f = '[Yatube] logic.Video.get_page'
        if not self.Success:
            sh.com.cancel(f)
            return
        video = mt.objs.get_videos().get_current()
        if video.page:
            return video.page
        if not video.url:
            sh.com.rep_empty(f)
            return video.page
        video.page = sh.Get(video.url).run()
        return video.page
    
    def assign_online(self):
        f = '[Yatube] logic.Video.assign_online'
        if not self.Success:
            sh.com.cancel(f)
            return
        video = mt.objs.get_videos().get_current()
        if not video.author:
            ''' Do not use 'self.channel_id' or 'self.playid' here since
                we do not want unnecessary DB updates.
            '''
            mt.VideoInfo().get_channel_id()
        video.search = video.author.lower() + ' ' + video.title.lower()
        video.fdtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
                          
    def dump(self):
        f = '[Yatube] logic.Video.dump'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' Do no write default data.
            Do not forget to commit where necessary.
        '''
        video = mt.objs.get_videos().get_current()
        data = (video.id_, video.playid, video.chid, video.author, video.title
               ,video.search, video.len_, video.pause, video.ptime, video.dtime
               ,video.ftime, video.ltime, video.fdtime
               )
        if not video.author or not video.title:
            sh.com.rep_empty(f)
            return
        objs.get_db().add_video(data)
        
    def assign_offline(self, data):
        f = '[Yatube] logic.Video.assign_offline'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not data:
            sh.com.rep_empty(f)
            return
        data_len = 13
        if len(data) != data_len:
            sub = f'{len(data)} == {data_len}'
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f, mes).show_error()
            return
        video = mt.objs.get_videos().get_current()
        video.id_ = data[0]
        video.playid = data[1]
        video.chid = data[2]
        video.author = data[3]
        video.title = data[4]
        video.search = data[5]
        video.len_ = data[6]
        video.pause = data[7]
        #TODO: implement
        #video.bytes_ = None
        video.ptime = data[8]
        video.dtime = data[9]
        video.ftime = data[10]
        video.ltime = data[11]
        video.fdtime = data[12]
    
    def set_new(self):
        ''' Separating this code allows to skip a slow 'get_video' procedure
            when we are processing videos not known by the DB.
        '''
        f = '[Yatube] logic.Video.set_new'
        if not self.Success:
            sh.com.cancel(f)
            return
        id_ = mt.objs.get_videos().get_current().id_
        mes = _('Get new video info: {}').format(id_)
        sh.objs.get_mes(f, mes, True).show_info()
        self.assign_online()
        self.dump()
    
    def get(self):
        f = '[Yatube] logic.Video.get'
        if not self.Success:
            sh.com.cancel(f)
            return
        video = mt.objs.get_videos().get_current()
        video.Saved = objs.get_db().get_video(video.id_)
        ''' We use 'self.unsupported' for both online and offline value
            assigning. Do not put it in the end - we want DB to be clean of
            unsupported symbols, because we may want to use separate methods
            instead of the whole 'self.get'
            (for example, see 'yatube.Commands.fill_known').
        '''
        if video.Saved:
            self.assign_offline(video.Saved)
        else:
            self.set_new()
    
    def show_summary(self):
        f = '[Yatube] logic.Video.show_summary'
        if not self.Success:
            sh.com.cancel(f)
            return
        video = mt.objs.get_videos().get_current()
        logic = Video()
        logic.get_length()
        logic.set_stat()
        logic.set_desc_thumb()
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
        
    def get_path(self):
        f = '[Yatube] logic.Video.get_path'
        if not self.Success:
            sh.com.cancel(f)
            return
        video = mt.objs.get_videos().get_current()
        if video.path:
            return video.path
        author = sh.FixBaseName (basename = video.author
                                ,AllOS = AllOS
                                ,max_len = 100
                                ).run()
        title = sh.FixBaseName (basename = video.title
                                ,AllOS = AllOS
                                ,max_len = 100
                                ).run()
        ''' For some reason, 'youtube_dl' does not screen correctly characters
            such as '%' and throws an error when downloading videos containing
            such characters in their path. We delete '%' instead of replacing
            with '%%' since 'mpv' also seems to have such issues.
        '''
        title = title.replace('%', '')
        video.dir_ = objs.get_default().ihome.add_config('Youtube', author)
        video.path = objs.default.ihome.add_config('Youtube', author, title)
        video.pathsh = sh.Text (text = sh.Path(video.path).get_basename()
                               ,Auto = False
                               ).shorten (max_len = 20
                                         ,FromEnd = False
                                         ,ShowGap = True
                                         )
        ''' #NOTE: youtube_dl may try to use ffmpeg to merge audio and video,
            but ffmpeg reacts to file extentions rather than to magic numbers
            and that causes files with a wrong extension to be unplayable.
        '''
        video.path += '.mp4'
        return video.path
    
    def make_dir(self):
        f = '[Yatube] logic.Video.make_dir'
        if not self.Success:
            sh.com.cancel(f)
            return
        video = mt.objs.get_videos().get_current()
        if not video.dir_:
            self.Success = False
            sh.com.rep_empty(f)
            return
        self.Success = sh.Path(video.dir_).create()
    
    def download(self, callback=None, format_='mp4'):
        f = '[Yatube] logic.Video.download'
        self.make_dir()
        if not self.Success:
            sh.com.cancel(f)
            return
        video = mt.objs.get_videos().get_current()
        if not video.path:
            sh.com.rep_empty(f)
            return
        mes = _('Download "{}"').format(video.path)
        sh.objs.get_mes(f, mes, True).show_info()
        #TODO: select quality
        ''' There was a video for which 'webm' downloaded successfully, but
            'mp4' failed.
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
            mt.com.show_error(f, e)
    
    def generate_url(self, videoid, quality='best'):
        f = '[Yatube] logic.Video.generate_url'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not videoid:
            sh.com.rep_empty(f)
            return
        ''' If we do not set 'format', then 'youtube_dl' will not provide
            info_dict['url']. Instead, it will generate 'url' for each
            available format.
        '''
        options = {'format'            :quality
                  ,'ignoreerrors'      :True
                  ,'nocheckcertificate':True
                  ,'socket_timeout'    :7
                  ,'username'          :mt.objs.get_credentials().login
                  ,'password'          :mt.objs.credentials.password
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
                    sh.objs.get_mes(f, mes).show_warning()
        except Exception as e:
            mt.com.show_error(f,e)
    
    def stream(self, quality='best'):
        ''' Stream a video with preset parameters. Examples of 'quality'
            settings: 'best', 'worst', 'worst[height<=1080]',
            'best[height<=480]'.
        '''
        f = '[Yatube] logic.Video.stream'
        if not self.Success:
            sh.com.cancel(f)
            return
        video = mt.objs.get_videos().get_current()
        gen_url = self.generate_url(video.id_,quality)
        if gen_url:
            return gen_url
        gen_url = self.generate_url(video.id_)
        if not gen_url:
            mes = _('This video is not available.')
            sh.objs.get_mes(f, mes).show_warning()
            return
        mes = _('Selected quality is not available, using default quality.')
        sh.objs.get_mes(f, mes).show_warning()
        return gen_url



class URL:
    
    def __init__(self, url):
        f = '[Yatube] logic.URL.__init__'
        self.url = url
        self.url = sh.Input(f, self.url).get_not_none()
        self.url = str(self.url)
        self.url = self.url.strip()
    
    def get_videoid(self):
        self.get_video_full()
        return self.url.replace(pattern1, '')
    
    def get_video_full(self):
        f = '[Yatube] logic.URL.get_video_full'
        if not self.url:
            sh.com.rep_empty(f)
            return self.url
        self.trash()
        self.trash_v()
        self.url = self.url.replace('/embed/', '/watch?v=')
        self.set_prefixes()
        if not pattern1 in self.url:
            self.url = pattern1 + self.url
        return self.url
    
    def get_channel_full(self):
        f = '[Yatube] logic.URL.get_channel_full'
        if not self.url:
            sh.com.rep_empty(f)
            return ''
        self.trash()
        self.set_prefixes()
        self.set_prefixes_ch()
        self.set_suffixes_ch()
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
        self.url = re.sub('#t=\d+', '', self.url)
        if 'watch?v' in self.url:
            search = sh.Search (text = self.url
                               ,pattern = '?'
                               )
            search.get_next()
            i = search.get_next()
            # 'search.i' is updated only on a successful search
            if i and i > 0:
                self.url = self.url[i::]
        else:
            self.url = re.sub('\?.*', '', self.url)
        self.url = re.sub('\&.*', '', self.url)
        return self.url
    
    def set_prefixes(self):
        if self.url.startswith('youtube.com'):
            self.url = 'https://www.' + self.url
        elif self.url.startswith('youtu.be'):
            self.url = 'https://' + self.url
        self.url = self.url.replace('http://', 'https://')
        self.url = self.url.replace('m.youtube.com', 'youtube.com')
        self.url = self.url.replace ('https://youtube.com'
                                    ,'https://www.youtube.com'
                                    )
        self.url = self.url.replace('https://youtu.be/', pattern1)
            
    def set_prefixes_ch(self):
        if not pattern3 in self.url:
            self.url = pattern3 + self.url
        if '/user/' in self.url or '/channel/' in self.url \
        or '/c/' in self.url:
            return
        self.url += '/user'
        
    def set_suffixes_ch(self):
        if not '/videos' in self.url:
            self.url += '/videos'



class DefaultConfig:
    
    def __init__(self, product='yatube'):
        self.set_values()
        self.ihome = sh.Home(product)
        self.Success = self.ihome.create_conf()
    
    def set_values(self):
        self.fsubsc = ''
        self.fblock = ''
        self.fblockw = ''
        self.fdb = ''
        self.fconf = ''
        self.api_key = ''
        self.ffreq = ''
    
    def set_frequent(self):
        f = '[Yatube] logic.DefaultConfig.set_frequent'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.ffreq = self.ihome.add_config('frequent channels.txt')
        if not self.ffreq:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if os.path.exists(self.ffreq):
            self.Success = sh.File(self.ffreq).Success
        else:
            iwrite = sh.WriteTextFile (file = self.ffreq
                                      ,Rewrite = True
                                      )
            iwrite.write('# ' + _('Put here titles of frequent channels'))
            self.Success = iwrite.Success
    
    def get_api_key(self):
        f = '[MClient] logic.DefaultConfig.get_api_key'
        if not self.Success:
            sh.com.cancel(f)
            return self.api_key
        if not self.api_key:
            file = self.ihome.add_config('api-key.txt')
            self.api_key = sh.ReadTextFile(file).get()
            self.api_key = self.api_key.strip()
        return self.api_key
    
    def get_config(self):
        f = '[MClient] logic.DefaultConfig.get_config'
        if not self.Success:
            sh.com.cancel(f)
            return self.fconf
        if not self.fconf:
            self.fconf = self.ihome.add_config('yatube.cfg')
        return self.fconf
    
    def set_db(self):
        f = '[Yatube] logic.DefaultConfig.set_db'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.fdb = self.ihome.add_config('yatube.db')
        if not self.fdb:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if os.path.exists(self.fdb):
            self.Success = sh.File(self.fdb).Success
    
    def set_block_words(self):
        f = '[Yatube] logic.DefaultConfig.set_block_words'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.fblockw = self.ihome.add_config('block words.txt')
        if not self.fblockw:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if os.path.exists(self.fblockw):
            self.Success = sh.File(self.fblockw).Success
        else:
            iwrite = sh.WriteTextFile (file = self.fblockw
                                      ,Rewrite = True
                                      )
            iwrite.write('# ' + _('Put here words to block in titles (case is ignored)'))
            self.Success = iwrite.Success
    
    def set_block_channels(self):
        f = '[Yatube] logic.DefaultConfig.set_block_channels'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.fblock = self.ihome.add_config('block channels.txt')
        if not self.fblock:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if os.path.exists(self.fblock):
            self.Success = sh.File(self.fblock).Success
        else:
            iwrite = sh.WriteTextFile (file = self.fblock
                                      ,Rewrite = True
                                      )
            iwrite.write(sample_block)
            self.Success = iwrite.Success
    
    def subscribe(self):
        f = '[Yatube] logic.DefaultConfig.subscribe'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.fsubsc = self.ihome.add_config('subscribe.txt')
        if not self.fsubsc:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if os.path.exists(self.fsubsc):
            self.Success = sh.File(self.fsubsc).Success
        else:
            iwrite = sh.WriteTextFile (file = self.fsubsc
                                      ,Rewrite = True
                                      )
            iwrite.write(sample_subscribe)
            self.Success = iwrite.Success
    
    def run(self):
        f = '[Yatube] logic.DefaultConfig.run'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.get_config()
        self.subscribe()
        self.set_block_channels()
        self.set_block_words()
        self.set_frequent()
        self.set_db()



class ChannelHistory:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.no = 0
        self.authors = []
        self.urls = []
    
    def reset(self):
        self.set_values()
    
    def add(self,author,urls):
        f = '[Yatube] logic.ChannelHistory.add'
        if not author or not urls:
            sh.com.rep_empty(f)
            return
        if not urls in self.urls:
            self.authors.append(author)
            self.urls.append(urls)
            self.no = len(self.urls) - 1
    
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
        if self.no == 0 and len(self.authors) == 0 and len(self.urls) == 0:
            sh.com.rep_lazy(f)
            return
        if 0 <= self.no < len(self.authors) and 0 <= self.no < len(self.urls):
            return(self.authors[self.no], self.urls[self.no])
        min_val = min(len(self.authors), len(self.urls))
        sub = '0 <= {} < {}'.format(self.no, min_val)
        mes = _('The condition "{}" is not observed!').format(sub)
        sh.objs.get_mes(f, mes).show_error()
    
    def get_next(self):
        f = '[Yatube] logic.ChannelHistory.get_next'
        self.inc()
        if self.no == 0 and len(self.authors) == 0 and len(self.urls) == 0:
            sh.com.rep_lazy(f)
            return
        if 0 <= self.no < len(self.authors) and 0 <= self.no < len(self.urls):
            return(self.authors[self.no], self.urls[self.no])
        min_val = min(len(self.authors), len(self.urls))
        sub = f'0 <= {self.no} < {min_val}'
        mes = _('The condition "{}" is not observed!').format(sub)
        sh.objs.get_mes(f, mes).show_error()


objs = Objects()
com = Commands()
DefaultKeys()
objs.get_config()
mt.API_KEY = objs.get_default().get_api_key()
mt.objs.get_stat()


if __name__ == '__main__':
    url = 'https://www.youtube.com/embed/1jjSSXr5J7A?hl=ru_RU'
    print(URL(url).get_videoid())
