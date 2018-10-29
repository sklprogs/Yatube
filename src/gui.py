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

product = 'Yatube'
version = '1.5'

context_items = (_('Show the full summary')
                ,_('Stream')
                ,_('Play')
                ,_('Download')
                ,_('Mark as watched')
                ,_('Mark as not watched')
                ,_('Delete the downloaded file')
                ,_('Add to favorites')
                ,_('Remove from favorites')
                ,_('Add to watchlist')
                ,_('Remove from watchlist')
                ,_('Extract links')
                ,_('Load this channel')
                ,_('Block this channel')
                ,_('Unblock')
                ,_('Subscribe to this channel')
                ,_('Unsubscribe')
                ,_('Open video URL')
                ,_('Copy video URL')
                ,_('Show comments')
                ,_('Open channel URL')
                ,_('Copy channel URL')
                )

url_items = (_('Show summary')
            ,_('Stream')
            ,_('Play')
            ,_('Download')
            ,_('Delete')
            ,_('Extract links')
            ,_('Full menu')
            )

other_actions = (_('Other')
                ,_('Manage subscriptions')
                ,_('Manage blocked authors')
                ,_('Manage blocked words')
                ,_('Show new videos')
                ,_('History')
                ,_('Favorites')
                ,_('Watchlist')
                ,_('Welcome screen')
                ,_('Select all new videos')
                ,_('Mark as watched')
                ,_('Mark as not watched')
                ,_('Add to favorites')
                ,_('Remove from favorites')
                ,_('Add to watchlist')
                ,_('Remove from watchlist')
                ,_('Delete selected')
                )

default_entry_width = 19
icon_path = sh.objs.pdir().add('..','resources','icon_64x64_yatube.gif')


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
    
    def widgets(self):
        self.btn_upd = sg.Button (parent = self.frame1
                                 ,text   = _('Update subscriptions')
                                 )
        self.btn_upd.focus()
        self.opt_act = sg.OptionMenu (parent  = self.frame1
                                     ,items   = other_actions
                                     ,default = _('Other')
                                     )
        self.btn_prv = sg.Button (parent = self.frame1
                                 ,text   = _('Backward')
                                 )
        self.btn_nxt = sg.Button (parent = self.frame1
                                 ,text   = _('Forward')
                                 )
        self.lbl_max = sg.Label (parent = self.frame1
                                ,side   = 'left'
                                ,text   = _('Max videos:')
                                ,font   = 'Sans 10'
                                ,Close  = False
                                )
        self.opt_max = sg.OptionMenu (parent  = self.frame1
                                     ,items   = (5,10,15,30,50,100)
                                     ,default = 30
                                     )
        self.lbl_wrp = sg.Label (parent = self.frame1
                                ,side   = 'left'
                                ,text   = _('Page:')
                                ,font   = 'Sans 10'
                                ,Close  = False
                                )
        self.opt_wrp = sg.OptionMenu (parent = self.frame1
                                     ,anchor = 'w'
                                     ,Combo  = True
                                     )
        self.opt_wrp.widget.config(width=4)
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
                                   ,action = toggle_select
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
            text = sh.List(lst1=[product,version]).space_items()
            if selected:
                text += _(' (selected: %d/%d)') % (selected,total)
        self.parent.title(text)
    
    def gui(self):
        self.widget = self.parent.widget
        self.frames()
        self.widgets()
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
        self.ent_url.widget.config(fg='black',font='Serif 10')
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
        self._widgets  = []
        self._author   = _('Author')
        self._title    = _('Title')
        self._duration = _('Duration')
        self._image    = objs.def_image()
    
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
                               ,text   = _('Duration:')
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
                                ,action = report_selection
                                )
                                
    def gui(self):
        self.frames()
        self.checkboxes()
        self.labels()
        self.objects()
        self.bindings()
        
    def toggle_cbox(self,event=None):
        self.cbox.toggle()
        report_selection()
    
    def bindings(self):
        for obj in self._objects:
            sg.bind (obj      = obj
                    ,bindings = '<ButtonRelease-1>'
                    ,action   = self.toggle_cbox
                    )
        
    def reset (self,author,title,duration
              ,image=None,no=0
              ):
        self._author   = author
        self._title    = title
        self._duration = duration
        self._image    = image
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
        self.label8._text = self._duration
        self.label8.reset()
        self.pic()



