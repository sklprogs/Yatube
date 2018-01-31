#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import io
import pafy      as pf
import shared    as sh
import sharedGUI as sg
import gui       as gi
import db
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','./locale')


product = 'Yatube'
version = '(alpha)'
AllOS = False


class Memory:
    
    def __init__(self):
        self._urls     = []
        self._channels = []
        self._videos   = []
        
    def get(self,url):
        if url in self._urls:
            ind = self._urls.index(url)
            channel = self._channels[ind]
        else:
            channel = Channel(user=url)
        return channel


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
                              
    def run(self):
        if self._text:
            self.poses()
        else:
            sh.log.append ('Links.run'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )



class Video:
    
    def __init__(self,url):
        self.values()
        self._url = url
        
    def values(self):
        self.Success = True
        self._video  = self._image = self._bytes = self.Saved = None
        self._author = self._title = self._date = self._cat \
                     = self._desc = self._dur = ''
        self._len    = self._views = self._likes = self._dislikes = 0
        self._rating = 0.0
        
    def assign_online(self):
        if self._video:
            self._author   = self._video.author
            self._title    = self._video.title
            self._date     = self._video.published
            self._cat      = self._video.category
            self._desc     = self._video.description
            self._dur      = self._video.duration
            self._len      = self._video.length
            self._views    = self._video.viewcount
            self._likes    = self._video.likes
            self._dislikes = self._video.dislikes
            self._rating   = self._video.rating
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
                       ,self._rating,self._bytes,False,False
                       )
                objs.db().add_video(data)
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
            data_len = 12
            if len(data) >= data_len:
                self._author   = data[0]
                self._title    = data[1]
                self._date     = data[2]
                self._cat      = data[3]
                self._desc     = data[4]
                self._dur      = data[5]
                self._len      = data[6]
                self._views    = data[7]
                self._likes    = data[8]
                self._dislikes = data[9]
                self._rating   = data[10]
                self._bytes    = data[11]
                img = sg.Image()
                img._bytes = self._bytes
                img.loader()
                self._image = img.image()
            else:
                sg.Message ('Video.assign_offline'
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
                                         ,basic = True
                                         ,gdata = False
                                         )
                except:
                    self.Success = False
                    sh.log.append ('Videos.video'
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
                               ).run()
                if image:
                    img = sg.Image()
                    self._bytes = img._bytes = image
                    img.loader()
                    self._image = img.image()
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
            self.Saved = objs.db().get_video(url=self._url)
            if self.Saved:
                self.assign_offline(self.Saved)
            else:
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
        
    def download(self,path):
        if self.Success:
            if self._video and path:
                sh.log.append ('Video.download'
                              ,_('INFO')
                              ,_('Download "%s"') % path
                              )
                sg.objs.waitbox().reset (func_title = 'Video.download'
                                        ,message    = _('Download %s') \
                                                      % path
                                        )
                sg.objs._waitbox.show()
                #todo: select format & quality
                stream = self._video.getbest()
                stream.download (filepath = path
                                #,quiet    = True
                                )
                sg.objs._waitbox.close()
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



