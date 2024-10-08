#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
import skl_shared.image.controller as im

VERSION = '2.4'

context_items = (_('Show the full summary')
                ,_('Stream')
                ,_('Play')
                ,_('Set pause time')
                ,_('Extract links')
                ,_('Load this channel')
                ,_('Open video URL')
                ,_('Copy video URL')
                ,_('Open channel URL')
                ,_('Copy channel URL')
                ,_('Show comments')
                ,_('Download')
                ,_('Delete the downloaded file')
                ,_('Mark as watched')
                ,_('Mark as not watched')
                ,_('Add to watchlist')
                ,_('Remove from watchlist')
                ,_('Add to favorites')
                ,_('Remove from favorites')
                ,_('Block this channel')
                ,_('Unblock')
                ,_('Subscribe to this channel')
                ,_('Unsubscribe')
                ,_('Add to frequent channels')
                ,_('Remove from frequent channels')
                )

url_items = (_('Show summary')
            ,_('Stream')
            ,_('Play')
            ,_('Download')
            ,_('Delete')
            ,_('Extract links')
            ,_('Full menu')
            )

update_items = (_('Update')
               ,_('Channel')
               ,_('Frequent channels')
               ,_('Subscriptions')
               )

view_items = (_('View')
             ,_('All feed')
             ,_('History')
             ,_('Watchlist')
             ,_('Favorites')
             ,_('Welcome screen')
             )

selection_items = (_('Selection')
                  ,_('Select all new videos')
                  ,_('Delete selected')
                  ,_('Mark as watched')
                  ,_('Mark as not watched')
                  ,_('Add to watchlist')
                  ,_('Remove from watchlist')
                  ,_('Add to favorites')
                  ,_('Remove from favorites')
                  )

edit_items = (_('Edit')
             ,_('Subscriptions')
             ,_('Frequent channels')
             ,_('Blocked authors')
             ,_('Blocked words')
             )

qual_items = (_('Best qual.')
             ,_('Worst qual.')
             )

res_items = (_('Auto'),'<=2160p'
            ,'<=1440p','<=1080p'
            ,'<=720p','<=480p'
            ,'<=360p','<=240p'
            )

search_items = (_('Search online')
               ,_('Search database')
               )

default_entry_width = 19
ICON = sh.objs.get_pdir().add('..','resources','icon_64x64_yatube.gif')


