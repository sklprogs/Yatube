#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import subprocess
import skl_shared.shared as sh
import logic             as lg
import gui               as gi
import meta              as mt

import gettext
import skl_shared.gettext_windows

skl_shared.gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')



class Pause:
    
    def __init__(self):
        self.values()
        self.gui = gi.Pause()
        self.bindings()
    
    def values(self):
        self._id    = ''
        self._pause = 0
    
    def delete(self,event=None):
        lg.objs.db().update_pause(self._id)
        mt.objs.videos().current()._pause = 0
        self.close()
        objs.commands().mark_watched(Unselect=False)
        objs._commands.remove_from_watchlist(Unselect=False)
        if objs.channels().current()._type == 'watchlist':
            objs._commands.reload_channel()
        else:
            objs._commands.update_video()
    
    def reset(self,video_id,pause):
        self._id    = video_id
        self._pause = pause
        self.fill()
    
    def fill(self,event=None):
        hours, minutes, seconds = sh.com.split_time(self._pause)
        self.gui.ent_hrs.reset()
        self.gui.ent_min.reset()
        self.gui.ent_sec.reset()
        self.gui.ent_hrs.insert(hours)
        self.gui.ent_min.insert(minutes)
        self.gui.ent_sec.insert(seconds)
        self.update()
    
    def save(self,event=None):
        hours   = self.get_hrs()
        minutes = self.get_min()
        seconds = self.get_sec()
        all_sec = hours * 3600 + minutes * 60 + seconds
        mt.objs.videos().current()._pause = all_sec
        lg.objs.db().update_pause (video_id = self._id
                                  ,pause    = all_sec
                                  )
        self.close()
        objs.commands().mark_not_watched(Unselect=False)
        objs._commands.add2watchlist(Unselect=False)
        if objs.channels().current()._type == 'watchlist':
            objs._commands.reload_channel()
        else:
            objs._commands.update_video()
    
    def bindings(self):
        self.gui.btn_del.action = self.delete
        self.gui.btn_hrd.action = self.dec_hrs
        self.gui.btn_hru.action = self.inc_hrs
        self.gui.btn_mnd.action = self.dec_min
        self.gui.btn_mnu.action = self.inc_min
        self.gui.btn_rst.action = self.fill
        self.gui.btn_sav.action = self.save
        self.gui.btn_scd.action = self.dec_sec
        self.gui.btn_scu.action = self.inc_sec
        sh.com.bind (obj      = self.gui.ent_hrs
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.upd_hrs
                    )
        sh.com.bind (obj      = self.gui.ent_min
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.upd_min
                    )
        sh.com.bind (obj      = self.gui.ent_sec
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.upd_sec
                    )
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = ('<F2>','<Control-s>')
                    ,action   = self.save
                    )
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = ('<Escape>','<Control-w>','<Control-q>')
                    ,action   = self.close
                    )
        self.gui.widget.protocol('WM_DELETE_WINDOW',self.close)
    
    def get_sec(self,event=None):
        f = '[Yatube] yatube.Pause.get_sec'
        seconds = sh.Input (title = f
                           ,value = self.gui.ent_sec.get()
                           ).integer()
        # 'sh.Input.integer' already throws an error at negative values
        if seconds > 59:
            sub = '0 <= {} <= 59'.format(seconds)
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.mes(f,mes).warning()
            seconds = 59
            self.gui.ent_sec.reset()
            self.gui.ent_sec.insert(seconds)
        return seconds
    
    def get_min(self,event=None):
        f = '[Yatube] yatube.Pause.get_min'
        minutes = sh.Input (title = f
                           ,value = self.gui.ent_min.get()
                           ).integer()
        # 'sh.Input.integer' already throws an error at negative values
        if minutes > 59:
            sub = '0 <= {} <= 59'.format(minutes)
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.mes(f,mes).warning()
            minutes = 59
            self.gui.ent_min.reset()
            self.gui.ent_min.insert(minutes)
        return minutes
    
    def get_hrs(self,event=None):
        f = '[Yatube] yatube.Pause.get_hrs'
        return sh.Input (title = f
                        ,value = self.gui.ent_hrs.get()
                        ).integer()
    
    def update(self,event=None):
        self.upd_hrs()
        self.upd_min()
        self.upd_sec()
    
    def upd_sec(self,event=None):
        seconds = self.get_sec()
        if seconds < 59:
            self.gui.btn_scu.active()
        else:
            self.gui.btn_scu.inactive()
        if seconds > 0:
            self.gui.btn_scd.active()
        else:
            self.gui.btn_scd.inactive()
    
    def upd_min(self,event=None):
        minutes = self.get_min()
        if minutes < 59:
            self.gui.btn_mnu.active()
        else:
            self.gui.btn_mnu.inactive()
        if minutes > 0:
            self.gui.btn_mnd.active()
        else:
            self.gui.btn_mnd.inactive()
    
    def upd_hrs(self,event=None):
        self.gui.btn_hru.active()
        if self.get_hrs() > 0:
            self.gui.btn_hrd.active()
        else:
            self.gui.btn_hrd.inactive()
    
    def inc_sec(self,event=None):
        seconds = self.get_sec()
        if seconds < 59:
            seconds += 1
        self.gui.ent_sec.reset()
        self.gui.ent_sec.insert(seconds)
        self.upd_sec()
    
    def inc_min(self,event=None):
        minutes = self.get_min()
        if minutes < 59:
            minutes += 1
        self.gui.ent_min.reset()
        self.gui.ent_min.insert(minutes)
        self.upd_min()
    
    def inc_hrs(self,event=None):
        hours = self.get_hrs() + 1
        self.gui.ent_hrs.reset()
        self.gui.ent_hrs.insert(hours)
        self.upd_hrs()
    
    def dec_sec(self,event=None):
        seconds = self.get_sec()
        if seconds > 0:
            seconds -= 1
        self.gui.ent_sec.reset()
        self.gui.ent_sec.insert(seconds)
        self.upd_sec()
    
    def dec_min(self,event=None):
        minutes = self.get_min()
        if minutes > 0:
            minutes -= 1
        self.gui.ent_min.reset()
        self.gui.ent_min.insert(minutes)
        self.upd_min()
    
    def dec_hrs(self,event=None):
        hours = self.get_hrs()
        if hours > 0:
            hours -= 1
        self.gui.ent_hrs.reset()
        self.gui.ent_hrs.insert(hours)
        self.upd_hrs()
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()



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
            sh.com.lazy(f)
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Extractor.fetch_prev'
        sh.com.lazy(f)
    
    def fetch_next(self):
        f = '[Yatube] yatube.Extractor.fetch_next'
        sh.com.lazy(f)
    
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
            gui.cbx_vno.action = objs.commands().report_selection
            for obj in gui._objects:
                sh.com.bind (obj      = obj
                            ,bindings = '<ButtonRelease-1>'
                            ,action   = objs._commands.toggle_cbox
                            )
                sh.com.bind (obj      = obj
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
            sh.com.empty(f)
            self.add('history')
        if self.i < 0 or self.i >= len(self._channels):
            sub = '0 <= {} < {}'.format(self.i,len(self._channels))
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.mes(f,mes).error()
            self.i = 0
        return self._channels[self.i]
    
    def go_mode(self,mode):
        f = '[Yatube] yatube.Channels.go_mode'
        types = [channel._type for channel in self._channels]
        if types:
            if mode in types:
                self.i = types.index(mode)
            else:
                mes = _('Wrong input data: "{}"!').format(mode)
                sh.objs.mes(f,mes).error()
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
            mes = _('Wrong input data: "{}"!').format(mode)
            sh.objs.mes(f,mes).error()
    
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
    
    def save_close(self,event=None):
        self.save()
        self.close()
    
    def open(self,event=None):
        f = '[Yatube] yatube.AddId.open'
        author = self.gui.lst_id1.get()
        if author:
            ind     = self.gui.lst_id1.lst.index(author)
            ''' 'myid' will be a valid playlist ID since incorrect
                values are not added when using 'AddId'.
            '''
            myid = self.gui.lst_id3.lst[ind]
            url  = 'https://www.youtube.com/playlist?list={}'.format(myid)
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
            mes = _('"{}" is already in the list!').format(self._author)
            sh.objs.mes(f,mes).info()
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
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(mode,'play_id; channel_id; user')
                sh.objs.mes(f,mes).error()
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
        self.gui.ent_ath.clear()
        self.gui.ent_ath.insert(author)
        self.gui.ent_pid.clear()
        self.gui.ent_pid.insert(pid)
        self.delete()
    
    def bindings(self):
        self.gui.btn_add.action = self.add
        self.gui.btn_cls.action = self.close
        self.gui.btn_del.action = self.delete
        self.gui.btn_edt.action = self.edit
        self.gui.btn_opn.action = self.open
        self.gui.btn_rst.action = self.reset
        self.gui.btn_sav.action = self.save_close
        sh.com.bind (obj      = self.gui
                    ,bindings = ('<F5>','<Control-r>')
                    ,action   = self.reset
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = ('<F2>','<Control-s>')
                    ,action   = self.save_close
                    )
        sh.com.bind (obj      = self.gui
                    ,bindings = ('<Escape>','<Control-w>','<Control-q>')
                    ,action   = self.close
                    )
        sh.com.bind (obj      = self.gui.ent_ath
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.add
                    )
        sh.com.bind (obj      = self.gui.ent_pid
                    ,bindings = ('<Return>','<KP_Enter>')
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
            sub = '{} = {} = {}'.format(len(id1),len(id2),len(id3))
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.mes(f,mes).warning()
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
        self.gui   = gi.Comments()
        self.logic = mt.Comments()
        self.bindings()
        self.reset()
    
    def values(self):
        self.Success = True
    
    def bindings(self):
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = '<Alt-Left>'
                    ,action   = self.prev
                    )
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = '<Alt-Right>'
                    ,action   = self.next
                    )
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = ('<Escape>','<Control-w>','<Control-q>')
                    ,action   = self.close
                    )
        sh.com.bind (obj      = self.gui.txt_com
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.next
                    )
        self.gui.btn_prv.action = self.prev
        self.gui.btn_nxt.action = self.next
        self.gui.widget.protocol('WM_DELETE_WINDOW',self.close)
    
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
        self.logic.fetch()
        self.Success = self.logic.Success
        self.update()
    
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
            if self.logic._texts:
                try:
                    text = self.logic._texts[self.logic.i]
                except IndexError:
                    text = ''
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes).warning()
                text     = sh.Text(text).delete_unsupported()
                old_text = self.gui.txt_com.get()
                # A new line is inserted when read from the widget
                text = text.strip()
                old_text.strip()
                # Keep a scrollbar position if there are no pages left
                if old_text != text:
                    self.gui.txt_com.enable()
                    self.gui.txt_com.reset()
                    self.gui.txt_com.insert(text)
                    self.gui.txt_com.disable()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
        
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()



