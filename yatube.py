#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','./locale')

import sys
import os
import io
import pafy   as pf
import shared as sh
import model  as md
import db



class Commands:
    
    def __init__(self,Silent=False):
        self._menu    = None
        self._channel = None
        self._videos  = []
        self.Silent = Silent
        itime = md.Time()
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
        const = md.Constants()
        self._countries = const.countries()
        self._trending  = const.trending()
        lists = md.Lists(Silent=Silent)
        lists.load()
        self._fblock     = lists._fblock
        self._fsubsc     = lists._fsubsc
        self._block_auth = lists._block_auth
        self._block_urls = lists._block_urls
        self._subsc_auth = lists._subsc_auth
        self._subsc_urls = lists._subsc_urls
        #todo: implement
        default_channels = [_('Channels')] #,_('All')
        if self._subsc_auth:
            self._channels = default_channels + self._subsc_auth
        else:
            self._channels = default_channels
    
    def update_channel(self,author,url,Show=True):
        self._menu.om_chnl.set(author)
        self._channel = md.Channel(user=url)
        self._channel.run()
        self.reset_channel_gui()
        self.channel_gui()
        if Show:
            gi.objs._channel.show()
        
    def _get_links(self,url):
        path = sh.objs.pdir().add('Youtube',_('Search'))
        if sh.Path(path=path).create():
            channel = self._channel = md.Channel (user         = url
                                                 ,download_dir = path
                                                 )
            channel._channel = url
            ''' We assume that there is no need to delete
                unsupported characters in countries.
            '''
            channel.create()
            channel.check_dir()
            channel.page()
            channel.links()
            self.reset_channel_gui()
            self.channel_gui()
            gi.objs._channel.show()
        else:
            sh.log.append ('Menu._get_links'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def set_channel(self,event=None):
        if self._menu.om_chnl.choice == _('Channels'):
            sh.log.append ('Commands.set_channel'
                          ,_('INFO')
                          ,_('Nothing to do.')
                          )
        else:
            sh.log.append ('Commands.set_channel'
                          ,_('INFO')
                          ,_('Switch to channel "%s"') \
                          % str(self._menu.om_chnl.choice)
                          )
            if self._menu.om_chnl.choice in self._subsc_auth:
                author = self._menu.om_chnl.choice
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
        result = self._menu.en_lnks.get()
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
        result = self._menu.en_gurl.get()
        if result and result != _('Get video from URL'):
            sh.log.append ('Commands.get_url'
                          ,_('INFO')
                          ,_('Download "%s"') % result
                          )
            #todo: check URL
            video = Video(url=result)
            video.video()
            video.assign_online()
            #todo: create './Youtube/_(Search)' path automatically
            path = sh.objs.pdir().add('Youtube',_('Search'))
            if sh.Path(path=path).create():
                #todo: sanitize
                title = video._title.replace('/','').replace('"','')
                if not title:
                    title = 'video'
                path = os.path.join(path,title)
                #todo: set extension automatically
                path += '.mp4'
                video.download(path=path)
                #todo: if downloaded successfully:
                self._menu.clear_url()
            else:
                sh.log.append ('Commands.get_url'
                              ,_('WARNING')
                              ,_('Operation has been canceled.')
                              )
        else:
            sh.log.append ('Commands.get_url'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def toggle_select(self):
        if self._menu.cb_slct.get():
            for video in gi.objs.channel()._videos:
                video.cbox.enable()
        else:
            for video in gi.objs.channel()._videos:
                video.cbox.disable()
                
    def set_trending(self,event=None):
        sh.log.append ('Commands.set_trending'
                      ,_('INFO')
                      ,_('Switch to channel "%s"') \
                      % str(self._menu.om_trnd.choice)
                      )
        country = 'RU'
        if self._menu.om_trnd.choice == _('Trending'):
            user = _('Trending') + ' - ' + _('Russia')
        else:
            user = _('Trending') + ' - ' + self._menu.om_trnd.choice
            country = self._countries[self._menu.om_trnd.choice]
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
        result = self._menu.en_srch.get()
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
        result = self._menu.en_fltr.get()
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
        sg.bind (obj      = self._menu.en_srch
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.search_youtube
                )
        sg.bind (obj      = self._menu.en_gurl
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.get_url
                )
        sg.bind (obj      = self._menu.en_lnks
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.get_links
                )
        
        sg.bind (obj      = self._menu.en_fltr
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.filter_view
                )
        # Menu: checkboxes
        self._menu.cb_slct.widget.config(command=self.toggle_select)
        # Menu: OptionMenus
        self._menu.om_wday.reset (items   = self._days
                                 ,default = self._day
                                 )
        self._menu.om_mnth.reset (items   = self._months
                                 ,default = self._month
                                 )
        self._menu.om_yers.reset (items   = self._years
                                 ,default = self._year
                                 )
        self._menu.om_trnd.reset (items   = self._trending
                                 ,default = _('Trending')
                                 ,command = self.set_trending
                                 )
        self._menu.om_chnl.reset (items = self._channels
                                 ,default = _('Channels')
                                 ,command = self.set_channel
                                 )
        
    def select_new(self,event=None):
        sg.Message ('Commands.select_new'
                   ,_('INFO')
                   ,_('Not implemented yet!')
                   )
        
    def play(self,event=None):
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
        
    def download(self,event=None):
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
        
    def update_channels(self,event=None):
        for i in range(len(self._subsc_auth)):
            self.update_channel (author = self._subsc_auth[i]
                                ,url    = self._subsc_urls[i]
                                ,Show   = False
                                )
        gi.objs.channel().show()
        
    def update_trending (self,event=None,user=None
                        ,url=None
                        ):
        if not user:
            user = _('Trending') + ' - ' + _('Russia')
        if not url:
            url = 'https://www.youtube.com/feed/trending?gl=RU'
        self._channel = md.Channel(user=user)
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
        
    def reset_channel_gui(self):
        # Clears the old Channel widget
        self._menu.framev.widget.pack_forget()
        self._menu.framev = sg.Frame (parent = self._menu.parent)
        gi.objs._channel = None
        gi.objs.channel(parent=self._menu.framev)
        
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
        dbi.save()
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
    
    def zzz(self):
        pass


class UI:
    
    def __init__(self,Silent=False):
        self.Silent = Silent
        
    def show(self):
        if not self.Silent:
            sg.objs.start()
            
    def menu(self):
        if self.Silent:
            #todo: implement
            self._menu = None
        else:
            parent = gi.objs.parent()
            #cur
            sg.Geometry(parent=parent).set('985x600')
            #sg.Geometry(parent=parent).maximize()
            self._menu = gi.objs.menu()
        commands._menu = self._menu
            
    def close(self):
        if not self.Silent:
            sg.objs.end()



# Requires dbi
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



if __name__ == '__main__':
    if len(sys.argv) > 1:
        Silent = True
        print(_('Sorry! Command-line interface is not implemented yet.'))
    else:
        Silent = False
        import sharedGUI as sg
        import gui       as gi
    ui = UI(Silent=Silent)
    ui.show()
    dbi = db.DB(Silent=Silent)
    commands = Commands(Silent=Silent)
    ui.menu()
    if not Silent:
        commands.bindings()
        ui._menu.show()
    dbi.save()
    dbi.close()
    ui.close()