class Pause:
    
    def __init__(self):
        self.set_values()
        self.set_gui()
        self.reset()
    
    def set_values(self):
        self.icn_up0 = sh.objs.get_pdir().add ('..','resources','buttons'
                                              ,'icon_36x36_up_off.gif'
                                              )
        self.icn_up1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_up.gif'
                                        )
        self.icn_dn0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_down_off.gif'
                                        )
        self.icn_dn1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_down.gif'
                                        )
        self.icn_del = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_delete.gif'
                                        )
        self.icn_rst = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_reload.gif'
                                        )
        self.icn_sav = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_save.gif'
                                        )
        
    
    def reset(self):
        self.btn_hrd.inactivate()
        self.btn_hru.activate()
        self.ent_hrs.reset()
        self.ent_hrs.insert('0')
        self.btn_mnd.inactivate()
        self.btn_mnu.activate()
        self.ent_min.reset()
        self.ent_min.insert('0')
        self.btn_scd.inactivate()
        self.btn_scu.activate()
        self.ent_sec.reset()
        self.ent_sec.insert('0')
    
    def set_frames(self):
        self.frm_prm = sh.Frame (parent = self.parent
                                ,expand = False
                                )
        self.frm_top = sh.Frame (parent = self.frm_prm
                                ,expand = False
                                ,side = 'top'
                                )
        self.frm_btm = sh.Frame (parent = self.frm_prm
                                ,expand = False
                                ,side = 'top'
                                )
        self.frm_hrs = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,side = 'left'
                                )
        self.frm_sp1 = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,side = 'left'
                                ,propag = False
                                ,width = 3
                                )
        self.frm_min = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,side = 'left'
                                )
        self.frm_sp2 = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,side = 'left'
                                ,propag = False
                                ,width = 3
                                )
        self.frm_sec = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,side = 'left'
                                )
    
    def set_hours(self):
        self.btn_hru = sh.Button (parent = self.frm_hrs
                                 ,inactive = self.icn_up0
                                 ,active = self.icn_up1
                                 ,side = 'top'
                                 )
        self.ent_hrs = sh.Entry (parent = self.frm_hrs
                                ,width = 2
                                ,justify = 'center'
                                )
        self.btn_hrd = sh.Button (parent = self.frm_hrs
                                 ,inactive = self.icn_dn0
                                 ,active = self.icn_dn1
                                 ,side = 'bottom'
                                 )
    
    def set_delimiters(self):
        sh.Label (parent = self.frm_sp1
                 ,text = ':'
                 ,expand = True
                 ,font = 'Sans 14 bold'
                 )
        sh.Label (parent = self.frm_sp2
                 ,text = ':'
                 ,expand = True
                 ,font = 'Serif 14 bold'
                 )
    
    def set_minutes(self):
        self.btn_mnu = sh.Button (parent = self.frm_min
                                 ,inactive = self.icn_up0
                                 ,active = self.icn_up1
                                 ,side = 'top'
                                 )
        self.ent_min = sh.Entry (parent = self.frm_min
                                ,width = 2
                                ,justify = 'center'
                                )
        self.btn_mnd = sh.Button (parent = self.frm_min
                                 ,inactive = self.icn_dn0
                                 ,active = self.icn_dn1
                                 ,side = 'bottom'
                                 )
    
    def set_seconds(self):
        self.btn_scu = sh.Button (parent = self.frm_sec
                                 ,inactive = self.icn_up0
                                 ,active = self.icn_up1
                                 ,side = 'top'
                                 )
        self.ent_sec = sh.Entry (parent = self.frm_sec
                                ,width = 2
                                ,justify = 'center'
                                )
        self.btn_scd = sh.Button (parent = self.frm_sec
                                 ,inactive = self.icn_dn0
                                 ,active = self.icn_dn1
                                 ,side = 'bottom'
                                 )
    
    def set_buttons(self):
        self.btn_del = sh.Button (parent = self.frm_btm
                                 ,text = _('Delete')
                                 ,hint = _('Delete & Close')
                                 ,side = 'left'
                                 ,active = self.icn_del
                                 ,inactive = self.icn_del
                                 )
        self.btn_rst = sh.Button (parent = self.frm_btm
                                 ,text = _('Reset')
                                 ,hint = _('Set the original time')
                                 ,side = 'left'
                                 ,active = self.icn_rst
                                 ,inactive = self.icn_rst
                                 )
        self.btn_sav = sh.Button (parent = self.frm_btm
                                 ,text = _('Save')
                                 ,hint = _('Save & Close')
                                 ,side = 'left'
                                 ,active = self.icn_sav
                                 ,inactive = self.icn_sav
                                 )
    
    def set_widgets(self):
        self.set_hours()
        self.set_minutes()
        self.set_seconds()
        self.set_delimiters()
        self.set_buttons()
    
    def set_gui(self):
        self.parent = sh.Top (icon = ICON
                             ,title = _('Set pause time')
                             )
        self.widget = self.parent.widget
        self.set_frames()
        self.set_widgets()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def set_title(self,text=None):
        if not text:
            text = _('Set pause time')
        self.parent.set_title(text=text)
    
    def set_icon(self,path=None):
        if path:
            self.parent.set_icon(path)
        else:
            self.parent.set_icon(ICON)



