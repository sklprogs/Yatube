#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import io
# pip3 install google-api-python-client
from googleapiclient.discovery import build as apiclient
import pafy
import shared as sh
import db

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


sample_subscribe = '''BostonDynamics	https://www.youtube.com/user/BostonDynamics/videos
Brave Wilderness	https://www.youtube.com/user/BreakingTrail/videos
Pravda GlazaRezhet	https://www.youtube.com/channel/UCgCqhDRyMH1wZBI4OOKLQ8g/videos
Дмитрий ПОТАПЕНКО	https://www.youtube.com/channel/UC54SBo5_usXGEoybX1ZVETQ/videos
Мохнатые Друзья	https://www.youtube.com/channel/UCqKbBJRz6SGrvUHNoZkpF2w/videos
'''

sample_block = '''Россия 24'''



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
        f = 'logic.Time.years'
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



class Channel:
       
    def __init__(self,url):
        self.reset(url=url)
        
    def reset(self,url):
        f = 'logic.Channel.reset'
        self.values()
        if url:
            self._url = url
            if ('youtube' in self._url or 'youtu.be' in self._url) \
            and not '?list=' in self._url \
            and not 'results?search_query=' in self._url \
            and not '?gl=' in self._url:
                self._url = URL(url=self._url).channel_full()
            elif len(self._url) == 11 and not 'https:' in self._url \
            and not 'http:' in self._url and not 'www.' in self._url:
                self._url = URL(url=self._url).video_full()
            elif not self._url.startswith('http'):
                self.Success = False
                sh.objs.mes (f,_('WARNING')
                            ,_('Wrong input data: "%s"') % self._url
                            )
        else:
            self.Success = False
            sh.com.empty(f)
        
    def values(self):
        self.Success = True
        self._url    = ''
        self._html   = ''
        self._links  = []
    
    def page(self):
        f = 'logic.Channel.page'
        if self.Success:
            response = sh.Get(url=self._url).run()
            if response:
                self._html = response
            return self._html
        else:
            sh.com.cancel(f)
    
    def links(self):
        f = 'logic.Channel.links'
        if self.Success:
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
                ''' We should do our best here to ensure that the URL
                    will refer to a Youtube video. There could be links
                    to 'youtube.com', e.g., from 'account.google.com'
                    that will not refer to videos. We need a slash here
                    because there can be links like
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
            self._links = ilinks._links
            sh.log.append (f,_('INFO')
                          ,_('Fetched %d links') % len(self._links)
                          )
            return self._links
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.page()
        self.links()
        return self._links



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
        self._subsc_urls  = []
    
    def match_blocked_word(self,word):
        f = 'logic.Lists.match_blocked_word'
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
        f = 'logic.Lists.load'
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
                    self._subsc_urls = dic.transl
            if self._subsc_auth:
                self._subsc_auth, self._subsc_urls = (list(x) for x \
                in zip (*sorted (zip (self._subsc_auth, self._subsc_urls)
                                ,key = lambda x:x[0].lower()
                                )
                       )
                                                     )
        else:
            sh.com.cancel(f)



class Objects:
    
    def __init__(self):
        self._online = self._lists = self._const = self._default \
                     = self._db = self._channels = None
        
    def db(self):
        f = 'logic.Objects.db'
        if not self._db:
            path = self.default(product='Yatube')._fdb
            if self._default.Success:
                self._db = db.DB(path=path)
            else:
                sh.log.append (f,_('WARNING')
                              ,_('Wrong input data!')
                              )
                self._db = db.DB()
        return self._db
    
    def default(self,product='Yatube'):
        if not self._default:
            self._default = DefaultConfig(product=product.lower())
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
    
    def __init__(self,video_id,callback=None):
        f = 'logic.Video.__init__'
        self.values()
        if video_id:
            if len(video_id) == 11 and not 'http:' in video_id \
            and not 'https:' in video_id and not 'www.' in video_id:
                self._video_id = video_id
                self._url      = URL(url=self._video_id).video_full()
                self._callback = callback
            else:
                self.Success = False
                sh.objs.mes (f,_('WARNING')
                            ,_('Wrong input data: "%s"') \
                            % str(video_id)
                            )
        else:
            self.Success = False
            sh.com.empty(f)
        
    def values(self):
        self.Success = True
        self.Block   = self.Ignore = False
        self._video  = self._bytes = self.Saved = None
        self._author = self._title = self._date = self._cat \
                     = self._desc = self._dur = self._path \
                     = self._search = self._channel_url = self._page \
                     = self._dir = self._pathsh = ''
        self._len    = self._views = self._likes = self._dislikes \
                     = self._timestamp = self._dtime = 0
        self._rating = 0.0
        
    def delete(self):
        f = 'logic.Video.delete'
        if self.Success:
            if self.path():
                # Do not warn about missing files
                if os.path.exists(self._path):
                    Success = sh.File(file=self._path).delete()
                    idir = sh.Directory(path=self._dir)
                    if not idir.files():
                        idir.delete()
                    return Success
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def page(self):
        f = 'logic.Video.page'
        if self.Success:
            if not self._page:
                if self._url:
                    self._page = sh.Get(url=self._url).run()
                else:
                    sh.com.empty(f)
            return self._page
        else:
            sh.com.cancel(f)
    
    def channel_url(self):
        f = 'logic.Video.channel_url'
        if self.Success:
            if not self._channel_url:
                if self.page():
                    pos1 = sh.Search (text   = self._page
                                     ,search = pattern2
                                     ).next()
                    if str(pos1).isdigit():
                        pos1 += len(pattern2)
                        if pos1 < len(self._page):
                            search = sh.Search (text   = self._page
                                               ,search = '"'
                                               )
                            search.i = pos1
                            pos2 = search.next()
                            if str(pos2).isdigit():
                                url = self._page[pos1:pos2]
                                if url:
                                    self._channel_url = pattern3a \
                                                        + url \
                                                        + pattern3b
                                    sh.log.append (f,_('DEBUG')
                                                  ,self._channel_url
                                                  )
                                    return self._channel_url
                                else:
                                    sh.com.empty(f)
                            else:
                                sh.log.append (f,_('WARNING')
                                              ,_('Wrong input data!')
                                              )
                        else:
                            sh.log.append (f,_('WARNING')
                                          ,_('Wrong input data!')
                                          )
                    else:
                        sh.log.append (f,_('WARNING')
                                      ,_('Wrong input data!')
                                      )
                else:
                    sh.com.empty(f)
            return self._channel_url
        else:
            sh.com.cancel(f)
    
    def assign_online(self):
        f = 'logic.Video.assign_online'
        if self.Success:
            if self._video:
                try:
                    self._author    = self._video.author
                    self._title     = self._video.title
                    self._date      = self._video.published
                    self._cat       = self._video.category
                    self._desc      = self._video.description
                    self._dur       = self._video.duration
                    self._len       = self._video.length
                    self._views     = self._video.viewcount
                    self._likes     = self._video.likes
                    self._dislikes  = self._video.dislikes
                    self._rating    = self._video.rating
                # Youtube says...
                except Exception as e:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Third party module has failed!\n\nDetails: %s') \
                                % str(e)
                                )
                self._search    = self._author.lower() + ' ' \
                                  + self._title.lower()
                itime           = sh.Time(pattern='%Y-%m-%d %H:%M:%S')
                itime._date     = self._date
                self._timestamp = itime.timestamp()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
                          
    def dump(self):
        f = 'logic.Video.dump'
        if self.Success:
            ''' Do no write default data.
                Do not forget to commit where necessary.
            '''
            if self._video:
                data = (self._video_id,self._author,self._title
                       ,self._date,self._cat,self._desc,self._dur
                       ,self._len,self._views,self._likes,self._dislikes
                       ,self._rating,self._bytes,self.Block,self.Ignore
                       ,self._search,self._timestamp,self._dtime
                       )
                objs.db().add_video(data)
            else:
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do.')
                              )
        else:
            sh.com.cancel(f)
        
    def assign_offline(self,data):
        f = 'logic.Video.assign_offline'
        if self.Success:
            if data:
                data_len = 15
                if len(data) >= data_len:
                    self._author    = data[0]
                    self._title     = data[1]
                    self._date      = data[2]
                    self._cat       = data[3]
                    self._desc      = data[4]
                    self._dur       = data[5]
                    self._len       = data[6]
                    self._views     = data[7]
                    self._likes     = data[8]
                    self._dislikes  = data[9]
                    self._rating    = data[10]
                    self._bytes     = data[11]
                    self._search    = data[12]
                    self._timestamp = data[13]
                    self._dtime     = data[14]
                else:
                    sh.objs.mes (f,_('ERROR')
                                ,_('The condition "%s" is not observed!') \
                                % '%d >= %d' % (len(data),data_len)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
        
    def video(self):
        f = 'logic.Video.video'
        if self.Success:
            if not self._video:
                try:
                    self._video = pafy.new (url   = self._video_id
                                           ,basic = False
                                           ,gdata = False
                                           )
                except Exception as e:
                    self.Success = False
                    sh.objs.mes (f,_('WARNING')
                                ,_('Error adding "%s"!\n\nDetails: %s')\
                                % (self._url,str(e))
                                )
            return self._video
        else:
            sh.com.cancel(f)
    
    def image(self):
        f = 'logic.Video.image'
        if self.Success:
            if self._video:
                image = sh.Get (url      = self._video.thumb
                               ,encoding = None
                               ,Verbose  = False
                               ).run()
                if image:
                    self._bytes = image
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def get(self):
        f = 'logic.Video.get'
        if self.Success:
            self.Saved = objs.db().get_video(video_id=self._video_id)
            if self.Saved:
                self.assign_offline(self.Saved)
            else:
                sh.log.append (f,_('INFO')
                              ,_('Get new video info: %s') \
                              % str(self._video_id)
                              )
                self.video()
                self.assign_online()
                self.image()
                self.dump()
        else:
            sh.com.cancel(f)
    
    def summary(self):
        f = 'logic.Video.summary'
        if self.Success:
            tmp = io.StringIO()
            tmp.write(_('Author'))
            tmp.write(': ')
            tmp.write(self._author)
            tmp.write('\n')
            tmp.write(_('Title'))
            tmp.write(': ')
            tmp.write(self._title)
            tmp.write('\n')
            tmp.write(_('Date'))
            tmp.write(': ')
            tmp.write(self._date)
            tmp.write('\n')
            tmp.write(_('Category'))
            tmp.write(': ')
            tmp.write(self._cat)
            tmp.write('\n')
            tmp.write(_('Description'))
            tmp.write(': ')
            tmp.write(self._desc)
            tmp.write('\n')
            tmp.write(_('Duration'))
            tmp.write(': ')
            tmp.write(self._dur)
            tmp.write('\n')
            tmp.write(_('Length'))
            tmp.write(': ')
            tmp.write(str(self._len))
            tmp.write('\n')
            tmp.write(_('Views'))
            tmp.write(': ')
            tmp.write(str(self._views))
            tmp.write('\n')
            tmp.write(_('Likes'))
            tmp.write(': ')
            tmp.write(str(self._likes))
            tmp.write('\n')
            tmp.write(_('Dislikes'))
            tmp.write(': ')
            tmp.write(str(self._dislikes))
            tmp.write('\n')
            tmp.write(_('Rating'))
            tmp.write(': ')
            tmp.write(str(self._rating))
            tmp.write('\n')
            #todo: elaborate
            if self._video:
                tmp.write(_('Small video picture URL'))
                tmp.write(': ')
                tmp.write(str(self._video.thumb))
                tmp.write('\n')
            result = tmp.getvalue()
            result = sh.Text(text=result).delete_unsupported()
            tmp.close()
            return result
        else:
            sh.com.cancel(f)
        
    def path(self):
        f = 'logic.Video.path'
        if self.Success:
            if not self._path:
                author = sh.FixBaseName (basename = self._author
                                        ,AllOS    = AllOS
                                        ,max_len  = 100
                                        ).run()
                title  = sh.FixBaseName (basename = self._title
                                        ,AllOS    = AllOS
                                        ,max_len  = 100
                                        ).run()
                author = sh.Text(text=author).delete_unsupported()
                title  = sh.Text(text=title).delete_unsupported()
                self._dir  = objs.default().ihome.add_config ('Youtube'
                                                             ,author
                                                             )
                self._path = objs._default.ihome.add_config ('Youtube'
                                                            ,author
                                                            ,title
                                                            )
                self._pathsh = sh.Text (text = sh.Path(self._path).basename()
                                       ,Auto = False
                                       ).shorten (max_len = 20
                                                 ,FromEnd = False
                                                 ,ShowGap = True
                                                 )
                self._path += '.mp4'
            return self._path
        else:
            sh.com.cancel(f)
    
    def make_dir(self):
        f = 'logic.Video.make_dir'
        if self.Success:
            if self._dir:
                self.Success = sh.Path(path=self._dir).create()
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def download(self):
        f = 'logic.Video.download'
        self.make_dir()
        if self.Success:
            if self._video and self._path:
                sh.log.append (f,_('INFO')
                              ,_('Download "%s"') % self._path
                              )
                #todo: select format & quality
                try:
                    stream = self._video.getbest (preftype    = 'mp4'
                                                 ,ftypestrict = True
                                                 )
                    stream.download (filepath = self._path
                                    ,callback = self._callback
                                    )
                    # Tell other functions the operation was a success
                    return True
                except Exception as e:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Failed to download "%s"!\n\nDetails: %s') \
                                % (self._path,str(e))
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def stream(self):
        f = 'logic.Video.stream'
        if self.Success:
            if self._video:
                #todo: select quality
                try:
                    stream = self._video.getbest()
                    return stream.url
                except Exception as e:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Operation has failed!\n\nDetails: %s') \
                                % str(e)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class URL:
    
    def __init__(self,url):
        self._url = url
        self._url = sh.Input (title = 'URL.__init__'
                             ,value = self._url
                             ).not_none()
        self._url = str(self._url)
        self._url = self._url.strip()
    
    def video_id(self):
        self.video_full()
        return self._url.replace(pattern1,'')
    
    def video_full(self):
        f = 'logic.URL.video_full'
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
        f = 'logic.URL.channel_full'
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
            
    ''' There is no need to adjust channel URLs. Using this method will
        corrupt playlist URLs.
    '''
    def trash_v(self):
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



''' Any API operation has a timeout (even 'self.connect'), so we must
    reset the whole class each time.
