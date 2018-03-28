#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import shared as sh

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')

video_root_url = 'https://www.youtube.com/watch?v='



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
        # Year of Youtube birth
        first_year = 2005
        last_year  = self.itime.year()
        last_year  = sh.Input (func_title = 'Time.years'
                              ,val        = last_year
                              ).integer()
        if not last_year > first_year:
            sh.log.append ('Time.years'
                          ,_('WARNING')
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
       
    ''' 'user' must represent one of the following patterns:
        - 'https://www.youtube.com/channel/USER'
        - 'https://www.youtube.com/channel/USER/videos'
        - 'https://www.youtube.com/user/USER'
        - 'https://www.youtube.com/user/USER/videos'
        - 'USER'
    '''
    def __init__(self,url):
        self.values()
        self._url = url
        
    def warn(self):
        if not self._html:
            self.Success = False
            sh.objs.mes (func    = 'Channel.page'
                        ,level   = _('WARNING')
                        ,message = _('Channel "%s" does not exist!') \
                                   % self._channel
                        )
    
    def url(self):
        if self.Success:
            if self._url:
                if isinstance(self._url,str):
                    if self._url.endswith('/'):
                        self._url = self._url[:-1]
                    ''' 'https://www.youtube.com/user/AvtoKriminalist/videos?disable_polymer=1'
                        или
                        'https://www.youtube.com/user/AvtoKriminalist/videos'
                    '''
                    if self._link_p1 and self._link_p3 in self._url:
                        self._channel = self._url.replace(self._link_p1,'').replace(self._link_p2a,'').replace(self._link_p2b,'').replace(self._link_p3,'')
                        self.page()
                        self.warn()
                    # 'https://www.youtube.com/user/AvtoKriminalist'
                    elif self._link_p1 in self._url:
                        self._url += self._link_p3
                        self._channel = self._url.replace(self._link_p1,'').replace(self._link_p2a,'').replace(self._link_p2b,'')
                        self.page()
                    # 'AvtoKriminalist'
                    else:
                        # 'https://www.youtube.com/channel/AvtoKriminalist/videos'
                        self._channel = self._url
                        self._url = self._link_p1 + self._link_p2a \
                                                  + self._url \
                                                  + self._link_p3
                        self.page()
                        if not self._html:
                            # 'https://www.youtube.com/user/AvtoKriminalist/videos'
                            self._url = self._link_p1 + self._link_p2b \
                                                      + self._channel \
                                                      + self._link_p3
                            self.page()
                    sh.log.append ('Channel.url'
                                  ,_('DEBUG')
                                  ,_('User:') + ' ' + self._channel
                                  )
                    sh.log.append ('Channel.url'
                                  ,_('DEBUG')
                                  ,_('URL:') + ' ' + self._url
                                  )
                    self.warn()
                else:
                    self.Success = False
                    sh.log.append ('Channel.user'
                                  ,_('WARNING')
                                  ,_('Wrong input data!')
                                  )
            else:
                self.Success = False
                sh.log.append ('Channel.user'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Channel.user'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
            
    def values(self):
        self.Success    = True
        #todo: localize
        self._not_found = 'Такой канал не существует.'
        self._link_p1   = 'https://www.youtube.com/'
        self._link_p2a  = 'channel/'
        self._link_p2b  = 'user/'
        self._link_p3   = '/videos'
        self._channel   = ''
        self._html      = ''
        self._text      = ''
        self._links     = []
    
    def page(self):
        if self.Success:
            response = sh.Get(url=self._url).run()
            if response and not self._not_found in response:
                self._html = response
        else:
            sh.log.append ('Channel.page'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def links(self):
        if self.Success:
            result = Links(self._html)
            result.run()
            self._links = result._links
            sh.log.append ('Channel.links'
                          ,_('INFO')
                          ,_('Fetched %d links for the user "%s"') \
                          % (len(self._links),self._channel)
                          )
        else:
            sh.log.append ('Channel.links'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def run(self):
        self.url()
        self.links()
        


class Links:
    
    def __init__(self,text):
        self._root  = '<a href="/watch?v='
        self._pos   = 0
        self._links = []
        self._text  = text
    
    def poses(self):
        text = self._text
        search = sh.Search (text   = self._text
                           ,search = self._root
                           )
        loop = search.next_loop()
        for self._pos in loop:
            self.link()
            
    def link(self):
        pos = self._pos + len(self._root)
        if pos >= len(self._text):
            sh.log.append ('Links.link'
                          ,_('WARNING')
                          ,_('Unexpected end of text!')
                          )
        else:
            text = self._text[pos:]
            try:
                pos = text.index('"')
                self._links.append(text[:pos])
            except ValueError:
                sh.log.append ('Links.link'
                              ,_('WARNING')
                              ,_('Wrong input data!')
                              )
                              
    def delete_suffixes(self):
        for i in range(len(self._links)):
            self._links[i] = re.sub ('&amp;index=\d+&amp;list=.*'
                                    ,''
                                    ,self._links[i]
                                    )
            self._links[i] = re.sub ('&amp;list=.*'
                                    ,''
                                    ,self._links[i]
                                    )
    
    def run(self):
        if self._text:
            self.poses()
            self.delete_suffixes()
        else:
            sh.log.append ('Links.run'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )



class Lists:
    
    def __init__(self):
        self.values()
        self._fblock  = sh.objs.pdir().add('..','user','block.txt')
        self._fsubsc  = sh.objs.pdir().add('..','user','subscribe.txt')
        self._fsubsc2 = sh.objs.pdir().add('..','user','subscribe2.txt')
        
    def reset(self):
        self.values()
        self.load()
    
    def values(self):
        self._block      = ''
        self._subsc      = ''
        self._subsc2     = ''
        self._block_auth = []
        self._subsc_auth = []
        self._subsc_urls = []
    
    def load(self):
        text = sh.ReadTextFile(file=self._fblock).get()
        if text:
            self._block = text
            self._block_auth = text.splitlines()
        dic = sh.Dic (file     = self._fsubsc
                     ,Sortable = False
                     )
        if dic.Success:
            self._subsc      = dic.text
            self._subsc_auth = dic.orig
            self._subsc_urls = dic.transl
        dic = sh.Dic (file     = self._fsubsc2
                     ,Sortable = False
                     )
        if dic.Success:
            self._subsc2      = dic.text
            self._subsc_auth += dic.orig
            self._subsc_urls += dic.transl
        if self._subsc_auth:
            self._subsc_auth, self._subsc_urls = (list(x) for x \
            in zip (*sorted (zip (self._subsc_auth, self._subsc_urls)
                            ,key = lambda x:x[0].lower()
                            )
                   )
                                                 )



class Objects:
    
    def __init__(self):
        self._online = self._lists = self._const = None
        
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


objs = Objects()


if __name__ == '__main__':
    pass