class Commands:
    
    def __init__(self):
        self._mode      = None
        self._timestamp = None
        self._tip_tim   = None
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
    
    def quality(self,event=None):
        ''' Generate a quality argument for youtube_dl.
            Youtube's recommended resolution ratios:
            2160p: 3840x2160
            1440p: 2560x1440
            1080p: 1920x1080
            720p: 1280x720
            480p: 854x480
            360p: 640x360
            240p: 426x240
        '''
        f = '[Yatube] yatube.Commands.quality'
        qual = gi.objs.menu().opt_qal.choice
        res  = gi.objs._menu.opt_res.choice
        if qual == _('Best qual.'):
            qual = 'best'
        else:
            qual = 'worst'
        res = lg.com.extract_resolution(res)
        if res:
            res = '[height<={}]'.format(res)
        result = qual + res
        mes = '"{}"'.format(result)
        sh.objs.mes(f,mes,True).debug()
        return result
    
    def set_pause(self,event=None):
        objs.pause().reset (video_id = mt.objs.videos().current()._id
                           ,pause    = mt.objs._videos.current()._pause
                           )
        objs._pause.show()
    
    def hint(self,event=None):
        f = '[Yatube] yatube.Commands.hint'
        gui = self.get_widget(event)
        if gui:
            if hasattr(gui,'lbl_img'):
                mt.objs.videos().set_gui(gui)
                length = lg.Video().length()
                length = sh.com.easy_time(length)
                pause  = mt.objs._videos.current()._pause
                if pause:
                    text  = length + ', ' + _('pause:') + ' ' \
                            + sh.com.easy_time(pause)
                    width = 210
                else:
                    text  = length
                    width = 90
                self._tip_tim = sh.ToolTip (obj   = gui.lbl_img
                                           ,text  = text
                                           ,hdir  = 'bottom'
                                           ,delay = 400
                                           )
                self._tip_tim.showtip()
            else:
                mes = _('Wrong input data!')
                sh.objs.mes(f,mes).warning()
        else:
            sh.com.empty(f)
    
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
                #NOTE: this depends on the DB fields order
                dtimes = [item[11] for item in result if item[11]]
                ftimes = [item[12] for item in result if item[12]]
                ltimes = [item[13] for item in result if item[13]]
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
        gui = self.get_widget(event)
        if gui:
            gui.cbx_vno.toggle()
            objs.commands().report_selection()
        else:
            sh.com.empty(f)
    
    def toggle_select(self,event=None):
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        if self._menu.chb_sel.get():
            for gui in guis:
                gui.cbx_vno.enable()
        else:
            for gui in guis:
                gui.cbx_vno.disable()
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
        sh.objs.root().idle()
    
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
                dtime = data[11]
                ftime = data[12]
                ltime = data[13]
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
    
    def remove_from_watchlist(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.remove_from_watchlist'
        lg.objs.db().mark_later (video_id = mt.objs.videos().current()._id
                                ,ltime    = 0
                                )
        if Unselect:
            self.unselect()
    
    def add2watchlist(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.add2watchlist'
        lg.objs.db().mark_later (video_id = mt.objs.videos().current()._id
                                ,ltime    = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
                                )
        if Unselect:
            self.unselect()
    
    def sel_add2watchlist(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.sel_add2watchlist'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                mt.objs.videos().set_gui(video_gui)
                self.add2watchlist(Unselect=Unselect)
        else:
            sh.com.empty(f)
    
    def sel_remove_from_watchlist(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.sel_remove_from_watchlist'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                if mt.objs.videos().set_gui(video_gui):
                    self.remove_from_watchlist(Unselect=Unselect)
                else:
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes).warning()
        else:
            sh.com.empty(f)
    
    def unselect(self,event=None):
        f = '[Yatube] yatube.Commands.unselect'
        gui = mt.objs.videos().current()._gui
        if gui:
            gui.cbx_vno.disable()
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
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes).warning()
        else:
            sh.com.empty(f)
    
    def unstar(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.unstar'
        lg.objs.db().mark_starred (video_id = mt.objs.videos().current()._id
                                  ,ftime    = 0
                                  )
        if Unselect:
            self.unselect()
    
    def star(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.star'
        lg.objs.db().mark_starred (video_id = mt.objs.videos().current()._id
                                  ,ftime    = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
                                  )
        if Unselect:
            self.unselect()
            
    def sel_star(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.sel_star'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                if mt.objs.videos().set_gui(video_gui):
                    self.star(Unselect=Unselect)
                else:
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes).warning()
        else:
            sh.com.empty(f)
    
    def sel_mark_not_watched(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.sel_mark_not_watched'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                if mt.objs.videos().set_gui(video_gui):
                    self.mark_not_watched(Unselect=Unselect)
                else:
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes).warning()
        else:
            sh.com.lazy(f)
    
    def sel_mark_watched(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.sel_mark_watched'
        selection = self.selection()
        if selection:
            for video_gui in selection:
                if mt.objs.videos().set_gui(video_gui):
                    self.mark_watched(Unselect=Unselect)
                else:
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes).warning()
        else:
            sh.com.lazy(f)
    
    def mark_not_watched(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.mark_not_watched'
        video = mt.objs.videos().current()
        gui   = video._gui
        if gui:
            video._dtime = 0
            lg.objs.db().mark_downloaded (video_id = video._id
                                         ,dtime    = video._dtime
                                         )
            gui.black_out()
            if Unselect:
                self.unselect()
        else:
            sh.com.empty(f)
    
    def mark_watched(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.mark_watched'
        video = mt.objs.videos().current()
        gui   = video._gui
        if gui:
            video._dtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
            lg.objs.db().mark_downloaded (video_id = video._id
                                         ,dtime    = video._dtime
                                         )
            gui.gray_out()
            self.remove_from_watchlist(Unselect=False)
            if Unselect:
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
            if gui.cbx_vno.get():
                selected.append(gui)
        return selected
    
    def set_max_videos(self,event=None):
        f = '[Yatube] yatube.Commands.set_max_videos'
        if str(self._menu.opt_max.choice).isdigit():
            mt.MAX_VIDEOS = int(self._menu.opt_max.choice)
            self.reload_channel()
        else:
            mes = _('Wrong input data: "{}"')
            mes = mes.format(self._menu.opt_max.choice)
            sh.objs.mes(f,mes).error()
    
    def tooltips(self):
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        for gui in guis:
            sh.com.bind (obj      = gui.lbl_img
                        ,bindings = '<Enter>'
                        ,action   = self.hint
                        )
    
    def prev_channel(self,event=None):
        objs.channels().dec()
        objs._channels.fetch()
    
    def next_channel(self,event=None):
        objs.channels().inc()
        objs._channels.fetch()
    
    def show_comments(self,event=None):
        f = '[Yatube] yatube.Commands.show_comments'
        Comments().show()
    
    def menu_update(self,event=None):
        f = '[Yatube] yatube.Commands.menu_update'
        default = _('Update')
        choice  = self._menu.opt_upd.choice
        if choice == default:
            sh.com.lazy(f)
        elif choice == _('Subscriptions'):
            self._menu.opt_upd.set(default)
            self.update_channels()
        elif choice == _('Channel'):
            self._menu.opt_upd.set(default)
            self.reload_channel()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(choice,';'.join(gi.update_items))
            sh.objs.mes(f,mes).error()
    
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
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(choice,';'.join(gi.view_items))
            sh.objs.mes(f,mes).error()
    
    def menu_edit(self,event=None):
        f = '[Yatube] yatube.Commands.menu_edit'
        default = _('Edit')
        choice  = self._menu.opt_edt.choice
        if choice == default:
            sh.com.lazy(f)
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
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(choice,';'.join(gi.edit_items))
            sh.objs.mes(f,mes).error()
    
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
            if objs.channels().current()._type == 'watchlist':
                self.reload_channel()
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
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(choice,';'.join(gi.selection_items))
            sh.objs.mes(f,mes).error()
    
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
        gi.objs.channel().cvs_prm.move_top()
    
    def unsubscribe(self,event=None):
        f = '[Yatube] yatube.Commands.unsubscribe'
        video = mt.objs.videos().current()
        if video._author:
            if video._author in lg.objs.lists()._subsc_auth:
                mes = _('Unsubscribe from channel "{}"')
                mes = mes.format(video._author)
                sh.objs.mes(f,mes,True).info()
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
                sh.com.lazy(f)
        else:
            sh.com.empty(f)
    
    def unblock(self,event=None):
        f = '[Yatube] yatube.Commands.unblock'
        video = mt.objs.videos().current()
        if video._author:
            if video._author in lg.objs.lists()._block_auth:
                mes = _('Unblock channel "{}"').format(video._author)
                sh.objs.mes(f,mes,True).info()
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
                sh.com.lazy(f)
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
            sh.com.lazy(f)
    
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
            mt.objs._videos.current()._gui.cbx_vno.disable()
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
            sh.Clipboard().copy(text=url)
        else:
            sh.com.empty(f)
    
    def subscribe(self,event=None):
        f = '[Yatube] yatube.Commands.subscribe'
        video = mt.objs.videos().current()
        lg.Video().play_id()
        if video._author and video._play_id:
            if video._author in lg.objs.lists()._subsc_auth:
                sh.com.lazy(f)
            else:
                mes = _('Subscribe to channel "{}"')
                mes = mes.format(video._author)
                sh.objs.mes(f,mes,True).info()
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
                sh.com.lazy(f)
            else:
                mes = _('Block channel "{}"').format(video._author)
                sh.objs.mes(f,mes,True).info()
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
            lg.objs.online()._url = lg.pattern2 + channel_id
            lg.objs._online.browse()
        else:
            sh.com.empty(f)

    def copy_channel_url(self,event=None):
        f = '[Yatube] yatube.Commands.copy_channel_url'
        channel_id = lg.Video().channel_id()
        if channel_id:
            sh.Clipboard().copy(lg.pattern2+channel_id)
        else:
            sh.com.empty(f)
    
    def stream(self,event=None):
        f = '[Yatube] yatube.Commands.stream'
        selection = self.selection()
        if selection:
            mt.objs.videos().set_gui(selection[0])
            self.stream_video()
        else:
            sh.com.empty(f)
    
    def stream_video(self,event=None):
        f = '[Yatube] yatube.Commands.stream_video'
        url = lg.Video().stream(self.quality())
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
                mes = _('Unable to find a suitable application!')
                sh.objs.mes(f,mes).warning()
            if app:
                if self._menu.chb_slw.get():
                    args = self._stream_slow(app)
                else:
                    args = self._stream(app)
                if args:
                    custom_args = [app] + self.mpv_start(app,args) \
                                        + [url]
                else:
                    custom_args = [app,url]
                #'sh.Launch' checks the target
                try:
                    subprocess.Popen(custom_args)
                    Success = True
                except Exception as e:
                    mes = _('Failed to run "{}"!\n\nDetails: {}')
                    mes = mes.format(custom_args,e)
                    sh.objs.mes(f,mes).error()
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
        #'-ao','sdl',
        if 'mpv' in app:
            return ['-fs','-framedrop=vo','-cache','8192'
                   ,'--cache-initial','1024','--no-correct-pts'
                   ]
        elif 'mplayer' in app:
            return ['-fs','-framedrop','-cache','8192','-cache-min','50'
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
            sh.com.lazy(f)
    
    def get_widget(self,event=None):
        f = '[Yatube] yatube.Commands.get_widget'
        if event:
            ''' 'event' will be 'tuple' if it's a callback from
                'Button.click'.
            '''
            if isinstance(event,tuple):
                event = event[0]
            guis = [video._gui for video in mt.objs.videos()._videos \
                    if video._gui
                   ]
            for gui in guis:
                for obj in gui._objects:
                    ''' This works for Python 3.7.3 and Tkinter 8.6.
                        In previous versions I had to use
                        'if str(obj.widget) in str(event.widget)'.
                    '''
                    if obj.widget == event.widget:
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
            elif choice == _('Set pause time'):
                self.set_pause(self)
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
                if objs.channels().current()._type == 'watchlist':
                    self.reload_channel()
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
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(choice,';'.join(gi.context_items))
                sh.objs.mes(f,mes).error()
        else:
            sh.com.empty(f)
    
    def _color_context(self,message,color='green'):
        if message in gi.objs.context().lbx_prm.lst:
            ind = gi.objs._context.lbx_prm.lst.index(message)
            gi.objs._context.lbx_prm.widget.itemconfig(ind,fg=color)
    
    def color_context(self):
        f = '[Yatube] yatube.Commands.color_context'
        if gi.objs.context().lbx_prm.lst:
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
        gui = self.get_widget(event)
        if gui:
            mt.objs.videos().set_gui(gui)
            message = _('Video #{}:').format(gui._no)
            gi.objs.context().title(message)
            items = self.update_context()
            if not items:
                items = gi.context_items
            gi.objs._context.reset(lst=items)
            self.color_context()
            gi.objs._context.show()
            self._context(gi.objs._context.get())
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
            mes = _('Switch to channel "{}"')
            mes = mes.format(self._menu.opt_chl.choice)
            sh.objs.mes(f,mes,True).info()
            if self._menu.opt_chl.choice in lg.objs.lists()._subsc_auth:
                author  = self._menu.opt_chl.choice
                no      = lg.objs._lists._subsc_auth.index(author)
                play_id = lg.objs._lists._subsc_ids[no]
                objs.channels().add('playlist',play_id)
                objs._channels.fetch()
            else:
                mes = _('Wrong input data: "{}"')
                mes = mes.format(self._menu.opt_chl.choice)
                sh.objs.mes(f,mes).error()
        
    def get_url(self,event=None):
        f = '[Yatube] yatube.Commands.get_url'
        result = self._menu.ent_url.get()
        if result:
            if result == _('Paste URL here'):
                sh.com.lazy(f)
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
                            choice = gi.objs._context.get()
                            self._context(choice)
                    else:
                        sh.com.cancel(f)
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format (self._menu.opt_url.choice
                                 ,';'.join(gi.url_items)
                                 )
                sh.objs.mes(f,mes).error()
        else:
            sh.com.empty(f)
        
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
            mes = _('Filter by "{}"').format(result)
            sh.objs.mes(f,mes,True).info()
            result = result.lower()
            for gui in guis:
                mt.objs._videos.set_gui(gui)
                if result in mt.objs._videos.current()._search:
                    gui.red_out()
        else:
            sh.com.lazy(f)
    
    def bindings(self):
        # Menu: main window
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<F1>'
                    ,action   = self.statistics
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Alt-Left>'
                    ,action   = self.prev_page
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Alt-Right>'
                    ,action   = self.next_page
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Control-p>'
                    ,action   = self.play
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Control-d>'
                    ,action   = self.download
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Control-s>'
                    ,action   = self.stream
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = ('<Control-h>','<Alt-h>')
                    ,action   = self.history
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Alt-w>'
                    ,action   = self.watchlist
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Alt-f>'
                    ,action   = self.favorites
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Shift-Delete>'
                    ,action   = self.delete_selected
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Alt-c>'
                    ,action   = self.feed
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Alt-t>'
                    ,action   = self.update_trending
                    )
        sh.com.bind (obj      = self._menu.parent
                    ,bindings = '<Alt-b>'
                    ,action   = self.blank
                    )
        # Menu: buttons
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
        sh.com.bind (obj      = self._menu.ent_flt
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.filter_view
                    )
        sh.com.bind (obj      = self._menu.ent_src
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.search_youtube
                    )
        sh.com.bind (obj      = self._menu.ent_url
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.get_url
                    )
        # Menu: checkboxes
        self._menu.chb_dat.widget.config(command=self.filter_by_date)
        
        # Menu: OptionMenus
        ''' Updating selection menu is slow, so we run it only when
            clicking 'opt_sel' and not in 'self.report_selection'.
            This is a binding to the entire OptionMenu and will not
            interfere with bindings to OptionMenu items.
        '''
        sh.com.bind (obj      = self._menu.opt_sel
                    ,bindings = '<Button-1>'
                    ,action   = self.update_sel_menu
                    )
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
        guis  = [item._gui for item in mt.objs._videos._videos \
                 if item._gui
                ]
        for gui in guis:
            mt.objs._videos.set_gui(gui)
            # Drop all previous selections
            gui.cbx_vno.disable()
            if self._menu.chb_dat.get():
                cond = not video._dtime and not video.Block and \
                       self._date_filter()
            else:
                cond = not video._dtime and not video.Block
            if cond:
                gui.cbx_vno.enable()
        self.report_selection()
        
    def mpv_start(self,app,lst=[]):
        pause = mt.objs.videos().current()._pause
        if 'mpv' in app and pause:
            ''' 'mpv' already resumes about 2s prior to an actual pause,
                so we don't have to additionaly tune the pause to remind
                a user what is happening on the screen.
            '''
            lst += ['--start={}'.format(sh.com.easy_time(pause))]
        return lst
    
    def _play_slow(self,app='/usr/bin/mpv'):
        if 'mpv' in app:
            custom_args = ['-fs','-framedrop=vo','--no-correct-pts']
        elif 'mplayer' in app:
            custom_args = ['-fs','-framedrop','-nocorrect-pts']
        else:
            custom_args = []
        sh.Launch (target = lg.Video().path()
                  ).app (custom_app  = app
                        ,custom_args = self.mpv_start(app,custom_args)
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
            sh.com.lazy(f)
        
    def mark_downloaded(self,Unselect=True):
        f = '[Yatube] yatube.Commands.mark_downloaded'
        video = mt.objs.videos().current()
        video._dtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
        lg.objs.db().mark_downloaded (video_id = video._id
                                     ,dtime    = video._dtime
                                     )
        self.remove_from_watchlist(Unselect=False)
        if video._gui:
            video._gui.gray_out()
            if Unselect:
                self.unselect()
    
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
                    sh.Geometry(gi.objs._progress.obj).activate()
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
            sh.com.empty(f)
        
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
            mes = _('Switch to channel "{}"').format(choice)
            sh.objs.mes(f,mes,True).info()
            if choice in lg.objs.const()._countries:
                country = lg.objs._const._countries[choice]
            else:
                country = 'RU'
            mes = _('Country: {}').format(country)
            sh.objs.mes(f,mes,True).debug()
        self.update_trending(country=country)
        
    def reset_channel_gui(self):
        # Clears the old Channel widget
        guis = [video._gui for video in mt.objs.videos()._videos \
                if video._gui
               ]
        for gui in guis:
            gui.frm_prm.widget.destroy()
        self._menu.title()
        #todo: rework
        #self.save_url()
    
    def fill_default(self):
        f = '[Yatube] yatube.Commands.fill_default'
        # Operation takes ~0,56s but there seems nothing to speed up
        #timer = sh.Timer(f)
        #timer.start()
        gi.objs.channel(gi.objs.menu().framev)
        if mt.objs.videos()._videos:
            for i in range(len(mt.objs._videos._videos)):
                mt.objs._videos.i = i
                mt.objs._videos._videos[i]._gui = objs.videos().add(no=i+1)
        else:
            sh.com.empty(f)
        #timer.end()
            
    def dimensions(self):
        f = '[Yatube] yatube.Commands.dimensions'
        sh.objs.root().idle()
        height = gi.objs._channel.frm_emb.reqheight()
        ''' #NOTE: Extra space can be caused by a difference of
            the default and loaded pictures.
        '''
        mes = _('Widget must be at least {} pixels in height')
        mes = mes.format(height)
        sh.objs.mes(f,mes,True).debug()
        gi.objs._channel.cvs_prm.region (x        = 1024
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
                lg.Video().new()
                self.update_video(i=unknown[i])
            lg.objs.db().save()
        else:
            sh.com.lazy(f)
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
    
    def update_video(self,i=0):
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
            if video._pause:
                video._gui.green_out()
            if i > 0:
                #todo: renumber
                pass
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
                mes = _('{}/{} links are already stored in DB.')
                mes = mes.format(len(matches),len(ids))
                sh.objs.mes(f,mes,True).info()
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
        gi.objs._channel.cvs_prm.widget.xview_moveto(0)
        self.fill_known()
        ''' The less we use GUI update, the faster will be the program.
            Updating tkinter idle tasks may take ~0,4-1,7s, but this
            must be done after creating all video widgets and
            reading/updating images.
        '''
        sh.objs.root().idle()
        if Unknown:
            self.fill_unknown()
        # Using the canvas is fast, no need to time this
        objs.videos().bindings()
        self.dimensions()
        gi.objs._channel.cvs_prm.move_top()
        gi.objs._channel.cvs_prm.widget.xview_moveto(0)
        # Move focus away from 'ttk.Combobox' (OptionMenu)
        gi.objs._channel.cvs_prm.focus()
        self.tooltips()
    
    def manage_sub(self):
        objs.add_id().reset()
        objs._add_id.show()
        self.reset_channels()
                             
    def manage_blocked_authors(self,event=None):
        f = '[Yatube] yatube.Commands.manage_blocked_authors'
        words = sh.Words(text=lg.objs.lists()._block)
        gi.objs.blacklist().reset(words=words)
        gi.objs._blacklist.insert(text=lg.objs._lists._block)
        gi.objs._blacklist.show()
        text = gi.objs._blacklist.get()
        # We should allow an empty input
        if gi.objs._blacklist.Save:
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
                text = '# ' + _('Put here authors to be blocked')
                sh.WriteTextFile (file    = lg.objs.default()._fblock
                                 ,Rewrite = True
                                 ).write(text=text)
            lg.objs._lists.reset()
        else:
            mes = _('Operation has been canceled by the user.')
            sh.objs.mes(f,mes,True).info()
    
    def manage_blocked_words(self,event=None):
        f = '[Yatube] yatube.Commands.manage_blocked_words'
        words = sh.Words(text=lg.objs.lists()._blockw)
        gi.objs.blacklist().reset(words=words)
        gi.objs._blacklist.insert(text=lg.objs._lists._blockw)
        gi.objs._blacklist.show()
        text = gi.objs._blacklist.get()
        # We should allow an empty input
        if gi.objs._blacklist.Save:    
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
                text = '# ' + _('Put here words to block in titles (case is ignored)')
                sh.WriteTextFile (file    = lg.objs.default()._fblockw
                                 ,Rewrite = True
                                 ).write(text=text)
            lg.objs._lists.reset()
        else:
            mes = _('Operation has been canceled by the user.')
            sh.objs.mes(f,mes,True).info()



class Objects:
    
    def __init__(self):
        self._videos = self._add_id = self._commands = self._channels \
                     = self._pause = None
    
    def pause(self):
        if self._pause is None:
            self._pause = Pause()
        return self._pause
    
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


objs = Objects()


if __name__ == '__main__':
    f = '[Yatube] yatube.__main__'
    sh.com.start()
    sh.Geometry(gi.objs.parent()).set('1024x600')
    lg.objs.default(product='yatube')
    if lg.objs._default.Success:
        objs.commands().bindings()
        gi.objs.menu().opt_max.set(mt.MAX_VIDEOS)
        gi.objs._menu.show()
        lg.objs.db().save()
        lg.objs._db.close()
    else:
        mes = _('Unable to continue due to an invalid configuration.')
        sh.objs.mes(f,mes).warning()
    objs.commands().statistics(Silent=True)
    mes = _('Goodbye!')
    sh.objs.mes(f,mes,True).debug()
    sh.com.end()