class AddId:
    
    def __init__(self):
        self.set_gui()
    
    def paste_ath(self,event=None):
        self.ent_ath.clear_text()
        self.ent_ath.insert(sh.Clipboard().paste())
    
    def paste_pid(self,event=None):
        self.ent_pid.clear_text()
        self.ent_pid.insert(sh.Clipboard().paste())
    
    def set_bindings(self):
        sh.com.bind (obj = self.ent_ath
                    ,bindings = '<ButtonRelease-3>'
                    ,action = self.paste_ath
                    )
        sh.com.bind (obj = self.ent_pid
                    ,bindings = '<ButtonRelease-3>'
                    ,action = self.paste_pid
                    )
    
    def set_title(self,text=None):
        if not text:
            text = _('Add or remove IDs')
        self.parent.set_title(text=text)
    
    def set_icon(self,path=None):
        if path:
            self.parent.set_icon(path)
        else:
            self.parent.set_icon(ICON)
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def set_gui(self):
        self.parent = sh.Top (icon = ICON
                             ,title = _('Add or remove IDs')
                             )
        self.widget = self.parent.widget
        sh.Geometry(self.parent).set('800x600')
        self.set_frames()
        self.set_widgets()
        self.set_bindings()
        self.ent_ath.focus()
    
    def set_frames(self):
        self.frm_prm = sh.Frame (parent = self.parent
                                ,side = 'left'
                                )
        self.frm_rht = sh.Frame (parent = self.parent
                                ,expand = False
                                ,side = 'right'
                                )
        self.frm_top = sh.Frame (parent = self.frm_prm
                                ,side = 'top'
                                ,expand = False
                                )
        self.frm_bot = sh.Frame (parent = self.frm_prm)
        self.frm_rh1 = sh.Frame (parent = self.frm_rht
                                ,side = 'top'
                                )
        self.frm_rh2 = sh.Frame (parent = self.frm_rht
                                ,side = 'bottom'
                                )
        self.frm_bt1 = sh.Frame (parent = self.frm_bot
                                ,side = 'left'
                                )
        self.frm_bt2 = sh.Frame (parent = self.frm_bot
                                ,side = 'left'
                                )
        self.frm_bt3 = sh.Frame (parent = self.frm_bot
                                ,side = 'left'
                                )
    
    def set_widgets(self):
        self.lbl_ath = sh.Label (parent = self.frm_top
                                ,text = _('Channel title:')
                                )
        self.ent_ath = sh.Entry (parent = self.frm_top
                                ,fill = 'x'
                                )
        self.lbl_pid = sh.Label (parent = self.frm_top
                                ,text = _('Playlist ID, channel ID or Youtube user name:')
                                )
        self.ent_pid = sh.Entry (parent = self.frm_top
                                ,fill = 'x'
                                )
        self.lbl_id1 = sh.Label (parent = self.frm_bt1
                                ,text = _('Channel title:')
                                )
        self.lst_id1 = sh.ListBox(self.frm_bt1)
        self.lbl_id2 = sh.Label (parent = self.frm_bt2
                                ,text = _('Your ID:')
                                )
        self.lst_id2 = sh.ListBox(self.frm_bt2)
        self.lbl_id3 = sh.Label (parent = self.frm_bt3
                                ,text = _('Playlist ID:')
                                )
        self.lst_id3 = sh.ListBox(self.frm_bt3)
        self.btn_opn = sh.Button (parent = self.frm_rh1
                                 ,text = _('Open URL')
                                 ,side = 'top'
                                 )
        self.btn_add = sh.Button (parent = self.frm_rh1
                                 ,text = _('Add')
                                 ,side = 'top'
                                 )
        self.btn_edt = sh.Button (parent = self.frm_rh1
                                 ,text = _('Edit')
                                 ,side = 'top'
                                 )
        self.btn_del = sh.Button (parent = self.frm_rh1
                                 ,text = _('Delete')
                                 ,side = 'top'
                                 )
        self.btn_cls = sh.Button (parent = self.frm_rh2
                                 ,text = _('Close')
                                 ,hint = _('Reject and close')
                                 ,bindings = ('<Escape>','<Control-w>'
                                             ,'<Control-q>'
                                             )
                                 ,side = 'bottom'
                                 )
        self.btn_sav = sh.Button (parent = self.frm_rh2
                                 ,text = _('Save')
                                 ,hint = _('Save and close')
                                 ,bindings = ('<F2>','<Control-s>')
                                 ,side = 'bottom'
                                 )
        self.btn_rst = sh.Button (parent = self.frm_rh2
                                 ,text = _('Reset')
                                 ,hint = _('Reset all fields')
                                 ,bindings = ('<F5>','<Control-r>')
                                 ,side = 'bottom'
                                 )



