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
version = '1.1'

context_items = (_('Show the full summary')
                ,_('Download')
                ,_('Play')
                #,_('Stream')
                ,_('Toggle the download status')
                ,_('Delete the downloaded file')
                ,_('Extract links')
                ,_('Load this channel')
                ,_('Block this channel')
                ,_('Unblock')
                ,_('Subscribe to this channel')
                ,_('Unsubscribe')
                ,_('Open video URL')
                ,_('Copy video URL')
                ,_('Open channel URL')
                ,_('Copy channel URL')
                )

url_items = (_('Show summary')
            ,_('Download')
            ,_('Play')
            #,_('Stream')
            ,_('Delete')
            ,_('Extract links')
            ,_('Full menu')
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
        self.widget.destroy()
    
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
        ''' We can create an additional frame here for Channel, but
            Channel.bindings needs to have Toplevel as a parent.
        '''
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
        self.btn_sub = sg.Button (parent = self.frame1
                                 ,text   = _('Manage subscriptions')
                                 )
        self.btn_blk = sg.Button (parent = self.frame1
                                 ,text   = _('Manage blocklist')
                                 )
        self.btn_upd = sg.Button (parent = self.frame1
                                 ,text   = _('Update subscriptions')
                                 )
        self.btn_upd.focus()
        self.btn_all = sg.Button (parent = self.frame1
                                 ,text   = _('Select all new videos')
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
        self.btn_dld = sg.Button (parent = self.frame3
                                 ,text   = _('Download selected')
                                 )
        self.btn_ply = sg.Button (parent = self.frame3
                                 ,text   = _('Play')
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
    
    def title(self,text=None):
        if not text:
            text = sh.List(lst1=[product,version]).space_items()
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
    
    def __init__(self,parent,no=0):
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
        #This prevents the garbage collector from deleting the image
        self.label2.widget.image = self._image
    
    def labels(self):
        ''' Fixed width is set to ensure that sizes of a default and
            current video labels are the same.
        '''
        self.label1 = sg.Label (parent = self.frame1
                               ,text   = _('#%d') % self._no
                               ,side   = 'right'
                               ,anchor = 'w'
                               ,Close  = False
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
                                )
                                
    def bindings(self):
        for obj in self._objects:
            sg.bind (obj      = obj
                    ,bindings = '<ButtonRelease-1>'
                    ,action   = self.cbox.toggle
                    )
    
    def gui(self):
        self.frames()
        self.checkboxes()
        self.labels()
        self.objects()
        self.bindings()
        
    def reset (self,author,title,duration
              ,image=None,no=0
              ):
        self._no       = no
        self._author   = author
        self._title    = title
        self._duration = duration
        self._image    = image
        '''
        #note #todo For some reason, using 'widget.config' or 
        'Label.text' resets config options here.
        '''
        self.label1._text = _('#%d') % self._no
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
        self.set_parent()
        self.gui()
        
    def set_parent(self):
        if self.parent:
            self.obj = self.parent
        else:
            self.parent = sg.objs.root()
            self.obj    = sg.SimpleTop(parent=self.parent)
        
    def bindings(self):
        ''' If possible, most actions should be bound here, not in
            the controller (otherwise, we will have to rebind those
            actions each time the parent is destroyed).
        '''
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
    
    # orphan
    def center(self,max_x=0,max_y=0):
        if max_x and max_y:
            pass
        else:
            max_x = self.widget.winfo_reqwidth()
            max_y = self.widget.winfo_reqheight()
        sh.log.append ('Channel.center'
                      ,_('DEBUG')
                      ,_('Widget sizes: %dx%d') % (max_x,max_y)
                      )
        self.widget.update_idletasks()
        x = self.widget.winfo_screenwidth()/2 - max_x/2
        y = self.widget.winfo_screenheight()/2 - max_y/2
        self.widget.geometry("%dx%d+%d+%d" % ((max_x,max_y) + (x, y)))
        sh.log.append ('Channel.center'
                      ,_('INFO')
                      ,_('Set geometry to "%dx%d+%d+%d"') \
                       % ((max_x,max_y) + (x, y))
                      )
    
    def scroll(self):
        # Scroll canvas to the current video as the channel is loading
        self.canvas.widget.xview_moveto(0)
        self.canvas.move_bottom()
    
    def update_scroll(self):
        # Do this after adding all videos
        sg.objs.root().widget.update_idletasks()
        self._max_y = self.label.widget.winfo_reqheight()
        self._max_x = self.label.widget.winfo_reqwidth()
        '''
        # Too frequent
        sh.log.append ('Channel.update_scroll'
                      ,_('DEBUG')
                      ,_('Widget sizes: %dx%d') \
                       % (self._max_x,self._max_y)
                      )
        '''
        self.canvas.region (x        = self._max_x
                           ,y        = self._max_y
                           ,x_border = 20
                           ,y_border = 20
                           )
        self.scroll()
        
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
        self.frame   = sg.Frame (parent = self.obj)
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
    
    # Called in 'canvases'
    def labels(self):
        # Frames embedded into a canvas are not scrollable
        self.label  = sg.Label (parent = self.frame1
                               ,expand = True
                               ,fill   = 'both'
                               ,Close  = False
                               ,text   = _('Videos are placed here')
                               )
    
    def canvases(self):
        ''' Create a canvas before an object being embedded, otherwise,
            the canvas will overlap this object.
        '''
        self.canvas = sg.Canvas(parent=self.frame1)
        self.labels()
        self.canvas.embed(self.label)
    
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
        self.widget = self.obj.widget
        self.frames()
        self.canvases()
        self.scrollbars()
        self.canvas.focus()
        self.bindings()
        # This shows the 1st video
        self.canvas.region (x = self._max_x
                           ,y = self._max_y
                           )
        
    def add(self,no=0):
        self._no = no
        self._videos.append (Video (parent = self.label
                                   ,no     = self._no
                                   )
                            )
        
    def show(self,event=None):
        self.obj.show()
        
    def close(self,event=None):
        self.widget.destroy()
        
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
                        = self._subscribe = None
        
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
        if not self._channel:
            self._channel = Channel(parent=parent)
        return self._channel
        
    def parent(self):
        if not self._parent:
            self._parent = sg.SimpleTop(parent=sg.objs.root())
        return self._parent
    
    def menu(self):
        if not self._menu:
            self._menu = Menu(parent=self.parent())
            self._menu.parent.center()
        return self._menu


objs = Objects()


if __name__ == '__main__':
    '''
    # Menu
    sg.objs.start()
    sg.Geometry(parent=objs.parent()).set('1024x600')
    objs.menu().widget.wait_window()
    sg.objs.end()
    '''
    '''
    # Simulate filling a channel
    sg.objs.start(Close=0)
    objs.channel(parent=objs.parent())
    sg.objs.root().widget.update_idletasks()
    import time
    for i in range(20):
        objs._channel.add(no=i)
        video_gui = objs._channel._videos[-1]
        video_gui.reset (no       = i + 1
                        ,author   = 'Author (%d)' % (i + 1)
                        ,title    = 'Title (%d)'  % (i + 1)
                        ,duration = 60 * (i + 1)
                        )
        sg.objs.root().widget.update_idletasks()
        time.sleep(1)
    sg.objs.root().widget.wait_window()
    '''
    # Progress bar
    sg.objs.start(Close=0)
    objs.progress().add()
    objs._progress.show()
    objs._progress.obj.center()
    sg.objs.root().widget.wait_window()
