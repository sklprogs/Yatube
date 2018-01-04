#!/usr/bin/python3

from PIL import Image as ig
from PIL import ImageTk as it
import shared as sh
import sharedGUI as sg
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','./locale')


class Video:
    
    def __init__(self,parent_obj,no=0,no_pic_image=None):
        self._no        = no
        self._np_image  = no_pic_image
        self.parent_obj = parent_obj
        self.values()
        self.gui()
    
    def values(self):
        self._author   = _('Author')
        self._title    = _('Title')
        self._duration = _('Duration')
        self._picture  = None
    
    def frames(self):
        self.frame  = sg.Frame (parent_obj = self.parent_obj)
        self.frame1 = sg.Frame (parent_obj = self.frame
                               ,side       = 'left'
                               )
        self.frame2 = sg.Frame (parent_obj = self.frame
                               ,side       = 'left'
                               )
        self.frame3 = sg.Frame (parent_obj = self.frame
                               ,side       = 'right'
                               )
        self.frame4 = sg.Frame (parent_obj = self.frame3
                               ,side       = 'left'
                               )
        self.frame5 = sg.Frame (parent_obj = self.frame3
                               ,side       = 'right'
                               )
                                 
    def pic(self):
        if self._picture and sh.File(file=self._picture).Success:
            image = it.PhotoImage(ig.open(self._picture))
            self.label2.widget.config(image=image)
            #This prevents the garbage collector from deleting the image
            self.label2.widget.image = image
    
    def labels(self):
        ''' Fixed width is set to ensure that sizes of a default and
            current video labels are the same.
        '''
        self.label1 = sg.Label (parent_obj = self.frame1
                               ,text       = _('#%d') % self._no
                               ,side       = 'right'
                               ,anchor     = 'w'
                               ,Close      = False
                               ,width      = 4
                               )
        self.label2 = sg.Label (parent_obj = self.frame2
                               ,text       = _('Image')
                               ,side       = 'right'
                               ,image      = self._np_image
                               ,Close      = False
                               ,width      = 196
                               )
        self.label3 = sg.Label (parent_obj = self.frame4
                               ,text       = _('Author:')
                               ,Close      = False
                               ,width      = 20
                               )
        self.label4 = sg.Label (parent_obj = self.frame5
                               ,text       = _('Not Available')
                               ,anchor     = 'w'
                               ,Close      = False
                               ,width      = 60
                               )
        self.label5 = sg.Label (parent_obj = self.frame4
                               ,text       = _('Title:')
                               ,Close      = False
                               ,width      = 20
                               )
        self.label6 = sg.Label (parent_obj = self.frame5
                               ,text       = _('Not Available')
                               ,anchor     = 'w'
                               ,Close      = False
                               ,width      = 60
                               )
        self.label7 = sg.Label (parent_obj = self.frame4
                               ,text       = _('Duration:')
                               ,Close      = False
                               ,width      = 20
                               )
        self.label8 = sg.Label (parent_obj = self.frame5
                               ,text       = _('Not Available')
                               ,anchor     = 'w'
                               ,Close      = False
                               ,width      = 60
                               )
    
    def checkboxes(self):
        self.cbox = sg.CheckBox (parent_obj = self.frame1
                                ,Active     = False
                                ,side       = 'left'
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
        
    def reset(self,author,title,duration,picture=None,no=0):
        self._no       = no
        self._author   = author
        self._title    = title
        self._duration = duration
        self._picture  = picture
        '''
        # note # todo For some reason, using 'widget.config' or 
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
    
    def __init__(self,name=_('Channel')):
        self.values()
        self._name = name
        self.gui()
        
    def bindings(self):
        sg.bind (obj      = self.obj
                ,bindings = ['<Control-q>','<Control-w>','<Escape>']
                ,action   = self.close
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Down>'
                ,action   = self.scroll_down
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Up>'
                ,action   = self.scroll_up
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Left>'
                ,action   = self.scroll_left
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Right>'
                ,action   = self.scroll_right
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Next>'
                ,action   = self.scroll_page_down
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Prior>'
                ,action   = self.scroll_page_up
                )
        sg.bind (obj      = self.obj
                ,bindings = '<End>'
                ,action   = self.scroll_end
                )
        sg.bind (obj      = self.obj
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
        self.canvas.widget.yview_moveto(len(self._videos)*self._def_height)
    
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
        self._no         = 0
        self._videos     = []
        self._def_height = 110 # A default picture height
        _np_path         = './nopic.png'
        if sh.File(file=_np_path,Silent=True).Success:
            self._np_image = it.PhotoImage(ig.open(_np_path))
        else:
            self._np_image = None
        ''' These values set the width and height of the frame that 
            contains videos and therefore the scrolling region.
            The default Youtube video picture has the dimensions of
            196x110, therefore, the channel frame embedding 10 videos
            will have the height of at least 1100.
        '''
        self._max_x = 1024
        self._max_y = 1120
        
    def title(self,text=None):
        if text:
            self.obj.title(text)
        else:
            self.obj.title(self._name)
        
    def frames(self):
        self.frame   = sg.Frame (parent_obj = self.obj)
        self.frame_y = sg.Frame (parent_obj = self.frame
                                ,expand     = False
                                ,fill       = 'y'
                                ,side       = 'right'
                                )
        self.frame_x = sg.Frame (parent_obj = self.frame
                                ,expand     = False
                                ,fill       = 'x'
                                ,side       = 'bottom'
                                )
        # A frame that contains all contents except for scrollbars
        self.frame1  = sg.Frame (parent_obj = self.frame
                                ,side       = 'left'
                                ,width      = self._max_x
                                ,height     = self._max_y
                                )
    
    # Called in 'canvases'
    def labels(self):
        # Frames embedded into a canvas are not scrollable
        self.label  = sg.Label (parent_obj = self.frame1
                               ,expand     = True
                               ,fill       = 'both'
                               ,Close      = False
                               )
    
    def canvases(self):
        ''' Create a canvas before an object being embedded, otherwise,
            the canvas will overlap this object.
        '''
        self.canvas = sg.Canvas(parent_obj=self.frame1)
        self.labels()
        self.canvas.embed(self.label)
    
    def scrollbars(self):
        sg.Scrollbar (parent_obj = self.frame_x
                     ,scroll_obj = self.canvas
                     ,Horizontal = True
                     )
        sg.Scrollbar (parent_obj = self.frame_y
                     ,scroll_obj = self.canvas
                     ,Horizontal = False
                     )
    
    def gui(self):
        self.obj = sg.SimpleTop(parent_obj=sg.objs.root())
        self.widget = self.obj.widget
        self.title(text=self._name)
        self.frames()
        self.canvases()
        self.scrollbars()
        self.canvas.focus()
        self.bindings()
        
    def add(self,no=0):
        self._no = no
        self._videos.append (Video (parent_obj   = self.label
                                   ,no_pic_image = self._np_image
                                   ,no           = self._no
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
        self.canvas.widget.yview_moveto(self._no*self._def_height)
        
    def show(self,Lock=True,*args):
        self.obj.show(Lock=Lock)
        
    def close(self,*args):
        self.widget.destroy()



if __name__ == '__main__':
    sg.objs.start()
    channel = Channel(name='Максим Шелков')
    sg.Geometry(parent_obj=channel.obj).set('985x500')
    channel.center(max_x=986,max_y=500)
    for i in range(10):
        channel.add(no=i)
        # Show default picture & video information
        sg.objs.root().widget.update_idletasks()
        # Simulate long loading
        """
        count = 0
        for k in range(500000):
            count += k
        """
        video = channel._videos[i]
        video.reset (no       = i + 1
                    ,author   = 'Максим Шелков'
                    ,title    = 'НАГЛЫЙ ОБМАН от ПЕРЕКУПА! Автомобиль - Ford АВТОХЛАМ!'
                    ,duration = '14:16'
                    ,picture  = 
                    '/home/pete/downloads/hqdefault.jpg'
                    )
        ''' This does not work in 'Channel.__init__' for some reason, 
        calling this externally
        ''' 
        channel.update_scroll()
    # Move back to video #0
    channel.canvas.widget.yview_moveto(0)
    channel.show()
    sg.objs.end()
