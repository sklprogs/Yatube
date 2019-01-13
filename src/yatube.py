#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import subprocess
import shared    as sh
import sharedGUI as sg
import logic     as lg
import gui       as gi
import meta      as mt

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')



class Watchlist:
    
    def fetch(self):
        lg.objs.watchlist().fetch()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._watchlist.get_token()
        objs._commands.update_widgets()
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Watchlist.fetch_prev'
        lg.objs.watchlist().fetch_prev()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._watchlist.get_token()
        objs._commands.update_widgets()
    
    def fetch_next(self):
        f = '[Yatube] yatube.Watchlist.fetch_next'
        lg.objs.watchlist().fetch_next()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._watchlist.get_token()
        objs._commands.update_widgets()



class Playlist:
    
    def __init__(self,play_id=''):
        self._play_id = ''
        if play_id:
            self.reset(play_id)
    
    def fetch(self):
        mt.objs.playlist().run()
        objs._commands.channel_gui()
        objs._commands.update_widgets()
    
    def fetch_prev(self):
        mt.objs.playlist().fetch_prev()
        mt.objs._playlist.videos()
        objs._commands.channel_gui()
        objs._commands.update_widgets()
    
    def fetch_next(self):
        mt.objs.playlist().fetch_next()
        mt.objs._playlist.videos()
        objs._commands.channel_gui()
        objs._commands.update_widgets()
    
    def reset(self,play_id):
        self._play_id = play_id
        mt.objs.playlist().reset(play_id)



class Channels:
    
    def __init__(self):
        self._channels = []
    
    def add_watchlist(self):
        watchlist = Watchlist()
        self._channels.append(watchlist)
    
    def add_history(self):
        history = History()
        self._channels.append(history)
    
    def add_playlist(self,play_id):
        playlist = Playlist(play_id)
        self._channels.append(playlist)
    
    def fetch(self):
        f = '[Yatube] yatube.Channels.fetch'
        if self._channels:
            timer = sh.Timer(f)
            timer.start()
            objs.commands().reset_channel_gui()
            mt.objs.videos().reset()
            self._channels[-1].fetch()
            timer.end()
        else:
            sh.com.empty(f)
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Channels.fetch_prev'
        if self._channels:
            timer = sh.Timer(f)
            timer.start()
            objs.commands().reset_channel_gui()
            mt.objs.videos().reset()
            self._channels[-1].fetch_prev()
            timer.end()
        else:
            sh.com.empty(f)
    
    def fetch_next(self):
        f = '[Yatube] yatube.Channels.fetch_next'
        if self._channels:
            timer = sh.Timer(f)
            timer.start()
            objs.commands().reset_channel_gui()
            mt.objs.videos().reset()
            self._channels[-1].fetch_next()
            timer.end()
        else:
            sh.com.empty(f)



class History:
    
    def fetch(self):
        lg.objs.history().fetch()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._history.get_token()
        objs._commands.update_widgets()
    
    def fetch_prev(self):
        f = '[Yatube] yatube.History.fetch_prev'
        lg.objs.history().fetch_prev()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._history.get_token()
        objs._commands.update_widgets()
    
    def fetch_next(self):
        f = '[Yatube] yatube.History.fetch_next'
        lg.objs.history().fetch_next()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._history.get_token()
        objs._commands.update_widgets()



class AddId:
    
    def __init__(self):
        self.values()
        self.gui = gi.AddId()
        self.bindings()
    
    def open(self,event=None):
        f = '[Yatube] yatube.AddId.open'
        author = self.gui.lst_id1.get()
        if author:
            ind     = self.gui.lst_id1.lst.index(author)
            ''' 'myid' will be a valid playlist ID since incorrect
                values are not added when using 'AddId'.
            '''
            myid    = self.gui.lst_id3.lst[ind]
            url     = 'https://www.youtube.com/playlist?list=%s' % myid
            ionline = sh.Online()
            ionline._url = url
            ionline.browse()
        else:
            sh.com.empty(f)
    
    def delete(self,event=None):
        f = '[Yatube] yatube.AddId.delete'
        author = self.gui.lst_id1.get()
        if author:
            ind = self.gui.lst_id1.lst.index(author)
            del self.gui.lst_id1.lst[ind]
            del self.gui.lst_id2.lst[ind]
            del self.gui.lst_id3.lst[ind]
            self.gui.lst_id1.reset(self.gui.lst_id1.lst)
            self.gui.lst_id2.reset(self.gui.lst_id2.lst)
            self.gui.lst_id3.reset(self.gui.lst_id3.lst)
        else:
            sh.com.empty(f)
    
    def values(self):
        self._author = ''
        self._id     = ''
    
    def add_record(self,mode='user'):
        f = '[Yatube] yatube.AddId.add_record'
        id1 = self.gui.lst_id1.lst
        id2 = self.gui.lst_id2.lst
        id3 = self.gui.lst_id3.lst
        if self._author in id1:
            sh.objs.mes (f,_('INFO')
                        ,_('"%s" is already in the list!') \
                        % self._author
                        )
        else:
            ind = len(id1)
            Success = True
            if mode == 'play_id':
                id3.insert(ind,self._id)
            elif mode == 'channel_id':
                mt.objs.playid().reset(self._id)
                result = mt.objs._playid.by_channel_id()
                if result:
                    id3.insert(ind,result)
                else:
                    Success = False
                    sh.com.empty(f)
            elif mode == 'user':
                mt.objs.playid().reset(self._id)
                result = mt.objs._playid.by_user()
                if result:
                    id3.insert(ind,result)
                else:
                    Success = False
                    sh.com.empty(f)
            else:
                Success = False
                sh.objs.mes (f,_('ERROR')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".')\
                            % (str(mode),'play_id; channel_id; user')
                            )
            if Success:
                id1.insert(ind,self._author)
                id2.insert(ind,self._id)
                self.gui.lst_id1.reset(id1)
                self.gui.lst_id2.reset(id2)
                self.gui.lst_id3.reset(id3)
                self.gui.ent_ath.clear_text()
                self.gui.ent_pid.clear_text()
                self.gui.ent_ath.focus()
            else:
                sh.com.cancel(f)
    
    def add(self,event=None):
        f = '[Yatube] yatube.AddId.add'
        self._author = self.gui.ent_ath.get()
        self._id     = self.gui.ent_pid.get()
        self._author = self._author.strip()
        self._id     = self._id.strip()
        if self._author and self._id:
            if self._id.startswith('UU') and len(self._id) == 24:
                self.add_record('play_id')
            elif self._id.startswith('UC') and len(self._id) == 24:
                self.add_record('channel_id')
            else:
                self.add_record('user')
        else:
            sh.com.empty(f)
    
    def edit(self,event=None):
        f = '[Yatube] yatube.AddId.edit'
        author = self.gui.lst_id1.get()
        ind    = self.gui.lst_id1.lst.index(author)
        pid    = self.gui.lst_id3.lst[ind]
        self.gui.ent_ath.clear_text()
        self.gui.ent_ath.insert(author)
        self.gui.ent_pid.clear_text()
        self.gui.ent_pid.insert(pid)
        self.delete()
    
    def bindings(self):
        self.gui.btn_add.action = self.add
        self.gui.btn_cls.action = self.close
        self.gui.btn_del.action = self.delete
        self.gui.btn_edt.action = self.edit
        self.gui.btn_opn.action = self.open
        self.gui.btn_rst.action = self.reset
        self.gui.btn_sav.action = self.save
        self.gui.widget.protocol("WM_DELETE_WINDOW",self.close)
        sg.bind (obj      = self.gui
                ,bindings = ['<Escape>','<Control-w>','<Control-q>']
                ,action   = self.close
                )
        sg.bind (obj      = self.gui.ent_ath
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.add
                )
        sg.bind (obj      = self.gui.ent_pid
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.add
                )
    
    def reset(self,event=None):
        lg.objs.lists().reset()
        self.fill()
    
    def save(self,event=None):
        id1 = self.gui.lst_id1.lst
        id3 = self.gui.lst_id3.lst
        if id1 and id3:
            tmp = []
            for i in range(len(id1)):
                tmp.append(id1[i] + '\t' + id3[i])
            text = '\n'.join(tmp)
        else:
            text = '# ' + _('Put here authors to subscribe to')
        sh.WriteTextFile (file    = lg.objs.default()._fsubsc
                         ,Rewrite = True
                         ).write(text)
        lg.objs._lists.reset()
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.save()
        self.gui.close()
        # Do not forget to run 'Commands.reset_channels' afterwards

    def fill(self):
        f = '[Yatube] yatube.AddId.fill'
        ''' Filling the second (empty) column with non-empty values
            prevents from inserting a new record at a wrong place.
        '''
        id1 = lg.objs.lists()._subsc_auth
        id2 = '?' * len(lg.objs._lists._subsc_auth)
        id3 = lg.objs._lists._subsc_ids
        if len(id1) == len(id2) == len(id3):
            pass
        else:
            sh.objs.mes (f,_('WARNING')
                        ,_('The condition "%s" is not observed!') \
                        % '%d = %d = %d' % (len(id1),len(id2),len(id3))
                        )
        self.gui.lst_id1.reset(lst=id1)
        self.gui.lst_id2.reset(lst=id2)
        self.gui.lst_id3.reset(lst=id3)



