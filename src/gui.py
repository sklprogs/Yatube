#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' We need to explicitly import PIL, otherwise, cx_freeze will fail
    to build the program properly
'''
import PIL
import skl_shared.shared as sh
from skl_shared.localize import _

VERSION = '2.2'

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

default_entry_width = 19
ICON = sh.objs.pdir().add('..','resources','icon_64x64_yatube.gif')


class Pause:
    
    def __init__(self):
        self.values()
        self.parent = sh.Top()
        self.widget = self.parent.widget
        self.gui()
        self.reset()
    
    def values(self):
        self.icn_up0 = sh.objs.pdir().add ('..','resources','buttons'
                                          ,'icon_36x36_up_off.gif'
                                          )
        self.icn_up1 = sh.objs.pdir().add ('..','resources','buttons'
                                          ,'icon_36x36_up.gif'
                                          )
        self.icn_dn0 = sh.objs.pdir().add ('..','resources','buttons'
                                          ,'icon_36x36_down_off.gif'
                                          )
        self.icn_dn1 = sh.objs.pdir().add ('..','resources','buttons'
                                          ,'icon_36x36_down.gif'
                                          )
        self.icn_del = sh.objs.pdir().add ('..','resources','buttons'
                                          ,'icon_36x36_delete.gif'
                                          )
        self.icn_rst = sh.objs.pdir().add ('..','resources','buttons'
                                          ,'icon_36x36_reload.gif'
                                          )
        self.icn_sav = sh.objs.pdir().add ('..','resources','buttons'
                                          ,'icon_36x36_save.gif'
                                          )
        
    
    def reset(self):
        self.btn_hrd.inactive()
        self.btn_hru.active()
        self.ent_hrs.reset()
        self.ent_hrs.insert('0')
        self.btn_mnd.inactive()
        self.btn_mnu.active()
        self.ent_min.reset()
        self.ent_min.insert('0')
        self.btn_scd.inactive()
        self.btn_scu.active()
        self.ent_sec.reset()
        self.ent_sec.insert('0')
    
    def frames(self):
        self.frm_prm = sh.Frame (parent = self.parent
                                ,expand = False
                                )
        self.frm_top = sh.Frame (parent = self.frm_prm
                                ,expand = False
                                ,side   = 'top'
                                )
        self.frm_btm = sh.Frame (parent = self.frm_prm
                                ,expand = False
                                ,side   = 'top'
                                )
        self.frm_hrs = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,side   = 'left'
                                )
        self.frm_sp1 = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,side   = 'left'
                                ,propag = False
                                ,width  = 3
                                )
        self.frm_min = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,side   = 'left'
                                )
        self.frm_sp2 = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,side   = 'left'
                                ,propag = False
                                ,width  = 3
                                )
        self.frm_sec = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,side   = 'left'
                                )
    
    def hours(self):
        self.btn_hru = sh.Button (parent   = self.frm_hrs
                                 ,inactive = self.icn_up0
                                 ,active   = self.icn_up1
                                 ,side     = 'top'
                                 )
        self.ent_hrs = sh.Entry (parent    = self.frm_hrs
                                ,width     = 2
                                ,justify   = 'center'
                                )
        self.btn_hrd = sh.Button (parent   = self.frm_hrs
                                 ,inactive = self.icn_dn0
                                 ,active   = self.icn_dn1
                                 ,side     = 'bottom'
                                 )
    
    def delimiters(self):
        sh.Label (parent = self.frm_sp1
                 ,text   = ':'
                 ,expand = True
                 ,font   = 'Sans 14 bold'
                 )
        sh.Label (parent = self.frm_sp2
                 ,text   = ':'
                 ,expand = True
                 ,font   = 'Serif 14 bold'
                 )
    
    def minutes(self):
        self.btn_mnu = sh.Button (parent   = self.frm_min
                                 ,inactive = self.icn_up0
                                 ,active   = self.icn_up1
                                 ,side     = 'top'
                                 )
        self.ent_min = sh.Entry (parent  = self.frm_min
                                ,width   = 2
                                ,justify = 'center'
                                )
        self.btn_mnd = sh.Button (parent   = self.frm_min
                                 ,inactive = self.icn_dn0
                                 ,active   = self.icn_dn1
                                 ,side     = 'bottom'
                                 )
    
    def seconds(self):
        self.btn_scu = sh.Button (parent   = self.frm_sec
                                 ,inactive = self.icn_up0
                                 ,active   = self.icn_up1
                                 ,side     = 'top'
                                 )
        self.ent_sec = sh.Entry (parent    = self.frm_sec
                                ,width     = 2
                                ,justify   = 'center'
                                )
        self.btn_scd = sh.Button (parent   = self.frm_sec
                                 ,inactive = self.icn_dn0
                                 ,active   = self.icn_dn1
                                 ,side     = 'bottom'
                                 )
    
    def buttons(self):
        self.btn_del = sh.Button (parent   = self.frm_btm
                                 ,text     = _('Delete')
                                 ,hint     = _('Delete & Close')
                                 ,side     = 'left'
                                 ,active   = self.icn_del
                                 ,inactive = self.icn_del
                                 )
        self.btn_rst = sh.Button (parent   = self.frm_btm
                                 ,text     = _('Reset')
                                 ,hint     = _('Set the original time')
                                 ,side     = 'left'
                                 ,active   = self.icn_rst
                                 ,inactive = self.icn_rst
                                 )
        self.btn_sav = sh.Button (parent   = self.frm_btm
                                 ,text     = _('Save')
                                 ,hint     = _('Save & Close')
                                 ,side     = 'left'
                                 ,active   = self.icn_sav
                                 ,inactive = self.icn_sav
                                 )
    
    def widgets(self):
        self.hours()
        self.minutes()
        self.seconds()
        self.delimiters()
        self.buttons()
    
    def gui(self):
        self.frames()
        self.widgets()
        self.icon()
        self.title()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def title(self,text=None):
        if not text:
            text = _('Set pause time')
        self.parent.title(text=text)
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon(ICON)



class AddId:
    
    def __init__(self):
        self.parent = sh.Top()
        self.widget = self.parent.widget
        sh.Geometry(self.parent).set('800x600')
        self.gui()
    
    def paste_ath(self,event=None):
        self.ent_ath.clear_text()
        self.ent_ath.insert(sh.Clipboard().paste())
    
    def paste_pid(self,event=None):
        self.ent_pid.clear_text()
        self.ent_pid.insert(sh.Clipboard().paste())
    
    def bindings(self):
        sh.com.bind (obj      = self.ent_ath
                    ,bindings = '<ButtonRelease-3>'
                    ,action   = self.paste_ath
                    )
        sh.com.bind (obj      = self.ent_pid
                    ,bindings = '<ButtonRelease-3>'
                    ,action   = self.paste_pid
                    )
    
    def title(self,text=None):
        if not text:
            text = _('Add or remove IDs')
        self.parent.title(text=text)
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon(ICON)
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def gui(self):
        self.frames()
        self.widgets()
        self.icon()
        self.title()
        self.bindings()
        self.ent_ath.focus()
    
    def frames(self):
        self.frm_prm = sh.Frame (parent = self.parent
                                ,side   = 'left'
                                )
        self.frm_rht = sh.Frame (parent = self.parent
                                ,expand = False
                                ,side   = 'right'
                                )
        self.frm_top = sh.Frame (parent = self.frm_prm
                                ,side   = 'top'
                                ,expand = False
                                )
        self.frm_bot = sh.Frame (parent = self.frm_prm)
        self.frm_rh1 = sh.Frame (parent = self.frm_rht
                                ,side   = 'top'
                                )
        self.frm_rh2 = sh.Frame (parent = self.frm_rht
                                ,side   = 'bottom'
                                )
        self.frm_bt1 = sh.Frame (parent = self.frm_bot
                                ,side   = 'left'
                                )
        self.frm_bt2 = sh.Frame (parent = self.frm_bot
                                ,side   = 'left'
                                )
        self.frm_bt3 = sh.Frame (parent = self.frm_bot
                                ,side   = 'left'
                                )
    
    def widgets(self):
        self.lbl_ath = sh.Label (parent = self.frm_top
                                ,text   = _('Channel title:')
                                )
        self.ent_ath = sh.Entry (parent = self.frm_top
                                ,fill   = 'x'
                                )
        self.lbl_pid = sh.Label (parent = self.frm_top
                                ,text   = _('Playlist ID, channel ID or Youtube user name:')
                                )
        self.ent_pid = sh.Entry (parent = self.frm_top
                                ,fill   = 'x'
                                )
        self.lbl_id1 = sh.Label (parent = self.frm_bt1
                                ,text   = _('Channel title:')
                                )
        self.lst_id1 = sh.ListBox(self.frm_bt1)
        self.lbl_id2 = sh.Label (parent = self.frm_bt2
                                ,text   = _('Your ID:')
                                )
        self.lst_id2 = sh.ListBox(self.frm_bt2)
        self.lbl_id3 = sh.Label (parent = self.frm_bt3
                                ,text   = _('Playlist ID:')
                                )
        self.lst_id3 = sh.ListBox(self.frm_bt3)
        self.btn_opn = sh.Button (parent = self.frm_rh1
                                 ,text   = _('Open URL')
                                 ,side   = 'top'
                                 )
        self.btn_add = sh.Button (parent = self.frm_rh1
                                 ,text   = _('Add')
                                 ,side   = 'top'
                                 )
        self.btn_edt = sh.Button (parent = self.frm_rh1
                                 ,text   = _('Edit')
                                 ,side   = 'top'
                                 )
        self.btn_del = sh.Button (parent = self.frm_rh1
                                 ,text   = _('Delete')
                                 ,side   = 'top'
                                 )
        self.btn_cls = sh.Button (parent   = self.frm_rh2
                                 ,text     = _('Close')
                                 ,hint     = _('Reject and close')
                                 ,bindings = ('<Escape>','<Control-w>'
                                             ,'<Control-q>'
                                             )
                                 ,side     = 'bottom'
                                 )
        self.btn_sav = sh.Button (parent   = self.frm_rh2
                                 ,text     = _('Save')
                                 ,hint     = _('Save and close')
                                 ,bindings = ('<F2>','<Control-s>')
                                 ,side     = 'bottom'
                                 )
        self.btn_rst = sh.Button (parent   = self.frm_rh2
                                 ,text     = _('Reset')
                                 ,hint     = _('Reset all fields')
                                 ,bindings = ('<F5>','<Control-r>')
                                 ,side     = 'bottom'
                                 )



class Comments:
    
    def __init__(self):
        self.values()
        self.gui()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def title(self,text=None):
        if not text:
            text = _('Comments')
        self.parent.title(text=text)
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon(ICON)
    
    def values(self):
        self.icn_prv1 = sh.objs.pdir().add ('..','resources','buttons'
                                           ,'icon_36x36_go_back.gif'
                                           )
        self.icn_prv0 = sh.objs.pdir().add ('..','resources','buttons'
                                           ,'icon_36x36_go_back_off.gif'
                                           )
        self.icn_nxt1 = sh.objs.pdir().add ('..','resources','buttons'
                                           ,'icon_36x36_go_forward.gif'
                                           )
        self.icn_nxt0 = sh.objs.pdir().add ('..','resources','buttons'
                                           ,'icon_36x36_go_forward_off.gif'
                                           )
        
    def frames(self):
        self.frm_top = sh.Frame (parent = self.parent
                                ,expand = False
                                ,side   = 'top'
                                )
        self.frm_lft = sh.Frame (parent = self.frm_top
                                ,side   = 'left'
                                )
        self.frm_rht = sh.Frame (parent = self.frm_top
                                ,side   = 'right'
                                )
        self.frm_txt = sh.Frame (parent = self.parent
                                ,side   = 'top'
                                )
        self.frm_btm = sh.Frame (parent = self.parent
                                ,expand = False
                                ,side   = 'bottom'
                                )
    
    def widgets(self):
        self.btn_prv = sh.Button (parent   = self.frm_rht
                                 ,hint     = _('Go to the previous page')
                                 ,inactive = self.icn_prv0
                                 ,active   = self.icn_prv1
                                 ,side     = 'left'
                                 ,bindings = '<Alt-Left>'
                                 )
        self.btn_nxt = sh.Button (parent   = self.frm_rht
                                 ,hint     = _('Go to the next page')
                                 ,inactive = self.icn_nxt0
                                 ,active   = self.icn_nxt1
                                 ,side     = 'left'
                                 ,bindings = '<Alt-Right>'
                                 )
        self.txt_com = sh.TextBox(self.frm_txt)
        self.btn_cls = sh.Button (parent   = self.frm_btm
                                 ,action   = self.close
                                 ,text     = _('Close')
                                 ,hint     = _('Close this window')
                                 ,bindings = ('<Escape>','<Control-w>'
                                             ,'<Control-q>'
                                             )
                                 ,expand   = True
                                 )
    
    def gui(self):
        self.parent = sh.Top()
        self.widget = self.parent.widget
        sh.Geometry(self.parent).set('1024x768')
        self.frames()
        self.widgets()
        self.icon()
        self.title()
        self.txt_com.focus()



class Menu:
    
    def __init__(self,parent):
        self.parent = parent
        self.gui()
        
    def show(self,event=None):
        self.parent.show()
        
    def close(self,event=None):
        self.parent.close()
    
    def frames(self):
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
                               ,side   = 'right'
                               )
        self.framev = sh.Frame (parent = self.parent)
    
    def clear_filter(self,event=None,Force=False):
        if Force or self.ent_flt.get() == _('Filter this view'):
            self.ent_flt.clear_text()
        self.ent_flt.widget.config(fg='black',font='Serif 10')
        self.ent_flt.focus()
        #todo: Restore filtered videos here
                   
    def clear_search(self,event=None,Force=False):
        if Force or self.ent_src.get() == _('Search Youtube'):
            self.ent_src.clear_text()
        self.ent_src.widget.config(fg='black',font='Serif 10')
        self.ent_src.focus()
    
    def tooltips(self):
        sh.ToolTip (obj  = self.opt_max
                   ,text = _('Videos per page')
                   ,hdir = 'bottom'
                   )
    
    def widgets(self):
        self.opt_upd = sh.OptionMenu (parent  = self.frame1
                                     ,items   = update_items
                                     ,default = _('Update')
                                     )
        self.opt_viw = sh.OptionMenu (parent  = self.frame1
                                     ,items   = view_items
                                     ,default = _('View')
                                     )
        self.opt_sel = sh.OptionMenu (parent  = self.frame1
                                     ,items   = selection_items
                                     ,default = _('Selection')
                                     )
        self.opt_edt = sh.OptionMenu (parent  = self.frame1
                                     ,items   = edit_items
                                     ,default = _('Edit')
                                     )
        self.btn_prv = sh.Button (parent = self.frame1
                                 ,text   = _('←')
                                 ,hint   = _('Go to the previous channel')
                                 ,hdir   = 'bottom'
                                 )
        self.btn_nxt = sh.Button (parent = self.frame1
                                 ,text   = _('→')
                                 ,hint   = _('Go to the next channel')
                                 ,hdir   = 'bottom'
                                 )
        self.btn_ppg = sh.Button (parent = self.frame1
                                 ,text   = _('‹')
                                 ,hint   = _('Go to the previous page')
                                 ,hdir   = 'bottom'
                                 )
        self.btn_npg = sh.Button (parent = self.frame1
                                 ,text   = _('›')
                                 ,hint   = _('Go to the next page')
                                 ,hdir   = 'bottom'
                                 )
        self.opt_max = sh.OptionMenu (parent  = self.frame1
                                     ,items   = (5,10,15,30,50)
                                     ,default = 50
                                     )
        self.chb_dat = sh.CheckBox (parent = self.frame1
                                   ,Active = False
                                   ,side   = 'left'
                                   )
        self.opt_dat = sh.OptionMenu (parent  = self.frame1
                                     ,items   = (_('Newer than')
                                                ,_('Older than')
                                                )
                                     ,default = _('Newer than')
                                     )
        self.opt_day = sh.OptionMenu (parent = self.frame1)
        self.opt_mth = sh.OptionMenu (parent = self.frame1)
        self.opt_yrs = sh.OptionMenu (parent = self.frame1)
        # Search Youtube
        self.ent_src = sh.Entry (parent = self.frame2
                                ,font   = 'Serif 10 italic'
                                ,fg     = 'grey'
                                ,side   = 'left'
                                ,width  = default_entry_width
                                )
        self.ent_src.insert(_('Search Youtube'))
        self.btn_ytb = sh.Button (parent = self.frame2
                                 ,text   = _('Search')
                                 )
        # Paste URL here
        self.ent_url = sh.Entry (parent = self.frame2
                                ,font   = 'Serif 10 italic'
                                ,fg     = 'grey'
                                ,side   = 'left'
                                ,width  = default_entry_width
                                )
        self.ent_url.insert(_('Paste URL here'))
        self.opt_url = sh.OptionMenu (parent = self.frame2
                                     ,items  = url_items
                                     )
        # Filter this view
        self.ent_flt = sh.Entry (parent = self.frame2
                                ,font   = 'Serif 10 italic'
                                ,fg     = 'grey'
                                ,side   = 'left'
                                ,width  = default_entry_width
                                )
        self.ent_flt.insert(_('Filter this view'))
        self.btn_flt = sh.Button (parent = self.frame2
                                 ,text   = _('Filter')
                                 )
        self.chb_sel = sh.CheckBox (parent = self.frame3
                                   ,Active = False
                                   ,side   = 'left'
                                   )
        self.btn_ply = sh.Button (parent = self.frame3
                                 ,text   = _('Play')
                                 )
        self.btn_dld = sh.Button (parent = self.frame3
                                 ,text   = _('Download')
                                 )
        self.btn_stm = sh.Button (parent = self.frame3
                                 ,text   = _('Stream')
                                 )
        self.opt_qal = sh.OptionMenu (parent  = self.frame3
                                     ,side    = 'left'
                                     ,width   = 11
                                     ,items   = qual_items
                                     ,default = _('Best qual.')
                                     ,font    = 'Sans 10'
                                     )
        self.opt_res = sh.OptionMenu (parent  = self.frame3
                                     ,side    = 'left'
                                     ,width   = 7
                                     ,items   = res_items
                                     ,default = _('Auto')
                                     ,font    = 'Sans 10'
                                     )
        self.chb_slw = sh.CheckBox (parent = self.frame3
                                   ,Active = True
                                   ,side   = 'left'
                                   )
        self.lab_slw = sh.Label (parent = self.frame3
                                ,text   = _('Slow PC')
                                ,side   = 'left'
                                ,font   = 'Sans 10'
                                )
        self.opt_trd = sh.OptionMenu (parent = self.frame4
                                     ,side   = 'left'
                                     ,Combo  = True
                                     ,width  = 14
                                     )
        self.opt_chl = sh.OptionMenu (parent = self.frame4
                                     ,side   = 'left'
                                     ,Combo  = True
                                     ,width  = 15
                                     )
        sh.ToolTip (obj  = self.opt_qal
                   ,text = _('Streaming quality')
                   ,hdir = 'bottom'
                   )
        sh.ToolTip (obj  = self.opt_res
                   ,text = _('Streaming quality')
                   ,hdir = 'bottom'
                   )
    
    def update(self,event=None):
        pass
        #cur
        #self.btn_dld.widget.config(state='disabled')
        #self.btn_ply.widget.config(state='disabled')
                  
    def bindings(self):
        # Main window
        sh.com.bind (obj      = self.parent
                    ,bindings = ('<Control-w>','<Control-q>')
                    ,action   = self.close
                    )
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Escape>'
                    ,action   = self.minimize
                    )
        # Search Youtube
        sh.com.bind (obj      = self.ent_src
                    ,bindings = '<ButtonRelease-1>'
                    ,action   = self.clear_search
                    )
        sh.com.bind (obj      = self.ent_src
                    ,bindings = '<ButtonRelease-2>'
                    ,action   = self.paste_search
                    )
        sh.com.bind (obj      = self.ent_src
                    ,bindings = '<ButtonRelease-3>'
                    ,action   = lambda x:self.clear_search(Force=True)
                    )
        # Paste URL
        sh.com.bind (obj      = self.ent_url
                    ,bindings = ('<ButtonRelease-1>'
                                ,'<ButtonRelease-2>'
                                )
                    ,action   = self.paste_url
                    )
        sh.com.bind (obj      = self.ent_url
                    ,bindings = '<ButtonRelease-3>'
                    ,action   = self.clear_url
                    )
        # Filter this view
        sh.com.bind (obj      = self.ent_flt
                    ,bindings = '<ButtonRelease-1>'
                    ,action   = self.clear_filter
                    )
        sh.com.bind (obj      = self.ent_flt
                    ,bindings = '<ButtonRelease-2>'
                    ,action   = self.paste_filter
                    )
        sh.com.bind (obj      = self.ent_flt
                    ,bindings = '<ButtonRelease-3>'
                    ,action   = lambda x:self.clear_filter(Force=True)
                    )
        sh.com.bind (obj      = self
                    ,bindings = '<F3>'
                    ,action   = self.clear_search
                    )
        sh.com.bind (obj      = self.lab_slw
                    ,bindings = ('<ButtonRelease-1>'
                                ,'<ButtonRelease-3>'
                                )
                    ,action   = self.chb_slw.toggle
                    )
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
    
    def title(self,text=None,selected=0,total=0):
        if not text:
            text = sh.List(lst1=['Yatube',VERSION]).space_items()
            if selected:
                text += _(' (selected: {}/{})').format(selected,total)
        self.parent.title(text)
    
    def gui(self):
        self.widget = self.parent.widget
        self.frames()
        self.widgets()
        self.tooltips()
        self.bindings()
        self.update()
    
    def minimize(self,event=None):
        self.widget.iconify()
    
    def icon(self,path=None):
        if not path:
            path = ICON
        self.parent.icon(path)
    
    def clear_url(self,event=None):
        self.ent_url.clear_text()
        self.ent_url.widget.config (fg   = 'black'
                                   ,font = 'Serif 10'
                                   )
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
        self._no    = no
        self.parent = parent
        self.values()
        self.gui()
    
    def gray_out(self,event=None):
        for label in self._labels:
            label.widget.config(fg='gray40')
            
    def black_out(self,event=None):
        for label in self._labels:
            label.widget.config(fg='black')
            
    def red_out(self,event=None):
        for label in self._labels:
            label.widget.config(fg='red')
    
    def green_out(self,event=None):
        for label in self._labels:
            label.widget.config(fg='green')
    
    def objects(self):
        # Do not include 'self.cbx_vno'. Children must come first.
        self._labels  = [self.lbl_vno,self.lbl_img,self.lbl_aut
                        ,self.lbl_tit,self.lbl_dat
                        ]
        self._objects = self._labels + [self.frm_prm,self.frm_vno
                                       ,self.frm_img,self.frm_inf
                                       ]

    def values(self):
        self._objects = []
        self._widgets = []
        self._author  = _('Author')
        self._title   = _('Title')
        self._date    = _('Date')
        self._image   = objs.def_image()
    
    def frames(self):
        self.frm_prm = sh.Frame (parent = self.parent)
        self.frm_vno = sh.Frame (parent = self.frm_prm
                                ,side   = 'left'
                                )
        self.frm_img = sh.Frame (parent = self.frm_prm
                                ,side   = 'left'
                                )
        self.frm_inf = sh.Frame (parent = self.frm_prm
                                ,side   = 'left'
                                )
                                 
    def pic(self):
        if not self._image:
            self._image = objs.def_image()
        self.lbl_img.widget.config(image=self._image)
        # This prevents the garbage collector from deleting the image
        self.lbl_img.widget.image = self._image
    
    def labels(self):
        ''' Fixed width is set to ensure that sizes of a default and
            current video labels are the same.
        '''
        self.lbl_vno = sh.Label (parent  = self.frm_vno
                                ,text    = str(self._no)
                                ,side    = 'left'
                                ,font    = 'Mono 10'
                                ,width   = 3
                                ,justify = 'center'
                                )
        ''' 'image' argument must be specified even when the label
            is further configured with such image, otherwise, frames
            will be further extended to encompass the image
            thereby distorting the GUI structure.
        '''
        self.lbl_img = sh.Label (parent = self.frm_img
                                ,text   = _('Image')
                                ,image  = self._image
                                )
        self.lbl_aut = sh.Label (parent = self.frm_inf
                                ,text   = _('Not Available')
                                ,anchor = 'w'
                                ,width  = 85
                                ,padx   = 10
                                )
        self.lbl_tit = sh.Label (parent = self.frm_inf
                                ,text   = _('Not Available')
                                ,anchor = 'w'
                                ,width  = 85
                                ,padx   = 10
                                )
        self.lbl_dat = sh.Label (parent = self.frm_inf
                                ,text   = _('Not Available')
                                ,anchor = 'w'
                                ,width  = 85
                                ,padx   = 10
                                )
    
    def checkboxes(self):
        self.cbx_vno = sh.CheckBox (parent = self.frm_vno
                                   ,Active = False
                                   ,side   = 'left'
                                   )

    def gui(self):
        self.frames()
        self.checkboxes()
        self.labels()
        self.objects()
        
    def reset (self,author,title,date
              ,image=None,no=0
              ):
        self._author = author
        self._title  = title
        self._date   = date
        self._image  = image
        ''' 'no' normally remains unmodified, so we check the input
            so we don't have to set 'no' again and again each time
            'self.reset' is called.
        '''
        if no:
            self._no = no
        '''
        #note #todo For some reason, using 'widget.config' or 
        'Label.text' resets config options here.
        '''
        self.lbl_vno._text = str(self._no)
        self.lbl_vno.reset()
        self.lbl_aut._text = self._author
        self.lbl_aut.reset()
        self.lbl_tit._text = self._title
        self.lbl_tit.reset()
        self.lbl_dat._text = self._date
        self.lbl_dat.reset()
        self.pic()



class Channel:
    
    def __init__(self,parent):
        self.values()
        self.parent = parent
        self.gui()
        
    def scroll(self,i):
        f = '[Yatube] gui.Channel.scroll'
        #fix: seems that another unit type is required
        #cur
        value = i*112.133333333
        mes   = _('Scroll to {}').format(value)
        sh.objs.mes(f,mes,True).debug()
        self.cvs_prm.scroll(y=value)
        
    def values(self):
        ''' These values set the width and height of the frame that 
            contains videos and therefore the scrolling region.
            The default Youtube video picture has the dimensions of
            120x90, therefore, the channel frame embedding 10 videos
            will have the height of at least 900.
        '''
        self._max_x = 1024
        self._max_y = 920
        
    def frames(self):
        self.frm_prm = sh.Frame (parent = self.parent)
        self.frm_ver = sh.Frame (parent = self.frm_prm
                                ,expand = False
                                ,fill   = 'y'
                                ,side   = 'right'
                                )
        self.frm_hor = sh.Frame (parent = self.frm_prm
                                ,expand = False
                                ,fill   = 'x'
                                ,side   = 'bottom'
                                )
        # A frame that contains all contents except for scrollbars
        self.frm_cnt = sh.Frame (parent = self.frm_prm
                                ,side   = 'left'
                                ,width  = self._max_x
                                ,height = self._max_y
                                )
    
    def canvases(self):
        ''' Create a canvas before an object being embedded, otherwise,
            the canvas will overlap this object.
        '''
        self.cvs_prm = sh.Canvas(parent=self.frm_cnt)
        self.frm_emb = sh.Frame(parent=self.frm_cnt)
        self.cvs_prm.embed(self.frm_emb)
    
    def scrollbars(self):
        sh.Scrollbar (parent = self.frm_hor
                     ,scroll = self.cvs_prm
                     ,Horiz  = True
                     )
        sh.Scrollbar (parent = self.frm_ver
                     ,scroll = self.cvs_prm
                     ,Horiz  = False
                     )
    
    def gui(self):
        self.widget = self.parent.widget
        self.frames()
        self.canvases()
        self.scrollbars()
        self.cvs_prm.focus()
        self.cvs_prm.top_bindings (top  = objs.parent()
                                  ,Ctrl = False
                                  )
        # This shows the 1st video
        self.cvs_prm.region (x = self._max_x
                            ,y = self._max_y
                            )



class Objects:
    
    def __init__(self):
        self._def_image = self._channel = self._menu = self._parent \
                        = self._context = self._summary \
                        = self._progress = self._blacklist \
                        = self._subscribe = self._comments = None
    
    def comments(self):
        if not self._comments:
            top = sh.Top()
            sh.Geometry(parent=top).set('1024x600')
            self._comments = sh.TextBoxRO (title = _('Comments')
                                          ,icon  = ICON
                                          )
        return self._comments
    
    def subscribe(self):
        if not self._subscribe:
            self._subscribe = sh.TextBoxRW (title = _('Edit subscriptions:')
                                           ,icon  = ICON
                                           )
        return self._subscribe
    
    def blacklist(self):
        if not self._blacklist:
            self._blacklist = sh.TextBoxRW (icon  = ICON
                                           ,title = _('Edit the blacklist:')
                                           )
        return self._blacklist
    
    def progress(self):
        if not self._progress:
            self._progress = sh.ProgressBar(icon=ICON)
            # Widget is not created yet, do not 'center' it here!
        return self._progress
    
    def summary(self):
        if not self._summary:
            self._summary = sh.TextBoxRO (title = _('Full summary:')
                                         ,icon  = ICON
                                         )
        return self._summary
    
    def context(self):
        if not self._context:
            ''' #fix: Modifying 'SingleClick' and 'SelectionCloses' is
                needed here only not to toggle the checkbox of
                the parent (this is a bug and should be fixed).
            '''
            self._context = sh.ListBoxC (lst     = context_items
                                        ,title   = _('Select an action:')
                                        ,icon    = ICON
                                        ,ScrollY = False
                                        ,ScrollX = False
                                        ,width   = 250
                                        )
        return self._context
    
    def def_image(self):
        if not self._def_image:
            path = sh.objs.pdir().add('..','resources','nopic.png')
            self._def_image = sh.Image().open(path=path)
        return self._def_image

    def channel(self,parent=None):
        f = '[Yatube] gui.Objects.channel'
        if not self._channel:
            if parent is None:
                mes = _('Set the default parent.')
                sh.objs.mes(f,mes,True).info()
                parent = self.menu().framev
            self._channel = Channel(parent)
        return self._channel
        
    def parent(self):
        if not self._parent:
            title = sh.List(lst1=['Yatube',VERSION]).space_items()
            self._parent = sh.Top (icon  = ICON
                                  ,title = title
                                  )
        return self._parent
    
    def menu(self):
        if not self._menu:
            self._menu = Menu(parent=self.parent())
        return self._menu


objs = Objects()


if __name__ == '__main__':
    # Show the menu
    sh.com.start()
    sh.Geometry(objs.parent()).set('1024x600')
    objs.menu().show()
    sh.com.end()