class Channel:
       
    ''' 'user' must represent one of the following patterns:
        - 'https://www.youtube.com/channel/USER'
        - 'https://www.youtube.com/channel/USER/videos'
        - 'https://www.youtube.com/user/USER'
        - 'https://www.youtube.com/user/USER/videos'
        - 'USER'
    '''
    def __init__(self,user,download_dir='./Youtube'):
        self.values()
        self._user = user
        self._dir  = download_dir
        
    def warn(self):
        if not self._html:
            self.Success = False
            sg.Message (func    = 'Channel.page'
                       ,level   = _('WARNING')
                       ,message = _('Channel "%s" does not exist!') \
                                  % self._channel
                       )
    
    def user(self):
        if self.Success:
            if self._user:
                if isinstance(self._user,str):
                    if self._user.endswith('/'):
                        self._user = self._user[:-1]
                    ''' 'https://www.youtube.com/user/AvtoKriminalist/videos?disable_polymer=1'
                        или
                        'https://www.youtube.com/user/AvtoKriminalist/videos'
                    '''
                    if self._link_p1 and self._link_p3 in self._user:
                        self._channel = self._user
                        self._user    = self._user.replace(self._link_p1,'').replace(self._link_p2a,'').replace(self._link_p2b,'').replace(self._link_p3,'')
                        self.page()
                        self.warn()
                    # 'https://www.youtube.com/user/AvtoKriminalist'
                    elif self._link_p1 in self._user:
                        self._channel = self._user + self._link_p3
                        self._user    = self._user.replace(self._link_p1,'').replace(self._link_p2a,'').replace(self._link_p2b,'')
                        self.page()
                    # 'AvtoKriminalist'
                    else:
                        # 'https://www.youtube.com/channel/AvtoKriminalist/videos'
                        self._channel = self._link_p1 + self._link_p2a \
                                                      + self._user \
                                                      + self._link_p3
                        self.page()
                        if not self._html:
                            # 'https://www.youtube.com/user/AvtoKriminalist/videos'
                            self._channel = self._link_p1 \
                                            + self._link_p2b \
                                            + self._user \
                                            + self._link_p3
                            self.page()
                    sh.log.append ('Channel.user'
                                  ,_('DEBUG')
                                  ,_('User:') + ' ' + self._user
                                  )
                    sh.log.append ('Channel.user'
                                  ,_('DEBUG')
                                  ,_('URL:') + ' ' + self._channel
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
        
    def check_dir(self):
        if self.Success:
            if self._dir and isinstance(self._dir,str) and \
               sh.Directory(path=self._dir,Silent=True).Success:
                   self.Success = True
            else:
                self.Success = False
        else:
            sh.log.append ('Channel.check_dir'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
            
    def values(self):
        self.Success     = True
        #todo: localize
        self._not_found  = 'Такой канал не существует.'
        self._link_p1    = 'https://www.youtube.com/'
        self._link_p2a   = 'channel/'
        self._link_p2b   = 'user/'
        self._link_p3    = '/videos'
        self._channel    = ''
        self._html       = ''
        self._user       = ''
        self._escaped    = ''
        self._text       = ''
        self._links      = []
            
    def escape(self):
        if self.Success:
            self._escaped = sh.FixBaseName (basename = self._user
                                           ,AllOS    = AllOS
                                           ,max_len  = 100
                                           ).run()
            if self._escaped:
                self._dir = os.path.join(self._dir,self._escaped)
            else:
                self.Success = False
                sh.log.append ('Channel.escape'
                              ,_('WARNING')
                              ,_('Empty output is not allowed!')
                              )
        else:
            sh.log.append ('Channel.escape'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def create(self):
        if self.Success:
            self.Success = sh.Path(path=self._dir).create()
        else:
            sh.log.append ('Channel.create'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def page(self):
        if self.Success:
            response = sh.Get(url=self._channel).run()
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
                          % (len(self._links),self._user)
                          )
        else:
            sh.log.append ('Channel.links'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def run(self):
        self.check_dir()
        self.user()
        self.escape()
        self.create()
        self.links()



class Menu:
    
    def __init__(self,parent=None):
        self.values()
        self.set_date()
        self.parent = parent
        self.set_parent()
        self.gui()
        
    def values(self):
        self._days   = [str(day+1) for day in range(31)]
        # sh.Time outputs a day number preceded by 0
        self._days   = tuple ('0' + day if len(day) == 1 else day \
                              for day in self._days
                             )
        self._months = (_('Jan'),_('Feb'),_('Mar'),_('Apr'),_('May')
                       ,_('Jun'),_('Jul'),_('Aug'),_('Sep'),_('Oct')
                       ,_('Nov'),_('Dec')
                       )
        self.time_i = sh.Time(pattern='%d',MondayWarning=False)
        # Year of Youtube birth
        first_year = 2005
        last_year  = self.time_i.year()
        last_year  = sh.Input (func_title = 'Menu.values'
                              ,val        = last_year
                              ).integer()
        if not last_year > first_year:
            sh.log.append ('Menu.values'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )
            last_year = 2018
        self._years = tuple (str(year) for year in range (first_year
                                                         ,last_year + 1
                                                         )
                            )
        default_channels = [_('Channels'),_('All')]
        channels = objs.db().get_channels()
        if channels:
            self._channels = default_channels + channels
        else:
            self._channels = default_channels
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
        trending = self._countries.keys()
        trending = sorted(trending)
        self._trending = [_('Trending')] + trending
    
    def set_date(self,DaysDelta=7):
        self.time_i.add_days(days_delta=-DaysDelta)
        self._year = str(self.time_i.year())
        self._day = self.time_i.date()
        self.time_i.month_abbr()
        self._month = self.time_i.localize_month_abbr()
    
    def set_parent(self):
        if not self.parent:
            self.parent = objs.parent()
            
    def show(self,*args):
        self.parent.show()
        
    def close(self,*args):
        objs.db().save()
        objs._db.close()
        self.widget.destroy()
    
    def frames(self):
        self.frame1 = sg.Frame (parent = self.parent
                               ,expand = False
                               )
        self.frame2 = sg.Frame (parent = self.parent
                               ,expand = False
                               )
        self.frame3 = sg.Frame (parent = self.parent
                               ,expand = False
                               )
        self.frame4 = sg.Frame (parent = self.frame3
                               ,expand = False
                               ,side   = 'right'
                               )
        ''' We can create an additional frame here for gi.Channel, but
            gi.Channel.bindings needs to have Toplevel as a parent.
        '''
        self.framev = sg.Frame (parent = self.parent)
    
    def clear_filter(self,*args):
        self.clear_search()
        #todo: Restore filtered videos here
                   
    def clear_search(self,*args):
        self.en_srch.clear_text()
    
    def widgets(self):
        self.btn_sub = sg.Button (parent = self.frame1
                                 ,text   = _('Manage subscriptions')
                                 ,action = commands.manage_sub
                                 )
        self.btn_blk = sg.Button (parent = self.frame1
                                 ,text   = _('Manage blocklist')
                                 ,action = commands.manage_block
                                 )
        self.btn_upd = sg.Button (parent = self.frame1
                                 ,text   = _('Update subscriptions')
                                 ,action = commands.update_channels
                                 )
        self.btn_all = sg.Button (parent = self.frame2
                                 ,text   = _('Select all new videos')
                                 ,action = commands.select_new
                                 )
        self.btn_flt = sg.Button (parent = self.frame2
                                 ,text   = _('Select by filter')
                                 ,action = commands.filter
                                 )
        self.cb_date = sg.CheckBox (parent = self.frame2
                                   ,Active = False
                                   ,side   = 'left'
                                   )
        self.om_date = sg.OptionMenu (parent  = self.frame2
                                     ,items   = (_('Newer than')
                                                ,_('Older than')
                                                )
                                     ,default = _('Newer than')
                                     )
        self.om_wday = sg.OptionMenu (parent  = self.frame2
                                     ,items   = self._days
                                     ,default = self._day
                                     )
        self.om_mnth = sg.OptionMenu (parent  = self.frame2
                                     ,items   = self._months
                                     ,default = self._month
                                     )
        self.om_yers = sg.OptionMenu (parent  = self.frame2
                                     ,items   = self._years
                                     ,default = self._year
                                     )
        self.cb_srch = sg.CheckBox (parent = self.frame2
                                   ,Active = False
                                   ,side   = 'left'
                                   )
        self.en_srch = sg.Entry (parent    = self.frame2
                                ,Composite = True
                                ,side      = 'left'
                                )
        self.btn_clr = sg.Button (parent = self.frame2
                                 ,text   = _('Clear')
                                 ,action = self.clear_filter
                                 )
        self.cb_slct = sg.CheckBox (parent = self.frame3
                                   ,Active = False
                                   ,side   = 'left'
                                   ,action = self.toggle_select
                                   )
        self.btn_dld = sg.Button (parent = self.frame3
                                 ,text   = _('Download selected')
                                 ,action = commands.download
                                 )
        self.btn_ply = sg.Button (parent = self.frame3
                                 ,text   = _('Play')
                                 ,action = commands.play
                                 )
        self.om_trnd = sg.OptionMenu (parent  = self.frame4
                                     ,items   = self._trending
                                     ,side    = 'left'
                                     ,default = _('Trending')
                                     ,command = self.set_trending
                                     )
        self.om_chnl = sg.OptionMenu (parent  = self.frame4
                                     ,items   = self._channels
                                     ,side    = 'left'
                                     ,default = _('Channels')
                                     ,command = self.set_channel
                                     )
    
    def set_channel(self,*args):
        sh.log.append ('Menu.set_channel'
                      ,_('INFO')
                      ,_('Switch to channel "%s"') \
                      % str(self.om_chnl.choice)
                      )
        commands.update_channel(user=self.om_chnl.choice)
    
    def init_config(self):
        self.btn_upd.focus()
        self.en_srch.insert(_('Search in channels'))
        self.en_srch.widget.config (font = 'Serif 10 italic'
                                   ,fg   = 'grey'
                                   )
        # cur
        #self.btn_dld.widget.config(state='disabled')
        #self.btn_ply.widget.config(state='disabled')
                  
    def bindings(self):
        sg.bind (obj      = self.parent
                ,bindings = ['<Control-w>','<Control-q>']
                ,action   = self.close
                )
        sg.bind (obj      = self.parent
                ,bindings = '<Escape>'
                ,action   = self.minimize
                )
        sg.bind (obj      = self.en_srch
                ,bindings = ['<ButtonRelease-1>','<ButtonRelease-2>']
                ,action   = self.clear_search
                )
        sg.bind (obj      = self.parent
                ,bindings = '<Key-p>'
                ,action   = commands.play
                )
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
    
    def title(self,text=None):
        if not text:
            text = sh.List(lst1=[product,version]).space_items()
        self.parent.title(text)
    
    def gui(self):
        self.widget = self.parent.widget
        self.frames()
        self.widgets()
        self.init_config()
        self.icon()
        self.title()
        self.bindings()
        
    def toggle_select(self):
        if self.cb_slct.get():
            for video in gi.objs.channel()._videos:
                video.cbox.enable()
        else:
            for video in gi.objs.channel()._videos:
                video.cbox.disable()
                
    def set_trending(self):
        sh.log.append ('Menu.set_trending'
                      ,_('INFO')
                      ,_('Switch to channel "%s"') \
                      % str(self.om_trnd.choice)
                      )
        country = 'RU'
        if self.om_trnd.choice == _('Trending'):
            user = _('Trending') + ' - ' + _('Russia')
        else:
            user = _('Trending') + ' - ' + self.om_trnd.choice
            country = self._countries[self.om_trnd.choice]
        url = 'https://www.youtube.com/feed/trending?gl=%s' % country
        sh.log.append ('Menu.set_trending'
                      ,_('DEBUG')
                      ,user
                      )
        sh.log.append ('Menu.set_trending'
                      ,_('DEBUG')
                      ,country
                      )
        sh.log.append ('Menu.set_trending'
                      ,_('DEBUG')
                      ,url
                      )
        commands.update_trending(user=user,url=url)
    
    def minimize(self,event=None):
        self.widget.iconify()
    
    def icon(self,path=None):
        if not path:
            path = sh.objs.pdir().add ('resources'
                                      ,'icon_64x64_yatube.gif'
                                      )
        sg.WidgetShared.icon(self.parent,path)
    
    def zzz(self):
        pass



class Objects:
    
    def __init__(self):
        self._db = self._menu = self._parent = None
        
    def db(self):
        if not self._db:
            self._db = db.DB()
        return self._db
        
    def parent(self):
        if not self._parent:
            self._parent = sg.SimpleTop(parent=sg.objs.root())
            #sg.Geometry(parent=self._parent).set('985x600')
            sg.Geometry(parent=self._parent).maximize()
        return self._parent
    
    def menu(self):
        if not self._menu:
            self._menu = Menu(parent=self.parent())
        return self._menu



class Commands:
    
    def __init__(self):
        self._channel = None
        self._videos  = []
        
    def play(self,*args):
        #todo: refacture
        if self._channel:
            for video_gui in gi.objs.channel()._videos:
                if video_gui.cbox.get():
                    # Video numbering starts with 1
                    ''' #note: This condition may actually not be
                        observed because 'self._videos' are videos that
                        we successfuly got. If there are random
                        connection problems, the condition may fail.
                        #if len(self._videos) >= video_gui._no:
                    '''
                    #video = self._videos[video_gui._no]
                    video = video_gui.logic
                    #todo: sanitize video._title (FS)
                    video._title = video._title.replace('"','').replace('/','')
                    path = os.path.join (self._channel._dir
                                        ,video._title
                                        )
                    #todo: autodetect extension
                    path += '.mp4'
                    video._path = path
                    video.video()
                    video.download(path)
                    sh.Launch (target=path).app \
                              (custom_app  = '/usr/bin/mplayer'
                              ,custom_args = ['-fs','-framedrop'
                                             ,'-nocorrect-pts'
                                             ]
                              )
                    '''
                    else:
                        sg.Message ('Commands.play'
                                   ,_('ERROR')
                                   ,_('The condition "%s" is not observed!') \
                                   % ('%d > %d') % (len(self._videos)
                                                   ,video_gui._no
                                                   )
                                   )
                    '''
        else:
            sh.log.append ('Commands.play'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def select_new(self,*args):
        sg.Message ('Commands.select_new'
                   ,_('INFO')
                   ,_('Not implemented yet!')
                   )
    
    def filter(self,*args):
        sg.Message ('Commands.filter'
                   ,_('INFO')
                   ,_('Not implemented yet!')
                   )
        
    def download(self,*args):
        if self._channel:
            for video_gui in gi.objs.channel()._videos:
                if video_gui.cbox.get():
                    if len(self._videos) > video_gui._no:
                        #video = self._videos[video_gui._no]
                        video = video_gui.logic
                        #todo: sanitize video._title (FS)
                        video._title = video._title.replace('"','').replace('/','')
                        path = os.path.join (self._channel._dir
                                            ,video._title
                                            )
                        #todo: autodetect extension
                        path += '.mp4'
                        video._path = path
                        video.video()
                        video.download(path)
                    else:
                        sg.Message ('Commands.download'
                                   ,_('ERROR')
                                   ,_('The condition "%s" is not observed!') \
                                   % ('%d > %d') % (len(self._videos)
                                                   ,video_gui._no
                                                   )
                                   )
        else:
            sh.log.append ('Commands.download'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def update_channel(self,user='Centerstrain01'):
        objs.menu().om_chnl.set(user)
        self._channel = Channel(user=user)
        self._channel.run()
        self.reset_channel_gui()
        self.channel_gui()

    def update_channels(self,*args):
        channels = objs.db().get_channels()
        for channel in channels:
            self.update_channel(user=channel)

    def reset_channel_gui(self):
        # Clears the old Channel widget
        objs._menu.framev.widget.pack_forget()
        objs._menu.framev = sg.Frame (parent = objs._menu.parent)
        gi.objs._channel = None
        gi.objs.channel(parent=objs._menu.framev)
        
    def channel_gui(self):
        for i in range(len(self._channel._links)):
            gi.objs.channel().add(no=i)
            # Show default picture & video information
            sg.objs.root().widget.update_idletasks()
            video = Video(url=self._channel._links[i])
            video.get()
            if video.Success:
                self._videos.append(video)
                author    = sh.Text(text=video._author).delete_unsupported()
                title     = sh.Text(text=video._title).delete_unsupported()
                duration  = sh.Text(text=video._dur).delete_unsupported()
                video_gui = gi.objs._channel._videos[i]
                video_gui.reset (no       = i + 1
                                ,author   = author
                                ,title    = title
                                ,duration = duration
                                ,image    = video._image
                                ,logic    = video
                                )
                ''' This does not work in 'Channel.__init__' for some
                    reason, calling this externally.
                '''
                ''' #fix showing only videos No. 10-21 with 'update_scroll'
                    disabled
                '''
                #if not video.Saved:
                gi.objs._channel.update_scroll()
        objs.db().save()
        # Move back to video #0
        gi.objs._channel.canvas.widget.yview_moveto(0)
        gi.objs._channel.show()
    
    def update_trending (self,event=None,user=None
                        ,url=None
                        ):
        if not user:
            user = _('Trending') + ' - ' + _('Russia')
        if not url:
            url = 'https://www.youtube.com/feed/trending?gl=RU'
        self._channel = Channel(user=user)
        self._channel._channel = url
        ''' We assume that there is no need to delete unsupported
            characters in countries.
        '''
        #todo: set home dir automatically
        download_dir = '/home/pete/downloads/Youtube/' + user
        self._channel._dir = download_dir
        self._channel.create()
        self._channel.check_dir()
        self._channel.page()
        self._channel.links()
        self.reset_channel_gui()
        self.channel_gui()

    def manage_sub(self,*args):
        old_channels = objs.db().get_channels()
        gi.objs.sub().fill(lst=old_channels)
        gi.objs._sub.show()
        channels = gi.objs._sub.get()
        if not channels:
            channels = []
        for channel in channels:
            if not channel in old_channels:
                objs._db.add_channel(data=(channel,False,))
        objs._db.save()
                   
    def manage_block(self,*args):
        channels = objs.db().get_channels(block=1)
        gi.objs.block().fill(lst=channels)
        gi.objs._block.show()
        channels = gi.objs._block.get()
        if channels:
            objs._db.block_channels(channels,block=0)
            objs._db.block_channels(channels)
            objs._db.save()


objs = Objects()
commands = Commands()



if __name__ == '__main__':
    sg.objs.start()
    menu = objs.menu()
    gi.objs.channel(parent=objs._menu.framev)
    #gi.objs.channel(parent=objs._menu.parent)
    menu.show()
    sg.objs.end()