class Comments:
    
    def __init__(self):
        ''' Since comments are loaded partly, we should not rely
            on 'self.logic._texts'. We should also not rely on a total
            number of comments reported by 'VideoInfo' since there is
            no quota-efficient way to fetch all of these comments (some
            comments will eventually be missing, and a predicted number
            of screens will mismatch a factual number). Therefore, we
            should not show the number of comments in GUI at all.
        '''
        self.values()
        self.gui = gi.Comments()
        self.gui.close()
        self.logic = mt.Comments()
        self.bindings()
        self.reset()
    
    def values(self):
        self.Success = True
    
    def bindings(self):
        sg.bind (obj      = self.gui.parent
                ,bindings = '<Alt-Left>'
                ,action   = self.prev
                )
        sg.bind (obj      = self.gui.parent
                ,bindings = '<Alt-Right>'
                ,action   = self.next
                )
        sg.bind (obj      = self.gui.parent
                ,bindings = ['<Escape>','<Control-w>','<Control-q>']
                ,action   = self.close
                )
        sg.bind (obj      = self.gui.txt_com
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.next
                )
        self.gui.btn_prv.action = self.prev
        self.gui.btn_nxt.action = self.next
        self.gui.widget.protocol("WM_DELETE_WINDOW",self.close)
    
    def prev(self,event=None):
        f = '[Yatube] yatube.Comments.prev'
        if self.Success:
            self.logic.fetch_prev()
            self.update()
        else:
            sh.com.cancel(f)
    
    def next(self,event=None):
        f = '[Yatube] yatube.Comments.next'
        if self.Success:
            self.logic.fetch_next()
            self.update()
        else:
            sh.com.cancel(f)
    
    def reset(self):
        f = '[Yatube] yatube.Comments.reset'
        ''' We believe that the 'video_id' format should be checked
            earlier, so we don't verify it here.
        '''
        self.logic.reset()
        self.Success = self.logic.Success
        if self.Success:
            self.logic.fetch()
            self.update()
        else:
            sh.com.cancel(f)
    
    def update(self):
        self.update_text()
        self.update_buttons()
    
    def update_buttons(self):
        f = '[Yatube] yatube.Comments.update_buttons'
        if self.Success:
            if self.logic._texts:
                if self.logic.i == 0:
                    self.gui.btn_prv.inactive()
                elif self.logic.i > 0:
                    self.gui.btn_prv.active()
                if self.logic._next \
                or self.logic.i + 1 < len(self.logic._texts):
                    self.gui.btn_nxt.active()
                else:
                    self.gui.btn_nxt.inactive()
            else:
                self.gui.btn_prv.inactive()
                self.gui.btn_nxt.inactive()
        else:
            sh.com.cancel(f)
    
    def update_text(self):
        f = '[Yatube] yatube.Comments.update_text'
        if self.Success:
            try:
                text = self.logic._texts[self.logic.i]
            except IndexError:
                text = ''
                sh.objs.mes (f,_('WARNING')
                            ,_('Wrong input data!')
                            )
            text     = sh.Text(text).delete_unsupported()
            old_text = self.gui.txt_com.get()
            # A new line is inserted when read from the widget
            text = text.strip()
            old_text.strip()
            # Keep a scrollbar position if there are no pages left
            if old_text != text:
                self.gui.txt_com.read_only(False)
                self.gui.txt_com.reset()
                self.gui.txt_com.insert(text)
                self.gui.txt_com.read_only(True)
        else:
            sh.com.cancel(f)
        
    def show(self,event=None):
        f = '[Yatube] yatube.Comments.show'
        if self.Success:
            self.gui.show()
        else:
            sh.com.cancel(f)
    
    def close(self,event=None):
        f = '[Yatube] yatube.Comments.close'
        if self.Success:
            self.gui.close()
        else:
            sh.com.cancel(f)



