#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import shared    as sh
import sharedGUI as sg
import logic     as lg
import gui       as gi

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')


class Commands:
    
    def __init__(self):
        # Get a logic object by a GUI object
        self._videos    = {}
        self._video     = None
        self._gvideo    = None
        self._channel   = None
        self._timestamp = None
        self.FirstVideo = True
        self._menu      = gi.objs.menu()
        itime           = lg.Time()
        itime.set_date(DaysDelta=7)
        itime.years()
        itime.months()
        itime.days()
        self._years     = itime._years
        self._year      = itime._year
        self._months    = itime._months
        self._month     = itime._month
        self._days      = itime._days
        self._day       = itime._day
        lg.objs.lists().reset()
        self.reset_channels()
        
    def show_comments(self,event=None):
        if self._video:
            text = lg.Comments(videoid=self._video.model._video_id).run()
            if text:
                text = sh.Text(text=text).delete_unsupported()
                gi.objs.comments().read_only(ReadOnly=False)
                gi.objs._comments.reset()
                gi.objs._comments.insert(text)
                gi.objs._comments.read_only(ReadOnly=True)
                gi.objs._comments.show()
            else:
                sh.log.append ('Commands.show_comments'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Commands.show_comments'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def toggle_selected(self,event=None):
        for video_gui in gi.objs.channel()._videos:
            if video_gui.cbox.get():
                if video_gui in self._videos:
                    self._gvideo = video_gui
                    self._video  = self._videos[self._gvideo]
                    self.toggle_downloaded()
                else:
                    sh.log.append ('Commands.toggle_selected'
                                  ,_('ERROR')
                                  ,_('Wrong input data!')
                                  )
    
    def other(self,event=None):
        choice = self._menu.opt_act.choice
        if choice == _('Other'):
            pass
        elif choice == _('Manage subscriptions'):
            self._menu.opt_act.set(_('Other'))
            self.manage_sub()
        elif choice == _('Manage blocklist'):
            self._menu.opt_act.set(_('Other'))
            self.manage_block()
        elif choice == _('Show new videos'):
            self._menu.opt_act.set(_('Other'))
            self.show_new()
        elif choice == _('History'):
            self._menu.opt_act.set(_('Other'))
            self.history()
        elif choice == _('Welcome screen'):
            self._menu.opt_act.set(_('Other'))
            self.blank()
        elif choice == _('Select all new videos'):
            self._menu.opt_act.set(_('Other'))
            self.select_new()
        elif choice == _('Toggle status of selected'):
            self._menu.opt_act.set(_('Other'))
            self.toggle_selected()
        elif choice == _('Delete selected'):
            self._menu.opt_act.set(_('Other'))
            self.delete_selected()
        else:
            sh.objs.mes ('Commands.other'
                        ,_('ERROR')
                        ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                        % (str(choice),';'.join(gi.other_actions))
                        )
    
    def blank(self,event=None):
        self.reset_channel_gui()
        self._menu.clear_search(Force=True)
        self._menu.clear_url()
        self._menu.clear_filter(Force=True)
        gi.objs.parent().focus()
        self._menu.opt_chl.set(_('Channels'))
        self._menu.opt_trd.set(_('Trending'))
        gi.objs.channel().canvas.move_top()
    
    def history(self,event=None):
        urls = idb.downloaded()
        if urls:
            ''' URL can be any here, even 'None', but we do not use
                'None' in order to be on the safe side since many
                classes have checks against empty input in '__init__'.
            '''
            self._channel = lg.Channel(url='https://www.youtube.com/feed/trending?gl=RU')
            self._channel._links = urls
            self.reset_channel_gui()
            self.channel_gui()
        else:
            # Do not warn here since this is actually a common case
            sh.log.append ('Commands.history'
                          ,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def unsubscribe(self,event=None):
        if self._video and self._video.model.channel_url():
            self._video.model.video()
            if self._video.model._author:
                if self._video.model._author \
                in lg.objs.lists()._subsc_auth:
                    sh.log.append ('Commands.unsubscribe'
                                  ,_('INFO')
                                  ,_('Unsubscribe from channel "%s"') \
                                  % self._video.model._author
                                  )
                    if self._video.model._author \
                    in lg.objs._lists._subsc_auth1:
                        ind = lg.objs._lists._subsc_auth1.index(self._video.model._author)
                        del lg.objs._lists._subsc_auth1[ind]
                        del lg.objs._lists._subsc_urls1[ind]
                        subscriptions = []
                        for i in range(len(lg.objs._lists._subsc_auth1)):
                            subscriptions.append (lg.objs._lists._subsc_auth1[i]\
                                                 + '\t' \
                                                 + lg.objs._lists._subsc_urls1[i]
                                                 )
                        subscriptions = '\n'.join(subscriptions)
                        if subscriptions:
                            sh.WriteTextFile (file       = lg.objs._lists._fsubsc
                                             ,AskRewrite = False
                                             ).write(text=subscriptions)
                            lg.objs._lists.reset()
                            self.reset_channels()
                else:
                    sh.log.append ('Commands.unsubscribe'
                                  ,_('INFO')
                                  ,_('Nothing to do!')
                                  )
            else:
                sh.log.append ('Commands.unsubscribe'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Commands.unsubscribe'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def unblock(self,event=None):
        if self._video:
            self._video.model.video()
            if self._video.model._author:
                if self._video.model._author \
                in lg.objs.lists()._block_auth:
                    sh.log.append ('Commands.unblock'
                                  ,_('INFO')
                                  ,_('Unblock channel "%s"') \
                                  % self._video.model._author
                                  )
                    lg.objs._lists._block_auth.remove(self._video.model._author)
                    blocked = lg.objs._lists._block_auth
                    blocked = '\n'.join(blocked)
                    if blocked:
                        sh.WriteTextFile (file       = lg.objs._lists._fblock
                                         ,AskRewrite = False
                                         ).write(text=blocked)
                        lg.objs._lists.reset()
                        self.reset_channels()
                    else:
                        sh.log.append ('Commands.unblock'
                                      ,_('WARNING')
                                      ,_('Empty input is not allowed!')
                                      )
                else:
                    sh.log.append ('Commands.unblock'
                                  ,_('INFO')
                                  ,_('Nothing to do!')
                                  )
            else:
                sh.log.append ('Commands.unblock'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Commands.unblock'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def _show_new(self,urls):
        ''' URL can be any here, even 'None', but we do not use 'None'
                in order to be on the safe side since many classes have
                checks against empty input in '__init__'.
            '''
        self._channel = lg.Channel(url='https://www.youtube.com/feed/trending?gl=RU')
        self._channel._links = urls
        self.reset_channel_gui()
        self.channel_gui()
    
    def show_new(self,event=None):
        itime = sh.Time(pattern='%Y-%m-%d %H:%M:%S')
        itime.add_days(days_delta=-2)
        urls = idb.new_videos (timestamp = itime.timestamp()
                              ,authors   = lg.objs.lists()._subsc_auth
                              )
        if urls:
            self._show_new(urls)
        else:
            # Do not warn here since this is actually a common case
            sh.log.append ('Commands.show_new'
                          ,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    # GUI-only
    def delete_selected(self,event=None):
        deleted = []
        for video_gui in gi.objs.channel()._videos:
            if video_gui.cbox.get():
                if video_gui in self._videos:
                    self._gvideo = video_gui
                    self._video  = self._videos[self._gvideo]
                    if self.delete_video():
                        deleted.append(self._video.model.path())
                else:
                    sh.log.append ('Commands.delete_selected'
                                  ,_('ERROR')
                                  ,_('Wrong input data!')
                                  )
        if deleted:
            message = '\n\n'.join(deleted)
            message = _('%d files have been deleted:') % len(deleted) \
                      + '\n\n' \
                      + message
            sh.log.append ('Commands.delete_selected'
                          ,_('INFO')
                          ,message
                          )
    
    def delete_video(self,event=None):
        ''' Do not warn when the GUI object is not available (e.g.,
            performing deletion through OptionMenu.
        '''
        if self._gvideo:
            ''' We probably want to disable the checkbox even when
                the file was not removed, e.g., the user selected all
                videos on the channel and pressed 'Shift-Del'.
            '''
            self._gvideo.cbox.disable()
            gi.report_selection()
        if self._video:
            return self._video.model.delete()
        else:
            sh.log.append ('Commands.delete_video'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def reset_channels(self,event=None):
        default_channels = [_('Channels')]
        if lg.objs.lists()._subsc_auth:
            self._channels = default_channels \
                             + lg.objs._lists._subsc_auth
        else:
            self._channels = default_channels
        self._menu.opt_chl.reset (items   = self._channels
                                 ,default = _('Channels')
                                 ,action  = self.set_channel
                                 )
    
    def open_video_url(self,event=None):
        if self._video and self._video.model._url:
            lg.objs.online()._url = self._video.model._url
            lg.objs._online.browse()
        else:
            sh.log.append ('Commands.open_video_url'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                   
    def copy_video_url(self,event=None):
        if self._video and self._video.model._url:
            sg.Clipboard().copy(text=self._video.model._url)
        else:
            sh.log.append ('Commands.copy_video_url'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def subscribe(self,event=None):
        if self._video and self._video.model.channel_url():
            self._video.model.video()
            if self._video.model._author:
                if self._video.model._author \
                in lg.objs.lists()._subsc_auth:
                    sh.log.append ('Commands.subscribe'
                                  ,_('INFO')
                                  ,_('Nothing to do!')
                                  )
                else:
                    sh.log.append ('Commands.subscribe'
                                  ,_('INFO')
                                  ,_('Subscribe to channel "%s"') \
                                  % self._video.model._author
                                  )
                    subscriptions = []
                    for i in range(len(lg.objs._lists._subsc_auth1)):
                        subscriptions.append (lg.objs._lists._subsc_auth1[i]\
                                             + '\t' \
                                             + lg.objs._lists._subsc_urls1[i]
                                             )
                    subscriptions.append (self._video.model._author \
                                         + '\t' \
                                         + self._video.model._channel_url
                                         )
                    subscriptions = sorted (subscriptions
                                           ,key=lambda x:x[0].lower()
                                           )
                    subscriptions = '\n'.join(subscriptions)
                    if subscriptions:
                        sh.WriteTextFile (file       = lg.objs._lists._fsubsc
                                         ,AskRewrite = False
                                         ).write(text=subscriptions)
                        lg.objs._lists.reset()
                        self.reset_channels()
                    else:
                        sh.log.append ('Commands.subscribe'
                                      ,_('WARNING')
                                      ,_('Empty input is not allowed!')
                                      )
            else:
                sh.log.append ('Commands.subscribe'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Commands.subscribe'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def block(self,event=None):
        if self._video:
            self._video.model.video()
            if self._video.model._author:
                if self._video.model._author \
                in lg.objs.lists()._block_auth:
                    sh.log.append ('Commands.block'
                                  ,_('INFO')
                                  ,_('Nothing to do!')
                                  )
                else:
                    sh.log.append ('Commands.block'
                                  ,_('INFO')
                                  ,_('Block channel "%s"') \
                                  % self._video.model._author
                                  )
                    lg.objs._lists._block_auth.append(self._video.model._author)
                    blocked = lg.objs._lists._block_auth
                    blocked = sorted (blocked
                                     ,key=lambda x:x[0].lower()
                                     )
                    blocked = '\n'.join(blocked)
                    if blocked:
                        sh.WriteTextFile (file       = lg.objs._lists._fblock
                                         ,AskRewrite = False
                                         ).write(text=blocked)
                        lg.objs._lists.reset()
                        self.reset_channels()
                    else:
                        sh.log.append ('Commands.block'
                                      ,_('WARNING')
                                      ,_('Empty input is not allowed!')
                                      )
            else:
                sh.log.append ('Commands.block'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Commands.block'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                   
    def load_channel(self,event=None):
        if self._video and self._video.model.channel_url():
            self._channel = lg.Channel(url=self._video.model._channel_url)
            self._channel.run()
            self.reset_channel_gui()
            self.channel_gui()
        else:
            sh.log.append ('Commands.load_channel'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def open_channel_url(self,event=None):
        if self._video and self._video.model.channel_url():
            lg.objs.online()._url = self._video.model._channel_url
            lg.objs._online.browse()
        else:
            sh.log.append ('Commands.open_channel_url'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def copy_channel_url(self,event=None):
        if self._video and self._video.model.channel_url():
            sg.Clipboard().copy(text=self._video.model._channel_url)
        else:
            sh.log.append ('Commands.copy_channel_url'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def stream(self,event=None):
        sg.Message ('Commands.stream'
                   ,_('INFO')
                   ,_('Not implemented yet!')
                   )
                   
    def toggle_downloaded(self,event=None):
        if self._video and self._gvideo:
            if self._video.model._dtime:
                self._video.model._dtime = 0
            else:
                self._video.model._dtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
            idb.mark_downloaded (video_id = self._video.model._video_id
                                ,dtime    = self._video.model._dtime
                                )
            if self._video.model._dtime:
                self._gvideo.gray_out()
            else:
                self._gvideo.black_out()
        else:
            sh.log.append ('Commands.toggle_downloaded'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def reset_date_filter(self,event=None):
        self._timestamp = None
        self.filter_by_date()
    
    def timestamp(self,event=None):
        if not self._timestamp:
            day   = self._menu.opt_day.choice
            month = self._menu.opt_mth.choice
            year  = self._menu.opt_yrs.choice
            if month == _('Jan'):
                month = '01'
            elif month == _('Feb'):
                month = '02'
            elif month == _('Mar'):
                month = '03'
            elif month == _('Apr'):
                month = '04'
            elif month == _('May'):
                month = '05'
            elif month == _('Jun'):
                month = '06'
            elif month == _('Jul'):
                month = '07'
            elif month == _('Aug'):
                month = '08'
            elif month == _('Sep'):
                month = '09'
            elif month == _('Oct'):
                month = '10'
            elif month == _('Nov'):
                month = '11'
            elif month == _('Dec'):
                month = '12'
            itime = sh.Time(pattern='%Y-%m-%d')
            itime._date = year + '-' + month + '-' + day
            self._timestamp = itime.timestamp()
        return self._timestamp
    
    def _date_filter(self):
        cond1 = self._video.model._timestamp >= self.timestamp()
        cond2 = self._menu.opt_dat.choice == _('Newer than')
        if (cond1 and cond2) or (not cond1 and not cond2):
            return True
    
    ''' 'filter_by_date' uses the loop to filter videos by date upon
        event (changing filter date or filter settings).
        'video_date_filter' is used to mark a suitable video immediately
        when loading a channel.
        '_date_filter' is used by both methods (+'select_new') and
        should not be called externally in other cases.
    '''
    def video_date_filter(self,event=None):
        if self._video and self._gvideo and self._video.model._timestamp:
            if self._menu.chb_dat.get():
                if self._date_filter():
                    self._gvideo.red_out()
        else:
            sh.log.append ('Commands.video_date_filter'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def filter_by_date(self,event=None):
        # Do not allow to update channel GUI when no channels are loaded
        if gi.objs._channel:
            for video_gui in gi.objs._channel._videos:
                video_gui.black_out()
            if self._menu.chb_dat.get():
                timestamp = self.timestamp()
                for video_gui in gi.objs.channel()._videos:
                    if video_gui in self._videos:
                        self._gvideo = video_gui
                        self._video  = self._videos[self._gvideo]
                        if self._date_filter():
                            self._gvideo.red_out()
                    else:
                        sh.objs.mes ('Commands.filter_by_date'
                                    ,_('ERROR')
                                    ,_('Wrong input data!')
                                    )
        else:
            sh.log.append ('Commands.filter_by_date'
                          ,_('INFO')
                          ,_('Nothing to do.')
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
        if self._video:
            gi.objs.summary().reset()
            gi.objs._summary.insert(self._video.model.summary())
        gi.objs._summary.show()
    
    def _context(self,choice,event=None):
        if choice:
            if choice == _('Show the full summary'):
                self.summary()
            elif choice == _('Download'):
                self.download_video()
            elif choice == _('Play'):
                self.download_video()
                self.play_video()
            elif choice == _('Stream'):
                self.stream()
            elif choice == _('Toggle the download status'):
                self.toggle_downloaded()
            elif choice == _('Delete the downloaded file'):
                self.delete_video()
            elif choice == _('Extract links'):
                if self._video.model._url:
                    self.get_links(url=self._video.model._url)
                else:
                    sh.log.append ('Commands._context'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            elif choice == _('Load this channel'):
                self.load_channel()
            elif choice == _('Block this channel'):
                self.block()
            elif choice == _('Unblock'):
                self.unblock()
            elif choice == _('Subscribe to this channel'):
                self.subscribe()
            elif choice == _('Unsubscribe'):
                self.unsubscribe()
            elif choice == _('Open video URL'):
                self.open_video_url()
            elif choice == _('Copy video URL'):
                self.copy_video_url()
            elif choice == _('Show comments'):
                self.show_comments()
            elif choice == _('Open channel URL'):
                self.open_channel_url()
            elif choice == _('Copy channel URL'):
                self.copy_channel_url()
            else:
                sh.objs.mes ('Commands._context'
                            ,_('ERROR')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                            % (str(choice),';'.join(gi.context_items))
                            )
        else:
            sh.log.append ('Commands._context'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def context(self,event=None):
        # 'event' will be 'tuple' if it is a callback from 'Button.click'
        if isinstance(event,tuple):
            event = event[0]
        self.get_widget(event=event)
        if self._gvideo:
            if self._gvideo in self._videos:
                self._video = self._videos[self._gvideo]
                message = _('Video #%d:') % self._gvideo._no
                gi.objs.context().title(message)
                gi.objs._context.show()
                choice = gi.objs._context._get
                self._context(choice)
            else:
                sh.log.append ('Commands.context'
                              ,_('WARNING')
                              ,_('Wrong input data!')
                              )
    
    def update_channel(self,author,url):
        self._menu.opt_chl.set(author)
        self._channel = lg.Channel(url=url)
        self._channel.run()
        self.reset_channel_gui()
        self.channel_gui()
        
    def get_links(self,url):
        self._channel = lg.Channel(url=url)
        self._channel.run()
        self.reset_channel_gui()
        self.channel_gui()
                          
    def set_channel(self,event=None):
        if self._menu.opt_chl.choice == _('Channels'):
            self.show_new()
        else:
            sh.log.append ('Commands.set_channel'
                          ,_('INFO')
                          ,_('Switch to channel "%s"') \
                          % str(self._menu.opt_chl.choice)
                          )
            if self._menu.opt_chl.choice in lg.objs.lists()._subsc_auth:
                author = self._menu.opt_chl.choice
                no     = lg.objs._lists._subsc_auth.index(author)
                url    = lg.objs._lists._subsc_urls[no]
                self.update_channel (author = author
                                    ,url    = url
                                    )
            else:
                sh.objs.mes ('Commands.set_channel'
                            ,_('ERROR')
                            ,_('Wrong input data: "%s"') \
                            % str(self._menu.opt_chl.choice)
                            )
        
    def get_url(self,event=None):
        result = self._menu.ent_url.get()
        if result:
            if result == _('Paste URL here'):
                sh.log.append ('Commands.get_url'
                              ,_('INFO')
                              ,_('Nothing to do!')
                              )
            elif self._menu.opt_url.choice in gi.url_items:
                if self._menu.opt_url.choice == _('Extract links'):
                    self._video = self._gvideo = None
                    self.get_links(url=result)
                else:
                    video_id = lg.URL(url=result).video_id()
                    video = Video(video_id=video_id)
                    video.get()
                    if video.model.Success:
                        self._video = video
                        ''' Set to 'None', otherwise, wrong GUI object will
                            be manipulated!
                        '''
                        self._gvideo = None
                        if self._menu.opt_url.choice == _('Show summary'):
                            self.summary()
                        elif self._menu.opt_url.choice == _('Download'):
                            self.download_video()
                            gi.objs._progress.close()
                        elif self._menu.opt_url.choice == _('Play'):
                            self.download_video()
                            gi.objs._progress.close()
                            self.play_video()
                        elif self._menu.opt_url.choice == _('Stream'):
                            self.stream()
                        elif self._menu.opt_url.choice == _('Delete'):
                            self.delete_video()
                            self._menu.clear_url()
                        elif self._menu.opt_url.choice == _('Full menu'):
                            gi.objs.context().title(_('Selected video'))
                            gi.objs._context.show()
                            choice = gi.objs._context._get
                            self._context(choice)
                    else:
                        sh.log.append ('Commands.get_url'
                                      ,_('WARNING')
                                      ,_('Operation has been canceled.')
                                      )
            else:
                sh.objs.mes ('Commands.get_url'
                            ,_('WARNING')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                            % (str(self._menu.opt_url.choice)
                              ,';'.join(gi.url_items)
                              )
                            )
        else:
            sh.log.append ('Commands.get_url'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def set_trending(self,event=None):
        sh.log.append ('Commands.set_trending'
                      ,_('INFO')
                      ,_('Switch to channel "%s"') \
                      % str(self._menu.opt_trd.choice)
                      )
        country = lg.objs.const()._countries[self._menu.opt_trd.choice]
        url = 'https://www.youtube.com/feed/trending?gl=%s' % country
        sh.log.append ('Commands.set_trending'
                      ,_('DEBUG')
                      ,country
                      )
        sh.log.append ('Commands.set_trending'
                      ,_('DEBUG')
                      ,url
                      )
        self.update_trending(url=url)
        
    def search_youtube(self,event=None):
        result = self._menu.ent_src.get()
        if result and result != _('Search Youtube'):
            root_url = 'https://www.youtube.com/results?search_query=%s'
            result = sh.Online (base_str   = root_url
                               ,search_str = result
                               ,MTSpecific = False
                               ).url()
            self.get_links(url=result)
        else:
            sh.log.append ('Commands.search_youtube'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def filter_view(self,event=None):
        # Remove previous filter; drop selection if no filter is given
        for video_gui in gi.objs.channel()._videos:
            video_gui.black_out()
        result = self._menu.ent_flt.get()
        if result and result != _('Filter this view'):
            sh.log.append ('Commands.filter_view'
                          ,_('INFO')
                          ,_('Filter by "%s"') % result
                          )
            result = result.lower()
            for video_gui in gi.objs.channel()._videos:
                if video_gui in self._videos:
                    self._gvideo = video_gui
                    self._video  = self._videos[self._gvideo]
                    if result in self._video.model._search:
                        self._gvideo.red_out()
                else:
                    sh.log.append ('Commands.filter_view'
                                  ,_('WARNING')
                                  ,_('Wrong input data!')
                                  )
        else:
            sh.log.append ('Commands.filter_view'
                          ,_('INFO')
                          ,_('Nothing to do!')
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
        sg.bind (obj      = self._menu.parent
                ,bindings = ['<Control-h>','<Alt-h>']
                ,action   = self.history
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Shift-Delete>'
                ,action   = self.delete_selected
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Alt-c>'
                ,action   = self.show_new
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Alt-t>'
                ,action   = self.update_trending
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Alt-b>'
                ,action   = self.blank
                )
        # Menu: buttons
        self._menu.btn_upd.action = self.update_channels
        self._menu.btn_ytb.action = self.search_youtube
        self._menu.btn_flt.action = self.filter_view
        self._menu.btn_dld.action = self.download
        self._menu.btn_ply.action = self.play
        self._menu.btn_del.action = self.delete_selected
        # Menu: labels
        sg.bind (obj      = self._menu.ent_src
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.search_youtube
                )
        sg.bind (obj      = self._menu.ent_url
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.get_url
                )
        sg.bind (obj      = self._menu.ent_flt
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.filter_view
                )
        # Menu: checkboxes
        self._menu.chb_dat.widget.config(command=self.filter_by_date)
        
        # Menu: OptionMenus
        self._menu.opt_act.action = self.other
        self._menu.opt_dat.action = self.filter_by_date
        self._menu.opt_url.action = self.get_url
        self._menu.opt_day.reset (items   = self._days
                                 ,default = self._day
                                 ,action  = self.reset_date_filter
                                 )
        self._menu.opt_mth.reset (items   = self._months
                                 ,default = self._month
                                 ,action  = self.reset_date_filter
                                 )
        self._menu.opt_yrs.reset (items   = self._years
                                 ,default = self._year
                                 ,action  = self.reset_date_filter
                                 )
        self._menu.opt_trd.reset (items   = lg.objs.const()._trending
                                 ,default = _('Trending')
                                 ,action  = self.set_trending
                                 )
        self._menu.opt_chl.reset (items   = self._channels
                                 ,default = _('Channels')
                                 ,action  = self.set_channel
                                 )
        
    def select_new(self,event=None):
        for video_gui in gi.objs.channel()._videos:
            if video_gui in self._videos:
                self._gvideo = video_gui
                self._video  = self._videos[self._gvideo]
                # Drop all previous selections
                self._gvideo.cbox.disable()
                if self._menu.chb_dat.get():
                    cond = not self._video.model._dtime and \
                           not self._video.model.Block and \
                           self._date_filter()
                else:
                    cond = not self._video.model._dtime and \
                           not self._video.model.Block
                if cond:
                    self._gvideo.cbox.enable()
            else:
                sh.log.append ('Commands.select_new'
                              ,_('WARNING')
                              ,_('Wrong input data!')
                              )
        gi.report_selection()
        
    def _play_slow(self,app='/usr/bin/mplayer'):
        sh.Launch (target = self._video.model._path
                  ).app (custom_app  = app
                        ,custom_args = ['-ao','sdl','-fs'
                                       ,'-framedrop'
                                       ,'-nocorrect-pts'
                                       ]
                        )
                        
    def _play_default(self):
        sh.Launch(target=self._video.model._path).default()

    def play_video(self,event=None):
        if self._video:
            if self._menu.chb_slw.get():
                if os.path.exists('/usr/bin/mplayer'):
                    self._play_slow()
                elif os.path.exists('/usr/bin/mpv'):
                    self._play_slow(app='/usr/bin/mpv')
                else:
                    self._play_default()
            else:
                self._play_default()
        else:
            sh.log.append ('Commands.play_video'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def play(self,event=None):
        for video_gui in gi.objs.channel()._videos:
            if video_gui.cbox.get():
                if video_gui in self._videos:
                    self._gvideo = video_gui
                    self._video  = self._videos[self._gvideo]
                    self.download_video()
                    self.play_video()
                else:
                    sg.Message ('Commands.play'
                               ,_('ERROR')
                               ,_('Wrong input data!')
                               )
        gi.objs._progress.close()
        
    def mark_downloaded(self):
        self._video.model._dtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
        idb.mark_downloaded (video_id = self._video.model._video_id
                            ,dtime    = self._video.model._dtime
                            )
        if self._gvideo:
            self._gvideo.cbox.disable()
            self._gvideo.gray_out()
            gi.report_selection()
    
    def download_video(self,event=None):
        ''' In case of 'get_url', there is no GUI to be handled
            ('self._gvideo' must be set to 'None'), so we do not force
            'self._gvideo' check here.
        '''
        if self._video:
            self._video.model.video()
            self._video.model.path()
            if self._video.model._path:
                if os.path.exists(self._video.model._path):
                    ''' Lift videos up in history (update DTIME field)
                        even if they were already downloaded. However,
                        do not put this in the end because we do not
                        want to update failed downloads.
                    '''
                    self.mark_downloaded()
                else:
                    gi.objs.progress().add()
                    gi.objs._progress.show()
                    ''' Do not focus this widget since the user may do
                        some work in the background, and we do not want
                        to interrupt it. Just activate the window
                        without focusing so the user would see that
                        the program is downloading something.
                    '''
                    if self.FirstVideo:
                        sg.Geometry(parent=gi.objs._progress.obj).activate()
                        gi.objs._progress.obj.center()
                        self.FirstVideo = False
                    if self._video.model.download():
                        self.mark_downloaded()
            else:
                sh.log.append ('Commands.download_video'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Commands.download_video'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def download(self,event=None):
        new_videos = []
        for video_gui in gi.objs.channel()._videos:
            if video_gui.cbox.get():
                if video_gui in self._videos:
                    new_videos.append(video_gui)
                else:
                    sg.Message ('Commands.download'
                               ,_('ERROR')
                               ,_('Wrong input data!')
                               )
        for i in range(len(new_videos)):
            self._gvideo = new_videos[i]
            self._video  = self._videos[self._gvideo]
            gi.objs._progress.title (_('Download progress') \
                                     + ' (%d/%d)' % (i+1,len(new_videos))
                                    )
            self.download_video()
        gi.objs._progress.title()
        gi.objs._progress.close()
        
    def update_channels(self,event=None):
        # Update channels
        links    = []
        unknown  = []
        channels = lg.objs.lists()._subsc_urls
        sg.objs.waitbox().reset(func_title='Commands.update_channels')
        sg.objs._waitbox.obj.icon(gi.icon_path)
        sg.objs._waitbox.show()
        for i in range(len(channels)):
            message = _('Update channels (%d/%d)') % (i+1,len(channels))
            sg.objs._waitbox.reset (func_title = 'Commands.update_channels'
                                   ,message    = message
                                   )
            sg.objs._waitbox.update()
            channel = lg.Channel(url=channels[i])
            channel.run()
            links += channel._links
        sg.objs._waitbox.close()
        # Get new URLs
        sh.log.append ('Commands.update_channels'
                      ,_('DEBUG')
                      ,_('URLs in total: %d') % len(links)
                      )
        urls = idb.urls()
        unknown = [link for link in links if not link in urls]
        
        # Get metadata for new URLs
        if unknown:
            gi.objs.wait().show()
            for i in range(len(unknown)):
                gi.objs._wait.title (_('Get video info') \
                                     + ' (%d/%d)' % (i+1,len(unknown))
                                    )
                self._video = Video(video_id=unknown[i])
                self._video.model.video()
                self._video.model.assign_online()
                self._video.model.image()
                self._video.image()
                self._video.model.dump()
                author, title, duration = self.unsupported()
                gi.objs._wait.reset (author   = author
                                    ,title    = title
                                    ,duration = duration
                                    ,image    = self._video._image
                                    ,no       = i + 1
                                    )
                gi.objs._wait.update()
            idb.save()
            gi.objs._wait.title()
            gi.objs._wait.close()
            self._show_new(urls=unknown)
        else:
            sg.Message (func    = 'Commands.update_channels'
                       ,level   = _('INFO')
                       ,message = _('No new videos!')
                       )
        
    def update_trending(self,event=None,url=None):
        if not url:
            url = 'https://www.youtube.com/feed/trending?gl=RU'
        self._channel = lg.Channel(url=url)
        ''' We assume that there is no need to delete unsupported
            characters in countries.
        '''
        self._channel.run()
        self.reset_channel_gui()
        self.channel_gui()
        
    def reset_channel_gui(self):
        self._video = self._gvideo = None
        # Clears the old Channel widget
        for video_gui in gi.objs.channel()._videos:
            video_gui.frame.widget.pack_forget()
        gi.objs._channel._videos = []
        self._menu.title()
        
    def bind_context(self,event=None):
        for video_gui in gi.objs.channel()._videos:
            for obj in video_gui._objects:
                sg.bind (obj      = obj
                        ,bindings = '<ButtonRelease-3>'
                        ,action   = self.context
                        )
        
    def fill_default(self):
        #todo: Operation takes ~1,72s - speed this up (?)
        gi.objs.channel(parent=gi.objs.menu().framev)
        for i in range(len(self._channel._links)):
            gi.objs._channel.add(no=i)
            
    def dimensions(self):
        sg.objs.root().idle()
        height  = gi.objs._channel.label.widget.winfo_reqheight()
        ''' #NOTE: Extra space can be caused by a difference of
            the default and loaded pictures.
        '''
        #height = len(self._channel._links) * 112.133333333
        sh.log.append ('Commands.channel_gui'
                      ,_('DEBUG')
                      ,_('Widget must be at least %d pixels in height')\
                      % height
                      )
        gi.objs._channel.canvas.region (x        = 1024
                                       ,y        = height
                                       ,x_border = 20
                                       ,y_border = 20
                                       )
    
    def fill_unknown(self):
        unknown   = []
        unknown_g = []
        unknown_i = []
        for i in range(len(gi.objs.channel()._videos)):
            video_gui = gi.objs._channel._videos[i]
            if video_gui:
                if video_gui in self._videos:
                    video = self._videos[video_gui]
                    if not video.model.Saved:
                        unknown.append(video)
                        unknown_g.append(video_gui)
                        unknown_i.append(i)
                else:
                    sh.log.append ('Commands.fill_unknown'
                                  ,_('ERROR')
                                  ,_('Wrong input data!')
                                  )
            else:
                sh.log.append ('Commands.fill_unknown'
                              ,_('ERROR')
                              ,_('Empty input is not allowed!')
                              )
        if unknown:
            gi.objs.wait().show()
            for i in range(len(unknown)):
                gi.objs._wait.title (_('Get video info') \
                                     + ' (%d/%d)' % (i+1,len(unknown))
                                    )
                self._video  = unknown[i]
                self._gvideo = unknown_g[i]
                self._video.model.video()
                self._video.model.assign_online()
                self._video.model.image()
                self._video.image()
                self._video.model.dump()
                self.update_video(i=unknown_i[i])
                gi.objs._wait.reset (author   = self._gvideo._author
                                    ,title    = self._gvideo._title
                                    ,duration = self._gvideo._duration
                                    ,image    = self._video._image
                                    ,no       = unknown_i[i] + 1
                                    )
                gi.objs._wait.update()
            idb.save()
            gi.objs._wait.title()
            gi.objs._wait.close()
        else:
            sh.log.append ('Commands.fill_unknown'
                          ,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def unsupported(self):
        author   = sh.Text(text=self._video.model._author).delete_unsupported()
        title    = sh.Text(text=self._video.model._title).delete_unsupported()
        duration = sh.Text(text=self._video.model._dur).delete_unsupported()
        if author in lg.objs.lists()._block_auth \
        or self._video.model._author in lg.objs._lists._block_auth:
            author = title = _('BLOCKED')
            self._video._image = None
            self._video.model.Block = True
        return(author,title,duration)
    
    def update_video(self,i):
        if self._video:
            author, title, duration = self.unsupported()
            self._gvideo = gi.objs.channel()._videos[i]
            self._gvideo.reset (no       = i + 1
                               ,author   = author
                               ,title    = title
                               ,duration = duration
                               ,image    = self._video._image
                               )
            if self._video.model._dtime:
                self._gvideo.gray_out()
            self.video_date_filter()
        else:
            sh.log.append ('Commands.update_video'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def fill_known(self):
        for i in range(len(self._channel._links)):
            self._video = Video(video_id=self._channel._links[i])
            self._gvideo = gi.objs._channel._videos[i]
            self._videos[self._gvideo] = self._video
            self._video.model.Saved = idb.get_video(video_id=self._video.model._video_id)
            if self._video.model.Saved:
                self._video.model.assign_offline(self._video.model.Saved)
                #todo: elaborate 'Video.model.get' and delete this
                self._video.image()
                self.update_video(i)
    
    def channel_gui(self):
        self.fill_default()
        self.fill_known()
        ''' The less we use GUI update, the faster will be the program.
            Updating tkinter idle tasks may take ~0,4-1,7s, but this
            must be done after creating all video widgets and
            reading/updating images.
        '''
        sg.objs.root().idle()
        self.fill_unknown()
        self.bind_context()
        self.dimensions()
        gi.objs._channel.canvas.move_top()
        # Move focus away from 'ttk.Combobox' (OptionMenu)
        gi.objs._channel.canvas.focus()
    
    def manage_sub1(self):
        words = sh.Words(text=lg.objs.lists()._subsc)
        gi.objs.subscribe().reset(words=words)
        gi.objs._subscribe.insert(text=lg.objs._lists._subsc)
        gi.objs._subscribe.show()
        text = gi.objs._subscribe.get()
        if text:
            text = text.splitlines()
            text = sorted (text
                          ,key = lambda x:x[0].lower()
                          )
            text = '\n'.join(text)
            sh.WriteTextFile (file       = lg.objs._lists._fsubsc
                             ,AskRewrite = False
                             ).write(text=text)
        else:
            sh.log.append ('Commands.manage_sub1'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                             
    def manage_sub2(self):
        if os.path.exists(lg.objs.lists()._fsubsc2):
            words = sh.Words(text=lg.objs._lists._subsc2)
            gi.objs.subscribe().reset(words=words)
            gi.objs._subscribe.insert(text=lg.objs._lists._subsc2)
            gi.objs._subscribe.show()
            text = gi.objs._subscribe.get()
            if text:
                text = text.splitlines()
                text = sorted (text
                              ,key = lambda x:x[0].lower()
                              )
                text = '\n'.join(text)
                sh.WriteTextFile (file       = lg.objs._lists._fsubsc2
                                 ,AskRewrite = False
                                 ).write(text=text)
            else:
                sh.log.append ('Commands.manage_sub2'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Commands.manage_sub2'
                          ,_('INFO')
                          ,_('Nothing to do.')
                          )
    
    def manage_sub(self,event=None):
        self.manage_sub1()
        self.manage_sub2()
        lg.objs.lists().reset()
        self.reset_channels()
        
    def manage_block(self,event=None):
        words = sh.Words(text=lg.objs.lists()._block)
        gi.objs.blacklist().reset(words=words)
        gi.objs._blacklist.insert(text=lg.objs._lists._block)
        gi.objs._blacklist.show()
        text = gi.objs._blacklist.get()
        if text:
            text = text.splitlines()
            text = sorted (text
                          ,key = lambda x:x[0].lower()
                          )
            text = '\n'.join(text)
            sh.WriteTextFile (file       = lg.objs._lists._fblock
                             ,AskRewrite = False
                             ).write(text=text)
            lg.objs._lists.reset()
        else:
            sh.log.append ('Commands.manage_block'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )



# Requires idb
class Video:
    
    def __init__(self,video_id):
        self.model  = lg.Video (video_id = video_id
                               ,callback = self.progress
                               )
        self._image = None
        
    def progress (self,total=0,cur_size=0
                 ,ratio=0,rate=0,eta=0
                 ):
        total    = total    / 1000000
        cur_size = cur_size / 1000000
        
        percent = round((100*cur_size)/total)
        gi.objs.progress()._item.widget['value'] = percent
        
        total    = int(total)
        cur_size = int(cur_size)
        rate     = str(int(rate))
        eta      = str(int(eta))
        
        # Prevent from irritating message length changes
        rate = sh.Text(text=rate).grow (max_len = 4
                                       ,FromEnd = False
                                       )
        eta = sh.Text(text=eta).grow (max_len = 3
                                     ,FromEnd = False
                                     )
        gi.objs._progress._item.text (file     = self.model._pathsh
                                     ,cur_size = cur_size
                                     ,total    = total
                                     ,rate     = rate
                                     ,eta      = eta
                                     )
        # This is required to fill the progress bar on-the-fly
        sg.objs.root().widget.update_idletasks()
    
    def image(self):
        if self.model._bytes:
            img = sg.Image()
            img._bytes = self.model._bytes
            img.loader()
            self._image = img.image()
        else:
            sh.log.append ('Video.image'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def get(self):
        self.model.get()
        self.image()


if __name__ == '__main__':
    sg.objs.start()
    sg.Geometry(parent=gi.objs.parent()).set('1024x600')
    idb = lg.idb
    commands = Commands()
    commands.bindings()
    gi.objs.progress()
    gi.objs.menu().show()
    idb.save()
    idb.close()
    sg.objs.end()
