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


class Extractor:
    
    def __init__(self,url=''):
        self._type = 'extractor'
        self._url  = ''
        if url:
            self.reset(url)
    
    def fetch(self):
        f = '[Yatube] yatube.Extractor.fetch'
        objs.commands().reset_channel_gui()
        lg.objs.extractor().run()
        if lg.objs._extractor._urls:
            mt.objs.videos().reset()
            ''' We put a limit here just not to hang the program.
                Potential limit (after which GUI may freeze) may be
                around 500 videos. Moreover, each extracted video ID
                adds up quota.
            '''
            ids = list(lg.objs._extractor._urls)[:200]
            for vid in lg.objs._extractor._urls:
                video = mt.Video()
                video._id = vid
                mt.objs.videos().add(video)
            objs._commands.channel_gui()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Extractor.fetch_prev'
        sh.log.append (f,_('INFO')
                      ,_('Nothing to do!')
                      )
    
    def fetch_next(self):
        f = '[Yatube] yatube.Extractor.fetch_next'
        sh.log.append (f,_('INFO')
                      ,_('Nothing to do!')
                      )
    
    def reset(self,url):
        self._url = url
        lg.objs.extractor().reset(url=self._url)



class Trending:
    
    def __init__(self,country=''):
        self.values()
        if country:
            self.reset(country)
    
    def values(self):
        self._type    = 'trending'
        self._country = ''
    
    def fetch(self):
        mt.objs.trending().run()
        objs._commands.channel_gui()
    
    def fetch_prev(self):
        mt.objs.trending().fetch_prev()
        mt.objs._trending.videos()
        objs._commands.channel_gui()
    
    def fetch_next(self):
        mt.objs.trending().fetch_next()
        mt.objs._trending.videos()
        objs._commands.channel_gui()
    
    def reset(self,country):
        self._country = country
        mt.objs.trending().reset(self._country)



class Feed:
    
    def __init__(self):
        self._type = 'feed'
    
    def fetch(self):
        lg.objs.feed().fetch()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._feed.get_token()
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Feed.fetch_prev'
        lg.objs.feed().fetch_prev()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._feed.get_token()
    
    def fetch_next(self):
        f = '[Yatube] yatube.Feed.fetch_next'
        lg.objs.feed().fetch_next()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._feed.get_token()



class Search:
    
    def __init__(self,query=''):
        self.values()
        if query:
            self.reset(query)
    
    def values(self):
        self._type  = 'search'
        self._query = ''
    
    def fetch(self):
        mt.objs.search().run()
        objs._commands.channel_gui()
    
    def fetch_prev(self):
        mt.objs.search().fetch_prev()
        mt.objs._search.videos()
        objs._commands.channel_gui()
    
    def fetch_next(self):
        mt.objs.search().fetch_next()
        mt.objs._search.videos()
        objs._commands.channel_gui()
    
    def reset(self,query):
        self._query = query
        mt.objs.search().reset(self._query)



class Videos:
    ''' Currently this class comprises some controller-specific
        functionality of 'gi.Video'.
    '''
    def __init__(self):
        pass
    
    def bindings(self):
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        for gui in guis:
            gui.cbox.action = objs.commands().report_selection
            for obj in gui._objects:
                sg.bind (obj      = obj
                        ,bindings = '<ButtonRelease-1>'
                        ,action   = objs._commands.toggle_cbox
                        )
                sg.bind (obj      = obj
                        ,bindings = '<ButtonRelease-3>'
                        ,action   = objs._commands.context
                        )
    
    def add(self,no=1):
        ivideo = gi.Video (parent = gi.objs.channel().frm_emb
                          ,no     = no
                          )
        return ivideo



class Favorites:
    
    def __init__(self):
        self._type = 'favorites'
    
    def fetch(self):
        lg.objs.favorites().fetch()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._favorites.get_token()
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Favorites.fetch_prev'
        lg.objs.favorites().fetch_prev()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._favorites.get_token()
    
    def fetch_next(self):
        f = '[Yatube] yatube.Favorites.fetch_next'
        lg.objs.favorites().fetch_next()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._favorites.get_token()