class Commands:
    
    def __init__(self):
        self._mode      = None
        self._timestamp = None
        self.FirstVideo = True
        self._menu      = gi.objs.menu()
        itime           = lg.Time()
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
        lg.objs.lists().reset()
        self.reset_channels()
    
    def history(self,event=None):
        objs.channels().add_history()
        objs._channels.fetch()
    
    def update_context(self):
        f = '[Yatube] yatube.Commands.update_context'
        video = mt.objs.videos().current()
        if video:
            items = list(gi.context_items)
            data = lg.objs.db().get_video(video._id)
            if data:
                block = data[8]
                dtime = data[9]
                ftime = data[10]
                ltime = data[11]
                if dtime:
                    items.remove(_('Mark as watched'))
                else:
                    items.remove(_('Mark as not watched'))
                if ftime:
                    items.remove(_('Add to favorites'))
                else:
                    items.remove(_('Remove from favorites'))
                if ltime:
                    items.remove(_('Add to watchlist'))
                else:
                    items.remove(_('Remove from watchlist'))
                if block:
                    items.remove(_('Block this channel'))
                else:
                    items.remove(_('Unblock'))
            else:
                sh.com.empty(f)
            objs.video().logic.path()
            if video._path:
                if os.path.exists(video._path):
                    items.remove(_('Download'))
                else:
                    items.remove(_('Delete the downloaded file'))
            else:
                sh.com.empty(f)
            if video._author:
                if video._author in lg.objs.lists()._subsc_auth:
                    items.remove(_('Subscribe to this channel'))
                else:
                    items.remove(_('Unsubscribe'))
            else:
                sh.com.empty(f)
            return items
        else:
            sh.com.empty(f)
    
    def reload_channel(self,event=None):
        f = '[Yatube] yatube.Commands.reload_channel'
        sg.Message (f,_('INFO')
                   ,_('Not implemented yet!')
                   )
    
    def feed(self,event=None):
        f = '[Yatube] yatube.Commands.feed'
        urls = lg.objs.db().feed()
        if urls:
            #todo: rework
            #lg.objs.channel().reset(urls=urls)
            #lg.objs._channel.run()
            self.load_view()
        else:
            sh.com.empty(f)
    
    def prev_page(self,event=None):
        objs.channels().fetch_prev()
    
    def next_page(self,event=None):
        objs.channels().fetch_next()
    
    def watchlist(self,event=None):
        objs.channels().add_watchlist()
        objs._channels.fetch()
    
    def starred(self,event=None):
        f = '[Yatube] yatube.Commands.starred'
        urls = lg.objs.db().starred()
        if urls:
            #todo: rework
            #lg.objs.channel().reset(urls=urls)
            #lg.objs._channel.run()
            self.load_view()
        else:
            # Do not warn here since this is actually a common case
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def remove_from_watchlist(self,event=None):
        f = '[Yatube] yatube.Commands.remove_from_watchlist'
        lg.objs.db().mark_later (video_id = mt.objs.videos().current()._id
                                ,ltime    = 0
                                )
        self.unselect()
    
    def add2watchlist(self,event=None):
        f = '[Yatube] yatube.Commands.add2watchlist'
        lg.objs.db().mark_later (video_id = mt.objs.videos().current()._id
                                ,ltime    = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
                                )
        self.unselect()
    
    def sel_add2watchlist(self,event=None):
        f = '[Yatube] yatube.Commands.sel_add2watchlist'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                mt.objs.videos().set_gui(video_gui)
                self.add2watchlist()
        else:
            sh.com.empty(f)
    
    def sel_remove_from_watchlist(self,event=None):
        f = '[Yatube] yatube.Commands.sel_remove_from_watchlist'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                if mt.objs.videos().set_gui(video_gui):
                    self.remove_from_watchlist()
                else:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Wrong input data!')
                                )
        else:
            sh.com.empty(f)
    
    def unselect(self,event=None):
        f = '[Yatube] yatube.Commands.unselect'
        gui = mt.objs.videos().current()._gui
        if gui:
            gui.cbox.disable()
            gi.report_selection()
        else:
            sh.com.empty(f)
    
    def sel_unstar(self,event=None):
        f = '[Yatube] yatube.Commands.sel_unstar'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                if mt.objs.videos().set_gui(video_gui):
                    self.unstar()
                else:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Wrong input data!')
                                )
        else:
            sh.com.empty(f)
    
    def unstar(self,event=None):
        f = '[Yatube] yatube.Commands.unstar'
        lg.objs.db().mark_starred (video_id = mt.objs.videos().current()._id
                                  ,ftime    = 0
                                  )
        self.unselect()
    
    def star(self,event=None):
        f = '[Yatube] yatube.Commands.star'
        lg.objs.db().mark_starred (video_id = mt.objs.videos().current()._id
                                  ,ftime    = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
                                  )
        self.unselect()
            
    def sel_star(self,event=None):
        f = '[Yatube] yatube.Commands.sel_star'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                if mt.objs.videos().set_gui(video_gui):
                    self.star()
                else:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Wrong input data!')
                                )
        else:
            sh.com.empty(f)
    
    def sel_mark_not_watched(self,event=None):
        f = '[Yatube] yatube.Commands.sel_mark_not_watched'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                if mt.objs.videos().set_gui(video_gui):
                    self.mark_not_watched()
                else:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Wrong input data!')
                                )
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def sel_mark_watched(self,event=None):
        f = '[Yatube] yatube.Commands.sel_mark_watched'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                if mt.objs.videos().set_gui(video_gui):
                    self.mark_watched()
                else:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Wrong input data!')
                                )
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def mark_not_watched(self,event=None):
        f = '[Yatube] yatube.Commands.mark_not_watched'
        video = mt.objs.videos().current()
        gui   = video._gui
        if gui:
            video._dtime = 0
            lg.objs.db().mark_downloaded (video_id = video._id
                                         ,dtime    = video._dtime
                                         )
            gui.black_out()
            self.unselect()
        else:
            sh.com.empty(f)
    
    def mark_watched(self,event=None):
        f = '[Yatube] yatube.Commands.mark_watched'
        video = mt.objs.videos().current()
        gui   = video._gui
        if gui:
            video._dtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
            lg.objs.db().mark_downloaded (video_id = video._id
                                         ,dtime    = video._dtime
                                         )
            gui.gray_out()
            self.unselect()
        else:
            sh.com.empty(f)
    
    def selection(self,event=None):
        f = '[Yatube] yatube.Commands.selection'
        selected = []
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        for gui in guis:
            if gui.cbox.get():
                selected.append(gui)
        return selected
    
    def load_view(self):
        self.channel_gui()
        self.update_widgets()
        #todo: where we should place this?
        #self.save_extra()
    
    def set_max_videos(self,event=None):
        f = '[Yatube] yatube.Commands.set_max_videos'
        if str(self._menu.opt_max.choice).isdigit():
            mt.MAX_VIDEOS = int(self._menu.opt_max.choice)
        else:
            sh.objs.mes (f,_('ERROR')
                        ,_('Wrong input data: "%s"') \
                        % str(self._menu.opt_max.choice)
                        )
        self.load_view()
    
    def tooltips(self):
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        for gui in guis:
            if len(gui._title) > 60:
                sg.ToolTip (obj        = gui.frame
                           ,text       = gui._title
                           ,hint_width = 900
                           ,hint_dir   = 'top'
                           ,hint_font  = 'Serif 10'
                           )
    
    def update_buttons(self,event=None):
        #todo: implement
        pass
            
    def update_widgets(self,event=None):
        self.update_buttons()
    
    def save_url(self,event=None):
        f = '[Yatube] yatube.Commands.save_url'
        #todo: rework
        lg.objs.channels().add (author = self._menu.opt_chl.choice
                               ,urls   = lg.objs.channel()._ids
                               )
    
    def prev_url(self,event=None):
        f = '[Yatube] yatube.Commands.prev_url'
        result = lg.objs.channels().prev()
        if result:
            #todo: implement
            pass
        else:
            sh.com.empty(f)
    
    def next_url(self,event=None):
        f = '[Yatube] yatube.Commands.next_url'
        result = lg.objs.channels().next()
        if result:
            #todo: implement
            pass
        else:
            sh.com.empty(f)
    
    def show_comments(self,event=None):
        f = '[Yatube] yatube.Commands.show_comments'
        objs.comments().reset()
        objs._comments.show()
    
    def menu_update(self,event=None):
        f = '[Yatube] yatube.Commands.menu_update'
        default = _('Update')
        choice  = self._menu.opt_upd.choice
        if choice == default:
            pass
        elif choice == _('Subscriptions'):
            self._menu.opt_upd.set(default)
            self.update_channels()
        elif choice == _('Links'):
            self._menu.opt_upd.set(default)
            self.reload_channel()
        else:
            sh.objs.mes (f,_('ERROR')
                        ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                        % (str(choice),';'.join(gi.update_items))
                        )
    
    def menu_view(self,event=None):
        f = '[Yatube] yatube.Commands.menu_view'
        default = _('View')
        choice  = self._menu.opt_viw.choice
        if choice == default:
            pass
        elif choice == _('History'):
            self._menu.opt_viw.set(default)
            self.history()
        elif choice == _('All feed'):
            self._menu.opt_viw.set(default)
            self.feed()
        elif choice == _('Subscriptions'):
            self._menu.opt_viw.set(default)
            self.show_new()
        elif choice == _('Favorites'):
            self._menu.opt_viw.set(default)
            self.starred()
        elif choice == _('Watchlist'):
            self._menu.opt_viw.set(default)
            self.watchlist()
        elif choice == _('Welcome screen'):
            self._menu.opt_viw.set(default)
            self.blank()
        else:
            sh.objs.mes (f,_('ERROR')
                        ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                        % (str(choice),';'.join(gi.view_items))
                        )
    
    def menu_edit(self,event=None):
        f = '[Yatube] yatube.Commands.menu_edit'
        default = _('Edit')
        choice  = self._menu.opt_edt.choice
        if choice == default:
            pass
        elif choice == _('Subscriptions'):
            self._menu.opt_edt.set(default)
            self.manage_sub()
        elif choice == _('Blocked authors'):
            self._menu.opt_edt.set(default)
            self.manage_blocked_authors()
        elif choice == _('Blocked words'):
            self._menu.opt_edt.set(default)
            self.manage_blocked_words()
        else:
            sh.objs.mes (f,_('ERROR')
                        ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                        % (str(choice),';'.join(gi.edit_items))
                        )
    
    def menu_selection(self,event=None):
        f = '[Yatube] yatube.Commands.menu_selection'
        default = _('Selection')
        choice  = self._menu.opt_sel.choice
        if choice == default:
            pass
        elif choice == _('Select all new videos'):
            self._menu.opt_sel.set(default)
            self.select_new()
        elif choice == _('Mark as watched'):
            self._menu.opt_sel.set(default)
            self.sel_mark_watched()
        elif choice == _('Mark as not watched'):
            self._menu.opt_sel.set(default)
            self.sel_mark_not_watched()
        elif choice == _('Add to favorites'):
            self._menu.opt_sel.set(default)
            self.sel_star()
        elif choice == _('Remove from favorites'):
            self._menu.opt_sel.set(default)
            self.sel_unstar()
        elif choice == _('Delete selected'):
            self._menu.opt_sel.set(default)
            self.delete_selected()
        elif choice == _('Add to watchlist'):
            self._menu.opt_sel.set(default)
            self.sel_add2watchlist()
        elif choice == _('Remove from watchlist'):
            self._menu.opt_sel.set(default)
            self.sel_remove_from_watchlist()
        else:
            sh.objs.mes (f,_('ERROR')
                        ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                        % (str(choice),';'.join(gi.selection_items))
                        )
    
    def blank(self,event=None):
        # 'lg.objs.channel().reset' requires non-empty values at input
        self.reset_channel_gui()
        lg.objs.channel().values()
        lg.objs.channels().reset()
        mt.objs.videos().reset()
        self._menu.clear_search(Force=True)
        self._menu.clear_url()
        self._menu.clear_filter(Force=True)
        gi.objs.parent().focus()
        self._menu.opt_chl.set(_('Channels'))
        self._menu.opt_trd.set(_('Trending'))
        gi.objs.channel().canvas.move_top()
        self.update_widgets()
    
    def unsubscribe(self,event=None):
        f = '[Yatube] yatube.Commands.unsubscribe'
        video = mt.objs.videos().current()
        if video._author:
            if video._author in lg.objs.lists()._subsc_auth:
                sh.log.append (f,_('INFO')
                              ,_('Unsubscribe from channel "%s"') \
                              % video._author
                              )
                if video._author in lg.objs._lists._subsc_auth:
                    ind = lg.objs._lists._subsc_auth.index(video._author)
                    del lg.objs._lists._subsc_auth[ind]
                    del lg.objs._lists._subsc_ids[ind]
                    subscriptions = []
                    for i in range(len(lg.objs._lists._subsc_auth)):
                        subscriptions.append (lg.objs._lists._subsc_auth[i]\
                                             + '\t' \
                                             + lg.objs._lists._subsc_ids[i]
                                             )
                    subscriptions = '\n'.join(subscriptions)
                    if not subscriptions:
                        subscriptions = '# ' + _('Put here authors to subscribe to')
                    sh.WriteTextFile (file    = lg.objs.default()._fsubsc
                                     ,Rewrite = True
                                     ).write(text=subscriptions)
                    lg.objs._lists.reset()
                    self.reset_channels()
            else:
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
        else:
            sh.com.empty(f)
    
    def unblock(self,event=None):
        f = '[Yatube] yatube.Commands.unblock'
        video = mt.objs.videos().current()
        if video._author:
            if video._author in lg.objs.lists()._block_auth:
                sh.log.append (f,_('INFO')
                              ,_('Unblock channel "%s"') % video._author
                              )
                lg.objs._lists._block_auth.remove(video._author)
                blocked = lg.objs._lists._block_auth
                blocked = '\n'.join(blocked)
                if not blocked:
                    blocked = '# ' + _('Put here authors to be blocked')
                sh.WriteTextFile (file    = lg.objs.default()._fblock
                                 ,Rewrite = True
                                 ).write(text=blocked)
                lg.objs._lists.reset()
                self.reset_channels()
            else:
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
        else:
            sh.com.empty(f)
    
    def show_new(self,event=None):
        f = '[Yatube] yatube.Commands.show_new'
        itime = sh.Time(pattern='%Y-%m-%d %H:%M:%S')
        itime.add_days(days_delta=-3)
        urls = lg.objs.db().new_videos (timestamp = itime.timestamp()
                                       ,authors   = lg.objs.lists()._subsc_auth
                                       )
        if urls:
            lg.objs.channel().reset(urls=urls)
            lg.objs._channel.run()
            self.load_view()
        else:
            # Do not warn here since this is actually a common case
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    # GUI-only
    def delete_selected(self,event=None):
        f = '[Yatube] yatube.Commands.delete_selected'
        selection = self.selection()
        if selection:
            for gui in selection:
                mt.objs.videos().set_gui(gui)
                self.delete_video()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def delete_video(self,event=None):
        f = '[Yatube] yatube.Commands.delete_video'
        ''' Do not warn when the GUI object is not available (e.g.,
            performing deletion through OptionMenu.
        '''
        if mt.objs.videos().current()._gui:
            ''' We probably want to disable the checkbox even when
                the file was not removed, e.g., the user selected all
                videos on the channel and pressed 'Shift-Del'.
            '''
            mt.objs._videos.current()._gui.cbox.disable()
            gi.report_selection()
        return objs.video().logic.delete()
    
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
        f = '[Yatube] yatube.Commands.open_video_url'
        url = objs.video().logic.url()
        if url:
            lg.objs.online()._url = url
            lg.objs._online.browse()
        else:
            sh.com.empty(f)
                   
    def copy_video_url(self,event=None):
        f = '[Yatube] yatube.Commands.copy_video_url'
        url = objs.video().logic.url()
        if url:
            sg.Clipboard().copy(text=url)
        else:
            sh.com.empty(f)
    
    def subscribe(self,event=None):
        f = '[Yatube] yatube.Commands.subscribe'
        video = mt.objs.videos().current()
        if video._author and video._play_id:
            if video._author in lg.objs.lists()._subsc_auth:
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
            else:
                sh.log.append (f,_('INFO')
                              ,_('Subscribe to channel "%s"') \
                              % video._author
                              )
                subscriptions = []
                for i in range(len(lg.objs._lists._subsc_auth)):
                    subscriptions.append (lg.objs._lists._subsc_auth[i]\
                                         + '\t' \
                                         + lg.objs._lists._subsc_ids[i]
                                         )
                    subscriptions.append (video._author + '\t' \
                                         + video._play_id
                                         )
                    subscriptions = sorted (subscriptions
                                           ,key=lambda x:x[0].lower()
                                           )
                    subscriptions = '\n'.join(subscriptions)
                    if subscriptions:
                        sh.WriteTextFile (file    = lg.objs.default()._fsubsc
                                         ,Rewrite = True
                                         ).write(text=subscriptions)
                        lg.objs._lists.reset()
                        self.reset_channels()
                    else:
                        sh.com.empty(f)
        else:
            sh.com.empty(f)
    
    def block_channel(self,event=None):
        f = '[Yatube] yatube.Commands.block_channel'
        video = mt.objs.videos().current()
        if video._play_id:
            if video._author:
                if video._author in lg.objs.lists()._block_auth:
                    sh.log.append (f,_('INFO')
                                  ,_('Nothing to do!')
                                  )
                else:
                    sh.log.append (f,_('INFO')
                                  ,_('Block channel "%s"') \
                                  % video._author
                                  )
                    lg.objs._lists._block_auth.append(video._author)
                    blocked = lg.objs._lists._block_auth
                    blocked = sorted (blocked
                                     ,key=lambda x:x[0].lower()
                                     )
                    blocked = '\n'.join(blocked)
                    if blocked:
                        sh.WriteTextFile (file    = lg.objs.default()._fblock
                                         ,Rewrite = True
                                         ).write(text=blocked)
                        lg.objs._lists.reset()
                        self.reset_channels()
                    else:
                        sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)
                   
    def load_channel(self,event=None):
        f = '[Yatube] yatube.Commands.load_channel'
        if mt.objs.videos().current()._play_id:
            lg.objs.channel().reset(url=mt.objs._videos.current()._play_id)
            lg.objs._channel.run()
            self.load_view()
        else:
            sh.com.empty(f)
    
    def open_channel_url(self,event=None):
        f = '[Yatube] yatube.Commands.open_channel_url'
        url = objs.video().logic.channel_url()
        if url:
            lg.objs.online()._url = url
            lg.objs._online.browse()
        else:
            sh.com.empty(f)

    def copy_channel_url(self,event=None):
        f = '[Yatube] yatube.Commands.copy_channel_url'
        url = objs.video().logic.channel_url()
        if url:
            sg.Clipboard().copy(url)
        else:
            sh.com.empty(f)
    
    def stream(self,event=None):
        f = '[Yatube] yatube.Commands.stream'
        selection = self.selection()
        if selection:
            mt.objs.videos().set_gui(selection[0])
            self.stream_video()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def stream_video(self,event=None):
        f = '[Yatube] yatube.Commands.stream_video'
        url = objs.video().logic.stream()
        if url:
            ''' Consider using newer python/OS builds if you have
                SSL/TLS problems here.
            '''
            if os.path.exists('/usr/bin/mpv'):
                app = '/usr/bin/mpv'
            elif os.path.exists('/usr/bin/vlc'):
                app = '/usr/bin/vlc'
            elif os.path.exists('/usr/bin/mplayer'):
                app = '/usr/bin/mplayer'
            else:
                app = ''
                sh.objs.mes (f,_('WARNING')
                            ,_('Unable to find a suitable application!')
                            )
            if app:
                if self._menu.chb_slw.get():
                    args = self._stream_slow(app)
                else:
                    args = self._stream(app)
                if args:
                    custom_args = [app] + args + [url]
                else:
                    custom_args = [app,url]
                #'sh.Launch' checks the target
                try:
                    subprocess.Popen(custom_args)
                    Success = True
                except:
                    sh.objs.mes (f,_('ERROR')
                                ,_('Failed to run "%s"!') \
                                % str(custom_args)
                                )
                    Success = False
                if Success:
                    self.mark_downloaded()
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)
    
    def _stream_slow(self,app):
        if 'mpv' in app:
            return ['-ao','sdl','-fs','-framedrop=vo'
                   ,'-cache','8192','--cache-initial','1024'
                   ,'--no-correct-pts'
                   ]
        elif 'mplayer' in app:
            return ['-ao','sdl','-fs','-framedrop'
                   ,'-cache','8192','-cache-min','50'
                   ,'-nocorrect-pts'
                   ]
    
    def _stream(self,app):
        if 'mpv' in app:
            return ['-cache','8192','--cache-initial','1024']
        elif 'mplayer' in app:
            return ['-cache','8192','-cache-min','50']
                   
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
        cond1 = mt.objs.videos().current()._ptime >= self.timestamp()
        cond2 = self._menu.opt_dat.choice == _('Newer than')
        if (cond1 and cond2) or (not cond1 and not cond2):
            return True
    
    def video_date_filter(self,event=None):
        ''' 'filter_by_date' uses the loop to filter videos by date upon
            event (changing filter date or filter settings).
            'video_date_filter' is used to mark a suitable video
            immediately when loading a channel.
            '_date_filter' is used by both methods (+'select_new') and
            should not be called externally in other cases.
            '''
        f = '[Yatube] yatube.Commands.video_date_filter'
        video = mt.objs.videos().current()
        if video._gui and video._ptime:
            if self._menu.chb_dat.get():
                if self._date_filter():
                    video._gui.red_out()
        else:
            sh.com.empty(f)
    
    def filter_by_date(self,event=None):
        f = '[Yatube] yatube.Commands.filter_by_date'
        # Do not allow to update channel GUI when no channels are loaded
        if gi.objs._channel:
            guis = [video._gui for video in mt.objs.videos()._videos \
                    if video._gui
                   ]
            for gui in guis:
                gui.black_out()
            if self._menu.chb_dat.get():
                timestamp = self.timestamp()
                for gui in guis:
                    mt.objs.videos().set_gui(gui)
                    if self._date_filter():
                        gui.red_out()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do.')
                          )
    
    def get_widget(self,event=None):
        f = '[Yatube] yatube.Commands.get_widget'
        if event:
            ''' Widgets must be in a string format to be compared
                (otherwise, we will have, for example,
                'Tkinter.Frame object' vs 'string').
                For some reason, Tkinter adds some information to
                the address of the widget got as 'event.widget'
                (original widget address will be shorter)
            '''
            guis = [video._gui for video in mt.objs.videos()._videos \
                    if video._gui
                   ]
            for gui in guis:
                for obj in gui._objects:
                    if str(obj.widget) in str(event.widget):
                        return gui
        else:
            sh.com.empty(f)
    
    def summary(self,event=None):
        f = '[Yatube] yatube.Commands.summary'
        if mt.objs.videos().current()._id:
            #self.save_extra()
            gi.objs.summary().reset()
            gi.objs._summary.insert(objs.video().logic.summary())
            gi.objs._summary.show()
        else:
            sh.com.empty(f)
    
    def _context(self,choice,event=None):
        f = '[Yatube] yatube.Commands._context'
        if choice:
            url = objs.video().logic.url()
            if choice == _('Show the full summary'):
                self.summary()
            elif choice == _('Download'):
                self.download_video()
            elif choice == _('Play'):
                self.download_video()
                self.play_video()
            elif choice == _('Stream'):
                self.stream_video()
            elif choice == _('Mark as watched'):
                self.mark_watched()
            elif choice == _('Mark as not watched'):
                self.mark_not_watched()
            elif choice == _('Add to favorites'):
                self.star()
            elif choice == _('Remove from favorites'):
                self.unstar()
            elif choice == _('Add to watchlist'):
                self.add2watchlist()
            elif choice == _('Remove from watchlist'):
                self.remove_from_watchlist()
            elif choice == _('Delete the downloaded file'):
                self.delete_video()
            elif choice == _('Extract links'):
                if url:
                    self.get_links(url)
                else:
                    sh.com.empty(f)
            elif choice == _('Load this channel'):
                self.load_channel()
            elif choice == _('Block this channel'):
                self.block_channel()
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
                sh.objs.mes (f,_('ERROR')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                            % (str(choice),';'.join(gi.context_items))
                            )
        else:
            sh.com.empty(f)
    
    def context(self,event=None):
        f = '[Yatube] yatube.Commands.context'
        # 'event' will be 'tuple' if it is a callback from 'Button.click'
        if isinstance(event,tuple):
            event = event[0]
        gui = self.get_widget(event=event)
        if gui:
            mt.objs.videos().set_gui(gui)
            message = _('Video #%d:') % gui._no
            gi.objs.context().title(message)
            items = self.update_context()
            if not items:
                items = gi.context_items
            gi.objs._context.reset(lst=items)
            gi.objs._context.show()
            choice = gi.objs._context._get
            self._context(choice)
        else:
            sh.com.empty(f)
    
    def update_channel(self,author,play_id):
        f = '[Yatube] logic.Commands.update_channel'
        timer = sh.Timer(f)
        timer.start()
        # We need to delete GUI before resetting logic
        self.reset_channel_gui()
        if author:
            self._menu.opt_chl.set(author)
        lg.objs.channel().reset(play_id)
        lg.objs._channel.run()
        self.load_view()
        timer.end()
        
    def get_links(self,url):
        lg.objs.extractor().reset(url=url)
        lg.objs._extractor.run()
        self.load_view()
                          
    def set_channel(self,event=None):
        f = '[Yatube] yatube.Commands.set_channel'
        if self._menu.opt_chl.choice == _('Channels'):
            self.show_new()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Switch to channel "%s"') \
                          % str(self._menu.opt_chl.choice)
                          )
            if self._menu.opt_chl.choice in lg.objs.lists()._subsc_auth:
                author  = self._menu.opt_chl.choice
                no      = lg.objs._lists._subsc_auth.index(author)
                play_id = lg.objs._lists._subsc_ids[no]
                objs.channels().add_playlist(play_id)
                objs._channels.fetch()
            else:
                sh.objs.mes (f,_('ERROR')
                            ,_('Wrong input data: "%s"') \
                            % str(self._menu.opt_chl.choice)
                            )
        
    def get_url(self,event=None):
        f = '[Yatube] yatube.Commands.get_url'
        result = self._menu.ent_url.get()
        if result:
            if result == _('Paste URL here'):
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
            elif self._menu.opt_url.choice in gi.url_items:
                if self._menu.opt_url.choice == _('Extract links'):
                    self.get_links(url=result)
                else:
                    video = Video()
                    video._id = lg.URL(result).video_id()
                    mt.objs.videos().add(video)
                    mt.objs._videos.i = len(mt.objs._videos._videos) - 1
                    objs.video().get()
                    if objs._video.logic.Success:
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
                            self.stream_video()
                        elif self._menu.opt_url.choice == _('Delete'):
                            self.delete_video()
                            self._menu.clear_url()
                        elif self._menu.opt_url.choice == _('Full menu'):
                            gi.objs.context().title(_('Selected video'))
                            gi.objs._context.show()
                            choice = gi.objs._context._get
                            self._context(choice)
                    else:
                        sh.com.cancel(f)
            else:
                sh.objs.mes (f,_('WARNING')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                            % (str(self._menu.opt_url.choice)
                              ,';'.join(gi.url_items)
                              )
                            )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def set_trending(self,event=None):
        f = '[Yatube] yatube.Commands.set_trending'
        sh.log.append (f,_('INFO')
                      ,_('Switch to channel "%s"') \
                      % str(self._menu.opt_trd.choice)
                      )
        if self._menu.opt_trd.choice in lg.objs.const()._countries:
            country = lg.objs._const._countries[self._menu.opt_trd.choice]
        else:
            country = 'RU'
        url = 'https://www.youtube.com/feed/trending?gl=%s' % country
        sh.log.append (f,_('DEBUG')
                      ,country
                      )
        sh.log.append (f,_('DEBUG')
                      ,url
                      )
        self.update_trending(url=url)
        
    def search_youtube(self,event=None):
        f = '[Yatube] yatube.Commands.search_youtube'
        result = self._menu.ent_src.get()
        if result and result != _('Search Youtube'):
            root_url = 'https://www.youtube.com/results?search_query=%s'
            result = sh.Online (base_str   = root_url
                               ,search_str = result
                               ,MTSpecific = False
                               ).url()
            self.get_links(url=result)
        else:
            sh.com.empty(f)
                          
    def filter_view(self,event=None):
        f = '[Yatube] yatube.Commands.filter_view'
        # Remove previous filter; drop selection if no filter is given
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        for gui in guis:
            gui.black_out()
        result = self._menu.ent_flt.get()
        if result and result != _('Filter this view'):
            sh.log.append (f,_('INFO')
                          ,_('Filter by "%s"') % result
                          )
            result = result.lower()
            for gui in guis:
                mt.objs._videos.set_gui(gui)
                if result in mt.objs._videos.current()._search:
                    gui.red_out()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def bindings(self):
        # Menu: main window
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Alt-Left>'
                ,action   = self.prev_page
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Alt-Right>'
                ,action   = self.next_page
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Control-Left>'
                ,action   = self.prev_url
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Control-Right>'
                ,action   = self.next_url
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Control-p>'
                ,action   = self.play
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Control-d>'
                ,action   = self.download
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Control-s>'
                ,action   = self.stream
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = ['<Control-h>','<Alt-h>']
                ,action   = self.history
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Alt-w>'
                ,action   = self.watchlist
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Alt-f>'
                ,action   = self.starred
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
        self._menu.btn_del.action = self.delete_selected
        self._menu.btn_dld.action = self.download
        self._menu.btn_flt.action = self.filter_view
        self._menu.btn_npg.action = self.next_page
        self._menu.btn_nxt.action = self.next_url
        self._menu.btn_ply.action = self.play
        self._menu.btn_ppg.action = self.prev_page
        self._menu.btn_prv.action = self.prev_url
        self._menu.btn_stm.action = self.stream
        self._menu.btn_ytb.action = self.search_youtube
        # Menu: labels
        sg.bind (obj      = self._menu.ent_flt
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.filter_view
                )
        sg.bind (obj      = self._menu.ent_src
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.search_youtube
                )
        sg.bind (obj      = self._menu.ent_url
                ,bindings = ['<Return>','<KP_Enter>']
                ,action   = self.get_url
                )
        # Menu: checkboxes
        self._menu.chb_dat.widget.config(command=self.filter_by_date)
        
        # Menu: OptionMenus
        self._menu.opt_upd.action = self.menu_update
        self._menu.opt_viw.action = self.menu_view
        self._menu.opt_sel.action = self.menu_selection
        self._menu.opt_edt.action = self.menu_edit
        self._menu.opt_chl.reset (items   = self._channels
                                 ,default = _('Channels')
                                 ,action  = self.set_channel
                                 )
        self._menu.opt_dat.action = self.filter_by_date
        self._menu.opt_day.reset (items   = self._days
                                 ,default = self._day
                                 ,action  = self.reset_date_filter
                                 )
        self._menu.opt_max.action = self.set_max_videos
        self._menu.opt_mth.reset (items   = self._months
                                 ,default = self._month
                                 ,action  = self.reset_date_filter
                                 )
        self._menu.opt_trd.reset (items   = lg.objs.const()._trending
                                 ,default = _('Trending')
                                 ,action  = self.set_trending
                                 )
        self._menu.opt_url.action = self.get_url
        self._menu.opt_yrs.reset (items   = self._years
                                 ,default = self._year
                                 ,action  = self.reset_date_filter
                                 )
        
    def select_new(self,event=None):
        f = '[Yatube] yatube.Commands.select_new'
        video = mt.objs.videos().current()
        guis  = [video._gui for video in mt.objs._videos._videos \
                 if video._gui
                ]
        for gui in guis:
            mt.objs._videos.set_gui(gui)
            # Drop all previous selections
            gui.cbox.disable()
            if self._menu.chb_dat.get():
                cond = not video._dtime and not video.Block and \
                       self._date_filter()
            else:
                cond = not video._dtime and not video.Block
                if cond:
                    gui.cbox.enable()
        gi.report_selection()
        
    def _play_slow(self,app='/usr/bin/mpv'):
        if 'mpv' in app:
            custom_args = ['-ao','sdl','-fs','-framedrop=vo'
                          ,'--no-correct-pts'
                          ]
        elif 'mplayer' in app:
            custom_args = ['-ao','sdl','-fs','-framedrop'
                          ,'-nocorrect-pts'
                          ]
        else:
            custom_args = []
        sh.Launch (target = objs.video().logic._path
                  ).app (custom_app  = app
                        ,custom_args = custom_args
                        )
                        
    def _play_default(self):
        sh.Launch(target=objs.video().logic._path).default()

    def play_video(self,event=None):
        f = '[Yatube] yatube.Commands.play_video'
        if mt.objs.videos().current()._id:
            if self._menu.chb_slw.get():
                if os.path.exists('/usr/bin/mpv'):
                    self._play_slow()
                elif os.path.exists('/usr/bin/mplayer'):
                    self._play_slow(app='/usr/bin/mplayer')
                else:
                    self._play_default()
            else:
                self._play_default()
        else:
            sh.com.empty(f)
    
    def play(self,event=None):
        f = '[Yatube] yatube.Commands.play'
        selection = self.selection()
        if selection:
            # Download all videos, play the first one only
            for i in range(len(selection)):
                mt.objs.videos().set_gui(selection[i])
                gi.objs.progress().title (_('Download progress') \
                                         + ' (%d/%d)' % (i + 1
                                                        ,len(selection)
                                                        )
                                         )
                self.download_video()
                if i == 0:
                    self.play_video()
            gi.objs._progress.title()
            gi.objs._progress.close()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
        
    def mark_downloaded(self):
        f = '[Yatube] yatube.Commands.mark_downloaded'
        video = mt.objs.videos().current()
        video._dtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
        lg.objs.db().mark_downloaded (video_id = video._id
                                     ,dtime    = video._dtime
                                     )
        self.remove_from_watchlist()
        if video._gui:
            video._gui.cbox.disable()
            video._gui.gray_out()
            gi.report_selection()
    
    def download_video(self,event=None):
        f = '[Yatube] yatube.Commands.download_video'
        ''' In case of 'get_url', there is no GUI to be handled
            ('mt.Video._gui' must be set to 'None'), so we do not force
            'mt.Video._gui' check here.
        '''
        if objs.video().logic.path():
            if os.path.exists(objs._video.logic._path):
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
                if objs._video.logic.download():
                    self.mark_downloaded()
        else:
            sh.com.empty(f)
    
    def download(self,event=None):
        f = '[Yatube] yatube.Commands.download'
        selection = self.selection()
        if selection:
            for i in range(len(selection)):
                mt.objs.videos().set_gui(selection[i])
                gi.objs.progress().title (_('Download progress') \
                                         + ' (%d/%d)' % (i + 1
                                                        ,len(selection)
                                                        )
                                         )
                self.download_video()
            gi.objs._progress.title()
            gi.objs._progress.close()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
        
    def update_channels(self,event=None):
        f = '[Yatube] yatube.Commands.update_channels'
        authors  = lg.objs.lists()._subsc_auth
        play_ids = lg.objs._lists._subsc_ids
        for i in range(len(play_ids)):
            self.update_channel (author  = authors[i]
                                ,play_id = play_ids[i]
                                )
        
    def update_trending(self,event=None,url=None):
        if not url:
            url = 'https://www.youtube.com/feed/trending?gl=RU'
            # This is needed if we use hotkeys (update an old value)
            self._menu.opt_trd.set(_('Trending'))
        lg.objs.channel().reset(url=url)
        lg.objs._channel.run()
        self.load_view()
        
    def reset_channel_gui(self):
        # Clears the old Channel widget
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        for gui in guis:
            gui.frame.widget.destroy()
        self._menu.title()
        self.save_url()
    
    def bind_context(self,event=None):
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        for gui in guis:
            for obj in gui._objects:
                sg.bind (obj      = obj
                        ,bindings = '<ButtonRelease-3>'
                        ,action   = self.context
                        )
        
    def fill_default(self):
        f = '[Yatube] yatube.Commands.fill_default'
        # Operation takes ~0,56s but there seems nothing to speed up
        #timer = sh.Timer(f)
        #timer.start()
        gi.objs.channel(parent=gi.objs.menu().framev)
        if mt.objs.videos()._videos:
            for i in range(len(mt.objs._videos._videos)):
                mt.objs._videos.i = i
                mt.objs._videos._videos[i]._gui = gi.objs._channel.add(no=i+1)
        else:
            sh.com.empty(f)
        #timer.end()
            
    def dimensions(self):
        f = '[Yatube] yatube.Commands.dimensions'
        sg.objs.root().idle()
        height = gi.objs._channel.frm_emb.widget.winfo_reqheight()
        ''' #NOTE: Extra space can be caused by a difference of
            the default and loaded pictures.
        '''
        #height = len(lg.objs.channel()._urls) * 112.133333333
        sh.log.append (f,_('DEBUG')
                      ,_('Widget must be at least %d pixels in height')\
                      % height
                      )
        gi.objs._channel.canvas.region (x        = 1024
                                       ,y        = height
                                       ,x_border = 20
                                       ,y_border = 20
                                       )
    
    def fill_unknown(self):
        f = '[Yatube] yatube.Commands.fill_unknown'
        #timer = sh.Timer(f)
        #timer.start()
        unknown = []
        for i in range(len(mt.objs.videos()._videos)):
            mt.objs._videos.i = i
            if not mt.objs._videos.current().Saved:
                unknown.append(i)
        if unknown:
            for i in range(len(unknown)):
                mt.objs._videos.i = unknown[i]
                objs.video().logic.assign_online()
                objs._video.logic.image()
                objs._video.image()
                objs._video.logic.dump()
                self.update_video(i=unknown[i])
            lg.objs.db().save()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
        #timer.end()
    
    def set_block(self):
        video  = mt.objs.videos().current()
        author = video._author
        title  = video._title
        if author in lg.objs.lists()._block_auth \
        or author in lg.objs._lists._block_auth \
        or lg.objs._lists.match_blocked_word(title+video._title):
            author = title = _('BLOCKED')
            objs.video()._image = None
            video.Block  = True
        return(author,title)
    
    def update_video(self,i):
        f = '[Yatube] yatube.Commands.update_video'
        gui = mt.objs.videos().current()._gui
        if gui:
            date = sh.Time (_timestamp = mt.objs.videos().current()._ptime
                           ,pattern    ='%Y-%m-%d %H:%M'
                           ).date()
            author, title = self.set_block()
            gui.reset (author = author
                      ,title  = title
                      ,date   = date
                      ,image  = objs.video()._image
                      )
            if mt.objs._videos.current()._dtime:
                gui.gray_out()
                self.video_date_filter()
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)
    
    def fill_known(self):
        f = '[Yatube] yatube.Commands.fill_known'
        #timer = sh.Timer(f)
        #timer.start()
        if mt.objs.videos()._videos:
            ids = [vid._id for vid in mt.objs._videos._videos]
            result = lg.objs.db().get_videos(ids)
            if result:
                matches = [item[0] for item in result if item]
                sh.log.append (f,_('INFO')
                              ,_('%d/%d links are already stored in DB.')\
                              % (len(matches),len(ids))
                              )
                for i in range(len(ids)):
                    mt.objs._videos.i = i
                    if result[i]:
                        mt.objs._videos.current().Saved = result[i]
                        objs.video().logic.assign_offline(result[i])
                        #todo: elaborate 'Video.model.get' and delete this
                        objs._video.image()
                        self.update_video(i)
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)
        #timer.end()
            
    def channel_gui(self,Unknown=True):
        ''' Do not forget to run 'reset_channel_gui' BEFORE resetting
            logic and running this procedure.
        '''
        self.fill_default()
        ''' After setting default images, we should align the left
            border, otherwise, it looks shabby. However, we cannot
            control the top border, since we need to recalculate
            a canvas region first, and this need an extra
            'root().idle()'.
        '''
        gi.objs._channel.canvas.widget.xview_moveto(0)
        self.fill_known()
        ''' The less we use GUI update, the faster will be the program.
            Updating tkinter idle tasks may take ~0,4-1,7s, but this
            must be done after creating all video widgets and
            reading/updating images.
        '''
        sg.objs.root().idle()
        if Unknown:
            self.fill_unknown()
        # Using the canvas is fast, no need to time this
        self.bind_context()
        self.dimensions()
        gi.objs._channel.canvas.move_top()
        gi.objs._channel.canvas.widget.xview_moveto(0)
        # Move focus away from 'ttk.Combobox' (OptionMenu)
        gi.objs._channel.canvas.focus()
        self.tooltips()
        self.update_widgets()
    
    def manage_sub(self):
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
            sh.WriteTextFile (file    = lg.objs.default()._fsubsc
                             ,Rewrite = True
                             ).write(text=text)
        else:
            # 'WriteTextFile' cannot write an empty text
            text = '# ' + _('Put here authors to subscribe to')
            sh.WriteTextFile (file    = lg.objs.default()._fsubsc
                             ,Rewrite = True
                             ).write(text=text)
        lg.objs.lists().reset()
        self.reset_channels()
                             
    def manage_blocked_authors(self,event=None):
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
            sh.WriteTextFile (file    = lg.objs.default()._fblock
                             ,Rewrite = True
                             ).write(text=text)
        else:
            # 'WriteTextFile' cannot write an empty text
            text = '# ' + _('Put here authors to be blocked')
            sh.WriteTextFile (file    = lg.objs.default()._fblock
                             ,Rewrite = True
                             ).write(text=text)
        lg.objs._lists.reset()
    
    def manage_blocked_words(self,event=None):
        words = sh.Words(text=lg.objs.lists()._blockw)
        gi.objs.blacklist().reset(words=words)
        gi.objs._blacklist.insert(text=lg.objs._lists._blockw)
        gi.objs._blacklist.show()
        text = gi.objs._blacklist.get()
        if text:
            text = text.splitlines()
            text = sorted (text
                          ,key = lambda x:x[0].lower()
                          )
            text = '\n'.join(text)
            sh.WriteTextFile (file    = lg.objs.default()._fblockw
                             ,Rewrite = True
                             ).write(text=text)
        else:
            # 'WriteTextFile' cannot write an empty text
            text = '# ' + _('Put here words to block in titles (case is ignored)')
            sh.WriteTextFile (file    = lg.objs.default()._fblockw
                             ,Rewrite = True
                             ).write(text=text)
        lg.objs._lists.reset()



