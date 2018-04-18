#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import io
import pafy   as pf
import shared as sh
import db

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')

video_root_url = 'https://www.youtube.com/watch?v='
AllOS = False
idb = db.DB()



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
        last_year  = sh.Input (title = 'Time.years'
                              ,value = last_year
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
                    '''
                    sh.log.append ('Channel.url'
                                  ,_('DEBUG')
                                  ,_('User:') + ' ' + self._channel
                                  )
                    sh.log.append ('Channel.url'
                                  ,_('DEBUG')
                                  ,_('URL:') + ' ' + self._url
                                  )
                    '''
                    self.warn()
                else:
                    self.Success = False
                    sh.log.append ('Channel.url'
                                  ,_('WARNING')
                                  ,_('Wrong input data!')
                                  )
            else:
                self.Success = False
                sh.log.append ('Channel.url'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Channel.url'
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
                          ,_('Fetched %d links') % len(self._links)
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
        if os.path.exists(self._fsubsc2):
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



# Requires idb
class Video:
    
    def __init__(self,url,callback=None):
        self.values()
        self._url = url
        self._callback = callback
        
    def values(self):
        self.Success = True
        self.Block   = self.Ignore = self.Ready = False
        self._video  = self._bytes = self.Saved = None
        self._author = self._title = self._date = self._cat \
                     = self._desc = self._dur = self._path \
                     = self._pathsh = self._search = self._timestamp \
                     = ''
        self._len    = self._views = self._likes = self._dislikes = 0
        self._rating = 0.0
        
    def assign_online(self):
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
            # Youtube says: invalid parameters
            except:
                sh.log.append ('Video.assign_online'
                              ,_('WARNING')
                              ,_('Third party module has failed!')
                              )
            self._search    = self._author.lower() + ' ' \
                              + self._title.lower()
            itime           = sh.Time(pattern='%Y-%m-%d %H:%M:%S')
            itime._date     = self._date
            self._timestamp = itime.timestamp()
        else:
            sh.log.append ('Video.assign_online'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def dump(self):
        if self.Success:
            ''' Do no write default data.
                Do not forget to commit where necessary.
            '''
            if self._video:
                data = (self._url,self._author,self._title,self._date
                       ,self._cat,self._desc,self._dur,self._len
                       ,self._views,self._likes,self._dislikes
                       ,self._rating,self._bytes,self.Block,self.Ignore
                       ,self.Ready,self._search,self._timestamp
                       )
                idb.add_video(data)
            else:
                sh.log.append ('Video.dump'
                              ,_('INFO')
                              ,_('Nothing to do.')
                              )
        else:
            sh.log.append ('Video.dump'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        
    def assign_offline(self,data):
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
                self.Ready      = data[12]
                self._search    = data[13]
                self._timestamp = data[14]
            else:
                sh.objs.mes ('Video.assign_offline'
                            ,_('ERROR')
                            ,_('The condition "%s" is not observed!') \
                            % '%d >= %d' % (len(data),data_len)
                            )
        else:
            sh.log.append ('Video.assign_offline'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        
    def video(self):
        if self.Success:
            if not self._video:
                try:
                    self._video = pf.new (url   = self._url
                                         ,basic = False
                                         ,gdata = False
                                         )
                except:
                    self.Success = False
                    sh.log.append ('Video.video'
                                  ,_('WARNING')
                                  ,_('Error adding "%s"!') % self._url
                                  )
        else:
            sh.log.append ('Video.video'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def image(self):
        if self.Success:
            if self._video:
                image = sh.Get (url      = self._video.thumb
                               ,encoding = None
                               ,Verbose  = False
                               ).run()
                if image:
                    self._bytes = image
                else:
                    sh.log.append ('Video.image'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                sh.log.append ('Video.image'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Video.image'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def get(self):
        if self.Success:
            self.Saved = idb.get_video(url=self._url)
            if self.Saved:
                self.assign_offline(self.Saved)
            else:
                sh.log.append ('Video.get'
                              ,_('INFO')
                              ,_('Get new URL: %s') % str(self._url)
                              )
                self.video()
                self.assign_online()
                self.image()
                self.dump()
        else:
            sh.log.append ('Video.get'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def summary(self):
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
            sh.log.append ('Video.summary'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        
    def path(self):
        if self.Success:
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
            folder = sh.objs.pdir().add('..','user','Youtube',author)
            self.Success = sh.Path(path=folder).create()
            self._path = sh.objs.pdir().add ('..','user','Youtube'
                                            ,author,title
                                            )
            self._pathsh = sh.Text(text=self._path).shorten (max_len = 19
                                                            ,FromEnd = 1
                                                            )
            self._path += '.mp4'
        else:
            sh.log.append ('Video.path'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def download(self):
        if self.Success:
            if self._video and self._path:
                sh.log.append ('Video.download'
                              ,_('INFO')
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
                except:
                    sh.objs.mes ('Video.download'
                                ,_('WARNING')
                                ,_('Failed to download "%s"!') \
                                % self._path
                                )
            else:
                sh.log.append ('Video.download'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Video.download'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )


objs = Objects()


if __name__ == '__main__':
    pass
