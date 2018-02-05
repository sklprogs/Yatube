#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','./locale')

product = 'Yatube'
version = '(alpha)'
# A default picture height
def_height = 110


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
        if Force or self.en_fltr.get() == _('Filter this view'):
            self.en_fltr.clear_text()
        self.en_fltr.widget.config(fg='black',font='Serif 10')
        self.en_fltr.focus()
        #todo: Restore filtered videos here
                   
    def clear_search(self,event=None,Force=False):
        if Force or self.en_srch.get() == _('Search Youtube'):
            self.en_srch.clear_text()
        self.en_srch.widget.config(fg='black',font='Serif 10')
        self.en_srch.focus()
    
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
        self.cb_date = sg.CheckBox (parent = self.frame1
                                   ,Active = False
                                   ,side   = 'left'
                                   )
        self.om_date = sg.OptionMenu (parent  = self.frame1
                                     ,items   = (_('Newer than')
                                                ,_('Older than')
                                                )
                                     ,default = _('Newer than')
                                     )
        self.om_wday = sg.OptionMenu (parent  = self.frame1)
        self.om_mnth = sg.OptionMenu (parent  = self.frame1)
        self.om_yers = sg.OptionMenu (parent  = self.frame1)
        # Search Youtube
        self.en_srch = sg.Entry (parent    = self.frame2
                                ,Composite = True
                                ,font      = 'Serif 10 italic'
                                ,fg        = 'grey'
                                ,side      = 'left'
                                )
        self.en_srch.insert(_('Search Youtube'))
        self.btn_ytb = sg.Button (parent = self.frame2
                                 ,text   = _('Search')
                                 )
        # Get video from URL
        self.en_gurl = sg.Entry (parent    = self.frame2
                                ,Composite = True
                                ,font      = 'Serif 10 italic'
                                ,fg        = 'grey'
                                ,side      = 'left'
                                )
        self.en_gurl.insert(_('Get video from URL'))
        self.btn_url = sg.Button (parent = self.frame2
                                 ,text   = _('Download')
                                 )
        # Get links from URL
        self.en_lnks = sg.Entry (parent    = self.frame2
                                ,Composite = True
                                ,font      = 'Serif 10 italic'
                                ,fg        = 'grey'
                                ,side      = 'left'
                                )
        self.en_lnks.insert(_('Get links from URL'))
        self.btn_lnk = sg.Button (parent = self.frame2
                                 ,text   = _('Get')
                                 )
        # Filter this view
        self.en_fltr = sg.Entry (parent    = self.frame2
                                ,Composite = True
                                ,font      = 'Serif 10 italic'
                                ,fg        = 'grey'
                                ,side      = 'left'
                                )
        self.en_fltr.insert(_('Filter this view'))
        self.btn_flt = sg.Button (parent = self.frame2
                                 ,text   = _('Filter')
                                 )
        self.cb_slct = sg.CheckBox (parent = self.frame3
                                   ,Active = False
                                   ,side   = 'left'
                                   )
        self.btn_dld = sg.Button (parent = self.frame3
                                 ,text   = _('Download selected')
                                 )
        self.btn_ply = sg.Button (parent = self.frame3
                                 ,text   = _('Play')
                                 )
        self.om_trnd = sg.OptionMenu (parent  = self.frame4
                                     ,side    = 'left'
                                     )
        self.om_chnl = sg.OptionMenu (parent  = self.frame4
                                     ,side    = 'left'
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
        sg.bind (obj      = self.en_srch
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.clear_search
                )
        sg.bind (obj      = self.en_srch
                ,bindings = '<ButtonRelease-2>'
                ,action   = self.paste_search
                )
        sg.bind (obj      = self.en_srch
                ,bindings = '<ButtonRelease-3>'
                ,action   = lambda x:self.clear_search(Force=True)
                )
        # Get video from URL
        sg.bind (obj      = self.en_gurl
                ,bindings = ['<ButtonRelease-1>','<ButtonRelease-2>']
                ,action   = self.paste_url
                )
        sg.bind (obj      = self.en_gurl
                ,bindings = '<ButtonRelease-3>'
                ,action   = self.clear_url
                )
        # Get links from URL
        sg.bind (obj      = self.en_lnks
                ,bindings = ['<ButtonRelease-1>','<ButtonRelease-2>']
                ,action   = self.paste_links
                )
        sg.bind (obj      = self.en_lnks
                ,bindings = '<ButtonRelease-3>'
                ,action   = self.clear_links
                )
        # Filter this view
        sg.bind (obj      = self.en_fltr
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.clear_filter
                )
        sg.bind (obj      = self.en_fltr
                ,bindings = '<ButtonRelease-2>'
                ,action   = self.paste_filter
                )
        sg.bind (obj      = self.en_fltr
                ,bindings = '<ButtonRelease-3>'
                ,action   = lambda x:self.clear_filter(Force=True)
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
            path = sh.objs.pdir().add ('resources'
                                      ,'icon_64x64_yatube.gif'
                                      )
        sg.WidgetShared.icon(self.parent,path)
    
    def clear_url(self,event=None):
        self.en_gurl.clear_text()
        self.en_gurl.widget.config(fg='black',font='Serif 10')
        self.en_gurl.focus()
        
    def paste_url(self,event=None):
        self.clear_url()
        self.en_gurl.insert(text=sg.Clipboard().paste())
        
    def paste_search(self,event=None):
        self.clear_search(Force=True)
        self.en_srch.insert(text=sg.Clipboard().paste())
        
    def paste_filter(self,event=None):
        self.clear_filter()
        self.en_fltr.insert(text=sg.Clipboard().paste())
    
    def paste_links(self,event=None):
        self.clear_links()
        self.en_lnks.insert(text=sg.Clipboard().paste())
    
    def clear_links(self,event=None):
        self.en_lnks.clear_text()
        self.en_lnks.widget.config(fg='black',font='Serif 10')
        self.en_lnks.focus()
    
    def zzz(self):
        pass


class Video:
    
    def __init__(self,parent,no=0):
        self._no    = no
        self.parent = parent
        self.values()
        self.gui()
    
    def values(self):
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
        sg.bind (obj      = self.label1
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.cbox.toggle
                )
        sg.bind (obj      = self.label2
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.cbox.toggle
                )
        sg.bind (obj      = self.label3
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.cbox.toggle
                )
        sg.bind (obj      = self.label4
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.cbox.toggle
                )
        sg.bind (obj      = self.label5
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.cbox.toggle
                )
        sg.bind (obj      = self.label6
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.cbox.toggle
                )
        sg.bind (obj      = self.label7
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.cbox.toggle
                )
        sg.bind (obj      = self.label8
                ,bindings = '<ButtonRelease-1>'
                ,action   = self.cbox.toggle
                )
    
    def gui(self):
        self.frames()
        self.checkboxes()
        self.labels()
        self.bindings()
        
    def reset (self,author,title,duration
              ,logic,image=None,no=0
              ):
        self._no       = no
        self._author   = author
        self._title    = title
        self._duration = duration
        self._image    = image
        self.logic     = logic
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
        sg.bind (obj      = objs.parent()
                ,bindings = '<Down>'
                ,action   = self.scroll_down
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Up>'
                ,action   = self.scroll_up
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Left>'
                ,action   = self.scroll_left
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Right>'
                ,action   = self.scroll_right
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Next>'
                ,action   = self.scroll_page_down
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Prior>'
                ,action   = self.scroll_page_up
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<End>'
                ,action   = self.scroll_end
                )
        sg.bind (obj      = objs._parent
                ,bindings = '<Home>'
                ,action   = self.scroll_start
                )
                
    def scroll_left(self,*args):
        self.canvas.widget.xview_scroll(-1,'units')
        
    def scroll_right(self,*args):
        self.canvas.widget.xview_scroll(1,'units')
        
    def scroll_up(self,*args):
        self.canvas.widget.yview_scroll(-1,'units')
        
    def scroll_down(self,*args):
        self.canvas.widget.yview_scroll(1,'units')
        
    def scroll_page_down(self,*args):
        self.canvas.widget.yview_scroll(1,'pages')
        
    def scroll_page_up(self,*args):
        self.canvas.widget.yview_scroll(-1,'pages')
        
    def scroll_start(self,*args):
        self.canvas.widget.yview_moveto(0)
        
    def scroll_end(self,*args):
        self.canvas.widget.yview_moveto(len(self._videos)*def_height)
    
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
    
    def update_scroll(self):
        # Do this after adding all videos
        sg.objs.root().widget.update_idletasks()
        self._max_y = self.label.widget.winfo_reqheight()
        self._max_x = self.label.widget.winfo_reqwidth()
        sh.log.append ('Channel.update_scroll'
                      ,_('DEBUG')
                      ,_('Widget sizes: %dx%d') \
                       % (self._max_x,self._max_y)
                      )
        self.scrollregion()
        self.scroll2start()
        
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
                     ,scroll_obj = self.canvas
                     ,Horizontal = True
                     )
        sg.Scrollbar (parent     = self.frame_y
                     ,scroll_obj = self.canvas
                     ,Horizontal = False
                     )
    
    def gui(self):
        self.widget = self.obj.widget
        self.frames()
        self.canvases()
        self.scrollbars()
        self.canvas.focus()
        self.bindings()
        # This will allow to show the 1st video
        self.scrollregion()
        
    def add(self,no=0):
        self._no = no
        self._videos.append (Video (parent = self.label
                                   ,no     = self._no
                                   )
                            )
                            
    def scrollregion(self):
        if self._max_x and self._max_y:
            self.canvas.widget.configure \
                (scrollregion = (-self._max_x/2,-self._max_y/2
                                , self._max_x/2, self._max_y/2
                                )
                )
        else:
            sh.log.append ('Channel.scrollregion'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def scroll2start(self,*args):
        self.canvas.widget.xview_moveto(0)
        # Scroll canvas to the current video as the channel is loading
        self.canvas.widget.yview_moveto(self._no*def_height)
        
    def show(self,*args):
        self.obj.show()
        
    def close(self,*args):
        self.widget.destroy()



class Objects:
    
    def __init__(self):
        self._def_image = self._channel = self._menu = self._parent \
                        = None
        
    def def_image(self):
        if not self._def_image:
            path = sh.objs.pdir().add('nopic.png')
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
        return self._menu


objs = Objects()


if __name__ == '__main__':
    sg.objs.start()
    objs.menu().show()
    sg.objs.end()