class Video:
    
    def __init__(self):
        self.logic  = lg.Video(callback=self.progress)
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
        gi.objs._progress._item.text (file     = self.logic._pathsh
                                     ,cur_size = cur_size
                                     ,total    = total
                                     ,rate     = rate
                                     ,eta      = eta
                                     )
        # This is required to fill the progress bar on-the-fly
        sg.objs.root().widget.update_idletasks()
    
    def image(self):
        f = '[Yatube] yatube.Video.image'
        if mt.objs.videos().current()._bytes:
            img = sg.Image()
            img._bytes = mt.objs._videos.current()._bytes
            img.loader()
            self._image = img.image()
        else:
            sh.com.empty(f)
    
    def get(self):
        self.logic.get()
        self.image()



class Objects:
    
    def __init__(self):
        self._comments = self._video = self._add_id = self._commands \
                       = self._channels = None
    
    def channels(self):
        if self._channels is None:
            self._channels = Channels()
        return self._channels
    
    def commands(self):
        if self._commands is None:
            self._commands = Commands()
        return self._commands
    
    def add_id(self):
        if self._add_id is None:
            self._add_id = AddId()
        return self._add_id
    
    def video(self):
        if self._video is None:
            self._video = Video()
        return self._video
    
    def comments(self):
        if self._comments is None:
            self._comments = Comments()
        return self._comments


objs = Objects()


if __name__ == '__main__':
    f = '[Yatube] yatube.__main__'
    sg.objs.start()
    sg.Geometry(parent=gi.objs.parent()).set('1024x600')
    #todo: rename to 'yatube' when ready
    lg.objs.default(product='yatube2')
    if lg.objs._default.Success:
        objs.commands().bindings()
        gi.objs.menu().opt_max.set(mt.MAX_VIDEOS)
        objs._commands.update_widgets()
        gi.objs.progress()
        gi.objs._menu.show()
        lg.objs.db().save()
        lg.objs._db.close()
        #todo: del
        mt.objs.stat().report()
    else:
        sh.objs.mes (f,_('WARNING')
                    ,_('Unable to continue due to an invalid configuration.')
                    )
    sg.objs.end()