class Watchlist:
    
    def __init__(self):
        self._type = 'watchlist'
    
    def fetch(self):
        lg.objs.watchlist().fetch()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._watchlist.get_token()
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Watchlist.fetch_prev'
        lg.objs.watchlist().fetch_prev()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._watchlist.get_token()
    
    def fetch_next(self):
        f = '[Yatube] yatube.Watchlist.fetch_next'
        lg.objs.watchlist().fetch_next()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._watchlist.get_token()



class Playlist:
    
    def __init__(self,play_id=''):
        self._type    = 'playlist'
        self._play_id = ''
        if play_id:
            self.reset(play_id)
    
    def fetch(self):
        mt.objs.playlist().run()
        objs._commands.channel_gui()
    
    def fetch_prev(self):
        mt.objs.playlist().fetch_prev()
        mt.objs._playlist.videos()
        objs._commands.channel_gui()
    
    def fetch_next(self):
        mt.objs.playlist().fetch_next()
        mt.objs._playlist.videos()
        objs._commands.channel_gui()
    
    def reset(self,play_id):
        self._play_id = play_id
        mt.objs.playlist().reset(play_id)



class Channels:
    
    def __init__(self):
        self._channels = []
        self._modes    = ('favorites','feed','history','playlist'
                         ,'search','trending','watchlist','extractor'
                         )
        self._unique   = ('favorites','feed','history','watchlist')
        self._types    = []
        self.i         = 0
    
    def inc(self):
        if self.i == len(self._channels) - 1:
            self.i = 0
        elif self._channels:
            self.i += 1
    
    def dec(self):
        if self.i == 0:
            if self._channels:
                self.i = len(self._channels) - 1
        else:
            self.i -= 1
    
    def current(self):
        f = '[Yatube] yatube.Channels.current'
        if not self._channels:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
            self.add('history')
        if self.i < 0 or self.i >= len(self._channels):
            sh.objs.mes (f,_('ERROR')
                        ,_('The condition "%s" is not observed!') \
                        % '%d <= %d < %d' % (0,self.i
                                            ,len(self._channels)
                                            )
                        )
            self.i = 0
        return self._channels[self.i]
    
    def go_mode(self,mode):
        f = '[Yatube] yatube.Channels.go_mode'
        types = [channel._type for channel in self._channels]
        if types:
            if mode in types:
                self.i = types.index(mode)
            else:
                sh.objs.mes (f,_('ERROR')
                            ,_('Wrong input data: "%s"!') % str(mode)
                            )
        else:
            sh.com.empty(f)
    
    def add(self,mode='playlist',arg=None):
        f = '[Yatube] yatube.Channels.add'
        if mode in self._unique and mode in self._types:
            self.go_mode(mode)
        elif mode in self._modes:
            if mode == 'playlist':
                self._channels.append(Playlist(arg))
            elif mode == 'trending':
                self._channels.append(Trending(arg))
            elif mode == 'feed':
                self._channels.append(Feed())
            elif mode == 'search':
                self._channels.append(Search(arg))
            elif mode == 'favorites':
                self._channels.append(Favorites())
            elif mode == 'watchlist':
                self._channels.append(Watchlist())
            elif mode == 'history':
                self._channels.append(History())
            elif mode == 'extractor':
                self._channels.append(Extractor(arg))
            self.inc()
        else:
            sh.objs.mes (f,_('ERROR')
                        ,_('Wrong input data: "%s"!') % str(mode)
                        )
    
    def fetch(self):
        f = '[Yatube] yatube.Channels.fetch'
        if self._channels:
            timer = sh.Timer(f)
            timer.start()
            objs.commands().reset_channel_gui()
            mt.objs.videos().reset()
            self.current().fetch()
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
            self.current().fetch_prev()
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
            self.current().fetch_next()
            timer.end()
        else:
            sh.com.empty(f)



