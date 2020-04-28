#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import subprocess
import skl_shared.shared as sh
import logic             as lg
import gui               as gi
import meta              as mt
from skl_shared.localize import _


class Config:
    
    def __init__(self):
        ''' Do not use 'super' here since 'lg.Config' and
            'lg.DefaultConfig' are widely used in 'logic'.
        '''
        self.Success = lg.objs.get_config().Success
    
    def set(self):
        f = '[Yatube] yatube.Config.set'
        if self.Success:
            mes = _('Update config options')
            sh.objs.get_mes(f,mes,True).show_info()
            try:
                sh.lg.config_parser.set (sh.lg.SectionIntegers
                                        ,'max_videos'
                                        ,gi.objs.get_menu().opt_max.choice
                                        )
                choice = gi.objs.menu.opt_res.choice
                if choice == _('Auto'):
                    choice = 'auto'
                sh.lg.config_parser.set (sh.lg.SectionVariables
                                        ,'resolution'
                                        ,choice
                                        )
                choice = gi.objs.menu.opt_qal.choice
                if choice == _('Best qual.'):
                    choice = 'best'
                elif choice == _('Worst qual.'):
                    choice = 'worst'
                sh.lg.config_parser.set (sh.lg.SectionVariables
                                        ,'quality'
                                        ,choice
                                        )
            except Exception as e:
                self.Success = False
                mes = _('Third-party module has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.cancel(f)
    
    def save(self):
        f = '[Yatube] yatube.Config.save'
        if self.Success:
            mes = _('Save config options')
            sh.objs.get_mes(f,mes,True).show_info()
            try:
                with open(lg.objs.get_config().path,'w') as cf:
                    sh.lg.config_parser.write(cf)
            except Exception as e:
                self.Success = False
                mes = _('Third-party module has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.cancel(f)
    
    def restore_keys(self):
        f = '[Yatube] yatube.Config.restore_keys'
        if self.Success:
            mt.MAX_VIDEOS = sh.lg.globs['int']['max_videos']
            gi.objs.get_menu().opt_max.set(mt.MAX_VIDEOS)
            if sh.lg.globs['var']['quality'] == 'worst':
                gi.objs.menu.opt_qal.set(_('Worst qual.'))
            else:
                gi.objs.menu.opt_qal.set(_('Best qual.'))
            if sh.lg.globs['var']['resolution'] == 'auto':
                choice = _('Auto')
            else:
                choice = sh.lg.globs['var']['resolution']
            gi.objs.menu.opt_res.set(choice)
        else:
            sh.com.cancel(f)



class Pause:
    
    def __init__(self):
        self.set_values()
        self.gui = gi.Pause()
        self.set_bindings()
    
    def set_values(self):
        self.id_   = ''
        self.pause = 0
    
    def delete(self,event=None):
        lg.objs.get_db().update_pause(self.id_)
        mt.objs.get_videos().get_current().pause = 0
        self.close()
        objs.get_commands().mark_watched(Unselect=False)
        objs.commands.remove_from_watchlist(Unselect=False)
        if objs.get_channels().get_current().type_ == 'watchlist':
            objs.commands.reload_channel()
        else:
            objs.commands.update_video()
    
    def reset(self,videoid,pause):
        self.id_   = videoid
        self.pause = pause
        self.fill()
    
    def fill(self,event=None):
        hours, minutes, seconds = sh.com.split_time(self.pause)
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
        mt.objs.get_videos().get_current().pause = all_sec
        lg.objs.get_db().update_pause (videoid = self.id_
                                      ,pause   = all_sec
                                      )
        self.close()
        objs.get_commands().mark_not_watched(Unselect=False)
        objs.commands.add2watchlist(Unselect=False)
        if objs.get_channels().get_current().type_ == 'watchlist':
            objs.commands.reload_channel()
        else:
            objs.commands.update_video()
    
    def set_bindings(self):
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
        seconds = sh.Input(f,self.gui.ent_sec.get()).get_integer()
        # 'sh.Input.integer' already throws an error at negative values
        if seconds > 59:
            sub = '0 <= {} <= 59'.format(seconds)
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_warning()
            seconds = 59
            self.gui.ent_sec.reset()
            self.gui.ent_sec.insert(seconds)
        return seconds
    
    def get_min(self,event=None):
        f = '[Yatube] yatube.Pause.get_min'
        minutes = sh.Input(f,self.gui.ent_min.get()).get_integer()
        if 0 <= minutes <= 59:
            pass
        else:
            sub = '0 <= {} <= 59'.format(minutes)
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_warning()
            if minutes > 59:
                minutes = 59
            else:
                minutes = 0
            self.gui.ent_min.reset()
            self.gui.ent_min.insert(minutes)
        return minutes
    
    def get_hrs(self,event=None):
        f = '[Yatube] yatube.Pause.get_hrs'
        return sh.Input(f,self.gui.ent_hrs.get()).get_integer()
    
    def update(self,event=None):
        self.upd_hrs()
        self.upd_min()
        self.upd_sec()
    
    def upd_sec(self,event=None):
        seconds = self.get_sec()
        if seconds < 59:
            self.gui.btn_scu.activate()
        else:
            self.gui.btn_scu.inactivate()
        if seconds > 0:
            self.gui.btn_scd.activate()
        else:
            self.gui.btn_scd.inactivate()
    
    def upd_min(self,event=None):
        minutes = self.get_min()
        if minutes < 59:
            self.gui.btn_mnu.activate()
        else:
            self.gui.btn_mnu.inactivate()
        if minutes > 0:
            self.gui.btn_mnd.activate()
        else:
            self.gui.btn_mnd.inactivate()
    
    def upd_hrs(self,event=None):
        self.gui.btn_hru.activate()
        if self.get_hrs() > 0:
            self.gui.btn_hrd.activate()
        else:
            self.gui.btn_hrd.inactivate()
    
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
        self.type_ = 'extractor'
        self.url   = ''
        if url:
            self.reset(url)
    
    def fetch(self):
        f = '[Yatube] yatube.Extractor.fetch'
        objs.get_commands().reset_channel_gui()
        lg.objs.get_extractor().run()
        if lg.objs.extractor.urls:
            mt.objs.get_videos().reset()
            ''' We put a limit here just not to hang the program.
                Potential limit (after which GUI may freeze) may be
                around 500 videos. Moreover, each extracted video ID
                adds up quota.
            '''
            ids = list(lg.objs.extractor.urls)[:200]
            for vid in lg.objs.extractor.urls:
                video = mt.Video()
                video.id_ = vid
                mt.objs.get_videos().add(video)
            objs.commands.set_channel_gui()
        else:
            sh.com.rep_lazy(f)
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Extractor.fetch_prev'
        sh.com.rep_lazy(f)
    
    def fetch_next(self):
        f = '[Yatube] yatube.Extractor.fetch_next'
        sh.com.rep_lazy(f)
    
    def reset(self,url):
        self.url = url
        lg.objs.get_extractor().reset(url=self.url)



class Trending:
    
    def __init__(self,country=''):
        self.set_values()
        if country:
            self.reset(country)
    
    def set_values(self):
        self.type_   = 'trending'
        self.country = ''
    
    def fetch(self):
        mt.objs.get_trending().run()
        objs.commands.set_channel_gui()
    
    def fetch_prev(self):
        mt.objs.get_trending().fetch_prev()
        mt.objs.trending.get_videos()
        objs.commands.set_channel_gui()
    
    def fetch_next(self):
        mt.objs.get_trending().fetch_next()
        mt.objs.trending.get_videos()
        objs.commands.set_channel_gui()
    
    def reset(self,country):
        self.country = country
        mt.objs.get_trending().reset(self.country)



class Feed:
    
    def __init__(self):
        self.type_ = 'feed'
    
    def fetch(self):
        lg.objs.get_feed().fetch()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.feed.get_token()
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Feed.fetch_prev'
        lg.objs.get_feed().fetch_prev()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.feed.get_token()
    
    def fetch_next(self):
        f = '[Yatube] yatube.Feed.fetch_next'
        lg.objs.get_feed().fetch_next()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.feed.get_token()



class Search:
    
    def __init__(self,query=''):
        self.set_values()
        if query:
            self.reset(query)
    
    def set_values(self):
        self.type_ = 'search'
        self.query = ''
    
    def fetch(self):
        mt.objs.get_search().run()
        objs.commands.set_channel_gui()
    
    def fetch_prev(self):
        mt.objs.get_search().fetch_prev()
        mt.objs.search.get_videos()
        objs.commands.set_channel_gui()
    
    def fetch_next(self):
        mt.objs.get_search().fetch_next()
        mt.objs.search.get_videos()
        objs.commands.set_channel_gui()
    
    def reset(self,query):
        self.query = query
        mt.objs.get_search().reset(self.query)



class Videos:
    ''' Currently this class comprises some controller-specific
        functionality of 'gi.Video'.
    '''
    def __init__(self):
        pass
    
    def set_bindings(self):
        guis = [video.gui for video in mt.objs.get_videos().videos \
                if video.gui
               ]
        for gui in guis:
            gui.cbx_vno.action = objs.get_commands().report_selection
            for obj in gui.objects:
                sh.com.bind (obj      = obj
                            ,bindings = '<ButtonRelease-1>'
                            ,action   = objs.commands.toggle_cbox
                            )
                sh.com.bind (obj      = obj
                            ,bindings = '<ButtonRelease-3>'
                            ,action   = objs.commands.get_context
                            )
    
    def add(self,no=1):
        return gi.Video (parent = gi.objs.get_channel().frm_emb
                        ,no     = no
                        )



class Favorites:
    
    def __init__(self):
        self.type_ = 'favorites'
    
    def fetch(self):
        lg.objs.get_favorites().fetch()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.favorites.get_token()
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Favorites.fetch_prev'
        lg.objs.get_favorites().fetch_prev()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.favorites.get_token()
    
    def fetch_next(self):
        f = '[Yatube] yatube.Favorites.fetch_next'
        lg.objs.get_favorites().fetch_next()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.favorites.get_token()



class Watchlist:
    
    def __init__(self):
        self.type_ = 'watchlist'
    
    def fetch(self):
        lg.objs.get_watchlist().fetch()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.watchlist.get_token()
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Watchlist.fetch_prev'
        lg.objs.get_watchlist().fetch_prev()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.watchlist.get_token()
    
    def fetch_next(self):
        f = '[Yatube] yatube.Watchlist.fetch_next'
        lg.objs.get_watchlist().fetch_next()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.watchlist.get_token()



class Playlist:
    
    def __init__(self,playid=''):
        self.type_  = 'playlist'
        self.playid = ''
        if playid:
            self.reset(playid)
    
    def fetch(self):
        mt.objs.get_playlist().run()
        objs.commands.set_channel_gui()
    
    def fetch_prev(self):
        mt.objs.get_playlist().fetch_prev()
        mt.objs.playlist.set_videos()
        objs.commands.set_channel_gui()
    
    def fetch_next(self):
        mt.objs.get_playlist().fetch_next()
        mt.objs.playlist.set_videos()
        objs.commands.set_channel_gui()
    
    def reset(self,playid):
        self.playid = playid
        mt.objs.get_playlist().reset(playid)



class Channels:
    
    def __init__(self):
        self.channels = []
        self.modes    = ('favorites','feed','history','playlist'
                        ,'search','trending','watchlist','extractor'
                        )
        self.unique   = ('favorites','feed','history','watchlist')
        self.types    = []
        self.i        = 0
    
    def inc(self):
        if self.i == len(self.channels) - 1:
            self.i = 0
        elif self.channels:
            self.i += 1
    
    def dec(self):
        if self.i == 0:
            if self.channels:
                self.i = len(self.channels) - 1
        else:
            self.i -= 1
    
    def get_current(self):
        f = '[Yatube] yatube.Channels.get_current'
        if not self.channels:
            sh.com.rep_empty(f)
            self.add('history')
        if self.i < 0 or self.i >= len(self.channels):
            sub = '0 <= {} < {}'.format(self.i,len(self.channels))
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_error()
            self.i = 0
        return self.channels[self.i]
    
    def go_mode(self,mode):
        f = '[Yatube] yatube.Channels.go_mode'
        types = [channel.type_ for channel in self.channels]
        if types:
            if mode in types:
                self.i = types.index(mode)
            else:
                mes = _('Wrong input data: "{}"!').format(mode)
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.rep_empty(f)
    
    def add(self,mode='playlist',arg=None):
        f = '[Yatube] yatube.Channels.add'
        if mode in self.unique and mode in self.types:
            self.go_mode(mode)
        elif mode in self.modes:
            if mode == 'playlist':
                self.channels.append(Playlist(arg))
            elif mode == 'trending':
                self.channels.append(Trending(arg))
            elif mode == 'feed':
                self.channels.append(Feed())
            elif mode == 'search':
                self.channels.append(Search(arg))
            elif mode == 'favorites':
                self.channels.append(Favorites())
            elif mode == 'watchlist':
                self.channels.append(Watchlist())
            elif mode == 'history':
                self.channels.append(History())
            elif mode == 'extractor':
                self.channels.append(Extractor(arg))
            self.inc()
        else:
            mes = _('Wrong input data: "{}"!').format(mode)
            sh.objs.get_mes(f,mes).show_error()
    
    def fetch(self):
        f = '[Yatube] yatube.Channels.fetch'
        if self.channels:
            timer = sh.Timer(f)
            timer.start()
            objs.get_commands().reset_channel_gui()
            mt.objs.get_videos().reset()
            self.get_current().fetch()
            timer.end()
        else:
            sh.com.rep_empty(f)
    
    def fetch_prev(self):
        f = '[Yatube] yatube.Channels.fetch_prev'
        if self.channels:
            timer = sh.Timer(f)
            timer.start()
            objs.get_commands().reset_channel_gui()
            mt.objs.get_videos().reset()
            self.get_current().fetch_prev()
            timer.end()
        else:
            sh.com.rep_empty(f)
    
    def fetch_next(self):
        f = '[Yatube] yatube.Channels.fetch_next'
        if self.channels:
            timer = sh.Timer(f)
            timer.start()
            objs.get_commands().reset_channel_gui()
            mt.objs.get_videos().reset()
            self.get_current().fetch_next()
            timer.end()
        else:
            sh.com.rep_empty(f)



class History:
    
    def __init__(self):
        self.type_ = 'history'
    
    def fetch(self):
        lg.objs.get_history().fetch()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.history.get_token()
    
    def fetch_prev(self):
        f = '[Yatube] yatube.History.fetch_prev'
        lg.objs.get_history().fetch_prev()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.history.get_token()
    
    def fetch_next(self):
        f = '[Yatube] yatube.History.fetch_next'
        lg.objs.get_history().fetch_next()
        objs.commands.set_channel_gui(Unknown=False)
        lg.objs.history.get_token()



class AddId:
    
    def __init__(self):
        self.set_values()
        self.gui = gi.AddId()
        self.set_bindings()
    
    def save_close(self,event=None):
        self.save()
        self.close()
    
    def open(self,event=None):
        f = '[Yatube] yatube.AddId.open'
        author = self.gui.lst_id1.get()
        if author:
            ind = self.gui.lst_id1.lst.index(author)
            ''' 'myid' will be a valid playlist ID since incorrect
                values are not added when using 'AddId'.
            '''
            myid = self.gui.lst_id3.lst[ind]
            url = 'https://www.youtube.com/playlist?list={}'.format(myid)
            ionline = sh.Online()
            ionline.url = url
            ionline.browse()
        else:
            sh.com.rep_empty(f)
    
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
            sh.com.rep_empty(f)
    
    def set_values(self):
        self.author = ''
        self.id_    = ''
    
    def add_record(self,mode='user'):
        f = '[Yatube] yatube.AddId.add_record'
        id1 = self.gui.lst_id1.lst
        id2 = self.gui.lst_id2.lst
        id3 = self.gui.lst_id3.lst
        if self.author in id1:
            mes = _('"{}" is already in the list!').format(self.author)
            sh.objs.get_mes(f,mes).show_info()
        else:
            ind = len(id1)
            Success = True
            if mode == 'playid':
                id3.insert(ind,self.id_)
            elif mode == 'channel_id':
                mt.objs.get_playid().reset(self.id_)
                result = mt.objs.playid.get_by_channel_id()
                if result:
                    id3.insert(ind,result)
                else:
                    Success = False
                    sh.com.rep_empty(f)
            elif mode == 'user':
                mt.objs.get_playid().reset(self.id_)
                result = mt.objs.playid.get_by_user()
                if result:
                    id3.insert(ind,result)
                else:
                    Success = False
                    sh.com.rep_empty(f)
            else:
                Success = False
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(mode,'playid; channel_id; user')
                sh.objs.get_mes(f,mes).show_error()
            if Success:
                id1.insert(ind,self.author)
                id2.insert(ind,self.id_)
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
        self.author = self.gui.ent_ath.get()
        self.id_    = self.gui.ent_pid.get()
        self.author = self.author.strip()
        self.id_    = self.id_.strip()
        if self.author and self.id_:
            if self.id_.startswith('UU') and len(self.id_) == 24:
                self.add_record('playid')
            elif self.id_.startswith('UC') and len(self.id_) == 24:
                self.add_record('channel_id')
            else:
                self.add_record('user')
        else:
            sh.com.rep_empty(f)
    
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
    
    def set_bindings(self):
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
        lg.objs.get_lists().reset()
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
        sh.WriteTextFile (file    = lg.objs.get_default().fsubsc
                         ,Rewrite = True
                         ).write(text)
        lg.objs.lists.reset()
    
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
        id1 = lg.objs.get_lists().subauth
        id2 = '?' * len(lg.objs.lists.subauth)
        id3 = lg.objs.lists.subids
        if len(id1) == len(id2) == len(id3):
            pass
        else:
            sub = '{} = {} = {}'.format(len(id1),len(id2),len(id3))
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_warning()
        self.gui.lst_id1.reset(lst=id1)
        self.gui.lst_id2.reset(lst=id2)
        self.gui.lst_id3.reset(lst=id3)



class Comments:
    
    def __init__(self):
        ''' Since comments are loaded partly, we should not rely
            on 'self.logic.texts'. We should also not rely on a total
            number of comments reported by 'VideoInfo' since there is
            no quota-efficient way to fetch all of these comments (some
            comments will eventually be missing, and a predicted number
            of screens will mismatch a factual number). Therefore, we
            should not show the number of comments in GUI at all.
        '''
        self.set_values()
        self.gui   = gi.Comments()
        self.logic = mt.Comments()
        self.set_bindings()
        self.reset()
    
    def set_values(self):
        self.Success = True
    
    def set_bindings(self):
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = '<Alt-Left>'
                    ,action   = self.get_prev
                    )
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = '<Alt-Right>'
                    ,action   = self.get_next
                    )
        sh.com.bind (obj      = self.gui.parent
                    ,bindings = ('<Escape>','<Control-w>','<Control-q>')
                    ,action   = self.close
                    )
        sh.com.bind (obj      = self.gui.txt_com
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.get_next
                    )
        self.gui.btn_prv.action = self.get_prev
        self.gui.btn_nxt.action = self.get_next
        self.gui.widget.protocol('WM_DELETE_WINDOW',self.close)
    
    def get_prev(self,event=None):
        f = '[Yatube] yatube.Comments.get_prev'
        if self.Success:
            self.logic.fetch_prev()
            self.update()
        else:
            sh.com.cancel(f)
    
    def get_next(self,event=None):
        f = '[Yatube] yatube.Comments.get_next'
        if self.Success:
            self.logic.fetch_next()
            self.update()
        else:
            sh.com.cancel(f)
    
    def reset(self):
        f = '[Yatube] yatube.Comments.reset'
        ''' We believe that the 'videoid' format should be checked
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
            if self.logic.texts:
                if self.logic.i == 0:
                    self.gui.btn_prv.inactivate()
                elif self.logic.i > 0:
                    self.gui.btn_prv.activate()
                if self.logic.next \
                or self.logic.i + 1 < len(self.logic.texts):
                    self.gui.btn_nxt.activate()
                else:
                    self.gui.btn_nxt.inactivate()
            else:
                self.gui.btn_prv.inactivate()
                self.gui.btn_nxt.inactivate()
        else:
            sh.com.cancel(f)
    
    def update_text(self):
        f = '[Yatube] yatube.Comments.update_text'
        if self.Success:
            if self.logic.texts:
                try:
                    text = self.logic.texts[self.logic.i]
                except IndexError:
                    text = ''
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes).show_warning()
                text = sh.Text(text).delete_unsupported()
                # A new line is inserted when read from the widget
                text     = text.strip()
                text     = sh.Text(text).convert_line_breaks()
                old_text = self.gui.txt_com.get()
                old_text.strip()
                # Keep a scrollbar position if there are no pages left
                if old_text != text:
                    self.gui.txt_com.enable()
                    self.gui.txt_com.reset()
                    self.gui.txt_com.insert(text)
                    self.gui.txt_com.disable()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()



class Commands:
    
    def __init__(self):
        self.mode     = None
        self.tstamp   = None
        self.tip_tim  = None
        self.FirstVid = True
        self.menu     = gi.objs.get_menu()
        itime         = lg.Time()
        itime.set_date(DaysDelta=7)
        itime.get_years()
        itime.get_months()
        itime.get_days()
        self.years  = itime.years
        self.year   = itime.year
        self.months = itime.months
        self.month  = itime.month
        self.days   = itime.days
        self.day    = itime.day
        lg.objs.get_lists().reset()
        self.reset_channels()
    
    def get_quality(self,event=None):
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
        f = '[Yatube] yatube.Commands.get_quality'
        qual = gi.objs.get_menu().opt_qal.choice
        res  = gi.objs.menu.opt_res.choice
        if qual == _('Best qual.'):
            qual = 'best'
        else:
            qual = 'worst'
        res = lg.com.extract_resolution(res)
        if res:
            res = '[height<={}]'.format(res)
        result = qual + res
        mes = '"{}"'.format(result)
        sh.objs.get_mes(f,mes,True).show_debug()
        return result
    
    def set_pause(self,event=None):
        objs.get_pause().reset (videoid = mt.objs.get_videos().get_current().id_
                               ,pause   = mt.objs.videos.get_current().pause
                               )
        objs.pause.show()
    
    def set_hint(self,event=None):
        f = '[Yatube] yatube.Commands.set_hint'
        gui = self.get_widget(event)
        if gui:
            if hasattr(gui,'lbl_img'):
                mt.objs.get_videos().set_gui(gui)
                length = lg.Video().get_length()
                length = sh.com.get_easy_time(length)
                pause  = mt.objs.videos.get_current().pause
                if pause:
                    text  = length + ', ' + _('pause:') + ' ' \
                            + sh.com.get_easy_time(pause)
                    width = 210
                else:
                    text  = length
                    width = 90
                self.tip_tim = sh.ToolTip (obj   = gui.lbl_img
                                          ,text  = text
                                          ,hdir  = 'bottom'
                                          ,delay = 400
                                          )
                self.tip_tim.showtip()
            else:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def update_sel_menu(self,event=None):
        f = '[Yatube] yatube.Commands.update_sel_menu'
        selection = self.get_sel()
        if selection:
            items = list(gi.selection_items)
            Found = False
            for gui in selection:
                mt.objs.get_videos().set_gui(gui)
                path = lg.Video().get_path()
                if path and os.path.exists(path):
                    Found = True
                    break
            if not Found:
                items.remove(_('Delete selected'))
            ids = []
            for gui in selection:
                mt.objs.videos.set_gui(gui)
                ids.append(mt.objs.videos.get_current().id_)
            result = lg.objs.get_db().get_videos(ids)
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
        self.menu.opt_sel.reset (items   = list(items)
                                ,default = _('Selection')
                                )
    
    def toggle_cbox(self,event=None):
        f = '[Yatube] Commands.toggle_cbox'
        gui = self.get_widget(event)
        if gui:
            gui.cbx_vno.toggle()
            objs.get_commands().report_selection()
        else:
            sh.com.rep_empty(f)
    
    def toggle_select(self,event=None):
        guis = [video.gui for video in mt.objs.get_videos().videos \
                if video.gui
               ]
        if self.menu.chb_sel.get():
            for gui in guis:
                gui.cbx_vno.enable()
        else:
            for gui in guis:
                gui.cbx_vno.disable()
        self.report_selection()
    
    def report_selection(self,event=None):
        selection = self.get_sel()
        if selection:
            count = len(selection)
        else:
            count = 0
        self.menu.set_title (selected = count
                            ,total    = len(mt.objs.get_videos().videos)
                            )
    
    def show_stat(self,event=None,Silent=False):
        mt.objs.get_stat().report(Silent=Silent)
    
    def show_progress(self,data):
        ''' Depending on situation, youtube_dl may not provide some keys,
            so be aware of KeyError.
        '''
        if 'total_bytes' in data:
            total = data['total_bytes']
        else:
            total = 0
        if 'downloaded_bytes' in data:
            cursize = data['downloaded_bytes']
        else:
            cursize = 0
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
        if cursize is None:
            cursize = 0
        if eta is None:
            eta = 0
        if rate is None:
            rate = 0
        total   = total    / 1000000
        cursize = cursize / 1000000
        # Prevent ZeroDivisionError
        if total:
            percent = round((100*cursize)/total)
        else:
            percent = 0
        gi.objs.get_progress().item.widget['value'] = percent
        rate = int(rate) // 1000
        # Prevent from irritating message length changes
        rate = sh.Text(text=str(rate)).grow (max_len = 4
                                            ,FromEnd = False
                                            )
        eta = sh.Text(text=str(eta)).grow (max_len = 3
                                          ,FromEnd = False
                                          )
        gi.objs.progress.item.set_text (file    = mt.objs.get_videos().get_current().pathsh
                                       ,cursize = cursize
                                       ,total   = total
                                       ,rate    = rate
                                       ,eta     = eta
                                       )
        # This is required to fill the progress bar on-the-fly
        sh.objs.get_root().update_idle()
    
    def show_history(self,event=None):
        objs.get_channels().add('history')
        objs.channels.fetch()
    
    def update_context(self):
        f = '[Yatube] yatube.Commands.update_context'
        video = mt.objs.get_videos().get_current()
        if video:
            items = list(gi.context_items)
            data = lg.objs.get_db().get_video(video.id_)
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
                sh.com.rep_empty(f)
            if video.Block:
                items.remove(_('Block this channel'))
            else:
                items.remove(_('Unblock'))
            lg.Video().get_path()
            if video.path:
                if os.path.exists(video.path):
                    items.remove(_('Download'))
                else:
                    items.remove(_('Delete the downloaded file'))
            else:
                sh.com.rep_empty(f)
            if video.author:
                if video.author in lg.objs.get_lists().subauth:
                    items.remove(_('Subscribe to this channel'))
                else:
                    items.remove(_('Unsubscribe'))
            else:
                sh.com.rep_empty(f)
            return items
        else:
            sh.com.rep_empty(f)
    
    def reload_channel(self,event=None):
        objs.get_channels().fetch()
    
    def show_feed(self,event=None):
        objs.get_channels().add('feed')
        objs.channels.fetch()
    
    def show_prev_page(self,event=None):
        objs.get_channels().fetch_prev()
    
    def show_next_page(self,event=None):
        objs.get_channels().fetch_next()
    
    def show_watchlist(self,event=None):
        objs.get_channels().add('watchlist')
        objs.channels.fetch()
    
    def show_favorites(self,event=None):
        objs.get_channels().add('favorites')
        objs.channels.fetch()
    
    def remove_from_watchlist(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.remove_from_watchlist'
        ivideo = mt.objs.get_videos().get_current()
        lg.objs.get_db().mark_later (videoid = ivideo.id_
                                    ,ltime   = 0.0
                                    )
        ivideo.ltime = 0.0
        ivideo.pause = 0
        lg.objs.get_db().update_pause (videoid = ivideo.id_
                                      ,pause   = ivideo.pause
                                      )
        if Unselect:
            self.unselect()
    
    def add2watchlist(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.add2watchlist'
        lg.objs.get_db().mark_later (videoid = mt.objs.get_videos().get_current().id_
                                    ,ltime   = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
                                )
        if Unselect:
            self.unselect()
    
    def sel_add2watchlist(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.sel_add2watchlist'
        selection = self.get_sel()
        if selection:
            for video_gui in selection:
                mt.objs.get_videos().set_gui(video_gui)
                self.add2watchlist(Unselect=Unselect)
        else:
            sh.com.rep_empty(f)
    
    def sel_remove_from_watchlist(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.sel_remove_from_watchlist'
        selection = self.get_sel()
        if selection:
            for video_gui in selection:
                if mt.objs.get_videos().set_gui(video_gui):
                    self.remove_from_watchlist(Unselect=Unselect)
                else:
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def unselect(self,event=None):
        f = '[Yatube] yatube.Commands.unselect'
        gui = mt.objs.get_videos().get_current().gui
        if gui:
            gui.cbx_vno.disable()
            self.report_selection()
        else:
            sh.com.rep_empty(f)
    
    def sel_unstar(self,event=None):
        f = '[Yatube] yatube.Commands.sel_unstar'
        selection = self.get_sel()
        if selection:
            for video_gui in selection:
                if mt.objs.get_videos().set_gui(video_gui):
                    self.unstar()
                else:
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def unstar(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.unstar'
        lg.objs.get_db().mark_starred (videoid = mt.objs.get_videos().get_current().id_
                                      ,ftime    = 0
                                      )
        if Unselect:
            self.unselect()
    
    def star(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.star'
        lg.objs.get_db().mark_starred (videoid = mt.objs.get_videos().get_current().id_
                                      ,ftime   = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
                                      )
        if Unselect:
            self.unselect()
            
    def sel_star(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.sel_star'
        selection = self.get_sel()
        if selection:
            for video_gui in selection:
                if mt.objs.get_videos().set_gui(video_gui):
                    self.star(Unselect=Unselect)
                else:
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def sel_mark_not_watched(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.sel_mark_not_watched'
        selection = self.get_sel()
        if selection:
            for video_gui in selection:
                if mt.objs.get_videos().set_gui(video_gui):
                    self.mark_not_watched(Unselect=Unselect)
                else:
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_lazy(f)
    
    def sel_mark_watched(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.sel_mark_watched'
        selection = self.get_sel()
        if selection:
            for video_gui in selection:
                if mt.objs.get_videos().set_gui(video_gui):
                    self.mark_watched(Unselect=Unselect)
                else:
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_lazy(f)
    
    def mark_not_watched(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.mark_not_watched'
        video = mt.objs.get_videos().get_current()
        gui   = video.gui
        if gui:
            video.dtime = 0
            lg.objs.get_db().mark_downloaded (videoid = video.id_
                                             ,dtime   = video.dtime
                                             )
            gui.black_out()
            if Unselect:
                self.unselect()
        else:
            sh.com.rep_empty(f)
    
    def mark_watched(self,event=None,Unselect=True):
        f = '[Yatube] yatube.Commands.mark_watched'
        video = mt.objs.get_videos().get_current()
        gui   = video.gui
        if gui:
            video.dtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
            lg.objs.get_db().mark_downloaded (videoid = video.id_
                                             ,dtime    = video.dtime
                                             )
            gui.gray_out()
            self.remove_from_watchlist(Unselect=False)
            if Unselect:
                self.unselect()
        else:
            sh.com.rep_empty(f)
    
    def get_sel(self,event=None):
        f = '[Yatube] yatube.Commands.get_sel'
        selected = []
        guis = [video.gui for video in mt.objs.get_videos().videos \
                if video.gui
               ]
        for gui in guis:
            if gui.cbx_vno.get():
                selected.append(gui)
        return selected
    
    def set_max_videos(self,event=None):
        f = '[Yatube] yatube.Commands.set_max_videos'
        if str(self.menu.opt_max.choice).isdigit():
            mt.MAX_VIDEOS = int(self.menu.opt_max.choice)
            self.reload_channel()
        else:
            mes = _('Wrong input data: "{}"')
            mes = mes.format(self.menu.opt_max.choice)
            sh.objs.get_mes(f,mes).show_error()
    
    def set_tooltips(self):
        guis = [video.gui for video in mt.objs.get_videos().videos \
                if video.gui
               ]
        for gui in guis:
            sh.com.bind (obj      = gui.lbl_img
                        ,bindings = '<Enter>'
                        ,action   = self.set_hint
                        )
    
    def show_prev_channel(self,event=None):
        objs.get_channels().dec()
        objs.channels.fetch()
    
    def show_next_channel(self,event=None):
        objs.get_channels().inc()
        objs.channels.fetch()
    
    def show_comments(self,event=None):
        f = '[Yatube] yatube.Commands.show_comments'
        Comments().show()
    
    def run_menu_update(self,event=None):
        f = '[Yatube] yatube.Commands.run_menu_update'
        default = _('Update')
        choice  = self.menu.opt_upd.choice
        if choice == default:
            sh.com.rep_lazy(f)
        elif choice == _('Subscriptions'):
            self.menu.opt_upd.set(default)
            self.update_channels()
        elif choice == _('Channel'):
            self.menu.opt_upd.set(default)
            self.reload_channel()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(choice,';'.join(gi.update_items))
            sh.objs.get_mes(f,mes).show_error()
    
    def run_menu_view(self,event=None):
        f = '[Yatube] yatube.Commands.run_menu_view'
        default = _('View')
        choice  = self.menu.opt_viw.choice
        if choice == default:
            pass
        elif choice == _('History'):
            self.menu.opt_viw.set(default)
            self.show_history()
        elif choice == _('All feed'):
            self.menu.opt_viw.set(default)
            self.show_feed()
        elif choice == _('Favorites'):
            self.menu.opt_viw.set(default)
            self.show_favorites()
        elif choice == _('Watchlist'):
            self.menu.opt_viw.set(default)
            self.show_watchlist()
        elif choice == _('Welcome screen'):
            self.menu.opt_viw.set(default)
            self.blank()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(choice,';'.join(gi.view_items))
            sh.objs.get_mes(f,mes).show_error()
    
    def run_menu_edit(self,event=None):
        f = '[Yatube] yatube.Commands.run_menu_edit'
        default = _('Edit')
        choice  = self.menu.opt_edt.choice
        if choice == default:
            sh.com.rep_lazy(f)
        elif choice == _('Subscriptions'):
            self.menu.opt_edt.set(default)
            self.manage_sub()
        elif choice == _('Blocked authors'):
            self.menu.opt_edt.set(default)
            self.manage_blocked_authors()
        elif choice == _('Blocked words'):
            self.menu.opt_edt.set(default)
            self.manage_blocked_words()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(choice,';'.join(gi.edit_items))
            sh.objs.get_mes(f,mes).show_error()
    
    def run_menu_selection(self,event=None):
        f = '[Yatube] yatube.Commands.run_menu_selection'
        default = _('Selection')
        choice  = self.menu.opt_sel.choice
        if choice == default:
            pass
        elif choice == _('Select all new videos'):
            self.menu.opt_sel.set(default)
            self.select_new()
        elif choice == _('Mark as watched'):
            self.menu.opt_sel.set(default)
            self.sel_mark_watched()
            if objs.get_channels().get_current().type_ == 'watchlist':
                self.reload_channel()
        elif choice == _('Mark as not watched'):
            self.menu.opt_sel.set(default)
            self.sel_mark_not_watched()
            ''' Do not put this code into 'self.mark_not_watched'
                because it is used by 'self.sel_mark_not_watched'.
            '''
            if objs.get_channels().get_current().type_ == 'history':
                self.reload_channel()
        elif choice == _('Add to favorites'):
            self.menu.opt_sel.set(default)
            self.sel_star()
        elif choice == _('Remove from favorites'):
            self.menu.opt_sel.set(default)
            self.sel_unstar()
            ''' Do not put this code into 'self.unstar'
                because the latter is used by 'self.sel_unstar'.
            '''
            if objs.get_channels().get_current().type_ == 'favorites':
                self.reload_channel()
        elif choice == _('Delete selected'):
            self.menu.opt_sel.set(default)
            self.delete_selected()
        elif choice == _('Add to watchlist'):
            self.menu.opt_sel.set(default)
            self.sel_add2watchlist()
        elif choice == _('Remove from watchlist'):
            self.menu.opt_sel.set(default)
            self.sel_remove_from_watchlist()
            ''' Do not put this code into 'self.remove_from_watchlist'
                because the latter is used by
                'self.sel_remove_from_watchlist'.
            '''
            if objs.get_channels().get_current().type_ == 'watchlist':
                self.reload_channel()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(choice,';'.join(gi.selection_items))
            sh.objs.get_mes(f,mes).show_error()
    
    def blank(self,event=None):
        # 'lg.objs.get_channel().reset' requires non-empty values at input
        self.reset_channel_gui()
        lg.objs.get_channel().set_values()
        lg.objs.get_channels().reset()
        mt.objs.get_videos().reset()
        self.menu.clear_search(Force=True)
        self.menu.clear_url()
        self.menu.clear_filter(Force=True)
        gi.objs.get_parent().focus()
        self.menu.opt_chl.set(_('Channels'))
        self.menu.opt_trd.set(_('Trending'))
        gi.objs.get_channel().cvs_prm.move_top()
    
    def unsubscribe(self,event=None):
        f = '[Yatube] yatube.Commands.unsubscribe'
        video = mt.objs.get_videos().get_current()
        if video.author:
            if video.author in lg.objs.get_lists().subauth:
                mes = _('Unsubscribe from channel "{}"')
                mes = mes.format(video.author)
                sh.objs.get_mes(f,mes,True).show_info()
                if video.author in lg.objs.lists.subauth:
                    ind = lg.objs.lists.subauth.index(video.author)
                    del lg.objs.lists.subauth[ind]
                    del lg.objs.lists.subids[ind]
                    subscriptions = []
                    for i in range(len(lg.objs.lists.subauth)):
                        subscriptions.append (lg.objs.lists.subauth[i]\
                                             + '\t' \
                                             + lg.objs.lists.subids[i]
                                             )
                    subscriptions = '\n'.join(subscriptions)
                    if not subscriptions:
                        subscriptions = '# ' + _('Put here authors to subscribe to')
                    sh.WriteTextFile (file    = lg.objs.get_default().fsubsc
                                     ,Rewrite = True
                                     ).write(text=subscriptions)
                    lg.objs.lists.reset()
                    self.reset_channels()
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.rep_empty(f)
    
    def unblock(self,event=None):
        f = '[Yatube] yatube.Commands.unblock'
        video = mt.objs.get_videos().get_current()
        if video.author:
            if video.author in lg.objs.get_lists().blauth:
                mes = _('Unblock channel "{}"').format(video.author)
                sh.objs.get_mes(f,mes,True).show_info()
                ''' The 'Block' boolean will actually be set after
                    reloading the channel, however, we want to inform
                    the context menu about the changes.
                '''
                video.Block = False
                lg.objs.lists.blauth.remove(video.author)
                blocked = lg.objs.lists.blauth
                blocked = '\n'.join(blocked)
                if not blocked:
                    blocked = '# ' + _('Put here authors to be blocked')
                sh.WriteTextFile (file    = lg.objs.get_default().fblock
                                 ,Rewrite = True
                                 ).write(text=blocked)
                lg.objs.lists.reset()
                self.reset_channels()
                self.reload_channel()
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.rep_empty(f)
    
    # GUI-only
    def delete_selected(self,event=None):
        f = '[Yatube] yatube.Commands.delete_selected'
        selection = self.get_sel()
        if selection:
            for gui in selection:
                mt.objs.get_videos().set_gui(gui)
                self.delete_video()
        else:
            sh.com.rep_lazy(f)
    
    def delete_video(self,event=None):
        f = '[Yatube] yatube.Commands.delete_video'
        ''' Do not warn when the GUI object is not available (e.g.,
            performing deletion through OptionMenu.
        '''
        if mt.objs.get_videos().get_current().gui:
            ''' We probably want to disable the checkbox even when
                the file was not removed, e.g., the user selected all
                videos on the channel and pressed 'Shift-Del'.
            '''
            mt.objs.videos.get_current().gui.cbx_vno.disable()
            self.report_selection()
        return lg.Video().delete()
    
    def reset_channels(self,event=None):
        default_channels = [_('Channels')]
        if lg.objs.get_lists().subauth:
            self.channels = default_channels + lg.objs.lists.subauth
        else:
            self.channels = default_channels
        self.menu.opt_chl.reset (items   = self.channels
                                ,default = _('Channels')
                                ,action  = self.set_channel
                                )
    
    def open_video_url(self,event=None):
        f = '[Yatube] yatube.Commands.open_video_url'
        url = lg.Video().get_url()
        if url:
            lg.objs.get_online().url = url
            lg.objs.online.browse()
        else:
            sh.com.rep_empty(f)
                   
    def copy_video_url(self,event=None):
        f = '[Yatube] yatube.Commands.copy_video_url'
        url = lg.Video().get_url()
        if url:
            sh.Clipboard().copy(text=url)
        else:
            sh.com.rep_empty(f)
    
    def subscribe(self,event=None):
        f = '[Yatube] yatube.Commands.subscribe'
        video = mt.objs.get_videos().get_current()
        lg.Video().get_playid()
        if video.author and video.playid:
            if video.author in lg.objs.get_lists().subauth:
                sh.com.rep_lazy(f)
            else:
                mes = _('Subscribe to channel "{}"')
                mes = mes.format(video.author)
                sh.objs.get_mes(f,mes,True).show_info()
                subscriptions = []
                for i in range(len(lg.objs.lists.subauth)):
                    subscriptions.append (lg.objs.lists.subauth[i]\
                                         + '\t' \
                                         + lg.objs.lists.subids[i]
                                         )
                subscriptions.append(video.author + '\t' + video.playid)
                subscriptions = sorted (subscriptions
                                       ,key=lambda x:x[0].lower()
                                       )
                subscriptions = '\n'.join(subscriptions)
                if subscriptions:
                    sh.WriteTextFile (file    = lg.objs.get_default().fsubsc
                                     ,Rewrite = True
                                     ).write(text=subscriptions)
                    lg.objs.lists.reset()
                    self.reset_channels()
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
    
    def block_channel(self,event=None):
        f = '[Yatube] yatube.Commands.block_channel'
        video = mt.objs.get_videos().get_current()
        if video.author:
            if video.author in lg.objs.get_lists().blauth:
                sh.com.rep_lazy(f)
            else:
                mes = _('Block channel "{}"').format(video.author)
                sh.objs.get_mes(f,mes,True).show_info()
                ''' The 'Block' boolean will actually be set after
                    reloading the channel, however, we want to inform
                    the context menu about the changes.
                '''
                video.Block = True
                lg.objs.lists.blauth.append(video.author)
                blocked = lg.objs.lists.blauth
                blocked = sorted (blocked
                                 ,key=lambda x:x[0].lower()
                                 )
                blocked = '\n'.join(blocked)
                if blocked:
                    sh.WriteTextFile (file    = lg.objs.get_default().fblock
                                     ,Rewrite = True
                                     ).write(text=blocked)
                    lg.objs.lists.reset()
                    self.reset_channels()
                    self.reload_channel()
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
                   
    def load_channel(self,event=None):
        f = '[Yatube] yatube.Commands.load_channel'
        playid = lg.Video().get_playid()
        if playid:
            objs.get_channels().add('playlist',playid)
            objs.channels.fetch()
        else:
            sh.com.rep_empty(f)
    
    def open_channel_url(self,event=None):
        f = '[Yatube] yatube.Commands.open_channel_url'
        channel_id = lg.Video().get_channel_id()
        if channel_id:
            lg.objs.get_online().url = lg.pattern2 + channel_id
            lg.objs.online.browse()
        else:
            sh.com.rep_empty(f)

    def copy_channel_url(self,event=None):
        f = '[Yatube] yatube.Commands.copy_channel_url'
        channel_id = lg.Video().get_channel_id()
        if channel_id:
            sh.Clipboard().copy(lg.pattern2+channel_id)
        else:
            sh.com.rep_empty(f)
    
    def stream(self,event=None):
        f = '[Yatube] yatube.Commands.stream'
        selection = self.get_sel()
        if selection:
            mt.objs.get_videos().set_gui(selection[0])
            self.stream_video()
        else:
            sh.com.rep_empty(f)
    
    def stream_video(self,event=None):
        f = '[Yatube] yatube.Commands.stream_video'
        url = lg.Video().stream(self.get_quality())
        if url:
            ''' - Consider using newer python/OS builds if you have
                  SSL/TLS problems here.
                - If streaming fails, try streaming with another quality
                  or downloading a different format.
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
                sh.objs.get_mes(f,mes).show_warning()
            if app:
                if self.menu.chb_slw.get():
                    args = self._stream_slow(app)
                else:
                    args = self._stream(app)
                if args:
                    custom_args = [app] + self.start_mpv(app,args) \
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
                    sh.objs.get_mes(f,mes).show_error()
                    Success = False
                if Success:
                    self.mark_downloaded()
                    if objs.get_channels().get_current().type_ == 'watchlist':
                        self.reload_channel()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
    
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
                   
    def reset_filter_date(self,event=None):
        self.tstamp = None
        self.filter_by_date()
    
    def get_timestamp(self,event=None):
        if not self.tstamp:
            day   = self.menu.opt_day.choice
            month = self.menu.opt_mth.choice
            year  = self.menu.opt_yrs.choice
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
            itime.date = year + '-' + month + '-' + day
            self.tstamp = itime.get_timestamp()
        return self.tstamp
    
    def _filter_date(self):
        cond1 = mt.objs.get_videos().get_current().ptime >= self.get_timestamp()
        cond2 = self.menu.opt_dat.choice == _('Newer than')
        if (cond1 and cond2) or (not cond1 and not cond2):
            return True
    
    def filter_video_date(self,event=None):
        ''' 'filter_by_date' uses the loop to filter videos by date upon
            event (changing filter date or filter settings).
            'filter_video_date' is used to mark a suitable video
            immediately when loading a channel.
            '_filter_date' is used by both methods (+'select_new') and
            should not be called externally in other cases.
            '''
        f = '[Yatube] yatube.Commands.filter_video_date'
        video = mt.objs.get_videos().get_current()
        if video.gui and video.ptime:
            if self.menu.chb_dat.get():
                if self._filter_date():
                    video.gui.red_out()
        else:
            sh.com.rep_empty(f)
    
    def filter_by_date(self,event=None):
        f = '[Yatube] yatube.Commands.filter_by_date'
        # Do not allow to update channel GUI when no channels are loaded
        if gi.objs.channel:
            guis = [video.gui for video in mt.objs.get_videos().videos \
                    if video.gui
                   ]
            for gui in guis:
                gui.black_out()
            if self.menu.chb_dat.get():
                timestamp = self.get_timestamp()
                for gui in guis:
                    mt.objs.get_videos().set_gui(gui)
                    if self._filter_date():
                        gui.red_out()
        else:
            sh.com.rep_lazy(f)
    
    def get_widget(self,event=None):
        f = '[Yatube] yatube.Commands.get_widget'
        if event:
            ''' 'event' will be 'tuple' if it's a callback from
                'Button.click'.
            '''
            if isinstance(event,tuple):
                event = event[0]
            guis = [video.gui for video in mt.objs.get_videos().videos \
                    if video.gui
                   ]
            for gui in guis:
                for obj in gui.objects:
                    ''' This works for Python 3.7.3 and Tkinter 8.6.
                        In previous versions I had to use
                        'if str(obj.widget) in str(event.widget)'.
                    '''
                    if obj.widget == event.widget:
                        return gui
        else:
            sh.com.rep_empty(f)
    
    def show_summary(self,event=None):
        f = '[Yatube] yatube.Commands.show_summary'
        if mt.objs.get_videos().get_current().id_:
            #self.save_extra()
            gi.objs.get_summary().reset()
            gi.objs.summary.insert(lg.Video().show_summary())
            gi.objs.summary.show()
        else:
            sh.com.rep_empty(f)
    
    def _get_context(self,choice,event=None):
        f = '[Yatube] yatube.Commands._get_context'
        if choice:
            url = lg.Video().get_url()
            if choice == _('Show the full summary'):
                self.show_summary()
            elif choice == _('Set pause time'):
                self.set_pause(self)
            elif choice == _('Download'):
                self.download_video()
            elif choice == _('Play'):
                self.download_video()
                self.play_video()
                if objs.get_channels().get_current().type_ == 'watchlist':
                    self.reload_channel()
            elif choice == _('Stream'):
                self.stream_video()
            elif choice == _('Mark as watched'):
                self.mark_watched()
                if objs.get_channels().get_current().type_ == 'watchlist':
                    self.reload_channel()
            elif choice == _('Mark as not watched'):
                self.mark_not_watched()
                ''' Do not put this code into 'self.mark_not_watched'
                    because the latter is used by
                    'self.sel_mark_not_watched'.
                '''
                if objs.get_channels().get_current().type_ == 'history':
                    self.reload_channel()
            elif choice == _('Add to favorites'):
                self.star()
            elif choice == _('Remove from favorites'):
                self.unstar()
                ''' Do not put this code into 'self.unstar' because
                    the latter is used by 'self.sel_unstar'.
                '''
                if objs.get_channels().get_current().type_ == 'favorites':
                    self.reload_channel()
            elif choice == _('Add to watchlist'):
                self.add2watchlist()
                ''' Do not put this code into 'self.add2watchlist'
                    because the latter is used by
                    'self.sel_add2watchlist'.
                '''
                if objs.get_channels().get_current().type_ == 'watchlist':
                    self.reload_channel()
            elif choice == _('Remove from watchlist'):
                self.remove_from_watchlist()
                ''' Do not put this code into
                    'self.remove_from_watchlist' because the latter is
                    used by 'self.sel_remove_from_watchlist'.
                '''
                if objs.get_channels().get_current().type_ == 'watchlist':
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
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.rep_empty(f)
    
    def _color_context(self,message,color='green'):
        if message in gi.objs.get_context().lbx_prm.lst:
            ind = gi.objs.context.lbx_prm.lst.index(message)
            gi.objs.context.lbx_prm.widget.itemconfig(ind,fg=color)
    
    def color_context(self):
        f = '[Yatube] yatube.Commands.color_context'
        if gi.objs.get_context().lbx_prm.lst:
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
            sh.com.rep_empty(f)
    
    def get_context(self,event=None):
        f = '[Yatube] yatube.Commands.get_context'
        gui = self.get_widget(event)
        if gui:
            mt.objs.get_videos().set_gui(gui)
            message = _('Video #{}:').format(gui.no)
            gi.objs.get_context().set_title(message)
            items = self.update_context()
            if not items:
                items = gi.context_items
            gi.objs.context.reset(lst=items)
            self.color_context()
            gi.objs.context.show()
            self._get_context(gi.objs.context.get())
        else:
            sh.com.rep_empty(f)
        
    def get_links(self,url):
        f = '[Yatube] yatube.Commands.get_links'
        if url:
            objs.get_channels().add('extractor',url)
            objs.channels.fetch()
        else:
            sh.com.rep_empty(f)
                          
    def set_channel(self,event=None):
        f = '[Yatube] yatube.Commands.set_channel'
        if self.menu.opt_chl.choice == _('Channels'):
            self.feed()
        else:
            mes = _('Switch to channel "{}"')
            mes = mes.format(self.menu.opt_chl.choice)
            sh.objs.get_mes(f,mes,True).show_info()
            if self.menu.opt_chl.choice in lg.objs.get_lists().subauth:
                author = self.menu.opt_chl.choice
                no     = lg.objs.lists.subauth.index(author)
                playid = lg.objs.lists.subids[no]
                objs.get_channels().add('playlist',playid)
                objs.channels.fetch()
            else:
                mes = _('Wrong input data: "{}"')
                mes = mes.format(self.menu.opt_chl.choice)
                sh.objs.get_mes(f,mes).show_error()
        
    def get_url(self,event=None):
        f = '[Yatube] yatube.Commands.get_url'
        result = self.menu.ent_url.get()
        if result:
            if result == _('Paste URL here'):
                sh.com.rep_lazy(f)
            elif self.menu.opt_url.choice in gi.url_items:
                if self.menu.opt_url.choice == _('Extract links'):
                    self.get_links(url=result)
                else:
                    video = mt.Video()
                    video.id_ = lg.URL(result).get_videoid()
                    mt.objs.get_videos().add(video)
                    mt.objs.videos.i = len(mt.objs.videos.videos) - 1
                    logic = lg.Video()
                    logic.get()
                    if logic.Success:
                        if self.menu.opt_url.choice == _('Show summary'):
                            self.show_summary()
                        elif self.menu.opt_url.choice == _('Download'):
                            self.download_video()
                            gi.objs.progress.close()
                        elif self.menu.opt_url.choice == _('Play'):
                            self.download_video()
                            gi.objs.progress.close()
                            self.play_video()
                        elif self.menu.opt_url.choice == _('Stream'):
                            self.stream_video()
                        elif self.menu.opt_url.choice == _('Delete'):
                            self.delete_video()
                            self.menu.clear_url()
                        elif self.menu.opt_url.choice == _('Full menu'):
                            gi.objs.get_context().set_title(_('Selected video'))
                            gi.objs.context.show()
                            choice = gi.objs.context.get()
                            self._get_context(choice)
                    else:
                        sh.com.cancel(f)
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format (self.menu.opt_url.choice
                                 ,';'.join(gi.url_items)
                                 )
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.rep_empty(f)
        
    def search_youtube(self,event=None):
        f = '[Yatube] yatube.Commands.search_youtube'
        query = self.menu.ent_src.get()
        if query and query != _('Search Youtube'):
            objs.get_channels().add('search',query)
            objs.channels.fetch()
        else:
            sh.com.rep_empty(f)
                          
    def filter_view(self,event=None):
        f = '[Yatube] yatube.Commands.filter_view'
        # Remove previous filter; drop selection if no filter is given
        guis = [video.gui for video in mt.objs.get_videos().videos \
                if video.gui
               ]
        for gui in guis:
            gui.black_out()
        result = self.menu.ent_flt.get()
        if result and result != _('Filter this view'):
            mes = _('Filter by "{}"').format(result)
            sh.objs.get_mes(f,mes,True).show_info()
            result = result.lower()
            for gui in guis:
                mt.objs.videos.set_gui(gui)
                if result in mt.objs.videos.get_current().search:
                    gui.red_out()
        else:
            sh.com.rep_lazy(f)
    
    def set_bindings(self):
        # Menu: main window
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<F1>'
                    ,action   = self.show_stat
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Alt-Left>'
                    ,action   = self.show_prev_page
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Alt-Right>'
                    ,action   = self.show_next_page
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Control-p>'
                    ,action   = self.play
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Control-d>'
                    ,action   = self.download
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Control-s>'
                    ,action   = self.stream
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = ('<Control-h>','<Alt-h>')
                    ,action   = self.show_history
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Alt-w>'
                    ,action   = self.show_watchlist
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Alt-f>'
                    ,action   = self.show_favorites
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Shift-Delete>'
                    ,action   = self.delete_selected
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Alt-c>'
                    ,action   = self.show_feed
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Alt-t>'
                    ,action   = self.update_trending
                    )
        sh.com.bind (obj      = self.menu.parent
                    ,bindings = '<Alt-b>'
                    ,action   = self.blank
                    )
        # Menu: buttons
        self.menu.btn_dld.action = self.download
        self.menu.btn_flt.action = self.filter_view
        self.menu.btn_npg.action = self.show_next_page
        self.menu.btn_nxt.action = self.show_next_channel
        self.menu.btn_ply.action = self.play
        self.menu.btn_ppg.action = self.show_prev_page
        self.menu.btn_prv.action = self.show_prev_channel
        self.menu.btn_stm.action = self.stream
        self.menu.btn_ytb.action = self.search_youtube
        self.menu.chb_sel.reset(action=self.toggle_select)
        # Menu: labels
        sh.com.bind (obj      = self.menu.ent_flt
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.filter_view
                    )
        sh.com.bind (obj      = self.menu.ent_src
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.search_youtube
                    )
        sh.com.bind (obj      = self.menu.ent_url
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action   = self.get_url
                    )
        # Menu: checkboxes
        self.menu.chb_dat.widget.config(command=self.filter_by_date)
        
        # Menu: OptionMenus
        ''' Updating selection menu is slow, so we run it only when
            clicking 'opt_sel' and not in 'self.report_selection'.
            This is a binding to the entire OptionMenu and will not
            interfere with bindings to OptionMenu items.
        '''
        sh.com.bind (obj      = self.menu.opt_sel
                    ,bindings = '<Button-1>'
                    ,action   = self.update_sel_menu
                    )
        self.menu.opt_upd.action = self.run_menu_update
        self.menu.opt_viw.action = self.run_menu_view
        self.menu.opt_sel.action = self.run_menu_selection
        self.menu.opt_edt.action = self.run_menu_edit
        self.menu.opt_chl.reset (items   = self.channels
                                ,default = _('Channels')
                                ,action  = self.set_channel
                                )
        self.menu.opt_dat.action = self.filter_by_date
        self.menu.opt_day.reset (items   = self.days
                                ,default = self.day
                                ,action  = self.reset_filter_date
                                )
        self.menu.opt_max.action = self.set_max_videos
        self.menu.opt_mth.reset (items   = self.months
                                ,default = self.month
                                ,action  = self.reset_filter_date
                                )
        self.menu.opt_trd.reset (items   = lg.objs.get_const().trending
                                ,default = _('Trending')
                                ,action  = self.set_trending
                                )
        self.menu.opt_url.action = self.get_url
        self.menu.opt_yrs.reset (items   = self.years
                                ,default = self.year
                                ,action  = self.reset_filter_date
                                )
        
    def select_new(self,event=None):
        f = '[Yatube] yatube.Commands.select_new'
        video = mt.objs.get_videos().get_current()
        guis = [item.gui for item in mt.objs.videos.videos if item.gui]
        for gui in guis:
            mt.objs.videos.set_gui(gui)
            # Drop all previous selections
            gui.cbx_vno.disable()
            if self.menu.chb_dat.get():
                cond = not video.dtime and not video.Block and \
                       self._filter_date()
            else:
                cond = not video.dtime and not video.Block
            if cond:
                gui.cbx_vno.enable()
        self.report_selection()
        
    def start_mpv(self,app,lst=[]):
        pause = mt.objs.get_videos().get_current().pause
        if 'mpv' in app and pause:
            ''' 'mpv' already resumes about 2s prior to an actual pause,
                so we don't have to additionaly tune the pause to remind
                a user what is happening on the screen.
            '''
            lst += ['--start={}'.format(sh.com.get_easy_time(pause))]
        return lst
    
    def _play_slow(self,app='/usr/bin/mpv'):
        if 'mpv' in app:
            custom_args = ['-fs','-framedrop=vo','--no-correct-pts']
        elif 'mplayer' in app:
            custom_args = ['-fs','-framedrop','-nocorrect-pts']
        else:
            custom_args = []
        command = self.start_mpv(app,custom_args)
        sh.Launch (target = lg.Video().get_path()
                  ).launch_app (custom_app  = app
                               ,custom_args = command
                               )
                        
    def _play_default(self):
        sh.Launch(target=lg.Video().get_path()).launch_default()

    def play_video(self,event=None):
        f = '[Yatube] yatube.Commands.play_video'
        if mt.objs.get_videos().get_current().id_:
            if self.menu.chb_slw.get():
                if os.path.exists('/usr/bin/mpv'):
                    self._play_slow()
                elif os.path.exists('/usr/bin/mplayer'):
                    self._play_slow(app='/usr/bin/mplayer')
                else:
                    self._play_default()
            else:
                self._play_default()
        else:
            sh.com.rep_empty(f)
    
    def play(self,event=None):
        f = '[Yatube] yatube.Commands.play'
        selection = self.get_sel()
        if selection:
            # Download all videos, play the first one only
            for i in range(len(selection)):
                mt.objs.get_videos().set_gui(selection[i])
                sub = ' ({}/{})'.format(i+1,len(selection))
                mes = _('Download progress') + sub
                gi.objs.get_progress().set_title(mes)
                self.download_video()
                if i == 0:
                    self.play_video()
            gi.objs.progress.set_title()
            gi.objs.progress.close()
            if objs.get_channels().get_current().type_ == 'watchlist':
                self.reload_channel()
        else:
            sh.com.rep_lazy(f)
        
    def mark_downloaded(self,Unselect=True):
        f = '[Yatube] yatube.Commands.mark_downloaded'
        video = mt.objs.get_videos().get_current()
        video.dtime = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
        lg.objs.get_db().mark_downloaded (videoid = video.id_
                                         ,dtime   = video.dtime
                                         )
        self.remove_from_watchlist(Unselect=False)
        if video.gui:
            video.gui.gray_out()
            if Unselect:
                self.unselect()
    
    def download_video(self,event=None):
        f = '[Yatube] yatube.Commands.download_video'
        ''' In case of 'get_url', there is no GUI to be handled
            ('mt.Video.gui' must be set to 'None'), so we do not force
            'mt.Video.gui' check here.
        '''
        logic = lg.Video()
        if logic.get_path():
            if os.path.exists(mt.objs.get_videos().get_current().path):
                ''' Lift videos up in history (update DTIME field)
                    even if they were already downloaded. However,
                    do not put this in the end because we do not
                    want to update failed downloads.
                '''
                self.mark_downloaded()
            else:
                gi.objs.get_progress().add()
                gi.objs.progress.show()
                ''' Do not focus this widget since the user may do
                    some work in the background, and we do not want
                    to interrupt it. Just activate the window
                    without focusing so the user would see that
                    the program is downloading something.
                '''
                if self.FirstVid:
                    sh.Geometry(gi.objs.progress.obj).activate()
                    gi.objs.progress.obj.center()
                    self.FirstVid = False
                if logic.download(self.show_progress):
                    self.mark_downloaded()
        else:
            sh.com.rep_empty(f)
    
    def download(self,event=None):
        f = '[Yatube] yatube.Commands.download'
        selection = self.get_sel()
        if selection:
            for i in range(len(selection)):
                mt.objs.get_videos().set_gui(selection[i])
                sub = ' ({}/{})'.format(i+1,len(selection))
                mes = _('Download progress') + sub
                gi.objs.get_progress().set_title(mes)
                self.download_video()
            gi.objs.progress.set_title()
            gi.objs.progress.close()
        else:
            sh.com.rep_empty(f)
        
    def update_channels(self,event=None):
        f = '[Yatube] yatube.Commands.update_channels'
        authors  = lg.objs.get_lists().subauth
        playids = lg.objs.lists.subids
        for i in range(len(playids)):
            self.menu.opt_chl.set(authors[i])
            objs.get_channels().add('playlist',playids[i])
            objs.channels.fetch()
        self.feed()
        
    def update_trending(self,event=None,country='RU'):
        f = '[Yatube] yatube.Commands.update_trending'
        ''' We need this procedure to be separate from
            'self.set_trending' because of hotkeys.
        '''
        objs.get_channels().add('trending',country)
        objs.channels.fetch()
    
    def set_trending(self,event=None):
        f = '[Yatube] yatube.Commands.set_trending'
        choice = self.menu.opt_trd.choice
        if choice == _('Trending'):
            country = 'RU'
        else:
            mes = _('Switch to channel "{}"').format(choice)
            sh.objs.get_mes(f,mes,True).show_info()
            if choice in lg.objs.get_const().countries:
                country = lg.objs.const.countries[choice]
            else:
                country = 'RU'
            mes = _('Country: {}').format(country)
            sh.objs.get_mes(f,mes,True).show_debug()
        self.update_trending(country=country)
        
    def reset_channel_gui(self):
        # Clears the old Channel widget
        guis = [video.gui for video in mt.objs.get_videos().videos \
                if video.gui
               ]
        for gui in guis:
            gui.frm_prm.widget.destroy()
        self.menu.set_title()
        #TODO: rework
        #self.save_url()
    
    def fill_default(self):
        f = '[Yatube] yatube.Commands.fill_default'
        # Operation takes ~0,56s but there seems nothing to speed up
        #timer = sh.Timer(f)
        #timer.start()
        gi.objs.get_channel(gi.objs.get_menu().framev)
        if mt.objs.get_videos().videos:
            for i in range(len(mt.objs.videos.videos)):
                mt.objs.videos.i = i
                mt.objs.videos.videos[i].gui = objs.get_videos().add(no=i+1)
        else:
            sh.com.rep_empty(f)
        #timer.end()
            
    def set_dimensions(self):
        f = '[Yatube] yatube.Commands.set_dimensions'
        sh.objs.get_root().update_idle()
        height = gi.objs.channel.frm_emb.get_reqheight()
        ''' #NOTE: Extra space can be caused by a difference of
            the default and loaded pictures.
        '''
        mes = _('Widget must be at least {} pixels in height')
        mes = mes.format(height)
        sh.objs.get_mes(f,mes,True).show_debug()
        gi.objs.channel.cvs_prm.set_region (x       = 1024
                                           ,y       = height
                                           ,xborder = 20
                                           ,yborder = 20
                                           )
    
    def fill_unknown(self):
        f = '[Yatube] yatube.Commands.fill_unknown'
        #timer = sh.Timer(f)
        #timer.start()
        unknown = []
        for i in range(len(mt.objs.get_videos().videos)):
            mt.objs.videos.i = i
            if not mt.objs.videos.get_current().Saved:
                unknown.append(i)
        if unknown:
            for i in range(len(unknown)):
                mt.objs.videos.i = unknown[i]
                lg.Video().set_new()
                self.update_video(i=unknown[i])
            lg.objs.get_db().save()
        else:
            sh.com.rep_lazy(f)
        #timer.end()
    
    def set_block(self):
        video  = mt.objs.get_videos().get_current()
        author = video.author
        title  = video.title
        if author in lg.objs.get_lists().blauth \
        or author in lg.objs.lists.blauth \
        or lg.objs.lists.match_blocked_word(title+video.title):
            author = title = _('BLOCKED')
            video.image = None
            video.Block  = True
        return(author,title)
    
    def update_video(self,i=0):
        f = '[Yatube] yatube.Commands.update_video'
        video = mt.objs.get_videos().get_current()
        if video.gui:
            date = sh.Time (tstamp  = video.ptime
                           ,pattern = '%Y-%m-%d %H:%M'
                           ).get_date()
            author, title = self.set_block()
            video.gui.reset (author = author
                            ,title = title
                            ,date  = date
                            ,image = video.image
                            )
            if video.dtime:
                video.gui.gray_out()
                self.filter_video_date()
            if video.pause:
                video.gui.green_out()
            if i > 0:
                #TODO: renumber
                pass
        else:
            sh.com.rep_empty(f)
    
    def fill_known(self):
        f = '[Yatube] yatube.Commands.fill_known'
        #timer = sh.Timer(f)
        #timer.start()
        if mt.objs.get_videos().videos:
            ids = [vid.id_ for vid in mt.objs.videos.videos]
            result = lg.objs.get_db().get_videos(ids)
            if result:
                matches = [item[0] for item in result if item]
                mes = _('{}/{} links are already stored in DB.')
                mes = mes.format(len(matches),len(ids))
                sh.objs.get_mes(f,mes,True).show_info()
                for i in range(len(ids)):
                    mt.objs.videos.i = i
                    if result[i]:
                        mt.objs.videos.get_current().Saved = result[i]
                        logic = lg.Video()
                        logic.assign_offline(result[i])
                        logic.delete_unsupported()
                        logic.load_image()
                        self.update_video(i)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
        #timer.end()
            
    def set_channel_gui(self,Unknown=True):
        ''' Do not forget to run 'reset_channel_gui' BEFORE resetting
            logic and running this procedure.
        '''
        self.fill_default()
        ''' After setting default images, we should align the left
            border, otherwise, it looks shabby. However, we cannot
            control the top border, since we need to recalculate
            a canvas region first, and this need an extra
            'root().update_idle()'.
        '''
        gi.objs.channel.cvs_prm.widget.xview_moveto(0)
        self.fill_known()
        ''' The less we use GUI update, the faster will be the program.
            Updating tkinter idle tasks may take ~0,4-1,7s, but this
            must be done after creating all video widgets and
            reading/updating images.
        '''
        sh.objs.get_root().update_idle()
        if Unknown:
            self.fill_unknown()
        # Using the canvas is fast, no need to time this
        objs.get_videos().set_bindings()
        self.set_dimensions()
        gi.objs.channel.cvs_prm.move_top()
        gi.objs.channel.cvs_prm.widget.xview_moveto(0)
        # Move focus away from 'ttk.Combobox' (OptionMenu)
        gi.objs.channel.cvs_prm.focus()
        self.set_tooltips()
    
    def manage_sub(self):
        objs.get_add_id().reset()
        objs.add_id.show()
        self.reset_channels()
                             
    def manage_blocked_authors(self,event=None):
        f = '[Yatube] yatube.Commands.manage_blocked_authors'
        words = sh.Words(text=lg.objs.get_lists().block)
        gi.objs.get_blacklist().reset(words=words)
        gi.objs.blacklist.insert(text=lg.objs.lists.block)
        gi.objs.blacklist.show()
        text = gi.objs.blacklist.get()
        # We should allow an empty input
        if gi.objs.blacklist.Save:
            if text:
                text = text.splitlines()
                text = sorted (text
                              ,key = lambda x:x[0].lower()
                              )
                text = '\n'.join(text)
                sh.WriteTextFile (file    = lg.objs.get_default().fblock
                                 ,Rewrite = True
                                 ).write(text=text)
            else:
                text = '# ' + _('Put here authors to be blocked')
                sh.WriteTextFile (file    = lg.objs.get_default().fblock
                                 ,Rewrite = True
                                 ).write(text=text)
            lg.objs.lists.reset()
        else:
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f,mes,True).show_info()
    
    def manage_blocked_words(self,event=None):
        f = '[Yatube] yatube.Commands.manage_blocked_words'
        words = sh.Words(text=lg.objs.get_lists().blockw)
        gi.objs.get_blacklist().reset(words=words)
        gi.objs.blacklist.insert(text=lg.objs.lists.blockw)
        gi.objs.blacklist.show()
        text = gi.objs.blacklist.get()
        # We should allow an empty input
        if gi.objs.blacklist.Save:    
            if text:
                text = text.splitlines()
                text = sorted (text
                              ,key = lambda x:x[0].lower()
                              )
                text = '\n'.join(text)
                sh.WriteTextFile (file    = lg.objs.get_default().fblockw
                                 ,Rewrite = True
                                 ).write(text=text)
            else:
                text = '# ' + _('Put here words to block in titles (case is ignored)')
                sh.WriteTextFile (file    = lg.objs.get_default().fblockw
                                 ,Rewrite = True
                                 ).write(text=text)
            lg.objs.lists.reset()
        else:
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f,mes,True).show_info()