class Comments:
    
    def __init__(self):
        self.set_values()
        self.set_gui()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def set_title(self,text=None):
        if not text:
            text = _('Comments')
        self.parent.set_title(text=text)
    
    def set_icon(self,path=None):
        if path:
            self.parent.set_icon(path)
        else:
            self.parent.set_icon(ICON)
    
    def set_values(self):
        self.icn_prv1 = sh.objs.get_pdir().add ('..','resources'
                                               ,'buttons'
                                               ,'icon_36x36_go_back.gif'
                                               )
        self.icn_prv0 = sh.objs.pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_go_back_off.gif'
                                         )
        self.icn_nxt1 = sh.objs.pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_go_forward.gif'
                                         )
        self.icn_nxt0 = sh.objs.pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_go_forward_off.gif'
                                         )
        
    def set_frames(self):
        self.frm_top = sh.Frame (parent = self.parent
                                ,expand = False
                                ,side = 'top'
                                )
        self.frm_lft = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                )
        self.frm_rht = sh.Frame (parent = self.frm_top
                                ,side = 'right'
                                )
        self.frm_txt = sh.Frame (parent = self.parent
                                ,side = 'top'
                                )
        self.frm_btm = sh.Frame (parent = self.parent
                                ,expand = False
                                ,side = 'bottom'
                                )
    
    def set_widgets(self):
        self.btn_prv = sh.Button (parent = self.frm_rht
                                 ,hint = _('Go to the previous page')
                                 ,inactive = self.icn_prv0
                                 ,active = self.icn_prv1
                                 ,side = 'left'
                                 ,bindings = '<Alt-Left>'
                                 ,hdir = 'bottom'
                                 )
        self.btn_nxt = sh.Button (parent = self.frm_rht
                                 ,hint = _('Go to the next page')
                                 ,inactive = self.icn_nxt0
                                 ,active = self.icn_nxt1
                                 ,side = 'left'
                                 ,bindings = '<Alt-Right>'
                                 ,hdir = 'bottom'
                                 )
        self.txt_com = sh.SearchBox(self.frm_txt)
        self.btn_cls = sh.Button (parent = self.frm_btm
                                 ,action = self.close
                                 ,text = _('Close')
                                 ,hint = _('Close this window')
                                 ,bindings = ('<Escape>','<Control-w>'
                                             ,'<Control-q>'
                                             )
                                 ,expand = True
                                 )
    
    def set_gui(self):
        self.parent = sh.Top (icon = ICON
                             ,title = _('Comments')
                             )
        self.widget = self.parent.widget
        sh.Geometry(self.parent).set('1024x768')
        self.set_frames()
        self.set_widgets()
        self.txt_com.focus()