class History:
    
    def __init__(self):
        self._type = 'history'
    
    def fetch(self):
        lg.objs.history().fetch()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._history.get_token()
    
    def fetch_prev(self):
        f = '[Yatube] yatube.History.fetch_prev'
        lg.objs.history().fetch_prev()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._history.get_token()
    
    def fetch_next(self):
        f = '[Yatube] yatube.History.fetch_next'
        lg.objs.history().fetch_next()
        objs._commands.channel_gui(Unknown=False)
        lg.objs._history.get_token()



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
    
    def update_sel_menu(self,event=None):
        f = '[Yatube] yatube.Commands.update_sel_menu'
        selection = self.selection()
        if selection:
            items = list(gi.selection_items)
            Found = False
            for gui in selection:
                mt.objs.videos().set_gui(gui)
                path = lg.Video().path()
                if path and os.path.exists(path):
                    Found = True
                    break
            if not Found:
                items.remove(_('Delete selected'))
            ids = []
            for gui in selection:
                mt.objs._videos.set_gui(gui)
                ids.append(mt.objs._videos.current()._id)
            result = lg.objs.db().get_videos(ids)
            if result:
                dtimes = [item[10] for item in result if item[10]]
                ftimes = [item[11] for item in result if item[11]]
                ltimes = [item[12] for item in result if item[12]]
                if len(dtimes) == len(result):
                    items.remove(_('Mark as watched'))
                elif not dtimes:
                    items.remove(_('Mark as not watched'))
                if len(ftimes) == len(result):
                    items.remove(_('Add to favorites'))
                elif not ftimes:
                   items.remove(_('Remove from favorites')) 
                if len(ltimes) == len(result):
                    items.remove(_('Add to watchlist'))
                elif not ltimes:
                   items.remove(_('Remove from watchlist')) 
        else:
            items = (_('Selection')
                    ,_('Select all new videos')
                    )
        self._menu.opt_sel.reset (items   = list(items)
                                 ,default = _('Selection')
                                 )
    
    def toggle_cbox(self,event=None):
        f = '[Yatube] Commands.toggle_cbox'
        gui = self.get_widget(event=event)
        if gui:
            gui.cbox.toggle()
            objs.commands().report_selection()
        else:
            sh.com.empty(f)
    
    def toggle_select(self,event=None):
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        if self._menu.chb_sel.get():
            for gui in guis:
                gui.cbox.enable()
        else:
            for gui in guis:
                gui.cbox.disable()
        self.report_selection()
    
    def report_selection(self,event=None):
        selection = self.selection()
        if selection:
            count = len(selection)
        else:
            count = 0
        self._menu.title (selected = count
                         ,total    = len(mt.objs.videos()._videos)
                         )
        self.update_sel_menu()
    
    def statistics(self,event=None,Silent=False):
        mt.objs.stat().report(Silent=Silent)
    
    def progress(self,data):
        ''' Depending on situation, youtube_dl may not provide some keys,
            so be aware of KeyError.
        '''
        if 'total_bytes' in data:
            total = data['total_bytes']
        else:
            total = 0
        if 'downloaded_bytes' in data:
            cur_size = data['downloaded_bytes']
        else:
            cur_size = 0
        if 'eta' in data:
            eta = data['eta']
        else:
            eta = 0
        if 'speed' in data:
            rate = data['speed']
        else:
            rate = 0
        # If unknown, values may be None
        if total is None:
            total = 0
        if cur_size is None:
            cur_size = 0
        if eta is None:
            eta = 0
        if rate is None:
            rate = 0
        total    = total    / 1000000
        cur_size = cur_size / 1000000
        # Prevent ZeroDivisionError
        if total:
            percent = round((100*cur_size)/total)
        else:
            percent = 0
        gi.objs.progress()._item.widget['value'] = percent
        rate = int(rate) // 1000
        # Prevent from irritating message length changes
        rate = sh.Text(text=str(rate)).grow (max_len = 4
                                            ,FromEnd = False
                                            )
        eta = sh.Text(text=str(eta)).grow (max_len = 3
                                          ,FromEnd = False
                                          )
        gi.objs._progress._item.text (file     = mt.objs.videos().current()._pathsh
                                     ,cur_size = cur_size
                                     ,total    = total
                                     ,rate     = rate
                                     ,eta      = eta
                                     )
        # This is required to fill the progress bar on-the-fly
        sg.objs.root().widget.update_idletasks()
    
    def history(self,event=None):
        objs.channels().add('history')
        objs._channels.fetch()
    
    def update_context(self):
        f = '[Yatube] yatube.Commands.update_context'
        video = mt.objs.videos().current()
        if video:
            items = list(gi.context_items)
            data = lg.objs.db().get_video(video._id)
            if data:
                ''' #note: do not forget to update indices in case of
                    changing the DB structure.
                '''
                dtime = data[10]
                ftime = data[11]
                ltime = data[12]
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
            else:
                sh.com.empty(f)
            if video.Block:
                items.remove(_('Block this channel'))
            else:
                items.remove(_('Unblock'))
            lg.Video().path()
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
        objs.channels().fetch()
    
    def feed(self,event=None):
        objs.channels().add('feed')
        objs._channels.fetch()
    
    def prev_page(self,event=None):
        objs.channels().fetch_prev()
    
    def next_page(self,event=None):
        objs.channels().fetch_next()
    
    def watchlist(self,event=None):
        objs.channels().add('watchlist')
        objs._channels.fetch()
    
    def favorites(self,event=None):
        objs.channels().add('favorites')
        objs._channels.fetch()
    
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
            self.report_selection()
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
    
    def set_max_videos(self,event=None):
        f = '[Yatube] yatube.Commands.set_max_videos'
        if str(self._menu.opt_max.choice).isdigit():
            mt.MAX_VIDEOS = int(self._menu.opt_max.choice)
        else:
            sh.objs.mes (f,_('ERROR')
                        ,_('Wrong input data: "%s"') \
                        % str(self._menu.opt_max.choice)
                        )
        self.channel_gui()
    
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
    
    def prev_channel(self,event=None):
        objs.channels().dec()
        objs._channels.fetch()
    
    def next_channel(self,event=None):
        objs.channels().inc()
        objs._channels.fetch()
    
    def show_comments(self,event=None):
        f = '[Yatube] yatube.Commands.show_comments'
        objs.comments().reset()
        objs._comments.show()
    
    def menu_update(self,event=None):
        f = '[Yatube] yatube.Commands.menu_update'
        default = _('Update')
        choice  = self._menu.opt_upd.choice
        if choice == default:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
        elif choice == _('Subscriptions'):
            self._menu.opt_upd.set(default)
            self.update_channels()
        elif choice == _('Channel'):
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
        elif choice == _('Favorites'):
            self._menu.opt_viw.set(default)
            self.favorites()
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
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
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
            ''' Do not put this code into 'self.mark_not_watched'
                because it is used by 'self.sel_mark_not_watched'.
            '''
            if objs.channels().current()._type == 'history':
                self.reload_channel()
        elif choice == _('Add to favorites'):
            self._menu.opt_sel.set(default)
            self.sel_star()
        elif choice == _('Remove from favorites'):
            self._menu.opt_sel.set(default)
            self.sel_unstar()
            ''' Do not put this code into 'self.unstar'
                because the latter is used by 'self.sel_unstar'.
            '''
            if objs.channels().current()._type == 'favorites':
                self.reload_channel()
        elif choice == _('Delete selected'):
            self._menu.opt_sel.set(default)
            self.delete_selected()
        elif choice == _('Add to watchlist'):
            self._menu.opt_sel.set(default)
            self.sel_add2watchlist()
        elif choice == _('Remove from watchlist'):
            self._menu.opt_sel.set(default)
            self.sel_remove_from_watchlist()
            ''' Do not put this code into 'self.remove_from_watchlist'
                because the latter is used by
                'self.sel_remove_from_watchlist'.
            '''
            if objs.channels().current()._type == 'watchlist':
                self.reload_channel()
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
                ''' The 'Block' boolean will actually be set after
                    reloading the channel, however, we want to inform
                    the context menu about the changes.
                '''
                video.Block = False
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
                self.reload_channel()
            else:
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
        else:
            sh.com.empty(f)
    
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
            self.report_selection()
        return lg.Video().delete()
    
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
        url = lg.Video().url()
        if url:
            lg.objs.online()._url = url
            lg.objs._online.browse()
        else:
            sh.com.empty(f)
                   
    def copy_video_url(self,event=None):
        f = '[Yatube] yatube.Commands.copy_video_url'
        url = lg.Video().url()
        if url:
            sg.Clipboard().copy(text=url)
        else:
            sh.com.empty(f)
    
    def subscribe(self,event=None):
        f = '[Yatube] yatube.Commands.subscribe'
        video = mt.objs.videos().current()
        lg.Video().play_id()
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
        if video._author:
            if video._author in lg.objs.lists()._block_auth:
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
            else:
                sh.log.append (f,_('INFO')
                              ,_('Block channel "%s"') % video._author
                              )
                ''' The 'Block' boolean will actually be set after
                    reloading the channel, however, we want to inform
                    the context menu about the changes.
                '''
                video.Block = True
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
                    self.reload_channel()
                else:
                    sh.com.empty(f)
        else:
            sh.com.empty(f)
                   
    def load_channel(self,event=None):
        f = '[Yatube] yatube.Commands.load_channel'
        play_id = lg.Video().play_id()
        if play_id:
            objs.channels().add('playlist',play_id)
            objs._channels.fetch()
        else:
            sh.com.empty(f)
    
    def open_channel_url(self,event=None):
        f = '[Yatube] yatube.Commands.open_channel_url'
        channel_id = lg.Video().channel_id()
        if channel_id:
            lg.objs.online()._url = lg.pattern3a + channel_id
            lg.objs._online.browse()
        else:
            sh.com.empty(f)

    def copy_channel_url(self,event=None):
        f = '[Yatube] yatube.Commands.copy_channel_url'
        channel_id = lg.Video().channel_id()
        if channel_id:
            url = lg.pattern3a + channel_id
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
        url = lg.Video().stream()
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
                    if objs.channels().current()._type == 'watchlist':
                        self.reload_channel()
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
            gi.objs._summary.insert(lg.Video().summary())
            gi.objs._summary.show()
        else:
            sh.com.empty(f)
    
    def _context(self,choice,event=None):
        f = '[Yatube] yatube.Commands._context'
        if choice:
            url = lg.Video().url()
            if choice == _('Show the full summary'):
                self.summary()
            elif choice == _('Download'):
                self.download_video()
            elif choice == _('Play'):
                self.download_video()
                self.play_video()
                if objs.channels().current()._type == 'watchlist':
                    self.reload_channel()
            elif choice == _('Stream'):
                self.stream_video()
            elif choice == _('Mark as watched'):
                self.mark_watched()
            elif choice == _('Mark as not watched'):
                self.mark_not_watched()
                ''' Do not put this code into 'self.mark_not_watched'
                    because the latter is used by
                    'self.sel_mark_not_watched'.
                '''
                if objs.channels().current()._type == 'history':
                    self.reload_channel()
            elif choice == _('Add to favorites'):
                self.star()
            elif choice == _('Remove from favorites'):
                self.unstar()
                ''' Do not put this code into 'self.unstar' because
                    the latter is used by 'self.sel_unstar'.
                '''
                if objs.channels().current()._type == 'favorites':
                    self.reload_channel()
            elif choice == _('Add to watchlist'):
                self.add2watchlist()
                ''' Do not put this code into 'self.add2watchlist'
                    because the latter is used by
                    'self.sel_add2watchlist'.
                '''
                if objs.channels().current()._type == 'watchlist':
                    self.reload_channel()
            elif choice == _('Remove from watchlist'):
                self.remove_from_watchlist()
                ''' Do not put this code into
                    'self.remove_from_watchlist' because the latter is
                    used by 'self.sel_remove_from_watchlist'.
                '''
                if objs.channels().current()._type == 'watchlist':
                    self.reload_channel()
            elif choice == _('Delete the downloaded file'):
                self.delete_video()
            elif choice == _('Extract links'):
                self.get_links(url)
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
    
    def _color_context(self,message,color='green'):
        if message in gi.objs.context().lst:
            ind = gi.objs._context.lst.index(message)
            gi.objs._context.widget.itemconfig(ind,fg=color)
    
    def color_context(self):
        f = '[Yatube] yatube.Commands.color_context'
        if gi.objs.context().lst:
            self._color_context(_('Download'),'green')
            self._color_context(_('Delete the downloaded file'),'red')
            self._color_context(_('Mark as watched'),'green')
            self._color_context(_('Mark as not watched'),'red')
            self._color_context(_('Add to favorites'),'green')
            self._color_context(_('Remove from favorites'),'red')
            self._color_context(_('Add to watchlist'),'green')
            self._color_context(_('Remove from watchlist'),'red')
            self._color_context(_('Block this channel'),'green')
            self._color_context(_('Unblock'),'red')
            self._color_context(_('Subscribe to this channel'),'green')
            self._color_context(_('Unsubscribe'),'red')
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
            self.color_context()
            gi.objs._context.show()
            choice = gi.objs._context._get
            self._context(choice)
        else:
            sh.com.empty(f)
        
    def get_links(self,url):
        f = '[Yatube] yatube.Commands.get_links'
        if url:
            objs.channels().add('extractor',url)
            objs._channels.fetch()
        else:
            sh.com.empty(f)
                          
    def set_channel(self,event=None):
        f = '[Yatube] yatube.Commands.set_channel'
        if self._menu.opt_chl.choice == _('Channels'):
            self.feed()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Switch to channel "%s"') \
                          % str(self._menu.opt_chl.choice)
                          )
            if self._menu.opt_chl.choice in lg.objs.lists()._subsc_auth:
                author  = self._menu.opt_chl.choice
                no      = lg.objs._lists._subsc_auth.index(author)
                play_id = lg.objs._lists._subsc_ids[no]
                objs.channels().add('playlist',play_id)
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
                    video = mt.Video()
                    video._id = lg.URL(result).video_id()
                    mt.objs.videos().add(video)
                    mt.objs._videos.i = len(mt.objs._videos._videos) - 1
                    logic = lg.Video()
                    logic.get()
                    if logic.Success:
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
        
    def search_youtube(self,event=None):
        f = '[Yatube] yatube.Commands.search_youtube'
        query = self._menu.ent_src.get()
        if query and query != _('Search Youtube'):
            objs.channels().add('search',query)
            objs._channels.fetch()
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
                ,bindings = '<F1>'
                ,action   = self.statistics
                )
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
                ,action   = self.prev_channel
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Control-Right>'
                ,action   = self.next_channel
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
                ,action   = self.favorites
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Shift-Delete>'
                ,action   = self.delete_selected
                )
        sg.bind (obj      = self._menu.parent
                ,bindings = '<Alt-c>'
                ,action   = self.feed
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
        self._menu.btn_nxt.action = self.next_channel
        self._menu.btn_ply.action = self.play
        self._menu.btn_ppg.action = self.prev_page
        self._menu.btn_prv.action = self.prev_channel
        self._menu.btn_stm.action = self.stream
        self._menu.btn_ytb.action = self.search_youtube
        self._menu.chb_sel.reset(action=self.toggle_select)
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
        self.report_selection()
        
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
        sh.Launch (target = lg.Video().path()
                  ).app (custom_app  = app
                        ,custom_args = custom_args
                        )
                        
    def _play_default(self):
        sh.Launch(target=lg.Video().path()).default()

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
            if objs.channels().current()._type == 'watchlist':
                self.reload_channel()
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
            self.report_selection()
    
    def download_video(self,event=None):
        f = '[Yatube] yatube.Commands.download_video'
        ''' In case of 'get_url', there is no GUI to be handled
            ('mt.Video._gui' must be set to 'None'), so we do not force
            'mt.Video._gui' check here.
        '''
        logic = lg.Video()
        if logic.path():
            if os.path.exists(mt.objs.videos().current()._path):
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
                if logic.download(self.progress):
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
            self._menu.opt_chl.set(authors[i])
            objs.channels().add('playlist',play_ids[i])
            objs._channels.fetch()
        self.feed()
        
    def update_trending(self,event=None,country='RU'):
        f = '[Yatube] yatube.Commands.update_trending'
        ''' We need this procedure to be separate from
            'self.set_trending' because of hotkeys.
        '''
        objs.channels().add('trending',country)
        objs._channels.fetch()
    
    def set_trending(self,event=None):
        f = '[Yatube] yatube.Commands.set_trending'
        choice = self._menu.opt_trd.choice
        if choice == _('Trending'):
            country = 'RU'
        else:
            sh.log.append (f,_('INFO')
                          ,_('Switch to channel "%s"') % str(choice)
                          )
            if choice in lg.objs.const()._countries:
                country = lg.objs._const._countries[choice]
            else:
                country = 'RU'
            sh.log.append (f,_('DEBUG')
                          ,_('Country: %s') % country
                          )
        self.update_trending(country=country)
        
    def reset_channel_gui(self):
        # Clears the old Channel widget
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        for gui in guis:
            gui.frame.widget.destroy()
        self._menu.title()
        #todo: rework
        #self.save_url()
    
    def fill_default(self):
        f = '[Yatube] yatube.Commands.fill_default'
        # Operation takes ~0,56s but there seems nothing to speed up
        #timer = sh.Timer(f)
        #timer.start()
        gi.objs.channel(parent=gi.objs.menu().framev)
        if mt.objs.videos()._videos:
            for i in range(len(mt.objs._videos._videos)):
                mt.objs._videos.i = i
                mt.objs._videos._videos[i]._gui = objs.videos().add(no=i+1)
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
                lg.Video().get()
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
            video._image = None
            video.Block  = True
        return(author,title)
    
    def update_video(self,i):
        f = '[Yatube] yatube.Commands.update_video'
        video = mt.objs.videos().current()
        if video._gui:
            date = sh.Time (_timestamp = video._ptime
                           ,pattern    = '%Y-%m-%d %H:%M'
                           ).date()
            author, title = self.set_block()
            video._gui.reset (author = author
                             ,title  = title
                             ,date   = date
                             ,image  = video._image
                             )
            if video._dtime:
                video._gui.gray_out()
                self.video_date_filter()
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
                        logic = lg.Video()
                        logic.assign_offline(result[i])
                        logic.unsupported()
                        logic.load_image()
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
        objs.videos().bindings()
        self.dimensions()
        gi.objs._channel.canvas.move_top()
        gi.objs._channel.canvas.widget.xview_moveto(0)
        # Move focus away from 'ttk.Combobox' (OptionMenu)
        gi.objs._channel.canvas.focus()
        self.tooltips()
    
    def manage_sub(self):
        objs.add_id().reset()
        objs._add_id.show()
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



class Objects:
    
    def __init__(self):
        self._comments = self._videos = self._add_id = self._commands \
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
    
    def videos(self):
        if self._videos is None:
            self._videos = Videos()
        return self._videos
    
    def comments(self):
        if self._comments is None:
            self._comments = Comments()
        return self._comments


objs = Objects()


if __name__ == '__main__':
    f = '[Yatube] yatube.__main__'
    sg.objs.start()
    sg.Geometry(parent=gi.objs.parent()).set('1024x600')
    lg.objs.default(product='yatube')
    if lg.objs._default.Success:
        objs.commands().bindings()
        gi.objs.menu().opt_max.set(mt.MAX_VIDEOS)
        gi.objs.progress()
        gi.objs._menu.show()
        lg.objs.db().save()
        lg.objs._db.close()
    else:
        sh.objs.mes (f,_('WARNING')
                    ,_('Unable to continue due to an invalid configuration.')
                    )
    objs.commands().statistics(Silent=True)
    sh.log.append (f,_('DEBUG')
                  ,_('Goodbye!')
                  )
    sg.objs.end()