class Objects:
    
    def __init__(self):
        self.videos = self.add_id = self.commands = self.channels \
                    = self.pause = self.config = None
    
    def get_config(self):
        if self.config is None:
            self.config = Config()
        return self.config
    
    def get_pause(self):
        if self.pause is None:
            self.pause = Pause()
        return self.pause
    
    def get_channels(self):
        if self.channels is None:
            self.channels = Channels()
        return self.channels
    
    def get_commands(self):
        if self.commands is None:
            self.commands = Commands()
        return self.commands
    
    def get_add_id(self):
        if self.add_id is None:
            self.add_id = AddId()
        return self.add_id
    
    def get_videos(self):
        if self.videos is None:
            self.videos = Videos()
        return self.videos


objs = Objects()


if __name__ == '__main__':
    f = '[Yatube] yatube.__main__'
    sh.com.start()
    sh.Geometry(gi.objs.get_parent()).set('1024x600')
    if objs.get_config().Success:
        objs.get_commands().set_bindings()
        objs.config.restore_keys()
        gi.objs.menu.show()
        objs.config.set()
        objs.config.save()
        lg.objs.get_db().save()
        lg.objs.db.close()
    else:
        mes = _('Unable to continue due to an invalid configuration.')
        sh.objs.get_mes(f,mes).show_warning()
    objs.get_commands().show_stat(Silent=True)
    mes = _('Goodbye!')
    sh.objs.get_mes(f,mes,True).show_debug()
    sh.com.end()