'''
class Comments:

    def __init__(self,videoid):
        self.values()
        self.reset(videoid)
        
    def run(self):
        self.connect()
        self.threads()
        return self.comments()
        
    def values(self):
        self.Success   = True
        self._connect  = None
        self._threads  = None
        self._videoid  = ''
        self._comments = ''
        ''' https://github.com/Sunil02324/Youtube-Meta-Data-Comments-Scraper
            Default max results you can get is 100. So if a video has
            more than 100 comments we need to iterate the same function
            to get all the comments.
        '''
        self._max_no   = 100
        
    def reset(self,videoid):
        f = 'logic.Comments.reset'
        if videoid:
            self._videoid = videoid
        else:
            self.Success = False
            sh.com.empty(f)
    
    def connect(self):
        f = 'logic.Comments.connect'
        if self.Success:
            if not self._connect:
                try:
                    self._connect = apiclient ('youtube','v3'
                                              ,developerKey = pafy.g.api_key
                                              ,cache        = MemoryCache()
                                              )
                except Exception as e:
                    self.Success = False
                    sh.objs.mes (f,_('WARNING')
                                ,_('Operation has failed!\n\nDetails: %s') \
                                % str(e)
                                )
            return self._connect
        else:
            sh.com.cancel(f)
    
    def threads(self):
        f = 'logic.Comments.threads'
        if self.Success:
            if not self._threads:
                try:
                    self._threads = self._connect.commentThreads().list(
                                         part       = "snippet"
                                        ,maxResults = self._max_no
                                        ,videoId    = self._videoid
                                        ,textFormat = "plainText"
                                        ,pageToken  = ''
                                        ).execute()
                except Exception as e:
                    self.Success = False
                    sh.objs.mes (f,_('WARNING')
                                ,_('Operation has failed!\n\nDetails: %s')\
                                % str(e)
                                )
            return self._threads
        else:
            sh.com.cancel(f)
                          
    def comments(self):
        f = 'logic.Comments.comments'
        if self.Success:
            if not self._comments:
                for item in self._threads["items"]:
                    comment = item["snippet"]["topLevelComment"]
                    author  = comment["snippet"]["authorDisplayName"]
                    text    = comment["snippet"]["textDisplay"]
                    self._comments += author + ': ' + text + '\n\n'
            return self._comments
        else:
            sh.com.cancel(f)



# https://github.com/google/google-api-python-client/issues/325#issuecomment-274349841
class MemoryCache:
    _CACHE = {}
    
    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content



class DefaultConfig:
    
    def __init__(self,product='Yatube'):
        self.values()
        self.ihome   = sh.Home(app_name=product)
        self.Success = self.ihome.create_conf()
    
    def values(self):
        self._fsubsc  = ''
        self._fblock  = ''
        self._fblockw = ''
        self._fdb     = ''
    
    def db(self):
        f = 'logic.DefaultConfig.db'
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
        f = 'logic.DefaultConfig.block_words'
        if self.Success:
            self._fblockw = self.ihome.add_config('block words.txt')
            if self._fblockw:
                if os.path.exists(self._fblockw):
                    self.Success = sh.File(file=self._fblockw).Success
                else:
                    iwrite = sh.WriteTextFile (file       = self._fblockw
                                              ,AskRewrite = False
                                              )
                    iwrite.write('# ' + _('Put here words to block in titles (case is ignored)'))
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def block_channels(self):
        f = 'logic.DefaultConfig.block_channels'
        if self.Success:
            self._fblock = self.ihome.add_config('block channels.txt')
            if self._fblock:
                if os.path.exists(self._fblock):
                    self.Success = sh.File(file=self._fblock).Success
                else:
                    iwrite = sh.WriteTextFile (file       = self._fblock
                                              ,AskRewrite = False
                                              )
                    iwrite.write(sample_block)
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def subscribe(self):
        f = 'logic.DefaultConfig.subscribe'
        if self.Success:
            self._fsubsc = self.ihome.add_config('subscribe.txt')
            if self._fsubsc:
                if os.path.exists(self._fsubsc):
                    self.Success = sh.File(file=self._fsubsc).Success
                else:
                    iwrite = sh.WriteTextFile (file       = self._fsubsc
                                              ,AskRewrite = False
                                              )
                    iwrite.write(sample_subscribe)
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        f = 'logic.DefaultConfig.run'
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
    
    def add(self,author,url):
        if not url in self._urls:
            self._authors.append(author)
            self._urls.append(url)
            self._no = len(self._urls) - 1
    
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
        f = 'logic.ChannelHistory.prev'
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
        f = 'logic.ChannelHistory.next'
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


if __name__ == '__main__':
    url = 'http://www.youtube.com/user/AvtoKriminalist/videos'
    links = Links(sh.Get(url).run())
    links.run()