class Menu:
    
    def __init__(self,parent):
        self.parent = parent
        self.set_gui()
        
    def show(self,event=None):
        self.parent.show()
        
    def close(self,event=None):
        self.parent.close()
    
    def set_frames(self):
        self.frame1 = sh.Frame (parent = self.parent
                               ,expand = False
                               )
        self.frame2 = sh.Frame (parent = self.parent
                               ,expand = False
                               )
        self.frame3 = sh.Frame (parent = self.parent
                               ,expand = False
                               )
        self.frame4 = sh.Frame (parent = self.frame3
                               ,expand = False
                               ,side = 'right'
                               )
        self.framev = sh.Frame (parent = self.parent)
    
    def clear_filter(self,event=None,Force=False):
        if Force or self.ent_flt.get() == _('Filter this view'):
            self.ent_flt.clear_text()
        self.ent_flt.widget.config (fg = 'black'
                                   ,font = 'Serif 10'
                                   )
        self.ent_flt.focus()
        #TODO: Restore filtered videos here
                   
    def clear_search(self,event=None,Force=False):
        if Force or self.ent_src.get() == _('Keywords'):
            self.ent_src.clear_text()
        self.ent_src.widget.config (fg = 'black'
                                   ,font = 'Serif 10'
                                   )
        self.ent_src.focus()
    
    def set_tooltips(self):
        sh.ToolTip (obj = self.opt_max
                   ,text = _('Videos per page')
                   ,hdir = 'bottom'
                   )
    
    def set_widgets(self):
        self.opt_upd = sh.OptionMenu (parent = self.frame1
                                     ,items = update_items
                                     ,default = _('Update')
                                     )
        self.opt_viw = sh.OptionMenu (parent = self.frame1
                                     ,items = view_items
                                     ,default = _('View')
                                     )
        self.opt_sel = sh.OptionMenu (parent = self.frame1
                                     ,items = selection_items
                                     ,default = _('Selection')
                                     )
        self.opt_edt = sh.OptionMenu (parent = self.frame1
                                     ,items = edit_items
                                     ,default = _('Edit')
                                     )
        self.btn_prv = sh.Button (parent = self.frame1
                                 ,text = _('←')
                                 ,hint = _('Go to the previous channel')
                                 ,hdir = 'bottom'
                                 )
        self.btn_nxt = sh.Button (parent = self.frame1
                                 ,text = _('→')
                                 ,hint = _('Go to the next channel')
                                 ,hdir = 'bottom'
                                 )
        self.btn_ppg = sh.Button (parent = self.frame1
                                 ,text = _('‹')
                                 ,hint = _('Go to the previous page')
                                 ,hdir = 'bottom'
                                 )
        self.btn_npg = sh.Button (parent = self.frame1
                                 ,text = _('›')
                                 ,hint = _('Go to the next page')
                                 ,hdir = 'bottom'
                                 )
        self.opt_max = sh.OptionMenu (parent = self.frame1
                                     ,items = (5,10,15,30,50)
                                     ,default = 50
                                     )
        self.chb_dat = sh.CheckBox (parent = self.frame1
                                   ,Active = False
                                   ,side = 'left'
                                   )
        self.opt_dat = sh.OptionMenu (parent = self.frame1
                                     ,items = (_('Newer than')
                                              ,_('Older than')
                                              )
                                     ,default = _('Newer than')
                                     )
        self.opt_day = sh.OptionMenu (parent = self.frame1)
        self.opt_mth = sh.OptionMenu (parent = self.frame1)
        self.opt_yrs = sh.OptionMenu (parent = self.frame1)
        # Search Youtube
        self.ent_src = sh.Entry (parent = self.frame2
                                ,font = 'Serif 10 italic'
                                ,fg = 'grey'
                                ,side = 'left'
                                ,width = default_entry_width
                                )
        self.ent_src.insert(_('Keywords'))
        self.opt_ytb = sh.OptionMenu (parent = self.frame2
                                     ,items = search_items
                                     )
        # Paste URL here
        self.ent_url = sh.Entry (parent = self.frame2
                                ,font = 'Serif 10 italic'
                                ,fg = 'grey'
                                ,side = 'left'
                                ,width = default_entry_width
                                )
        self.ent_url.insert(_('Paste URL here'))
        self.opt_url = sh.OptionMenu (parent = self.frame2
                                     ,items = url_items
                                     )
        # Filter this view
        self.ent_flt = sh.Entry (parent = self.frame2
                                ,font = 'Serif 10 italic'
                                ,fg = 'grey'
                                ,side = 'left'
                                ,width = default_entry_width
                                )
        self.ent_flt.insert(_('Filter this view'))
        self.btn_flt = sh.Button (parent = self.frame2
                                 ,text = _('Filter')
                                 )
        self.opt_lgn = sh.OptionMenu (parent = self.frame2
                                     ,items = (_('Login')
                                              ,_('Use')
                                              ,_('Set up')
                                              ,_('Forget')
                                              ,_('Forget & Delete')
                                              )
                                     ,default = _('Login')
                                     )
        self.chb_sel = sh.CheckBox (parent = self.frame3
                                   ,Active = False
                                   ,side = 'left'
                                   )
        self.btn_ply = sh.Button (parent = self.frame3
                                 ,text = _('Play')
                                 )
        self.btn_dld = sh.Button (parent = self.frame3
                                 ,text = _('Download')
                                 )
        self.btn_stm = sh.Button (parent = self.frame3
                                 ,text = _('Stream')
                                 )
        self.opt_qal = sh.OptionMenu (parent = self.frame3
                                     ,side = 'left'
                                     ,width = 11
                                     ,items = qual_items
                                     ,default = _('Best qual.')
                                     ,font = 'Sans 10'
                                     )
        self.opt_res = sh.OptionMenu (parent = self.frame3
                                     ,side = 'left'
                                     ,width = 7
                                     ,items = res_items
                                     ,default = _('Auto')
                                     ,font = 'Sans 10'
                                     )
        self.chb_slw = sh.CheckBox (parent = self.frame3
                                   ,Active = True
                                   ,side = 'left'
                                   )
        self.lab_slw = sh.Label (parent = self.frame3
                                ,text = _('Slow PC')
                                ,side = 'left'
                                ,font = 'Sans 10'
                                )
        self.opt_trd = sh.OptionMenu (parent = self.frame4
                                     ,side = 'left'
                                     ,Combo = True
                                     ,width = 14
                                     )
        self.opt_chl = sh.OptionMenu (parent = self.frame4
                                     ,side = 'left'
                                     ,Combo = True
                                     ,width = 15
                                     )
        sh.ToolTip (obj = self.opt_qal
                   ,text = _('Streaming quality')
                   ,hdir = 'bottom'
                   )
        sh.ToolTip (obj = self.opt_res
                   ,text = _('Streaming quality')
                   ,hdir = 'bottom'
                   )
    
    def update(self,event=None):
        pass
        #cur
        #self.btn_dld.widget.config(state='disabled')
        #self.btn_ply.widget.config(state='disabled')
                  
    def set_bindings(self):
        # Main window
        sh.com.bind (obj = self.parent
                    ,bindings = '<Control-q>'
                    ,action = self.close
                    )
        sh.com.bind (obj = self.parent
                    ,bindings = '<Escape>'
                    ,action = self.minimize
                    )
        # Search Youtube
        sh.com.bind (obj = self.ent_src
                    ,bindings = '<ButtonRelease-1>'
                    ,action = self.clear_search
                    )
        sh.com.bind (obj = self.ent_src
                    ,bindings = '<ButtonRelease-2>'
                    ,action = self.paste_search
                    )
        sh.com.bind (obj = self.ent_src
                    ,bindings = '<ButtonRelease-3>'
                    ,action = lambda x:self.clear_search(Force=True)
                    )
        # Paste URL
        sh.com.bind (obj = self.ent_url
                    ,bindings = ('<ButtonRelease-1>'
                                ,'<ButtonRelease-2>'
                                )
                    ,action = self.paste_url
                    )
        sh.com.bind (obj = self.ent_url
                    ,bindings = '<ButtonRelease-3>'
                    ,action = self.clear_url
                    )
        # Filter this view
        sh.com.bind (obj = self.ent_flt
                    ,bindings = '<ButtonRelease-1>'
                    ,action = self.clear_filter
                    )
        sh.com.bind (obj = self.ent_flt
                    ,bindings = '<ButtonRelease-2>'
                    ,action = self.paste_filter
                    )
        sh.com.bind (obj = self.ent_flt
                    ,bindings = '<ButtonRelease-3>'
                    ,action = lambda x:self.clear_filter(Force=True)
                    )
        sh.com.bind (obj = self
                    ,bindings = '<F3>'
                    ,action = self.clear_search
                    )
        sh.com.bind (obj = self.lab_slw
                    ,bindings = ('<ButtonRelease-1>'
                                ,'<ButtonRelease-3>'
                                )
                    ,action = self.chb_slw.toggle
                    )
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
    
    def set_title(self, text=None, selected=0, total=0):
        if not text:
            text = 'Yatube'
            if selected:
                text += _(' (selected: {}/{})').format(selected, total)
        self.parent.set_title(text)
    
    def set_gui(self):
        self.widget = self.parent.widget
        self.set_frames()
        self.set_widgets()
        self.set_tooltips()
        self.set_bindings()
        self.update()
    
    def minimize(self,event=None):
        self.widget.iconify()
    
    def set_icon(self,path=None):
        if not path:
            path = ICON
        self.parent.set_icon(path)
    
    def clear_url(self,event=None):
        self.ent_url.clear_text()
        self.ent_url.widget.config(fg='black', font='Serif 10')
        self.ent_url.focus()
        
    def paste_url(self,event=None):
        self.clear_url()
        self.ent_url.insert(text=sh.Clipboard().paste())
        
    def paste_search(self,event=None):
        self.clear_search(Force=True)
        self.ent_src.insert(text=sh.Clipboard().paste())
        
    def paste_filter(self,event=None):
        self.clear_filter()
        self.ent_flt.insert(text=sh.Clipboard().paste())



