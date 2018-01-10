#!/usr/bin/python3

import shared as sh
import sharedGUI as sg
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','./locale')

product = 'Yatube'
version = '(alpha)'

def_height = 110 # A default picture height


class Video:
    
    def __init__(self,parent_obj,no=0):
        self._no        = no
        self.parent_obj = parent_obj
        self.values()
        self.gui()
    
    def values(self):
        self._author   = _('Author')
        self._title    = _('Title')
        self._duration = _('Duration')
        self._image    = objs.def_image()
    
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
        if not self._image:
            self._image = objs.def_image()
        self.label2.widget.config(image=self._image)
        #This prevents the garbage collector from deleting the image
        self.label2.widget.image = self._image
    
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
        ''' 'image' argument must be specified even when the label
            is further configured with such image, otherwise, frames
            will be further extended to encompass the image
            thereby distorting the GUI structure.
        '''
        self.label2 = sg.Label (parent_obj = self.frame2
                               ,text       = _('Image')
                               ,side       = 'right'
                               ,Close      = False
                               ,width      = 196
                               ,image      = self._image
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
        
    def reset(self,author,title,duration,image=None,no=0):
        self._no       = no
        self._author   = author
        self._title    = title
        self._duration = duration
        self._image    = image
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
        self.canvas.widget.yview_moveto(len(self._videos)*def_height)
    
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
        # This will allow to show the 1st video
        self.scrollregion()
        
    def add(self,no=0):
        self._no = no
        self._videos.append (Video (parent_obj = self.label
                                   ,no         = self._no
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
        
    def show(self,Lock=True,*args):
        self.obj.show(Lock=Lock)
        
    def close(self,*args):
        self.widget.destroy()



class Menu:
    
    def __init__(self):
        self.parent_obj = sg.objs.root()
        self.choice     = _('Quit')
        self.gui()
        
    def title(self,text=None):
        if text:
            self.parent_obj.title(text)
        else:
            text = sh.List(lst1=[product,version]).space_items()
            self.obj.title(text)
    
    def show(self,*args):
        self.obj.show()
    
    def close(self,*args):
        self.obj.close()
    
    def action(self,choice,*args):
        self.choice = choice
        self.obj.close()
    
    def buttons(self):
        #todo: [cbox] Ignore videos older than ...
        ''' For some reason, separating the button text to a variable
            does not work correctly (the last action defined in such a
            way is selected).
        '''
        button = sg.Button (parent_obj = self.obj
                           ,text       = _('Update subscriptions')
                           ,action     = lambda x:self.action(_('Update subscriptions'))
                           ,side       = 'top'
                           )
        button.focus()
        sg.Button (parent_obj = self.obj
                  ,text       = _('Update trending')
                  ,action     = lambda x:self.action(_('Update trending'))
                  ,side       = 'top'
                  )
        sg.Button (parent_obj = self.obj
                  ,text       = _('Manage subscriptions')
                  ,action     = lambda x:self.action(_('Manage subscriptions'))
                  ,side       = 'top'
                  )
        sg.Button (parent_obj = self.obj
                  ,text       = _('Manage blocklist')
                  ,action     = lambda x:self.action(_('Manage blocklist'))
                  ,side       = 'top'
                  )
        sg.Button (parent_obj = self.obj
                  ,text       = _('Quit')
                  ,action     = lambda x:self.action(_('Quit'))
                  ,side       = 'top'
                  )
    
    def quit(self,*args):
        self.action(_('Quit'))
    
    def bindings(self):
        sg.bind (obj      = self.obj
                ,bindings = ['<Control-q>','<Control-w>','<Escape>']
                ,action   = self.close
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Down>'
                ,action   = self.focus_next
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Up>'
                ,action   = self.focus_prev
                )
        # Trying to pass lambda will result in an error
        self.widget.protocol("WM_DELETE_WINDOW",self.quit)
        
    def focus_next(self,event,*args):
        event.widget.tk_focusNext().focus()
        return 'break'
        
    def focus_prev(self,event,*args):
        event.widget.tk_focusPrev().focus()
        return 'break'
    
    def gui(self):
        self.obj = sg.objs.new_top(Maximize=False)
        self.widget = self.obj.widget
        self.buttons()
        self.title()
        self.bindings()


class Objects:
    
    def __init__(self):
        self._def_image = self._channel_gui = None
        
    def def_image(self):
        if not self._def_image:
            path = sh.objs.pdir().add('nopic.png')
            self._def_image = sg.Image().open(path=path)
        return self._def_image

    def channel_gui(self):
        if not self._channel_gui:
            self._channel_gui = Channel(name=_('Channels'))
            sg.Geometry(parent_obj=self._channel_gui.obj).set('985x500')
            self._channel_gui.center(max_x=986,max_y=500)
        return self._channel_gui


objs = Objects()


if __name__ == '__main__':
    pass