class Channel:
    
    def __init__(self,parent=None):
        self.values()
        self.parent = parent
        self.gui()
        
    def scroll(self,i):
        f = 'gui.Channel.scroll'
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
        self._no     = 0
        self._videos = []
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
        sg.Scrollbar (parent     = self.frame_x
                     ,scroll     = self.canvas
                     ,Horizontal = True
                     )
        sg.Scrollbar (parent     = self.frame_y
                     ,scroll     = self.canvas
                     ,Horizontal = False
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
        
    def add(self,no=1):
        self._no = no
        self._videos.append (Video (parent = self.frm_emb
                                   ,no     = self._no
                                   )
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
                        = self._subscribe = self._wait = self._comments\
                        = None
        
    def comments(self):
        if not self._comments:
            top = sg.Top(parent=sg.objs.root())
            sg.Geometry(parent=top).set('1024x768')
            self._comments = sg.TextBox (parent        = top
                                        ,SpecialReturn = True
                                        )
            self._comments.icon(icon_path)
            self._comments.title(_('First 100 comments:'))
        return self._comments
    
    def wait(self):
        if self._wait is None:
            self._wait = WaitMeta(parent=sg.Top(parent=sg.objs.root()))
        return self._wait
    
    def subscribe(self):
        if not self._subscribe:
            top = sg.Top(parent=sg.objs.root())
            sg.Geometry(parent=top).set('1024x768')
            self._subscribe = sg.TextBox (parent        = top
                                         ,SpecialReturn = False
                                         )
            self._subscribe.icon(icon_path)
            self._subscribe.title(_('Edit subscriptions:'))
        return self._subscribe
    
    def blacklist(self):
        if not self._blacklist:
            top = sg.Top(parent=sg.objs.root())
            sg.Geometry(parent=top).set('1024x768')
            self._blacklist = sg.TextBox (parent        = top
                                         ,SpecialReturn = False
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
                                       ,SelectionCloses = False
                                       )
            self._context.close()
        return self._context
    
    def def_image(self):
        if not self._def_image:
            path = sh.objs.pdir().add('..','resources','nopic.png')
            self._def_image = sg.Image().open(path=path)
        return self._def_image

    def channel(self,parent=None):
        f = 'gui.Objects.channel'
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



class WaitMeta:
    
    def __init__(self,parent):
        self._video = None
        self.parent = parent
        self.gui()
        
    def icon(self,path=None):
        if not path:
            path = icon_path
        sg.WidgetShared.icon(self.parent,path)
    
    def title(self,text=None):
        if not text:
            text = _('Get video info')
        self.parent.title(text)
    
    def gui(self):
        self.frame = sg.Frame (parent = self.parent)
        self.label = sg.Label (parent = self.frame
                              ,expand = True
                              ,fill   = 'x'
                              ,text   = _('Loading metadata. Please wait...')
                              )
        self._video = Video(parent=self.frame)
        self.title()
        self.icon()
        
    def update(self):
        self.frame.widget.update()
        
    def reset (self,author=_('Author'),title=_('Title')
              ,duration=_('Duration'),image=None,no=1
              ):
        f = 'gui.WaitMeta.reset'
        if self._video:
            ''' Though 'no' is already set when creating 'gui.Video',
                we reset this value here in order not to meddle with it
                in 'self.gui'.
            '''
            self._video.reset (author   = author
                              ,title    = title
                              ,duration = duration
                              ,image    = image
                              ,no       = no
                              )
        else:
            sh.com.cancel(f)
        
    def show(self):
        self.parent.show(Lock=False)
        self.update()
        self.parent.center(Force=1)
        
    def close(self):
        self.parent.close()


def report_selection(event=None):
    count = 0
    for video_gui in objs.channel()._videos:
        if video_gui.cbox.get():
            count += 1
    objs.menu().title (selected = count
                      ,total    = len(objs._channel._videos)
                      )
                      
def toggle_select(event=None):
    if objs.menu().chb_sel.get():
        for video in objs.channel()._videos:
            video.cbox.enable()
    else:
        for video in objs.channel()._videos:
            video.cbox.disable()
    report_selection()


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
        objs._channel.add(no=i+1)
        video_gui = objs._channel._videos[-1]
        video_gui.reset (author   = 'Author (%d)' % (i + 1)
                        ,title    = 'Title (%d)'  % (i + 1)
                        ,duration = 60 * (i + 1)
                        )
    sg.objs.root().idle()
    # height = 112.133333333
    height = objs._channel.frame.widget.winfo_reqheight()
    sh.log.append ('gui.__main__'
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