class Video:
    
    def __init__(self,parent,no=1):
        # 'no' does not involve logic, it's merely a part of GUI
        self.no = no
        self.parent = parent
        self.set_values()
        self.set_gui()
    
    def gray_out(self,event=None):
        for label in self.labels:
            label.widget.config(fg='gray40')
            
    def black_out(self,event=None):
        for label in self.labels:
            label.widget.config(fg='black')
            
    def red_out(self,event=None):
        for label in self.labels:
            label.widget.config(fg='red')
    
    def green_out(self,event=None):
        for label in self.labels:
            label.widget.config(fg='green')
    
    def set_objects(self):
        # Do not include 'self.cbx_vno'. Children must come first.
        self.labels = [self.lbl_vno,self.lbl_img,self.lbl_aut
                      ,self.lbl_tit,self.lbl_dat
                      ]
        self.objects = self.labels + [self.frm_prm,self.frm_vno
                                     ,self.frm_img,self.frm_inf
                                     ]

    def set_values(self):
        self.objects = []
        self.widgets = []
        self.author = _('Author')
        self.title = _('Title')
        self.date = _('Date')
        self.image = objs.get_def_image()
    
    def set_frames(self):
        self.frm_prm = sh.Frame (parent = self.parent)
        self.frm_vno = sh.Frame (parent = self.frm_prm
                                ,side = 'left'
                                )
        self.frm_img = sh.Frame (parent = self.frm_prm
                                ,side = 'left'
                                )
        self.frm_inf = sh.Frame (parent = self.frm_prm
                                ,side = 'left'
                                )
                                 
    def set_pic(self):
        if not self.image:
            self.image = objs.get_def_image()
        self.lbl_img.widget.config(image=self.image)
        # This prevents the garbage collector from deleting the image
        self.lbl_img.widget.image = self.image
    
    def set_labels(self):
        ''' Fixed width is set to ensure that sizes of a default and
            current video labels are the same.
        '''
        self.lbl_vno = sh.Label (parent = self.frm_vno
                                ,text = str(self.no)
                                ,side = 'left'
                                ,font = 'Mono 10'
                                ,width = 3
                                ,justify = 'center'
                                )
        ''' 'image' argument must be specified even when the label
            is further configured with such image, otherwise, frames
            will be further extended to encompass the image
            thereby distorting the GUI structure.
        '''
        self.lbl_img = sh.Label (parent = self.frm_img
                                ,text = _('Image')
                                ,image = self.image
                                )
        self.lbl_aut = sh.Label (parent = self.frm_inf
                                ,text = _('Not Available')
                                ,anchor = 'w'
                                ,width = 85
                                ,padx = 10
                                )
        self.lbl_tit = sh.Label (parent = self.frm_inf
                                ,text = _('Not Available')
                                ,anchor = 'w'
                                ,width = 85
                                ,padx = 10
                                )
        self.lbl_dat = sh.Label (parent = self.frm_inf
                                ,text = _('Not Available')
                                ,anchor = 'w'
                                ,width = 85
                                ,padx = 10
                                )
    
    def set_cboxes(self):
        self.cbx_vno = sh.CheckBox (parent = self.frm_vno
                                   ,Active = False
                                   ,side = 'left'
                                   )

    def set_gui(self):
        self.set_frames()
        self.set_cboxes()
        self.set_labels()
        self.set_objects()
        
    def reset(self, author, title, date, image=None, no=0):
        self.author = author
        self.title = title
        self.date = date
        self.image = image
        ''' 'no' normally remains unmodified, so we check the input
            so we don't have to set 'no' again and again each time
            'self.reset' is called.
        '''
        if no:
            self.no = no
        '''
        #NOTE: #TODO: For some reason, using 'widget.config' or 'Label.text'
        resets config options here.
        '''
        self.lbl_vno.text = str(self.no)
        self.lbl_vno.reset()
        self.lbl_aut.text = self.author
        self.lbl_aut.reset()
        self.lbl_tit.text = self.title
        self.lbl_tit.reset()
        self.lbl_dat.text = self.date
        self.lbl_dat.reset()
        self.set_pic()



