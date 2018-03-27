#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
import io
import pafy      as pf
import shared    as sh
import sharedGUI as sg
import logic     as lg
import gui       as gi
import db

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')


AllOS = False



class Commands:
    
    def __init__(self):
        # Get a logic object by a GUI object
        self._videos  = {}
        self._video   = None
        self._gvideo  = None
        self._channel = None
        self._menu    = gi.objs.menu()
        itime         = lg.Time()
        itime.set_date(DaysDelta=7)
        itime.years()
        itime.months()
        itime.days()
        self._years  = itime._years
        self._year   = itime._year
        self._months = itime._months
        self._month  = itime._month
        self._days   = itime._days
        self._day    = itime._day
        const        = lg.Constants()
        self._countries = const.countries()
        self._trending  = const.trending()
        lists           = lg.Lists()
        lists.load()
        self._fblock     = lists._fblock
        self._fsubsc     = lists._fsubsc
        self._block_auth = lists._block_auth
        self._subsc_auth = lists._subsc_auth
        self._subsc_urls = lists._subsc_urls
        #todo: implement
        default_channels = [_('Channels')] #,_('All')
        if self._subsc_auth:
            self._channels = default_channels + self._subsc_auth
        else:
            self._channels = default_channels
    
    def filter_by_date(self,event=None):
        for video_gui in gi.objs.channel()._videos:
            if video_gui in self._videos:
                video = self._videos[video_gui]
                if video._date:
                    pass
                else:
                    sh.log.append ('Commands.filter_by_date'
                                  ,_('WARNING')
                                  ,_('Wrong input data!')
                                  )
            else:
                sh.objs.mes ('Commands.filter_by_date'
                            ,_('ERROR')
                            ,_('Wrong input data!')
                            )
    
    def get_widget(self,event=None):
        if event:
            ''' Widgets must be in a string format to be compared
                (otherwise, we will have, for example,
                'Tkinter.Frame object' vs 'string').
                For some reason, Tkinter adds some information to
                the address of the widget got as 'event.widget'
                (original widget address will be shorter)
            '''
            for video_gui in gi.objs.channel()._videos:
                for obj in video_gui._objects:
                    if str(obj.widget) in str(event.widget):
                        self._gvideo = video_gui
                        return self._gvideo
        else:
            sh.log.append ('Commands.get_widget'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def summary(self,event=None):
        gi.objs.summary().read_only(False)
        if self._video:
            gi.objs._summary.reset()
            gi.objs._summary.insert(self._video.summary())
        gi.objs._summary.read_only(True)
        gi.objs._summary.show()
    
    def context(self,event=None):
        # 'event' will be 'tuple' if it is a callback from 'Button.click'
        if isinstance(event,tuple):
            event = event[0]
        self.get_widget(event=event)
        if self._gvideo:
            self._video = self._videos[self._gvideo]
            message = _('Video #%d:') % self._gvideo._no
            gi.objs.context().title(message)
            gi.objs._context.show()
            choice = gi.objs._context._get
            if choice:
                if choice == _('Show the full summary'):
                    self.summary()
                elif choice == _('Download'):
                    self.download_video()
                elif choice == _('Play'):
                    self.play_video()
                elif choice == _('Stream'):
                    print(_('Stream'))
                elif choice == _('Block this channel'):
                    print(_('Block this channel'))
                elif choice == _('Subscribe to this channel'):
                    print(_('Subscribe to this channel'))
                elif choice == _('Open video URL'):
                    print(_('Open video URL'))
                elif choice == _('Open channel URL'):
                    print(_('Open channel URL'))
                else:
                    sh.objs.mes ('Commands.context'
                                ,_('ERROR')
                                ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                                % (str(choice),';'.join(gi.context_items))
                                )
            else:
                sh.log.append ('Commands.context'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
    
    def update_channel(self,author,url,Show=True):
        self._menu.opt_chl.set(author)
        self._channel = lg.Channel(url=url)
        self._channel.run()
        self.reset_channel_gui()
        self.channel_gui()
        if Show:
            gi.objs._channel.show()
        
    def _get_links(self,url):
        channel = self._channel = lg.Channel(url=url)
        channel._channel = url
        ''' We assume that there is no need to delete
            unsupported characters in countries.
        '''
        channel.page()
        channel.links()
        self.reset_channel_gui()
        self.channel_gui()
        gi.objs._channel.show()
                          
    def set_channel(self,event=None):
        if self._menu.opt_chl.choice == _('Channels'):
            sh.log.append ('Commands.set_channel'
                          ,_('INFO')
                          ,_('Nothing to do.')
                          )
        else:
            sh.log.append ('Commands.set_channel'
                          ,_('INFO')
                          ,_('Switch to channel "%s"') \
                          % str(self._menu.opt_chl.choice)
                          )
            if self._menu.opt_chl.choice in self._subsc_auth:
                author = self._menu.opt_chl.choice
                no     = self._subsc_auth.index(author)
                url    = self._subsc_urls[no]
                self.update_channel(author=author,url=url)
            else:
                #todo: console + GUI
                sh.log.append ('Commands.set_channel'
                              ,_('ERROR')
                              ,_('Wrong input data!')
                              )
        
    def get_links(self,event=None):
        result = self._menu.ent_lnk.get()
        if result and result != _('Get links from URL'):
            sh.log.append ('Commands.get_links'
                          ,_('DEBUG')
                          ,_('Get links from "%s"') % result
                          )
            self._get_links(url=result)
        else:
            sh.log.append ('Commands.get_links'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def get_url(self,event=None):
        result = self._menu.ent_url.get()
        if result and result != _('Get video from URL'):
            sh.log.append ('Commands.get_url'
                          ,_('INFO')
                          ,_('Download "%s"') % result
                          )
            #todo: check URL
            video = Video(url=result)
            video.video()
            video.assign_online()
            video.path()
            video.download()
            #todo: if downloaded successfully:
            self._menu.clear_url()
        else:
            sh.log.append ('Commands.get_url'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def toggle_select(self):
        if self._menu.chb_sel.get():
            for video in gi.objs.channel()._videos:
                video.cbox.enable()
        else:
            for video in gi.objs.channel()._videos:
                video.cbox.disable()
                
    def set_trending(self,event=None):
        sh.log.append ('Commands.set_trending'
                      ,_('INFO')
                      ,_('Switch to channel "%s"') \
                      % str(self._menu.opt_trd.choice)
                      )
        country = 'RU'
        if self._menu.opt_trd.choice == _('Trending'):
            user = _('Trending') + ' - ' + _('Russia')
        else:
            user = _('Trending') + ' - ' + self._menu.opt_trd.choice
            country = self._countries[self._menu.opt_trd.choice]
        url = 'https://www.youtube.com/feed/trending?gl=%s' % country
        sh.log.append ('Commands.set_trending'
                      ,_('DEBUG')
                      ,user
                      )
        sh.log.append ('Commands.set_trending'
                      ,_('DEBUG')
                      ,country
                      )
        sh.log.append ('Commands.set_trending'
                      ,_('DEBUG')
                      ,url
                      )
        self.update_trending(user=user,url=url)
        
    def search_youtube(self,event=None):
        result = self._menu.ent_src.get()
        if result and result != _('Search Youtube'):
            root_url = 'https://www.youtube.com/results?search_query=%s'
            result = sh.Online (base_str   = root_url
                               ,search_str = result
                               ,MTSpecific = False
                               ).url()
            sh.log.append ('Commands.search_youtube'
                          ,_('DEBUG')
                          ,result
                          )
            self._get_links(url=result)
        else:
            sh.log.append ('Commands.search_youtube'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def filter_view(self,event=None):
        result = self._menu.ent_flt.get()
        if result and result != _('Filter this view'):
            sh.log.append ('Commands.filter_view'
                          ,_('INFO')
                          ,_('Filter by "%s"') % result
                          )
            sg.Message ('Commands.filter_view'
                       ,_('INFO')
                       ,_('Not implemented yet!')
                       )
            #todo: implement
        else:
            sh.log.append ('Commands.filter_view'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def bindings(self):
        # Menu: main window
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Control-p>'
                ,action   = self.play
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Control-d>'
                ,action   = self.download
                )
        # Menu: buttons
        self._menu.btn_sub.action = self.manage_sub
        self._menu.btn_blk.action = self.manage_block
        self._menu.btn_upd.action = self.update_channels
        self._menu.btn_all.action = self.select_new
        self._menu.btn_ytb.action = self.search_youtube
        self._menu.btn_url.action = self.get_url
        self._menu.btn_lnk.action = self.get_links
        self._menu.btn_flt.action = self.filter_view
        self._menu.btn_dld.action = self.download
        self._menu.btn_ply.action = self.play
        # Menu: labels
        sg.bind (obj      = self._menu.ent_src
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.search_youtube
                )
        sg.bind (obj      = self._menu.ent_url
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.get_url
                )
        sg.bind (obj      = self._menu.ent_lnk
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.get_links
                )
        sg.bind (obj      = self._menu.ent_flt
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.filter_view
                )
        # Menu: checkboxes
        self._menu.chb_sel.widget.config(command=self.toggle_select)
        self._menu.chb_dat.widget.config(command=self.filter_by_date)
        # Menu: OptionMenus
        self._menu.opt_day.reset (items   = self._days
                                 ,default = self._day
                                 )
        self._menu.opt_mth.reset (items   = self._months
                                 ,default = self._month
                                 )
        self._menu.opt_yrs.reset (items   = self._years
                                 ,default = self._year
                                 )
        self._menu.opt_trd.reset (items   = self._trending
                                 ,default = _('Trending')
                                 ,action  = self.set_trending
                                 )
        self._menu.opt_chl.reset (items   = self._channels
                                 ,default = _('Channels')
                                 ,action  = self.set_channel
                                 )
        
    def select_new(self,event=None):
        sg.Message ('Commands.select_new'
                   ,_('INFO')
                   ,_('Not implemented yet!')
                   )
        
    def play_video(self,event=None):
        if self._video:
            sh.Launch (target=self._video._path).app \
                          (custom_app  = '/usr/bin/mplayer'
                          ,custom_args = ['-ao','sdl','-fs'
                                         ,'-framedrop'
                                         ,'-nocorrect-pts'
                                         ]
                          )
        else:
            sh.log.append ('Commands.play_video'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def play(self,event=None):
        for video_gui in gi.objs.channel()._videos:
            if video_gui.cbox.get():
                self._gvideo = video_gui
                if self._gvideo in self._videos:
                    self._video = self._videos[self._gvideo]
                    self.download_video()
                    self.play_video()
                else:
                    sg.Message ('Commands.play'
                               ,_('ERROR')
                               ,_('Wrong input data!')
                               )
        
    def download_video(self,event=None):
        if self._video and self._gvideo:
            self._video.video()
            self._video.path()
            gi.objs.progress().add()
            gi.objs._progress.show()
            gi.objs._progress.obj.widget.focus_force()
            sg.Geometry(parent=gi.objs._progress.obj).activate()
            self._video.download()
            dbi.mark_downloaded(url=self._video._url)
            self._gvideo.cbox.disable()
            self._gvideo.gray_out()
        else:
            sh.log.append ('Commands.download_video'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def download(self,event=None):
        for video_gui in gi.objs.channel()._videos:
            if video_gui.cbox.get():
                self._gvideo = video_gui
                if self._gvideo in self._videos:
                    self._video = self._videos[self._gvideo]
                    self.download_video()
                else:
                    sg.Message ('Commands.download'
                               ,_('ERROR')
                               ,_('Wrong input data!')
                               )
        
    def update_channels(self,event=None):
        for i in range(len(self._subsc_auth)):
            self.update_channel (author = self._subsc_auth[i]
                                ,url    = self._subsc_urls[i]
                                ,Show   = False
                                )
        
    def update_trending (self,event=None,user=None
                        ,url=None
                        ):
        if not user:
            user = _('Trending') + ' - ' + _('Russia')
        if not url:
            url = 'https://www.youtube.com/feed/trending?gl=RU'
        self._channel = lg.Channel(url=url)
        self._channel._channel = user
        ''' We assume that there is no need to delete unsupported
            characters in countries.
        '''
        self._channel.page()
        self._channel.links()
        self.reset_channel_gui()
        self.channel_gui()
        
    def reset_channel_gui(self):
        self._video = self._gvideo = None
        # Clears the old Channel widget
        self._menu.framev.widget.pack_forget()
        self._menu.framev = sg.Frame(parent=self._menu.parent)
        gi.objs._channel = None
        gi.objs.channel(parent=self._menu.framev)
        
    def bind_context(self,event=None):
        for video_gui in gi.objs.channel()._videos:
            for obj in video_gui._objects:
                sg.bind (obj      = obj
                        ,bindings = '<ButtonRelease-3>'
                        ,action   = self.context
                        )
        
    def channel_gui(self):
        for i in range(len(self._channel._links)):
            gi.objs.channel().add(no=i)
            # Show default picture & video information
            sg.objs.root().widget.update_idletasks()
            video = Video(url=self._channel._links[i])
            video.get()
            if video.Success:
                author    = sh.Text(text=video._author).delete_unsupported()
                title     = sh.Text(text=video._title).delete_unsupported()
                duration  = sh.Text(text=video._dur).delete_unsupported()
                if author in self._block_auth \
                or video._author in self._block_auth:
                    author = title = _('BLOCKED')
                    video._image = None
                video_gui = gi.objs._channel._videos[i]
                video_gui.reset (no       = i + 1
                                ,author   = author
                                ,title    = title
                                ,duration = duration
                                ,image    = video._image
                                )
                if video.Ready:
                    video_gui.gray_out()
                self._videos[video_gui] = video
                #if not video.Saved:
                ''' #fix showing only videos No. 10-21 with 'update_scroll'
                    disabled.
                    This does not work in 'Channel.__init__' for some
                    reason, calling this externally.
                '''
                gi.objs._channel.update_scroll()
        dbi.save()
        self.bind_context()
        # Move back to video #0
        gi.objs._channel.canvas.widget.yview_moveto(0)
    
    #todo: elaborate
    def manage_sub(self,event=None):
        sh.Launch(self._fsubsc).default()
        #todo: reload
        
    #todo: elaborate
    def manage_block(self,event=None):
        sh.Launch(self._fblock).default()
        #todo: reload



# Requires dbi
class Video:
    
    def __init__(self,url):
        self.values()
        self._url = url
        
    def progress (self,total=0,cur_size=0
                 ,ratio=0,rate=0,eta=0
                 ):
        total    = total    / 1000000
        cur_size = cur_size / 1000000
        rate     = int(rate)
        eta      = int(eta)
        gi.objs.progress()._item.text (file     = self._pathsh
                                      ,cur_size = cur_size
                                      ,total    = total
                                      ,rate     = rate
                                      ,eta      = eta
                                      )
        percent = round((100*cur_size)/total)
        gi.objs._progress._item.widget['value'] = percent
        sg.objs.root().widget.update_idletasks()
    
    def values(self):
        self.Success = True
        self.Ready   = False
        self._video  = self._image = self._bytes = self.Saved = None
        self._author = self._title = self._date = self._cat \
                     = self._desc = self._dur = self._path \
                     = self._pathsh = ''
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
                       ,self._rating,self._bytes,False,False,False
                       )
                dbi.add_video(data)
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
            data_len = 13
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
                self.Ready     = data[12]
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
            self.Saved = dbi.get_video(url=self._url)
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
            self._path += '.mp4'
            self._pathsh = sh.Text(text=self._path).shorten (max_len = 22
                                                            ,FromEnd = 1
                                                            )
        else:
            sh.log.append ('Video.path'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def download(self):
        if self.Success:
            if self._video and self._path:
                if sh.rewrite(self._path):
                    sh.log.append ('Video.download'
                                  ,_('INFO')
                                  ,_('Download "%s"') % self._path
                                  )
                    #todo: select format & quality
                    stream = self._video.getbest (preftype    = 'mp4'
                                                 ,ftypestrict = True
                                                 )
                    stream.download (filepath = self._path
                                    ,callback = self.progress
                                    )
                else:
                    sh.log.append ('Video.download'
                                  ,_('INFO')
                                  ,_('Operation has been canceled by the user.')
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



if __name__ == '__main__':
    sg.objs.start()
    parent = gi.objs.parent()
    sg.Geometry(parent=parent).set('985x600')
    dbi = db.DB()
    commands = Commands()
    commands.bindings()
    gi.objs.progress()
    gi.objs.menu().widget.wait_window()
    dbi.save()
    dbi.close()
    sg.objs.end()
