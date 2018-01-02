#!/usr/bin/python3

from PIL import Image as ig
from PIL import ImageTk as it
import shared as sh
import sharedGUI as sg
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','./locale')


class Video:
    
    def __init__(self,parent_obj,no_pic_image=None):
        self._np_image = no_pic_image
        self.parent_obj = parent_obj
        self.values()
        self.gui()
    
    def values(self):
        self._no       = 0
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
        self.label1 = sg.Label (parent_obj = self.frame1
                               ,text       = _('#%d') % self._no
                               ,side       = 'right'
                               ,anchor     = 'w'
                               )
        self.label2 = sg.Label (parent_obj = self.frame2
                               ,text       = _('Image')
                               ,side       = 'right'
                               ,image      = self._np_image
                               )
        self.label3 = sg.Label (parent_obj = self.frame4
                               ,text       = _('Author:')
                               )
        self.label4 = sg.Label (parent_obj = self.frame5
                               ,text       = _('Not Available')
                               ,anchor     = 'w'
                               )
        self.label5 = sg.Label (parent_obj = self.frame4
                               ,text       = _('Title:')
                               )
        self.label6 = sg.Label (parent_obj = self.frame5
                               ,text       = _('Not Available')
                               ,anchor     = 'w'
                               )
        self.label7 = sg.Label (parent_obj = self.frame4
                               ,text       = _('Duration:')
                               )
        self.label8 = sg.Label (parent_obj = self.frame5
                               ,text       = _('Not Available')
                               ,anchor     = 'w'
                               )
    
    def gui(self):
        self.frames()
        self.cbox = sg.CheckBox (parent_obj = self.frame1
                                ,Active     = True
                                ,side       = 'left'
                                )
        self.labels()
        
    def reset(self,author,title,duration,picture=None,no=0):
        self._no       = no
        self._author   = author
        self._title    = title
        self._duration = duration
        self._picture  = picture
        self.label1.text(_('#%d') % self._no)
        self.label4.text(self._author)
        self.label6.text(self._title)
        self.label8.text(self._duration)
        self.pic()


class Channel:
    
    def __init__(self,name=_('Channel')):
        self.values()
        self._name = name
        self.gui()
        self.scrollregion()
        self.scroll2start()
        
    def values(self):
        self._videos = []
        _np_path     = './nopic.png'
        if sh.File(file=_np_path,Silent=True).Success:
            self._np_image = it.PhotoImage(ig.open(_np_path))
        else:
            self._np_image = None
        self._max_x = 1024
        self._max_y = 768
        
    def title(self,text=None):
        if text:
            self.obj.title(text)
        else:
            self.obj.title(self._name)
        
    def scrollbars(self):
        self.yscroll = tk.Scrollbar(master=self.frame_y.widget)
        self.canvas.widget.config(yscrollcommand=self.yscroll.set)
        self.yscroll.config(command=self.canvas.widget.yview)
        self.yscroll.pack(side='right',fill='y')
    
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
        ''' Create a canvas before an object being embedded, otherwise,
            the canvas will overlap this object.
        '''
        self.canvas = sg.Canvas(parent_obj=self.frame1)
        # Frames embedded into a canvas are not scrollable
        self.label  = sg.Label (parent_obj = self.frame1
                               ,expand     = True
                               ,fill       = 'both'
                               )
        self.canvas.embed(self.label)
    
    def gui(self):
        # cur
        '''
        self.obj = sg.Top (parent_obj = sg.objs.root()
                          ,Maximize   = False
                          ,AutoCenter = False
                          )
        '''
        self.obj = sg.SimpleTop(parent_obj=sg.objs.root())
        self.widget = self.obj.widget
        self.title(text=self._name)
        self.frames()
        self.scroll_x()
        self.scroll_y()
        self.canvas.focus()
        
    def scroll_x(self):
        self.xscroll = tk.Scrollbar (master = self.frame_x.widget
                                    ,orient = tk.HORIZONTAL
                                    )
        self.xscroll.pack (expand = True
                          ,fill   = 'x'
                          )
        self.canvas.widget.config(xscrollcommand=self.xscroll.set)
        self.xscroll.config(command=self.canvas.widget.xview)
    
    def scroll_y(self):
        self.yscroll = tk.Scrollbar(master=self.frame_y.widget)
        self.yscroll.pack (expand = True
                          ,fill   = 'y'
                          )
        self.canvas.widget.config(yscrollcommand=self.yscroll.set)
        self.yscroll.config(command=self.canvas.widget.yview)
                          
    def add(self):
        self._videos.append (Video (parent_obj   = self.label
                                   ,no_pic_image = self._np_image
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
        self.canvas.widget.yview_moveto(0)
        
    def show(self,Lock=True,*args):
        self.obj.show(Lock=Lock)
        
    def close(self,*args):
        self.obj.close()



if __name__ == '__main__':
    import tkinter as tk
    sg.objs.start()
    channel = Channel(name='Максим Шелков')
    sg.Geometry(parent_obj=channel).set('700x500')
    for i in range(10):
        channel.add()
    sg.objs.root().widget.update_idletasks()
    for i in range(len(channel._videos)):
        """
        count = 0
        for k in range(500000):
            count += k
        """
        video = channel._videos[i]
        video.reset (no       = i
                    ,author   = 'Максим Шелков'
                    ,title    = 'НАГЛЫЙ ОБМАН от ПЕРЕКУПА! Автомобиль - Ford АВТОХЛАМ!'
                    ,duration = '14:16'
                    ,picture  = 
                    '/home/pete/downloads/hqdefault.jpg'
                    )
        sg.objs.root().widget.update_idletasks()
    channel.show()
    sg.objs.end()