class Channel:
    
    def __init__(self,parent):
        self.set_values()
        self.parent = parent
        self.set_gui()
        
    def scroll(self,i):
        f = '[Yatube] gui.Channel.scroll'
        #FIX: seems that another unit type is required
        value = i*112.133333333
        mes = _('Scroll to {}').format(value)
        sh.objs.get_mes(f, mes, True).show_debug()
        self.cvs_prm.scroll(y=value)
        
    def set_values(self):
        ''' These values set the width and height of the frame that contains
            videos and therefore the scrolling region.
            The default Youtube video picture has the dimensions of 120x90;
            therefore, the channel frame embedding 10 videos will have
            the height of at least 900.
        '''
        self.max_x = 1024
        self.max_y = 920
        
    def set_frames(self):
        self.frm_prm = sh.Frame (parent = self.parent)
        self.frm_ver = sh.Frame (parent = self.frm_prm
                                ,expand = False
                                ,fill = 'y'
                                ,side = 'right'
                                )
        self.frm_hor = sh.Frame (parent = self.frm_prm
                                ,expand = False
                                ,fill = 'x'
                                ,side = 'bottom'
                                )
        # A frame that contains all contents except for scrollbars
        self.frm_cnt = sh.Frame (parent = self.frm_prm
                                ,side = 'left'
                                ,width = self.max_x
                                ,height = self.max_y
                                )
    
    def set_canvases(self):
        ''' Create a canvas before an object being embedded, otherwise,
            the canvas will overlap this object.
        '''
        self.cvs_prm = sh.Canvas(parent=self.frm_cnt)
        self.frm_emb = sh.Frame(parent=self.frm_cnt)
        self.cvs_prm.embed(self.frm_emb)
    
    def set_scroll(self):
        sh.Scrollbar (parent = self.frm_hor
                     ,scroll = self.cvs_prm
                     ,Horiz = True
                     )
        sh.Scrollbar (parent = self.frm_ver
                     ,scroll = self.cvs_prm
                     ,Horiz = False
                     )
    
    def set_gui(self):
        self.widget = self.parent.widget
        self.set_frames()
        self.set_canvases()
        self.set_scroll()
        self.cvs_prm.focus()
        self.cvs_prm.set_top_bindings (top = objs.get_parent()
                                      ,Ctrl = False
                                      )
        # This shows the 1st video
        self.cvs_prm.set_region (x = self.max_x
                                ,y = self.max_y
                                )



