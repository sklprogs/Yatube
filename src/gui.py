#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' We need to explicitly import PIL, otherwise, cx_freeze will fail
    to build the program properly
'''
import PIL
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')

VERSION = '2.1'

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

default_entry_width = 19
icon_path = sh.objs.pdir().add('..','resources','icon_64x64_yatube.gif')


class Pause:
    
    def __init__(self):
        self.values()
        self.parent = sg.objs.new_top()
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
        self.frm_prm = sg.Frame (parent = self.parent
                                ,expand = False
                                )
        self.frm_top = sg.Frame (parent = self.frm_prm
                                ,expand = False
                                ,side   = 'top'
                                )
        self.frm_btm = sg.Frame (parent = self.frm_prm
                                ,expand = False
                                ,side   = 'top'
                                )
        self.frm_hrs = sg.Frame (parent = self.frm_top
                                ,expand = False
                                ,side   = 'left'
                                )
        self.frm_sp1 = sg.Frame (parent = self.frm_top
                                ,expand = False
                                ,side   = 'left'
                                ,propag = False
                                ,width  = 3
                                )
        self.frm_min = sg.Frame (parent = self.frm_top
                                ,expand = False
                                ,side   = 'left'
                                )
        self.frm_sp2 = sg.Frame (parent = self.frm_top
                                ,expand = False
                                ,side   = 'left'
                                ,propag = False
                                ,width  = 3
                                )
        self.frm_sec = sg.Frame (parent = self.frm_top
                                ,expand = False
                                ,side   = 'left'
                                )
    
    def hours(self):
        self.btn_hru = sg.Button (parent   = self.frm_hrs
                                 ,inactive = self.icn_up0
                                 ,active   = self.icn_up1
                                 ,side     = 'top'
                                 )
        self.ent_hrs = sg.Entry (parent    = self.frm_hrs
                                ,Composite = True
                                ,width     = 2
                                ,justify   = 'center'
                                )
        self.btn_hrd = sg.Button (parent   = self.frm_hrs
                                 ,inactive = self.icn_dn0
                                 ,active   = self.icn_dn1
                                 ,side     = 'bottom'
                                 )
    
    def delimiters(self):
        sg.Label (parent = self.frm_sp1
                 ,text   = ':'
                 ,expand = True
                 ,Close  = False
                 ,font   = 'Sans 14 bold'
                 )
        sg.Label (parent = self.frm_sp2
                 ,text   = ':'
                 ,expand = True
                 ,Close  = False
                 ,font   = 'Serif 14 bold'
                 )
    
    def minutes(self):
        self.btn_mnu = sg.Button (parent   = self.frm_min
                                 ,inactive = self.icn_up0
                                 ,active   = self.icn_up1
                                 ,side     = 'top'
                                 )
        self.ent_min = sg.Entry (parent    = self.frm_min
                                ,Composite = True
                                ,width     = 2
                                ,justify   = 'center'
                                )
        self.btn_mnd = sg.Button (parent   = self.frm_min
                                 ,inactive = self.icn_dn0
                                 ,active   = self.icn_dn1
                                 ,side     = 'bottom'
                                 )
    
    def seconds(self):
        self.btn_scu = sg.Button (parent   = self.frm_sec
                                 ,inactive = self.icn_up0
                                 ,active   = self.icn_up1
                                 ,side     = 'top'
                                 )
        self.ent_sec = sg.Entry (parent    = self.frm_sec
                                ,Composite = True
                                ,width     = 2
                                ,justify   = 'center'
                                )
        self.btn_scd = sg.Button (parent   = self.frm_sec
                                 ,inactive = self.icn_dn0
                                 ,active   = self.icn_dn1
                                 ,side     = 'bottom'
                                 )
    
    def buttons(self):
        self.btn_del = sg.Button (parent   = self.frm_btm
                                 ,text     = _('Delete')
                                 ,hint     = _('Delete & Close')
                                 ,side     = 'left'
                                 ,active   = self.icn_del
                                 ,inactive = self.icn_del
                                 )
        self.btn_rst = sg.Button (parent   = self.frm_btm
                                 ,text     = _('Reset')
                                 ,hint     = _('Set the original time')
                                 ,side     = 'left'
                                 ,active   = self.icn_rst
                                 ,inactive = self.icn_rst
                                 )
        self.btn_sav = sg.Button (parent   = self.frm_btm
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
            self.parent.icon(icon_path)



class AddId:
    
    def __init__(self):
        self.parent = sg.Top(sg.objs.root())
        self.widget = self.parent.widget
        sg.Geometry(self.parent).set('800x600')
        self.gui()
    
    def paste_ath(self,event=None):
        self.ent_ath.clear_text()
        self.ent_ath.insert(sg.Clipboard().paste())
    
    def paste_pid(self,event=None):
        self.ent_pid.clear_text()
        self.ent_pid.insert(sg.Clipboard().paste())
    
    def bindings(self):
        sg.bind (obj      = self.ent_ath
                ,bindings = '<ButtonRelease-3>'
                ,action   = self.paste_ath
                )
        sg.bind (obj      = self.ent_pid
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
            self.parent.icon(icon_path)
    
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
        self.frm_prm = sg.Frame (parent = self.parent
                                ,side   = 'left'
                                )
        self.frm_rht = sg.Frame (parent = self.parent
                                ,expand = False
                                ,side   = 'right'
                                )
        self.frm_top = sg.Frame (parent = self.frm_prm
                                ,side   = 'top'
                                ,expand = False
                                )
        self.frm_bot = sg.Frame (parent = self.frm_prm)
        self.frm_rh1 = sg.Frame (parent = self.frm_rht
                                ,side   = 'top'
                                )
        self.frm_rh2 = sg.Frame (parent = self.frm_rht
                                ,side   = 'bottom'
                                )
        self.frm_bt1 = sg.Frame (parent = self.frm_bot
                                ,side   = 'left'
                                )
        self.frm_bt2 = sg.Frame (parent = self.frm_bot
                                ,side   = 'left'
                                )
        self.frm_bt3 = sg.Frame (parent = self.frm_bot
                                ,side   = 'left'
                                )
    
    def widgets(self):
        self.lbl_ath = sg.Label (parent = self.frm_top
                                ,text   = _('Channel title:')
                                ,Close  = True
                                )
        self.ent_ath = sg.Entry (parent    = self.frm_top
                                ,fill      = 'x'
                                ,Composite = True
                                )
        self.lbl_pid = sg.Label (parent = self.frm_top
                                ,text   = _('Playlist ID, channel ID or Youtube user name:')
                                ,Close  = True
                                )
        self.ent_pid = sg.Entry (parent    = self.frm_top
                                ,fill      = 'x'
                                ,Composite = True
                                )
        self.lbl_id1 = sg.Label (parent = self.frm_bt1
                                ,text   = _('Channel title:')
                                ,Close  = True
                                )
        self.lst_id1 = sg.ListBox (parent          = self.frm_bt1
                                  ,SelectionCloses = False
                                  ,SingleClick     = False
                                  ,Composite       = True
                                  ,Scrollbar       = True
                                  )
        self.lbl_id2 = sg.Label (parent = self.frm_bt2
                                ,text   = _('Your ID:')
                                ,Close  = True
                                )
        self.lst_id2 = sg.ListBox (parent          = self.frm_bt2
                                  ,SelectionCloses = False
                                  ,SingleClick     = False
                                  ,Composite       = True
                                  ,Scrollbar       = False
                                  )
        self.lbl_id3 = sg.Label (parent = self.frm_bt3
                                ,text   = _('Playlist ID:')
                                ,Close  = True
                                )
        self.lst_id3 = sg.ListBox (parent          = self.frm_bt3
                                  ,SelectionCloses = False
                                  ,SingleClick     = False
                                  ,Composite       = True
                                  ,Scrollbar       = False
                                  )
        self.btn_opn = sg.Button (parent = self.frm_rh1
                                 ,text   = _('Open URL')
                                 ,side   = 'top'
                                 )
        self.btn_add = sg.Button (parent = self.frm_rh1
                                 ,text   = _('Add')
                                 ,side   = 'top'
                                 )
        self.btn_edt = sg.Button (parent = self.frm_rh1
                                 ,text   = _('Edit')
                                 ,side   = 'top'
                                 )
        self.btn_del = sg.Button (parent = self.frm_rh1
                                 ,text   = _('Delete')
                                 ,side   = 'top'
                                 )
        self.btn_cls = sg.Button (parent = self.frm_rh2
                                 ,text   = _('Save & close')
                                 ,side   = 'bottom'
                                 )
        self.btn_sav = sg.Button (parent = self.frm_rh2
                                 ,text   = _('Save')
                                 ,side   = 'bottom'
                                 )
        self.btn_rst = sg.Button (parent = self.frm_rh2
                                 ,text   = _('Reset')
                                 ,side   = 'bottom'
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
            self.parent.icon(icon_path)
    
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
        self.frm_top = sg.Frame (parent = self.parent
                                ,expand = False
                                ,side   = 'top'
                                )
        self.frm_lft = sg.Frame (parent = self.frm_top
                                ,side   = 'left'
                                )
        self.frm_rht = sg.Frame (parent = self.frm_top
                                ,side   = 'right'
                                )
        self.frm_txt = sg.Frame (parent = self.parent
                                ,side   = 'top'
                                )
    
    def widgets(self):
        self.btn_prv = sg.Button (parent   = self.frm_rht
                                 ,hint     = _('Go to the previous page')
                                 ,inactive = self.icn_prv0
                                 ,active   = self.icn_prv1
                                 ,side     = 'left'
                                 ,bindings = '<Alt-Left>'
                                 )
        self.btn_nxt = sg.Button (parent   = self.frm_rht
                                 ,hint     = _('Go to the next page')
                                 ,inactive = self.icn_nxt0
                                 ,active   = self.icn_nxt1
                                 ,side     = 'left'
                                 ,bindings = '<Alt-Right>'
                                 )
        self.txt_com = sg.TextBox (parent    = self.frm_txt
                                  ,Composite = True
                                  )
    
    def gui(self):
        self.parent = sg.Top(sg.objs.root())
        self.widget = self.parent.widget
        sg.Geometry(self.parent).set('1024x768')
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
        self.framev = sg.Frame (parent = self.parent)
    
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
        sg.ToolTip (obj      = self.opt_max
                   ,text     = _('Videos per page')
                   ,hint_dir = 'bottom'
                   )
    
    def widgets(self):
        self.opt_upd = sg.OptionMenu (parent  = self.frame1
                                     ,items   = update_items
                                     ,default = _('Update')
                                     )
        self.opt_viw = sg.OptionMenu (parent  = self.frame1
                                     ,items   = view_items
                                     ,default = _('View')
                                     )
        self.opt_sel = sg.OptionMenu (parent  = self.frame1
                                     ,items   = selection_items
                                     ,default = _('Selection')
                                     )
        self.opt_edt = sg.OptionMenu (parent  = self.frame1
                                     ,items   = edit_items
                                     ,default = _('Edit')
                                     )
        self.btn_prv = sg.Button (parent   = self.frame1
                                 ,text     = _('←')
                                 ,hint     = _('Go to the previous channel')
                                 ,hint_dir = 'bottom'
                                 )
        self.btn_nxt = sg.Button (parent   = self.frame1
                                 ,text     = _('→')
                                 ,hint     = _('Go to the next channel')
                                 ,hint_dir = 'bottom'
                                 )
        self.btn_ppg = sg.Button (parent   = self.frame1
                                 ,text     = _('‹')
                                 ,hint     = _('Go to the previous page')
                                 ,hint_dir = 'bottom'
                                 )
        self.btn_npg = sg.Button (parent   = self.frame1
                                 ,text     = _('›')
                                 ,hint     = _('Go to the next page')
                                 ,hint_dir = 'bottom'
                                 )
        self.opt_max = sg.OptionMenu (parent  = self.frame1
                                     ,items   = (5,10,15,30,50)
                                     ,default = 50
                                     )
        self.chb_dat = sg.CheckBox (parent = self.frame1
                                   ,Active = False
                                   ,side   = 'left'
                                   )
        self.opt_dat = sg.OptionMenu (parent  = self.frame1
                                     ,items   = (_('Newer than')
                                                ,_('Older than')
                                                )
                                     ,default = _('Newer than')
                                     )
        self.opt_day = sg.OptionMenu (parent = self.frame1)
        self.opt_mth = sg.OptionMenu (parent = self.frame1)
        self.opt_yrs = sg.OptionMenu (parent = self.frame1)
        # Search Youtube
        self.ent_src = sg.Entry (parent    = self.frame2
                                ,Composite = True
                                ,font      = 'Serif 10 italic'
                                ,fg        = 'grey'
                                ,side      = 'left'
                                ,width     = default_entry_width
                                )
        self.ent_src.insert(_('Search Youtube'))
        self.btn_ytb = sg.Button (parent = self.frame2
                                 ,text   = _('Search')
                                 )
        # Paste URL here
        self.ent_url = sg.Entry (parent    = self.frame2
                                ,Composite = True
                                ,font      = 'Serif 10 italic'
                                ,fg        = 'grey'
                                ,side      = 'left'
                                ,width     = default_entry_width
                                )
        self.ent_url.insert(_('Paste URL here'))
        self.opt_url = sg.OptionMenu (parent = self.frame2
                                     ,items  = url_items
                                     )
        # Filter this view
        self.ent_flt = sg.Entry (parent    = self.frame2
                                ,Composite = True
                                ,font      = 'Serif 10 italic'
                                ,fg        = 'grey'
                                ,side      = 'left'
                                ,width     = default_entry_width
                                )
        self.ent_flt.insert(_('Filter this view'))
        self.btn_flt = sg.Button (parent = self.frame2
                                 ,text   = _('Filter')
                                 )
        self.chb_sel = sg.CheckBox (parent = self.frame3
                                   ,Active = False
                                   ,side   = 'left'
                                   )
        self.btn_stm = sg.Button (parent = self.frame3
                                 ,text   = _('Stream')
                                 )
        self.btn_ply = sg.Button (parent = self.frame3
                                 ,text   = _('Play')
                                 )
        self.btn_dld = sg.Button (parent = self.frame3
                                 ,text   = _('Download')
                                 )
        self.btn_del = sg.Button (parent = self.frame3
                                 ,text   = _('Delete')
                                 )
        self.chb_slw = sg.CheckBox (parent = self.frame3
                                   ,Active = True
                                   ,side   = 'left'
                                   )
        self.lab_slw = sg.Label (parent = self.frame3
                                ,text   = _('Slow PC')
                                ,side   = 'left'
                                ,font   = 'Sans 9'
                                ,Close  = False
                                )
        self.opt_trd = sg.OptionMenu (parent = self.frame4
                                     ,side   = 'left'
                                     ,Combo  = True
                                     )
        self.opt_chl = sg.OptionMenu (parent = self.frame4
                                     ,side   = 'left'
                                     ,Combo  = True
                                     )
    
    def update(self,event=None):
        pass
        #cur
        #self.btn_dld.widget.config(state='disabled')
        #self.btn_ply.widget.config(state='disabled')
                  
    def bindings(self):
        # Main window
        sg.bind (obj      = self.parent
                ,bindings = ['<Control-w>','<Control-q>']
                ,action   = self.close
                )
        sg.bind (obj      = self.parent
                ,bindings = '<Escape>'
                ,action   = self.minimize
                )
        # Search Youtube
        sg.bind (obj      = self.ent_src
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.clear_search
                )
        sg.bind (obj      = self.ent_src
                ,bindings = '<ButtonRelease-2>'
                ,action   = self.paste_search
                )
        sg.bind (obj      = self.ent_src
                ,bindings = '<ButtonRelease-3>'
                ,action   = lambda x:self.clear_search(Force=True)
                )
        # Paste URL
        sg.bind (obj      = self.ent_url
                ,bindings = ['<ButtonRelease-1>','<ButtonRelease-2>']
                ,action   = self.paste_url
                )
        sg.bind (obj      = self.ent_url
                ,bindings = '<ButtonRelease-3>'
                ,action   = self.clear_url
                )
        # Filter this view
        sg.bind (obj      = self.ent_flt
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.clear_filter
                )
        sg.bind (obj      = self.ent_flt
                ,bindings = '<ButtonRelease-2>'
                ,action   = self.paste_filter
                )
        sg.bind (obj      = self.ent_flt
                ,bindings = '<ButtonRelease-3>'
                ,action   = lambda x:self.clear_filter(Force=True)
                )
        sg.bind (obj      = self
                ,bindings = '<F3>'
                ,action   = self.clear_search
                )
        sg.bind (obj      = self.lab_slw
                ,bindings = ['<ButtonRelease-1>','<ButtonRelease-3>']
                ,action   = self.chb_slw.toggle
                )
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
    
    def title(self,text=None,selected=0,total=0):
        if not text:
            text = sh.List(lst1=['Yatube',VERSION]).space_items()
            if selected:
                text += _(' (selected: %d/%d)') % (selected,total)
        self.parent.title(text)
    
    def gui(self):
        self.widget = self.parent.widget
        self.frames()
        self.widgets()
        self.tooltips()
        self.icon()
        self.title()
        self.bindings()
        self.update()
    
    def minimize(self,event=None):
        self.widget.iconify()
    
    def icon(self,path=None):
        if not path:
            path = icon_path
        sg.WidgetShared.icon(self.parent,path)
    
    def clear_url(self,event=None):
        self.ent_url.clear_text()
        self.ent_url.widget.config (fg   = 'black'
                                   ,font = 'Serif 10'
                                   )
        self.ent_url.focus()
        
    def paste_url(self,event=None):
        self.clear_url()
        self.ent_url.insert(text=sg.Clipboard().paste())
        
    def paste_search(self,event=None):
        self.clear_search(Force=True)
        self.ent_src.insert(text=sg.Clipboard().paste())
        
    def paste_filter(self,event=None):
        self.clear_filter()
        self.ent_flt.insert(text=sg.Clipboard().paste())



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
        # Do not include 'self.cbox'. Children must come first.
        self._labels  = [self.label1,self.label2,self.label3,self.label4
                        ,self.label5,self.label6,self.label7,self.label8
                        ]
        self._objects = self._labels + [self.frame,self.frame1
                                       ,self.frame2,self.frame3
                                       ,self.frame4,self.frame5
                                       ]

    def values(self):
        self._objects = []
        self._widgets = []
        self._author  = _('Author')
        self._title   = _('Title')
        self._date    = _('Date')
        self._image   = objs.def_image()
    
    def frames(self):
        self.frame  = sg.Frame (parent = self.parent)
        self.frame1 = sg.Frame (parent = self.frame
                               ,side   = 'left'
                               )
        self.frame2 = sg.Frame (parent = self.frame
                               ,side   = 'left'
                               )
        self.frame3 = sg.Frame (parent = self.frame
                               ,side   = 'right'
                               )
        self.frame4 = sg.Frame (parent = self.frame3
                               ,side   = 'left'
                               )
        self.frame5 = sg.Frame (parent = self.frame3
                               ,side   = 'right'
                               )
                                 
    def pic(self):
        if not self._image:
            self._image = objs.def_image()
        self.label2.widget.config(image=self._image)
        # This prevents the garbage collector from deleting the image
        self.label2.widget.image = self._image
    
    def labels(self):
        ''' Fixed width is set to ensure that sizes of a default and
            current video labels are the same.
        '''
        self.label1 = sg.Label (parent = self.frame1
                               ,text   = str(self._no)
                               ,side   = 'right'
                               ,anchor = 'w'
                               ,Close  = False
                               ,font   = 'Mono 10'
                               ,width  = 4
                               )
        ''' 'image' argument must be specified even when the label
            is further configured with such image, otherwise, frames
            will be further extended to encompass the image
            thereby distorting the GUI structure.
        '''
        self.label2 = sg.Label (parent = self.frame2
                               ,text   = _('Image')
                               ,side   = 'right'
                               ,Close  = False
                               ,width  = 196
                               ,image  = self._image
                               )
        self.label3 = sg.Label (parent = self.frame4
                               ,text   = _('Author:')
                               ,Close  = False
                               ,width  = 20
                               )
        self.label4 = sg.Label (parent = self.frame5
                               ,text   = _('Not Available')
                               ,anchor = 'w'
                               ,Close  = False
                               ,width  = 60
                               )
        self.label5 = sg.Label (parent = self.frame4
                               ,text   = _('Title:')
                               ,Close  = False
                               ,width  = 20
                               )
        self.label6 = sg.Label (parent = self.frame5
                               ,text   = _('Not Available')
                               ,anchor = 'w'
                               ,Close  = False
                               ,width  = 60
                               )
        self.label7 = sg.Label (parent = self.frame4
                               ,text   = _('Date:')
                               ,Close  = False
                               ,width  = 20
                               )
        self.label8 = sg.Label (parent = self.frame5
                               ,text   = _('Not Available')
                               ,anchor = 'w'
                               ,Close  = False
                               ,width  = 60
                               )
    
    def checkboxes(self):
        self.cbox = sg.CheckBox (parent = self.frame1
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
        self.label1._text = str(self._no)
        self.label1.reset()
        self.label4._text = self._author
        self.label4.reset()
        self.label6._text = self._title
        self.label6.reset()
        self.label8._text = self._date
        self.label8.reset()
        self.pic()



class Channel:
    
    def __init__(self,parent=None):
        self.values()
        self.parent = parent
        self.gui()
        
    def scroll(self,i):
        f = '[Yatube] gui.Channel.scroll'
        #fix: seems that another unit type is required
        value = i*112.133333333
        sh.log.append (f,_('DEBUG')
                      ,_('Scroll to %d') % value
                      )
        self.canvas.scroll(y=value)
        
    def bindings(self):
        #todo: elaborate the value
        sg.bind (obj      = objs.parent()
                ,bindings = '<Down>'
                ,action   = self.canvas.move_down
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Up>'
                ,action   = self.canvas.move_up
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Left>'
                ,action   = self.canvas.move_left
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Right>'
                ,action   = self.canvas.move_right
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Next>'
                ,action   = self.canvas.move_page_down
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Prior>'
                ,action   = self.canvas.move_page_up
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<End>'
                ,action   = self.canvas.move_bottom
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Home>'
                ,action   = self.canvas.move_top
                )
        sg.bind (obj      = objs._parent
                ,bindings = ['<MouseWheel>','<Button 4>','<Button 5>']
                ,action   = self.mouse_wheel
                )
        
    def values(self):
        ''' These values set the width and height of the frame that 
            contains videos and therefore the scrolling region.
            The default Youtube video picture has the dimensions of
            196x110, therefore, the channel frame embedding 10 videos
            will have the height of at least 1100.
        '''
        self._max_x = 1024
        self._max_y = 1120
        
    def frames(self):
        self.frame   = sg.Frame (parent = self.parent)
        self.frame_y = sg.Frame (parent = self.frame
                                ,expand = False
                                ,fill   = 'y'
                                ,side   = 'right'
                                )
        self.frame_x = sg.Frame (parent = self.frame
                                ,expand = False
                                ,fill   = 'x'
                                ,side   = 'bottom'
                                )
        # A frame that contains all contents except for scrollbars
        self.frame1  = sg.Frame (parent = self.frame
                                ,side   = 'left'
                                ,width  = self._max_x
                                ,height = self._max_y
                                )
    
    def canvases(self):
        ''' Create a canvas before an object being embedded, otherwise,
            the canvas will overlap this object.
        '''
        self.canvas  = sg.Canvas(parent=self.frame1)
        self.frm_emb = sg.Frame(parent=self.frame1)
        self.canvas.embed(self.frm_emb)
    
    def scrollbars(self):
        sg.Scrollbar (parent = self.frame_x
                     ,scroll = self.canvas
                     ,Horiz  = True
                     )
        sg.Scrollbar (parent = self.frame_y
                     ,scroll = self.canvas
                     ,Horiz  = False
                     )
    
    def gui(self):
        self.widget = self.parent.widget
        self.frames()
        self.canvases()
        self.scrollbars()
        self.canvas.focus()
        self.bindings()
        # This shows the 1st video
        self.canvas.region (x = self._max_x
                           ,y = self._max_y
                           )
        
    def mouse_wheel(self,event=None):
        ''' #todo: fix: too small delta in Windows
            В Windows XP delta == -120, однако, в других версиях оно
            другое
        '''
        if event.num == 5 or event.delta < 0:
            self.canvas.move_down()
        if event.num == 4 or event.delta > 0:
            self.canvas.move_up()
        return 'break'



class Objects:
    
    def __init__(self):
        self._def_image = self._channel = self._menu = self._parent \
                        = self._context = self._summary \
                        = self._progress = self._blacklist \
                        = self._subscribe = self._comments = None
    
    def comments(self):
        if not self._comments:
            top = sg.Top(parent=sg.objs.root())
            sg.Geometry(parent=top).set('1024x768')
            self._comments = sg.TextBox (parent   = top
                                        ,SpReturn = True
                                        )
            self._comments.icon(icon_path)
            self._comments.title(_('Comments'))
        return self._comments
    
    def subscribe(self):
        if not self._subscribe:
            top = sg.Top(parent=sg.objs.root())
            sg.Geometry(parent=top).set('1024x768')
            self._subscribe = sg.TextBox (parent   = top
                                         ,SpReturn = False
                                         )
            self._subscribe.icon(icon_path)
            self._subscribe.title(_('Edit subscriptions:'))
        return self._subscribe
    
    def blacklist(self):
        if not self._blacklist:
            top = sg.Top(parent=sg.objs.root())
            sg.Geometry(parent=top).set('1024x768')
            self._blacklist = sg.TextBox (parent   = top
                                         ,SpReturn = False
                                         )
            self._blacklist.icon(icon_path)
            self._blacklist.title(_('Edit the blacklist:'))
        return self._blacklist
    
    def progress(self):
        if not self._progress:
            self._progress = sg.ProgressBar()
            self._progress.obj.icon(icon_path)
            # Widget is not created yet, do not 'center' it here!
        return self._progress
    
    def summary(self):
        if not self._summary:
            top = sg.Top(parent=sg.objs.root())
            sg.Geometry(parent=top).set('1024x768')
            self._summary = sg.TextBox(parent=top)
            self._summary.icon(icon_path)
            self._summary.title(_('Full summary:'))
        return self._summary
    
    def context(self):
        if not self._context:
            ''' #fix: Modifying 'SingleClick' and 'SelectionCloses' is
                needed here only not to toggle the checkbox of
                the parent (this is a bug and should be fixed).
            '''
            self._context = sg.ListBox (parent          = sg.objs.new_top()
                                       ,lst             = context_items
                                       ,title           = _('Select an action:')
                                       ,icon            = icon_path
                                       ,SingleClick     = False
                                       ,SelectionCloses = True
                                       )
            self._context.close()
        return self._context
    
    def def_image(self):
        if not self._def_image:
            path = sh.objs.pdir().add('..','resources','nopic.png')
            self._def_image = sg.Image().open(path=path)
        return self._def_image

    def channel(self,parent=None):
        f = '[Yatube] gui.Objects.channel'
        if not self._channel:
            if parent is None:
                sh.log.append (f,_('INFO')
                              ,_('Set the default parent.')
                              )
                parent = self.menu().framev
            self._channel = Channel(parent=parent)
        return self._channel
        
    def parent(self):
        if not self._parent:
            self._parent = sg.Top(parent=sg.objs.root())
        return self._parent
    
    def menu(self):
        if not self._menu:
            self._menu = Menu(parent=self.parent())
        return self._menu


objs = Objects()


if __name__ == '__main__':
    # Show the menu
    sg.objs.start()
    objs.menu().show()
    sg.objs.end()
    '''
    # Simulate meta updating
    sg.objs.start()
    import time
    wait = WaitMeta(parent=sg.objs.new_top())
    wait.show()
    time.sleep(2)
    wait.reset(author=_('BLOCKED'))
    wait.update()
    time.sleep(2)
    wait.close()
    sg.objs.end()
    '''
    '''
    # Simulate channel filling
    max_videos = 29
    sg.objs.start()
    sg.Geometry(parent=objs.parent()).set('1024x600')
    objs.channel(parent=objs.menu().framev)
    for i in range(max_videos):
        #todo: rework
        objs._channel.add(no=i+1)
        video_gui = objs._channel._videos[-1]
        video_gui.reset (author = 'Author (%d)' % (i + 1)
                        ,title  = 'Title (%d)'  % (i + 1)
                        ,date   = '2018-12-31'
                        )
    sg.objs.root().idle()
    # height = 112.133333333
    height = objs._channel.frame.widget.winfo_reqheight()
    sh.log.append ('[Yatube] gui.__main__'
                  ,_('DEBUG')
                  ,_('Widget must be at least %d pixels in height') \
                  % height
                  )
    # y = max_videos * height
    objs._channel.canvas.region (x        = 1024
                                ,y        = height
                                ,x_border = 20
                                ,y_border = 20
                                )
    objs._channel.canvas.move_top()
    objs._menu.show()
    sg.objs.end()
    '''
    '''
    # Progress bar
    sg.objs.start()
    objs.progress().add()
    objs._progress.show()
    sg.objs.end()
    '''