class Objects:
    
    def __init__(self):
        self.def_image = self.channel = self.menu = self.parent \
                       = self.context = self.summary = self.progress \
                       = self.blacklist = self.subscribe \
                       = self.comments = self.frequent = None
    
    def get_frequent(self):
        if self.frequent is None:
            self.frequent = sh.TextBoxRW (icon = ICON
                                         ,title = _('Edit frequent channels:')
                                         )
        return self.frequent
    
    def get_comments(self):
        if self.comments is None:
            self.comments = sh.TextBoxRO (title = _('Comments')
                                         ,icon = ICON
                                         )
        return self.comments
    
    def get_subscribe(self):
        if self.subscribe is None:
            self.subscribe = sh.TextBoxRW (title = _('Edit subscriptions:')
                                          ,icon = ICON
                                          )
        return self.subscribe
    
    def get_blacklist(self):
        if self.blacklist is None:
            self.blacklist = sh.TextBoxRW (icon = ICON
                                          ,title = _('Edit the blacklist:')
                                          )
        return self.blacklist
    
    def get_progress(self):
        if self.progress is None:
            self.progress = sh.ProgressBar (icon = ICON
                                           ,width = 750
                                           ,height = 200
                                           ,YScroll = True
                                           )
            #NOTE: Widget was not created yet, do not 'center' it here!
        return self.progress
    
    def get_summary(self):
        if self.summary is None:
            self.summary = sh.TextBoxRO (title = _('Full summary:')
                                        ,icon = ICON
                                        )
        return self.summary
    
    def get_context(self):
        if self.context is None:
            self.context = sh.ListBoxC (lst = context_items
                                       ,title = _('Select an action:')
                                       ,icon = ICON
                                       ,ScrollY = False
                                       ,ScrollX = False
                                       ,width = 250
                                       ,height = 365
                                       )
        return self.context
    
    def get_def_image(self):
        if self.def_image is None:
            path = sh.objs.get_pdir().add('..', 'resources', 'nopic.png')
            self.def_image = im.Image().open(path)
        return self.def_image

    def get_channel(self, parent=None):
        f = '[Yatube] gui.Objects.get_channel'
        if self.channel is None:
            if parent is None:
                mes = _('Set the default parent.')
                sh.objs.get_mes(f, mes, True).show_info()
                parent = self.menu().framev
            self.channel = Channel(parent)
        return self.channel
        
    def get_parent(self):
        if not self.parent:
            self.parent = sh.Top (icon = ICON
                                 ,title = 'Yatube'
                                 )
        return self.parent
    
    def get_menu(self):
        if not self.menu:
            self.menu = Menu(parent=self.get_parent())
        return self.menu


objs = Objects()


if __name__ == '__main__':
    # Show the menu
    sh.com.start()
    sh.Geometry(objs.get_parent()).set('1024x600')
    objs.get_menu().show()
    sh.com.end()
