#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys, os
import re
import io
import skl_shared.logic as lg
import skl_shared.gui   as gi

import gettext
import skl_shared.gettext_windows as gettext_windows
gettext_windows.setup_env()
gettext.install('shared','../resources/locale')

GUI_MES = True


class CreateInstance(lg.CreateInstance):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Config(lg.Config):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Decline(lg.Decline):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Dic(lg.Dic):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Diff(lg.Diff):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Directory(lg.Directory):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Email(lg.Email):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class File(lg.File):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class FilterList(lg.FilterList):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class FixBaseName(lg.FixBaseName):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Get(lg.Get):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Grep(lg.Grep):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Home(lg.Home):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Hotkeys(lg.Hotkeys):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Input(lg.Input):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Launch(lg.Launch):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Links(lg.Links):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class List(lg.List):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Log(lg.Log):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class MessagePool(lg.MessagePool):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class OCR(lg.OCR):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class OSSpecific(lg.OSSpecific):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Online(lg.Online):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Path(lg.Path):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class ProgramDir(lg.ProgramDir):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class ReadBinary(lg.ReadBinary):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class ReadTextFile(lg.ReadTextFile):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class References(lg.References):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Search(lg.Search):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Shortcut(lg.Shortcut):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Table(lg.Table):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Text(lg.Text):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class TextDic(lg.TextDic):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Time(lg.Time):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Timer(lg.Timer):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Words(lg.Words):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class WriteBinary(lg.WriteBinary):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class WriteTextFile(lg.WriteTextFile):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Panes:
    
    def __init__ (self,bg='old lace'
                 ,Extended=False,words1=None
                 ,words2=None,words3=None
                 ,words4=None
                 ):
        self._bg      = bg
        self.Extended = Extended
        self.add_gui()
        if words1 and words2:
            self.reset (words1 = words1
                       ,words2 = words2
                       ,words3 = words3
                       ,words4 = words4
                       )
        
    def frames(self):
        self.frm_prm = Frame (parent = self.parent)
        self.frm_top = Frame (parent = self.frm_prm
                             ,side   = 'top'
                             )
        self.frm_btm = Frame (parent = self.frm_prm
                             ,side   = 'bottom'
                             )
        self.frm_pn1 = Frame (parent = self.frm_top
                             ,side   = 'left'
                             ,propag = False
                             ,height = 1
                             )
        self.frm_pn2 = Frame (parent = self.frm_top
                             ,side   = 'right'
                             ,propag = False
                             ,height = 1
                             )
        if self.Extended:
            self.frm_pn3 = Frame (parent = self.frm_btm
                                 ,side   = 'left'
                                 ,propag = False
                                 ,height = 1
                                 )
            self.frm_pn4 = Frame (parent = self.frm_btm
                                 ,side   = 'right'
                                 ,propag = False
                                 ,height = 1
                                 )

    def panes(self):
        self.pane1 = TextBox(self.frm_pn1)
        self.pane2 = TextBox(self.frm_pn2)
        if self.Extended:
            self.pane3 = TextBox(self.frm_pn3)
            self.pane4 = TextBox(self.frm_pn4)
    
    def add_gui(self):
        self.parent = Top(Maximize=True)
        self.widget = self.parent.widget
        self.frames()
        self.panes()
        self.pane1.focus()
        if self.Extended:
            pane3 = self.pane3
            pane4 = self.pane4
        else:
            pane3, pane4 = None, None
        self.gui = gi.Panes (parent = self.parent
                            ,pane1  = self.pane1
                            ,pane2  = self.pane2
                            ,pane3  = pane3
                            ,pane4  = pane4
                            )
        if self.Extended:
            self.gui.pane1_config(bg=self._bg)
        self.icon()
        self.title()
        self.bindings()
        
    def title(self,text=_('Compare texts:')):
        self.gui.title(text=text)
        
    def show(self,event=None):
        self.gui.show()
        
    def close(self,event=None):
        self.gui.close()
        
    def bindings(self):
        ''' - We do not bind 'select1' to 'pane1' and 'select2' to
              'pane3' since we need to further synchronize references
              by LMB anyway, and this further binding will rewrite
              the current binding.
            - We do not use 'Control' for bindings. If we use it,
              Tkinter will execute its internal bindings for
              '<Control-Down/Up>' and '<Control-Left/Right>' before
              executing our own. Even though we can return 'break'
              in 'select1'-4, we should not do that because we need
              internal bindings for '<Control-Left>' and
              '<Control-Right>'. Thus, we should not use 'Control' at
              all because we cannot replace 'Alt' with 'Control'
              for all actions.
        '''
        com.bind (obj      = self.gui
                 ,bindings = ('<Control-q>','<Control-w>')
                 ,action   = self.close
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<Escape>'
                 ,action   = Geometry(parent=self.gui).minimize
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<Alt-Key-1>','<Control-Key-1>')
                 ,action   = self.select1
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<Alt-Key-2>','<Control-Key-2>')
                 ,action   = self.select2
                 )
        com.bind (obj      = self.pane1
                 ,bindings = '<ButtonRelease-1>'
                 ,action   = self.select1
                 )
        com.bind (obj      = self.pane2
                 ,bindings = '<ButtonRelease-1>'
                 ,action   = self.select2
                 )
        com.bind (obj      = self.pane1
                 ,bindings = '<Alt-Right>'
                 ,action   = self.select2
                 )
        com.bind (obj      = self.pane2
                 ,bindings = '<Alt-Left>'
                 ,action   = self.select1
                 )
        if self.Extended:
            com.bind (obj      = self.gui
                     ,bindings = ('<Alt-Key-3>','<Control-Key-3>')
                     ,action   = self.select3
                     )
            com.bind (obj      = self.gui
                     ,bindings = ('<Alt-Key-4>','<Control-Key-4>')
                     ,action   = self.select4
                     )
            com.bind (obj      = self.pane3
                     ,bindings = '<ButtonRelease-1>'
                     ,action   = self.select3
                     )
            com.bind (obj      = self.pane4
                     ,bindings = '<ButtonRelease-1>'
                     ,action   = self.select4
                     )
            com.bind (obj      = self.pane2
                     ,bindings = '<Alt-Right>'
                     ,action   = self.select3
                     )
            com.bind (obj      = self.pane3
                     ,bindings = '<Alt-Right>'
                     ,action   = self.select4
                     )
            com.bind (obj      = self.pane3
                     ,bindings = '<Alt-Left>'
                     ,action   = self.select2
                     )
            com.bind (obj      = self.pane4
                     ,bindings = '<Alt-Left>'
                     ,action   = self.select3
                     )
            com.bind (obj      = self.pane1
                     ,bindings = '<Alt-Down>'
                     ,action   = self.select3
                     )
            com.bind (obj      = self.pane2
                     ,bindings = '<Alt-Down>'
                     ,action   = self.select4
                     )
            com.bind (obj      = self.pane3
                     ,bindings = '<Alt-Up>'
                     ,action   = self.select1
                     )
            com.bind (obj      = self.pane4
                     ,bindings = '<Alt-Up>'
                     ,action   = self.select2
                     )
        else:
            com.bind (obj      = self.pane1
                     ,bindings = '<Alt-Down>'
                     ,action   = self.select2
                     )
            com.bind (obj      = self.pane2
                     ,bindings = '<Alt-Up>'
                     ,action   = self.select1
                     )
             
    def decolorize(self):
        self.gui.pane1_config(bg='white')
        self.gui.pane2_config(bg='white')
        if self.Extended:
            self.gui.pane3_config(bg='white')
            self.gui.pane4_config(bg='white')
    
    def select1(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane1.focus()
        if self.Extended:
            self.decolorize()
            self.gui.pane1_config(bg=self._bg)
        
    def select2(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane2.focus()
        if self.Extended:
            self.decolorize()
            self.gui.pane2_config(bg=self._bg)
        
    def select3(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane3.focus()
        self.decolorize()
        self.gui.pane3_config(bg=self._bg)
        
    def select4(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane4.focus()
        self.decolorize()
        self.gui.pane4_config(bg=self._bg)
        
    def icon(self,path=None):
        if path:
            self.gui.icon(path)
        else:
            self.gui.icon (lg.objs.pdir().add ('..','resources'
                                              ,'icon_64x64_cpt.gif'
                                              )
                          )
                          
    def reset(self,words1,words2,words3=None,words4=None):
        self.pane1.reset(words=words1)
        self.pane2.reset(words=words2)
        self.pane1.insert(words1._text_orig)
        self.pane2.insert(words2._text_orig)
        if self.Extended:
            self.pane3.reset(words=words3)
            self.pane4.reset(words=words4)
            self.pane3.insert(words3._text_orig)
            self.pane4.insert(words4._text_orig)
            self.select1()



class SearchBox:
    ''' #note: if duplicate spaces/line breaks are not deleted,
        text with and without punctuation will have a different number
        of words; thus, 'tkinter' will be supplied wrong positions upon
        Search. However, preserving extra spaces/line breaks causes
        the 'Words' algorithm to be much slower.
    '''
    def __init__(self,obj,words=None,Strict=False):
        self.type   = 'SearchBox'
        self.obj    = obj
        self.words  = words
        self.parent = self.obj.parent
        ''' We bind 'SearchBox' to a simple 'TextBox', so we don't have
            an icon yet.
        '''
        self.ientry = EntryC (title = _('Find:')
                             ,icon  = ''
                             )
        self.isel = obj.select
        self.reset (words  = self.words
                   ,Strict = Strict
                   )
        self.ientry.close()

    def reset(self,words=None,Strict=False):
        self.reset_logic (words  = words
                         ,Strict = Strict
                         )
    
    # Strict: case-sensitive, with punctuation
    def reset_logic(self,words=None,Strict=False):
        self.Success    = True
        self._prev_loop = self._next_loop = self._search = self._pos1 \
                        = self._pos2 = self._text = None
        self.i          = 0
        self.words      = words
        self.Strict     = Strict
        if self.words:
            # Do not get text from the widget - it's not packed yet
            if self.Strict:
                self._text = self.words._text_p
            else:
                self._text = self.words._text_n
            self.isel.reset(words=self.words)
            self.isearch = lg.Search(text=self._text)
        else:
            self.Success = False

    def reset_data(self):
        f = '[shared] shared.SearchBox.reset_data'
        self.Success    = True
        self._prev_loop = self._next_loop = self._search = self._pos1 \
                        = self._pos2 = None
        self.i          = 0
        self.search()
        if self._text and self._search:
            self.isearch.reset (text   = self._text
                               ,search = self._search
                               )
            self.isearch.next_loop()
            # Prevents from calling self.search() once again
            if not self.isearch._next_loop:
                mes = _('No matches!')
                objs.mes(f,mes).info()
                self.Success = False
        else:
            self.Success = False
            com.cancel(f)

    def loop(self):
        f = '[shared] shared.SearchBox.loop'
        if self.Success:
            if not self.isearch._next_loop:
                self.reset()
        else:
            com.cancel(f)
        return self.isearch._next_loop

    def add(self):
        f = '[shared] shared.SearchBox.add'
        if self.Success:
            if self.i < len(self.loop()) - 1:
                self.i += 1
        else:
            com.cancel(f)

    def subtract(self):
        f = '[shared] shared.SearchBox.subtract'
        if self.Success:
            if self.i > 0:
                self.i -= 1
        else:
            com.cancel(f)

    def new(self,event=None):
        self.reset_data()
        self.next()

    def select(self):
        f = '[shared] shared.SearchBox.select'
        if self.Success:
            if self.Strict:
                result1 = self.words.no_by_pos_p(pos=self.pos1())
                result2 = self.words.no_by_pos_p(pos=self.pos2())
            else:
                result1 = self.words.no_by_pos_n(pos=self.pos1())
                result2 = self.words.no_by_pos_n(pos=self.pos2())
            if result1 is None or result2 is None:
                mes = _('Wrong input data!')
                objs.mes(f,mes,True).error()
            else:
                _pos1 = self.words.words[result1].tf()
                _pos2 = self.words.words[result2].tl()
                self.isel.reset (pos1 = _pos1
                                ,pos2 = _pos2
                                ,bg   = 'green2'
                                )
                self.isel.set()
        else:
            com.cancel(f)

    def search(self):
        f = '[shared] shared.SearchBox.search'
        if self.Success:
            if self.words:
                if not self._search:
                    self.ientry.focus()
                    self.ientry.select_all()
                    self.ientry.show()
                    self._search = self.ientry.get()
                    if self._search and not self.Strict:
                        self._search = lg.Text (text = self._search
                                               ,Auto = False
                                               ).delete_punctuation()
                        self._search = lg.Text (text = self._search
                                               ,Auto = False
                                               ).delete_duplicate_spaces()
                        self._search = self._search.lower()
            else:
                com.empty(f)
            return self._search
        else:
            com.cancel(f)

    def next(self,event=None):
        f = '[shared] shared.SearchBox.next'
        if self.Success:
            _loop = self.loop()
            if _loop:
                old_i = self.i
                self.add()
                if old_i == self.i:
                    if len(_loop) == 1:
                        mes = _('Only one match has been found!')
                        objs.mes(f,mes).info()
                    else:
                        self.i = 0
                        mes = _('No more matches, continuing from the top!')
                        objs.mes(f,mes).info()
                self.select()
            else:
                mes = _('No matches!')
                objs.mes(f,mes).info()
        else:
            com.cancel(f)

    def prev(self,event=None):
        f = '[shared] shared.SearchBox.prev'
        if self.Success:
            _loop = self.loop()
            if _loop:
                old_i = self.i
                self.subtract()
                if old_i == self.i:
                    if len(_loop) == 1:
                        mes = _('Only one match has been found!')
                        objs.mes(f,mes).info()
                    else:
                        # Not just -1
                        self.i = len(_loop) - 1
                        mes = _('No more matches, continuing from the bottom!')
                        objs.mes(f,mes).info()
                self.select()
            else:
                mes = _('No matches!')
                objs.mes(f,mes).info()
        else:
            com.cancel(f)

    def pos1(self):
        f = '[shared] shared.SearchBox.pos1'
        if self.Success:
            if self._pos1 is None:
                self.loop()
                self.i = 0
            _loop = self.loop()
            if _loop:
                self._pos1 = _loop[self.i]
            return self._pos1
        else:
            com.cancel(f)

    def pos2(self):
        f = '[shared] shared.SearchBox.pos2'
        if self.Success:
            if self.pos1() is not None:
                self._pos2 = self._pos1 + len(self.search())
            return self._pos2
        else:
            com.cancel(f)



# Select words only
class Selection:
    ''' Usage:
        com.bind(itxt,'<ButtonRelease-1>',action)

    def action(event=None):
        """ Refresh coordinates (or set isel._pos1, isel._pos2
            manually).
        """
        isel.get()
        isel.set()
    '''
    def __init__(self,itxt,words=None):
        self.itxt = itxt
        self.reset(words=words)

    def reset (self
              ,words = None
              ,pos1  = None
              ,pos2  = None
              ,bg    = None
              ,fg    = None
              ,tag   = 'tag'
              ):
        self._pos1 = pos1
        self._pos2 = pos2
        self._text = ''
        self._bg   = bg
        self._fg   = fg
        if not self._bg and not self._fg:
            self._bg = 'cyan'
        self._tag  = tag
        self.words = words

    def clear(self,tag='sel',pos1='1.0',pos2='end'):
        self.itxt.tag_remove (tag  = tag
                             ,pos1 = pos1
                             ,pos2 = pos2
                             )

    def pos1(self):
        if self._pos1 is None:
            self.get()
        return self._pos1

    def pos2(self):
        if self._pos2 is None:
            self.get()
        return self._pos2

    def get(self,event=None):
        f = '[shared] shared.Selection.get'
        try:
            self._pos1, self._pos2 = self.itxt.gui.sel_index()
        except Exception as e:
            self._pos1, self._pos2 = None, None
            # Too frequent
            #com.failed(f,e)
        # Too frequent
        '''
        mes = '{}-{}'.format(self._pos1,self._pos2)
        objs.mes(f,mes,True).debug()
        '''
        return(self._pos1,self._pos2)

    def text(self):
        f = '[shared] shared.Selection.text'
        try:
            self._text = self.itxt.gui.get_sel.replace('\r','').replace('\n','')
        except Exception as e:
            self._text = ''
            com.failed(f,e)
        return self._text

    def select_all(self):
        self.itxt.select_all()

    def set(self,DelPrev=True,AutoScroll=True):
        if self.pos1() and self.pos2():
            mark = self._pos1
            self.itxt.tag_add (pos1    = self._pos1
                              ,pos2    = self._pos2
                              ,tag     = self._tag
                              ,DelPrev = DelPrev
                              )
        else:
            # Just need to return something w/o warnings
            _cursor = mark = self.itxt.cursor()
            self.itxt.tag_add (tag     = self._tag
                              ,pos1    = _cursor
                              ,pos2    = _cursor
                              ,DelPrev = DelPrev
                              )
        
        if self._bg:
            ''' This is not necessary for 'sel' tag which is hardcoded
                for selection and permanently colored with gray.
                A 'background' attribute cannot be changed for a 'sel'
                tag.
            '''
            self.itxt.tag_config (tag = self._tag
                                 ,bg  = self._bg
                                 )
        elif self._fg:
            self.itxt.tag_config (tag = self._tag
                                 ,fg  = self._fg
                                 )
        #todo: select either 'see' or 'autoscroll'
        if AutoScroll:
            #self.itxt.see(mark)
            self.itxt.autoscroll(mark)



class TextBoxC:
    
    def __init__ (self,SpReturn=True
                 ,Maximize=False,title=''
                 ,icon='',words=None
                 ):
        self.Save     = False
        self.SpReturn = SpReturn
        self.Maximize = Maximize
        self._title   = title
        self._icon    = icon
        self.words    = words
        self.add_gui()
        self.focus()
    
    def mark_remove(self,mark='insert'):
        self.obj.mark_remove(mark)
    
    def mark_add(self,mark='insert',pos='1.0'):
        self.obj.mark_add (mark = mark
                          ,pos  = pos
                          )
    
    def clear_marks(self,event=None):
        self.obj.clear_marks()
    
    def clear_tags(self,event=None):
        self.obj.clear_tags()
    
    def tag_config (self,tag='sel',bg=None
                   ,fg=None,font=None
                   ):
        self.obj.tag_config (tag  = tag
                            ,bg   = bg
                            ,fg   = fg
                            ,font = font
                            )
    
    def tag_remove (self,tag='sel'
                   ,pos1='1.0'
                   ,pos2='end'
                   ):
        self.obj.tag_remove (tag  = tag
                            ,pos1 = pos1
                            ,pos2 = pos2
                            )
    
    def tag_add (self,tag='sel',pos1='1.0'
                ,pos2='end',DelPrev=True
                ):
        self.obj.tag_add (tag     = tag
                         ,pos1    = pos1
                         ,pos2    = pos2
                         ,DelPrev = DelPrev
                         )
    
    def enable(self,event=None):
        self.obj.enable()
    
    def disable(self,event=None):
        self.obj.disable()
    
    def focus(self,event=None):
        # Focus on 'tk.Text' instead of 'tk.Toplevel'
        self.obj.focus()
    
    def insert (self,text=''
               ,pos='1.0',MoveTop=True
               ):
        self.obj.insert (text    = text
                        ,pos     = pos
                        ,MoveTop = MoveTop
                        )
    
    def reset(self,words=None,title=''):
        self.obj.reset(self.words)
        self.title(title)
    
    def add_gui(self):
        self.parent = Top(Maximize=self.Maximize)
        self.widget = self.parent.widget
        self.gui = gi.TextBoxC(self.parent)
        self.obj = TextBox (parent  = self.parent
                           ,words   = self.words
                           ,ScrollX = False
                           ,ScrollY = True
                           )
        self.title()
        self.icon()
    
    def spelling(self):
        ''' Tags can be marked only after text is inserted; thus, call
            this procedure separately before '.show'.
        '''
        f = '[shared] shared.TextBox.spelling'
        if self.words:
            self.words.sent_nos()
            result = []
            for i in range(self.words.len()):
                if not self.words.words[i].spell():
                    result.append(i)
            if result:
                self.clear_tags()
                for i in range(len(result)):
                    no   = self.words._no = result[i]
                    pos1 = self.words.words[no].tf()
                    pos2 = self.words.words[no].tl()
                    if pos1 and pos2:
                        self.tag_add (tag     = 'spell'
                                     ,pos1    = pos1
                                     ,pos2    = pos2
                                     ,DelPrev = False
                                     )
                
                mes = _('{} tags to assign').format(len(result))
                objs.mes(f,mes,True).debug()
                self.tag_config (tag = 'spell'
                                ,bg  = 'red'
                                )
            else:
                mes = _('Spelling seems to be correct.')
                objs.mes(f,mes,True).info()
        else:
            com.empty(f)
    
    def icon(self,path=''):
        if path:
            self._icon = path
        self.gui.icon(self._icon)

    def title(self,text=''):
        text = lg.com.sanitize(text)
        if text:
            self._title = text
        self.gui.title(self._title)
    
    def get(self,event=None):
        if self.Save:
            return self.obj.get()
    
    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()
    
    def save(self,event=None):
        self.Save = True
        self.close()
    
    def bindings(self):
        if self.SpReturn:
            # Do not add a new line
            self.gui.unbind('<Return>')
            self.gui.unbind('<KP_Enter>')
            com.bind (obj      = self.gui
                     ,bindings = ('<Return>','<KP_Enter>')
                     ,action   = self.save
                     )
        com.bind (obj      = self.gui
                 ,bindings = ('<Escape>','<Control-w>','<Control-q>')
                 ,action   = self.close
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<F2>','<Control-s>')
                 ,action   = self.save
                 )



class TextBox:

    def __init__ (self,parent,expand=True
                 ,side=None,fill='both'
                 ,words=None,font='Serif 14'
                 ,ScrollX=False,ScrollY=True
                 ,wrap='word'
                 ):
        self.values()
        self.parent  = parent
        self.expand  = expand
        self.side    = side
        self.fill    = fill
        self.words   = words
        self.font    = font
        self.ScrollX = ScrollX
        self.ScrollY = ScrollY
        self.wrap    = wrap
        
        self.select = Selection (itxt  = self
                                ,words = self.words
                                )
        self.search = SearchBox (obj   = self
                                ,words = self.words
                                )
        self.add_gui()

    def clear_marks(self,event=None):
        for mark in self.gui.marks():
            self.mark_remove(mark)
    
    def clear_tags(self,event=None):
        for tag in self.gui.tags():
            self.tag_remove(tag)
    
    def disable(self,event=None):
        self.gui.disable()
    
    def enable(self,event=None):
        self.gui.enable()
    
    def values(self):
        self.type    = 'TextBox'
        self.scr_ver = None
        self.scr_hor = None

    def frames(self):
        self.frm_prm = Frame(self.parent)
        self.frm_sec = Frame (parent = self.frm_prm
                             ,side   = 'top'
                             )
        self.frm_trt = Frame (parent = self.frm_sec
                             ,side   = 'left'
                             )
        self.frm_ver = Frame (parent = self.frm_sec
                             ,side   = 'right'
                             ,expand = False
                             ,fill   = 'y'
                             )
        self.frm_txt = Frame (parent = self.frm_trt
                             ,side   = 'top'
                             )
        self.frm_hor = Frame (parent = self.frm_trt
                             ,side   = 'bottom'
                             ,expand = False
                             ,fill   = 'x'
                             )
    
    def add_gui(self):
        self.frames()
        self.gui = gi.TextBox (parent = self.frm_txt
                              ,wrap   = self.wrap
                              ,expand = self.expand
                              ,side   = self.side
                              ,fill   = self.fill
                              ,font   = self.font
                              )
        self.widget = self.gui.widget
        if self.ScrollY:
            self.scr_ver = Scrollbar (parent = self.frm_ver
                                     ,scroll = self.gui
                                     )
        if self.ScrollX:
            self.scr_hor = Scrollbar (parent = self.frm_hor
                                     ,scroll = self.gui
                                     ,Horiz  = True
                                     )
        self.bindings()

    def reset(self,words=None):
        self.clear_text()
        self.clear_tags()
        self.clear_marks()
        if words:
            self.words = words
            # Selection is reset in 'SearchBox.reset'
            self.search.reset(self.words)

    def bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = ('<Control-f>','<Control-F3>')
                 ,action   = self.search.new
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<F3>'
                 ,action   = self.search.next
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<Shift-F3>'
                 ,action   = self.search.prev
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<Control-a>'
                 ,action   = self.select_all
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<Control-v>'
                 ,action   = self.paste
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<Control-Alt-u>'
                 ,action   = self.toggle_case
                 )

    def toggle_case(self,event=None):
        f = '[shared] shared.TextBox.toggle_case'
        text = Text(text=self.select.text()).toggle_case()
        pos1, pos2 = self.select.get()
        self.clear_selection()
        self.insert (text    = text
                    ,pos     = self.cursor()
                    ,MoveTop = False
                    )
        if pos1 and pos2:
            self.select.reset (pos1 = pos1
                              ,pos2 = pos2
                              ,tag  = 'sel'
                              ,bg   = 'gray'
                              )
            self.select.set(DelPrev=0,AutoScroll=0)
        else:
            com.empty(f)
        return 'break'

    def _get(self):
        f = '[shared] shared.TextBox._get'
        try:
            return self.gui.get()
        except Exception as e:
            com.failed(f,e)

    def get(self,Strip=True):
        result = self._get()
        if result:
            if Strip:
                return result.strip()
            else:
                return result.strip('\n')
        else:
            return ''

    def insert(self,text='',pos='1.0',MoveTop=True):
        f = '[shared] shared.TextBox.insert'
        try:
            self.gui.insert (text = text
                            ,pos  = pos
                            )
        except Exception as e:
            com.failed(f,e)
        if MoveTop:
            # Move to the beginning
            self.mark_add()
        else:
            self.scroll(mark='insert')

    def paste(self,event=None):
        self.clear_selection()
        self.insert (text = Clipboard().paste()
                    ,pos  = self.cursor()
                    )

    def select_all(self,event=None):
        ''' 'end-1c' allows to select text without the last newline
            (which is added automatically by 'tkinter').
        '''
        self.tag_add (tag  = 'sel'
                     ,pos1 = '1.0'
                     ,pos2 = 'end-1c'
                     )
        self.mark_add()
        return 'break'

    def tag_remove(self,tag='sel',pos1='1.0',pos2='end'):
        f = '[shared] shared.TextBox.tag_remove'
        try:
            self.gui.tag_remove (tag  = tag
                                ,pos1 = pos1
                                ,pos2 = pos2
                                )
        except Exception as e:
            com.failed(f,e)

    def tag_add (self,tag='sel',pos1='1.0'
                ,pos2='end',DelPrev=True
                ):
        f = '[shared] shared.TextBox.tag_add'
        if DelPrev:
            self.tag_remove(tag)
        try:
            self.gui.tag_add (tag  = tag
                             ,pos1 = pos1
                             ,pos2 = pos2
                             )
        except Exception as e:
            com.failed(f,e)

    def tag_config (self,tag='sel',bg=None
                   ,fg=None,font=None
                   ):
        f = '[shared] shared.TextBox.tag_config'
        try:
            self.gui.tag_config (tag  = tag
                                ,bg   = bg
                                ,fg   = fg
                                ,font = font
                                )
        except Exception as e:
            com.failed(f,e)

    def mark_add(self,mark='insert',pos='1.0'):
        f = '[shared] shared.TextBox.mark_add'
        try:
            self.gui.mark_add (mark = mark
                              ,pos  = pos
                              )
        except Exception as e:
            com.failed(f,e)

    def mark_remove(self,mark='insert'):
        f = '[shared] shared.TextBox.mark_remove'
        try:
            self.gui.mark_remove(mark)
        except Exception as e:
            com.failed(f,e)

    def clear_text(self,pos1='1.0',pos2='end'):
        f = '[shared] shared.TextBox.clear_text'
        try:
            self.gui.clear_text (pos1 = pos1
                                ,pos2 = pos2
                                )
        except Exception as e:
            com.failed(f,e)

    def clear_selection(self,event=None):
        f = '[shared] shared.TextBox.clear_selection'
        pos1, pos2 = self.select.get()
        if pos1 and pos2:
            self.clear_text (pos1 = pos1
                            ,pos2 = pos2
                            )

    def goto(self,GoTo=''):
        f = '[shared] shared.TextBox.goto'
        if GoTo:
            try:
                goto_pos = self.gui.search(GoTo)
                self.mark_add('goto',goto_pos)
                self.mark_add('insert',goto_pos)
                self.gui.scroll('goto')
            except Exception as e:
                com.failed(f,e)
        else:
            com.lazy(f)

    # Scroll screen to a tkinter position or a mark (tags do not work)
    def scroll(self,mark):
        f = '[shared] shared.TextBox.scroll'
        try:
            self.gui.scroll(mark)
        except Exception as e:
            com.failed(f,e)

    def autoscroll(self,mark='1.0'):
        ''' Scroll screen to a tkinter position or a mark if they
            are not visible (tags do not work).
        '''
        if not self.visible(mark):
            self.scroll(mark)

    #todo: select either 'see' or 'autoscroll'
    def see(self,mark):
        f = '[shared] shared.TextBox.see'
        if mark is None:
            com.empty(f)
        else:
            self.gui.see(mark)

    def visible(self,tk_pos):
        if self.widget.bbox(tk_pos):
            return True

    def cursor(self,event=None):
        f = '[shared] shared.TextBox.cursor'
        try:
            self._pos = self.gui.cursor()
        except Exception as e:
            self._pos = '1.0'
            com.failed(f,e)
        return self._pos

    def focus(self,event=None):
        self.gui.focus()



class EntryC:
    
    def __init__(self,title='',icon=''):
        self.type   = 'Entry'
        self.Save   = False
        self._title = title
        self._icon  = icon
        self.add_gui()
        self.reset()
    
    def select_all(self,event=None):
        self.obj.select_all()
    
    def focus(self,event=None):
        self.gui.focus()
    
    def reset(self,title=''):
        self.Save = False
        if title:
            self._title = title
        self.title()
        self.clear()
    
    def clear(self,event=None):
        self.obj.clear()
    
    def add_gui(self):
        self.parent = Top(AutoCr=False)
        self.gui    = gi.EntryC(self.parent)
        self.widget = self.gui.widget
        self.frames()
        self.obj = Entry (parent = self.frm_ent
                         ,expand = True
                         ,fill   = 'x'
                         )
        self.buttons()
        self.icon()
        self.bindings()
    
    def frames(self):
        self.frm_ent = Frame (parent = self.parent
                             ,side   = 'top'
                             ,expand = False
                             )
        self.frm_btn = Frame (parent = self.parent
                             ,side   = 'bottom'
                             ,expand = False
                             )
        self.frm_btl = Frame (parent = self.frm_btn
                             ,side   = 'left'
                             )
        self.frm_btr = Frame (parent = self.frm_btn
                             ,side   = 'right'
                             )
    
    def get(self,event=None):
        if self.Save:
            return self.obj.get()
        else:
            return ''
    
    def icon(self,path=''):
        if path:
            self._icon = path
        self.gui.icon(self._icon)

    def title(self,text=''):
        text = lg.com.sanitize(text)
        if text:
            self._title = text
        self.gui.title(self._title)
    
    def buttons(self):
        self.btn_cls = Button (parent = self.frm_btl
                              ,action = self.close
                              ,hint   = _('Reject and close')
                              ,text   = _('Close')
                              ,side   = 'left'
                              ,hdir   = 'bottom'
                              )
        self.btn_clr = Button (parent = self.frm_btl
                              ,action = self.clear
                              ,hint   = _('Clear the field')
                              ,text   = _('Clear')
                              ,side   = 'right'
                              ,hdir   = 'bottom'
                              )
        self.btn_sav = Button (parent = self.frm_btr
                              ,action = self.save
                              ,hint   = _('Accept and close')
                              ,text   = _('Save and close')
                              ,side   = 'right'
                              ,hdir   = 'bottom'
                              )
    
    def bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                 ,action   = self.close
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<F5>','<Control-r>')
                 ,action   = self.clear
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<Return>','<KP_Enter>'
                             ,'<F2>','<Control-s>'
                             )
                 ,action   = self.save
                 )
    
    def save(self,event=None):
        self.Save = True
        self.close()
    
    def close(self,event=None):
        self.gui.close()
    
    def show(self,event=None):
        self.obj.focus()
        self.gui.show()



class Entry:
    # Does not support marks or tags
    def __init__ (self,parent,side=None
                 ,ipadx=None,ipady=None
                 ,fill=None,width=None
                 ,expand=None,font='Sans 11'
                 ,bg=None,fg=None
                 ,justify='left'
                 ,AddBind=True
                ):
        self.type    = 'Entry'
        self.parent  = parent
        self.side    = side
        self.ipadx   = ipadx
        self.ipady   = ipady
        self._fill   = fill
        self.width   = width
        self.expand  = expand
        self.font    = font
        self.bg      = bg
        self.fg      = fg
        self.justify = justify
        self.AddBind = AddBind
        self.add_gui()

    def paste(self,event=None):
        self.clear()
        self.insert(Clipboard().paste())
    
    def add_gui(self):
        self.gui = gi.Entry (parent  = self.parent
                            ,side    = self.side
                            ,ipadx   = self.ipadx
                            ,ipady   = self.ipady
                            ,fill    = self._fill
                            ,width   = self.width
                            ,expand  = self.expand
                            ,font    = self.font
                            ,bg      = self.bg
                            ,fg      = self.fg
                            ,justify = self.justify
                            )
        self.widget = self.gui.widget
        self.bindings()
        self.extra_bind()
    
    def reset(self):
        self.clear_text()
    
    def disable(self,event=None):
        self.gui.disable()
    
    def enable(self,event=None):
        self.gui.enable()

    def bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = '<Control-a>'
                 ,action   = self.select_all
                 )
    
    def extra_bind(self):
        if self.AddBind:
            com.bind (obj      = self.gui
                     ,bindings = '<ButtonRelease-2>'
                     ,action   = self.paste
                     )
            com.bind (obj      = self.gui
                     ,bindings = '<ButtonRelease-3>'
                     ,action   = self.clear
                     )

    def _get(self):
        f = '[shared] shared.Entry._get'
        try:
            return self.gui.get()
        except Exception as e:
            com.failed(f,e)

    def get(self,Strip=False):
        f = '[shared] shared.Entry.get'
        result = self._get()
        if result is None:
            result = ''
        if Strip:
            return result.strip()
        else:
            return result.strip('\n')

    def insert(self,text='text',pos=0):
        f = '[shared] shared.Entry.insert'
        self.enable()
        try:
            self.widget.insert(pos,text)
        except Exception as e:
            com.failed(f,e)

    def select_all(self,event=None):
        return self.gui.select_all()

    def clear(self,event=None,pos1=0,pos2='end'):
        self.clear_text (pos1 = pos1
                        ,pos2 = pos2
                        )
    
    def clear_text(self,event=None,pos1=0,pos2='end'):
        f = '[shared] shared.Entry.clear_text'
        try:
            self.gui.clear_text (pos1 = pos1
                                ,pos2 = pos2
                                )
        except Exception as e:
            com.failed(f,e)

    def focus(self,event=None):
        return self.gui.focus()



class MultCBoxesC:
    
    def __init__ (self,text='',width=350
                 ,height=300,font='Sans 11'
                 ,MarkAll=False,icon=''
                 ):
        self._width  = width
        self._height = height
        self._icon   = icon
        self.font    = font
        self.add_gui()
        self.title()
        self.reset (text    = text
                   ,MarkAll = MarkAll
                   )
    
    def select_all(self,event=None):
        self.obj.select_all()
    
    def selected(self,event=None):
        return self.obj.selected()
    
    def toggle(self,event=None):
        self.obj.toggle()
    
    def bindings(self):
        com.bind (obj      = self.parent
                 ,bindings = ('<Control-q>','<Control-w>','<Escape>')
                 ,action   = self.close
                 )
        self.obj.cvs_prm.top_bindings (top  = self.parent
                                      ,Ctrl = False
                                      )
    
    def icon(self,path=''):
        if path:
            self._icon = path
        self.gui.icon(self._icon)
    
    def reset(self,text='',MarkAll=False):
        self._text = lg.com.sanitize(text)
        self.obj.reset (text    = text
                       ,MarkAll = MarkAll
                       )
    
    def frames(self):
        self.frm_prm = Frame (parent = self.parent)
        self.frm_ver = Frame (parent = self.frm_prm
                             ,expand = False
                             ,fill   = 'y'
                             ,side   = 'right'
                             )
        self.frm_bth = Frame (parent = self.parent
                             ,expand = False
                             ,fill   = 'both'
                             )
        self.frm_hor = Frame (parent = self.frm_prm
                             ,expand = False
                             ,fill   = 'x'
                             ,side   = 'bottom'
                             )
        self.frm_sec = Frame (parent = self.frm_prm)
        
    def scrollbars(self):
        self.scr_hor = Scrollbar (parent = self.frm_hor
                                 ,scroll = self.obj.cvs_prm
                                 ,Horiz  = True
                                 )
        self.scr_ver = Scrollbar (parent = self.frm_ver
                                 ,scroll = self.obj.cvs_prm
                                 )
    
    def widgets(self):
        self.btn_sel = Button (parent = self.frm_bth
                              ,text   = _('Toggle all')
                              ,hint   = _('Mark/unmark all checkboxes')
                              ,side   = 'left'
                              ,action = self.toggle
                              )
        self.btn_cls = Button (parent = self.frm_bth
                              ,text   = _('Close')
                              ,hint   = _('Close this window')
                              ,side   = 'right'
                              ,action = self.close
                              )
    
    def add_gui(self):
        self.parent = Top()
        Geometry(parent=self.parent).set ('%dx%d' % (self._width
                                                    ,self._height
                                                    )
                                         )
        self.gui    = gi.MultCBoxesC(self.parent)
        self.widget = self.gui.widget
        self.frames()
        self.obj = MultCBoxes (parent  = self.frm_sec
                              ,font    = self.font
                              )
        self.widgets()
        self.scrollbars()
        self.btn_cls.focus()
        self.bindings()
        self.title()
        self.icon()
    
    def title(self,text=None):
        if not text:
            text = _('Select files:')
        self.gui.title(text)
    
    def show(self,event=None):
        self.gui.show()
        
    def close(self,event=None):
        self.gui.close()
        


class MultCBoxes:

    def __init__ (self,parent,text=''
                 ,font='Sans 11'
                 ,MarkAll=False
                 ):
        self.parent = parent
        self.widget = self.parent.widget
        self._font  = font
        self.values()
        self.add_gui()
        self.reset (text    = text
                   ,MarkAll = MarkAll
                   )
    
    def select_all(self,event=None):
        for cbx in self._cboxes:
            cbx.enable()
    
    def selected(self,event=None):
        active = []
        for i in range(len(self._cboxes)):
            if self._cboxes[i].get():
                active.append(self._lbls[i]._text)
        return active
    
    def region(self):
        f = '[shared] shared.MultCBoxes.region'
        if self._frms:
            objs.root().idle()
            self.cvs_prm.region (x        = self.frm_emb.reqwidth()
                                ,y        = self.frm_emb.reqheight()
                                ,x_border = 5
                                ,y_border = 10
                                )
            self.cvs_prm.scroll()
        else:
            com.lazy(f)
        
    def values(self):
        self._frms   = []
        self._cboxes = []
        self._lbls   = []
        self._text   = ''
    
    def widgets(self):
        self.cvs_prm = Canvas(parent=self.parent)
        self.frm_emb = Frame(parent=self.parent)
        self.cvs_prm.embed(self.frm_emb)
        
    def add_row(self,text):
        frm = Frame (parent = self.frm_emb
                    ,expand = False
                    )
        cbx = CheckBox (parent = frm
                       ,side   = 'left'
                       )
        lbl = Label (parent = frm
                    ,text   = text
                    ,side   = 'left'
                    ,font   = self._font
                    )
        com.bind (obj      = lbl
                 ,bindings = '<ButtonRelease-1>'
                 ,action   = cbx.toggle
                 )
        self._frms.append(frm)
        self._cboxes.append(cbx)
        self._lbls.append(lbl)
        
    def toggle(self,event=None):
        Marked = False
        for cbox in self._cboxes:
            if cbox.get():
                Marked = True
                break
        if Marked:
            for cbox in self._cboxes:
                cbox.disable()
        else:
            for cbox in self._cboxes:
                cbox.enable()
    
    def reset(self,text='',MarkAll=False):
        for frame in self._frms:
            frame.kill()
        self.values()
        self._text = lg.com.sanitize(text)
        for item in self._text.splitlines():
            self.add_row(item)
        self.region()
        if MarkAll:
            self.select_all()
    
    def add_gui(self):
        self.widgets()



class CheckBox:
    ''' #note: For some reason, CheckBox that should be Active must be
        assigned to a variable (var = CheckBox(parent,Active=1))
    '''
    def __init__ (self,parent,Active=False
                 ,side=None,action=None
                 ):
        self.parent = parent
        self.side   = side
        self.action = action
        self.gui    = gi.CheckBox (parent = self.parent
                                  ,side   = self.side
                                  )
        self.widget = self.gui.widget
        self.reset (Active = Active
                   ,action = action
                   )

    def reset(self,Active=False,action=None):
        if Active:
            self.enable()
        else:
            self.disable()
        if action:
            self.action = action
            self.gui.set_action(self.action)

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()

    def focus(self,event=None):
        self.gui.focus()

    def enable(self,event=None):
        self.gui.enable()

    def disable(self,event=None):
        self.gui.disable()

    def get(self,event=None):
        return self.gui.get()

    def toggle(self,event=None):
        self.gui.toggle()



class ProgressBar:
    
    def __init__ (self,width=750,height=200
                 ,YScroll=True,title=_('Download progress')
                 ,icon=''
                 ):
        self.values()
        self._width  = width
        self._height = height
        self._icon   = icon
        self._title  = title
        self.YScroll = YScroll
        self.add_gui()
        
    def values(self):
        self._items  = []
        self._item   = None
        self._border = 80
    
    def frames(self):
        self.frm_prm = Frame (parent = self.parent)
        self.frm_hor = Frame (parent = self.frm_prm
                             ,expand = False
                             ,fill   = 'x'
                             ,side   = 'bottom'
                             )
        self.frm_ver = Frame (parent = self.frm_prm
                             ,expand = False
                             ,fill   = 'y'
                             ,side   = 'right'
                             )
        # This frame must be created after the bottom frame
        self.frm_sec = Frame (parent = self.frm_prm)
    
    def icon(self,path=''):
        if path:
            self._icon = path
        self.gui.icon(self._icon)
    
    def title(self,text=''):
        if text:
            self._title = text
        self.gui.title(self._title)
        
    def show(self,event=None):
        self.gui.show()
        
    def close(self,event=None):
        self.gui.close()
    
    def add_gui(self):
        self.parent = self.obj = Top(Lock=False)
        self.widget = self.parent.widget
        Geometry(self.parent).set('%dx%d' % (self._width,self._height))
        self.frames()
        self.widgets()
        self.canvas.region (x = self._width
                           ,y = self._height
                           )
        self.canvas.scroll()
        self.gui = gi.ProgressBar(self.parent)
        self.bindings()
        self.title()
        self.icon()
        
    def bindings(self):
        com.bind (obj      = self.parent
                 ,bindings = ('<Control-q>','<Control-w>','<Escape>')
                 ,action   = self.close
                 )
        self.canvas.top_bindings (top  = self.parent
                                 ,Ctrl = False
                                 )
    
    def widgets(self):
        self.canvas = Canvas(parent = self.frm_sec)
        self.label  = Label (parent = self.frm_sec
                            ,text   = 'ProgressBar'
                            ,expand = True
                            ,fill   = 'both'
                            )
        self.canvas.embed(self.label)
        if self.YScroll:
            self.yscroll = Scrollbar (parent = self.frm_ver
                                     ,scroll = self.canvas
                                     )
        self.canvas.focus()
        
    def add(self,event=None):
        f = '[shared] shared.ProgressBar.add'
        self._item = ProgressBarItem (parent = self.label
                                     ,length = self._width-self._border
                                     )
        self._items.append(self._item)
        objs.root().idle()
        max_x = self.label.reqwidth()
        max_y = self.label.reqheight()
        '''
        sub = '{}x{}'.format(max_x,max_y)
        mes = _('Widget sizes: {}').format(sub)
        objs.mes(f,mes,True).debug()
        '''
        self.canvas.region (x        = max_x
                           ,y        = max_y
                           ,x_border = 50
                           ,y_border = 20
                           )
        self.canvas.move_bottom()
        return self._item



class ProgressBarItem:
    
    def __init__ (self,parent,orient='horizontal'
                 ,length=100,mode='determinate'
                 ):
        self.parent = parent
        self.orient = orient
        self.length = length
        self.mode   = mode
        self.add_gui()
        
    def add_gui(self):
        self.frames()
        self.labels()
        self.text()
        self.gui = gi.ProgressBarItem (parent = self.frame2
                                      ,orient = self.orient
                                      ,length = self.length
                                      ,mode   = self.mode
                                      )
        self.widget = self.gui.widget
        
    def frames(self):
        self.frame  = Frame (parent = self.parent
                            ,expand = False
                            ,fill   = 'x'
                            )
        self.frame1 = Frame(parent=self.frame)
        self.frame2 = Frame(parent=self.frame)
        
    def labels(self):
        self.label = Label (parent = self.frame1
                           ,side   = 'left'
                           ,font   = 'Mono 11'
                           )

    def text (self,file='',cur_size=0
             ,total=0,rate=0,eta=0
             ):
        mes = _('File: "{}"; {}/{} MB; Rate: {} kbps; ETA: {}s')
        mes = mes.format(file,int(cur_size),int(total),rate,eta)
        self.label.text(mes)



class Image:
    ''' Load an image from a file, convert this image to bytes and
        convert bytes back to the image.
    '''
    def __init__(self):
        self._image = self._bytes = self._loader = None
        self.gui = gi.Image()
        
    def open(self,path):
        if lg.File(file=path).Success:
            self._loader = self.gui.loader(path)
            self._image  = self.gui.image(self._loader)
        return self._image
            
    def loader(self):
        f = '[shared] shared.Image.loader'
        if self._bytes:
            self._loader = self.gui.loader(io.BytesIO(self._bytes))
        else:
            com.empty(f)
        return self._loader
        
    def thumbnail(self,x,y):
        ''' Resize an image to x,y limits. PIL will keep an original
            aspect ratio.
        '''
        f = '[shared] shared.Image.thumbnail'
        if self._loader:
            try:
                self._loader.thumbnail([x,y])
            except Exception as e:
                mes = _('Third-party module has failed!\n\nDetails: {}')
                mes = mes.format(e)
                objs.mes(f,mes,True).warning()
        else:
            com.empty(f)
        return self._loader
    
    def image(self):
        f = '[shared] shared.Image.image'
        if self._loader:
            self._image = self.gui.image(self._loader)
        else:
            com.empty(f)
        return self._image
        
    def bytes(self,ext='PNG'):
        if self._loader:
            self._bytes = io.BytesIO()
            self._loader.save(self._bytes,format=ext)
            self._bytes = self._bytes.getvalue()
        else:
            com.empty(f)
        return self._bytes



class Canvas:
    
    def __init__(self,parent,expand=True
                ,side=None,region=None
                ,width=None,height=None
                ,fill='both'
                ):
        self.type    = 'Canvas'
        self.parent  = parent
        self.expand  = expand
        self.side    = side
        self._region = region
        self.width   = width
        self.height  = height
        self.fill    = fill
        self.gui     = gi.Canvas(self.parent)
        self.widget  = self.gui.widget
        
    def move_left_corner(self,event=None):
        self.gui.move_left_corner()
    
    def mouse_wheel(self,event=None):
        return self.gui.mouse_wheel(event)
    
    # These bindings are not enabled by default
    def top_bindings(self,top,Ctrl=True):
        f = '[shared] shared.Canvas.top_bindings'
        if top:
            if hasattr(top,'type') and top.type == 'Toplevel':
                com.bind (obj      = top
                         ,bindings = '<Down>'
                         ,action   = self.move_down
                         )
                com.bind (obj      = top
                         ,bindings = '<Up>'
                         ,action   = self.move_up
                         )
                com.bind (obj      = top
                         ,bindings = '<Left>'
                         ,action   = self.move_left
                         )
                com.bind (obj      = top
                         ,bindings = '<Right>'
                         ,action   = self.move_right
                         )
                com.bind (obj      = top
                         ,bindings = '<Next>'
                         ,action   = self.move_page_down
                         )
                com.bind (obj      = top
                         ,bindings = '<Prior>'
                         ,action   = self.move_page_up
                         )
                com.bind (obj      = top
                         ,bindings = ('<MouseWheel>','<Button 4>'
                                     ,'<Button 5>'
                                     )
                         ,action   = self.mouse_wheel
                         )
                if Ctrl:
                    com.bind (obj      = top
                             ,bindings = '<Control-Home>'
                             ,action   = self.move_top
                             )
                    com.bind (obj      = top
                             ,bindings = '<Control-End>'
                             ,action   = self.move_bottom
                             )
                else:
                    com.bind (obj      = top
                             ,bindings = '<Home>'
                             ,action   = self.move_top
                             )
                    com.bind (obj      = top
                             ,bindings = '<End>'
                             ,action   = self.move_bottom
                             )
            else:
                mes = _('Wrong input data!')
                objs.mes(f,mes,True).warning()
        else:
            com.empty(f)
    
    def move_up(self,event=None,value=-1):
        self.gui.move_up(value)
        
    def move_down(self,event=None,value=1):
        self.gui.move_down(value)
    
    def move_page_up(self,event=None,value=-1):
        self.gui.move_page_up(value)
        
    def move_page_down(self,event=None,value=1):
        self.gui.move_page_down(value)

    def move_left(self,event=None,value=-1):
        self.gui.move_left(value)
        
    def move_right(self,event=None,value=1):
        self.gui.move_right(value)
        
    def move_bottom(self,event=None):
        self.gui.move_bottom()
        
    def move_top(self,event=None):
        self.gui.move_top()
    
    def region (self,x=0,y=0
               ,x_border=0,y_border=0
               ):
        f = '[shared] shared.Canvas.region'
        # Both integer and float values are allowed at input
        if x and y:
            self.gui.region (x        = x
                            ,y        = y
                            ,x_border = x_border
                            ,y_border = y_border
                            )
        else:
            com.empty(f)
    
    def scroll(self,event=None,x=0,y=0):
        self.gui.scroll (x = x
                        ,y = y
                        )
        
    def embed(self,obj):
        f = '[shared] shared.Canvas.embed'
        if hasattr(obj,'widget'):
            self.gui.embed(obj)
        else:
            mes = _('Wrong input data!')
            objs.mes(f,mes,True).error()
        
    def focus(self,event=None):
        self.gui.focus()
    
    def show(self,event=None):
        self.gui.show()
        
    def close(self,event=None):
        self.gui.close()



class Clipboard:

    def __init__(self,Silent=False):
        self.Silent = Silent
        self.gui    = gi.Clipboard()

    def copy(self,text,CopyEmpty=True):
        f = '[shared] shared.Clipboard.copy'
        if text or CopyEmpty:
            text = lg.com.sanitize(text)
            try:
                self.gui.clear()
                self.gui.copy(text)
            except Exception as e:
                com.failed(f,e,self.Silent)
        else:
            com.empty(f)

    def paste(self):
        f = '[shared] shared.Clipboard.paste'
        text = ''
        try:
            text = str(self.gui.paste())
        except Exception as e:
            com.failed(f,e,self.Silent)
        # Further possible actions: strip, delete double line breaks
        return text



class SymbolMap:

    def __init__(self,items=(),title='',icon=''):
        self.parent  = Top()
        self.widget  = self.parent.widget
        self.frm_prm = None
        self.gui     = gi.SymbolMap(self.parent)
        self.bindings()
        self.reset (items = items
                   ,title = title
                   ,icon  = icon
                   )
    
    def get(self,event=None):
        return self.gui.get()
    
    def icon(self,path=''):
        self.gui.icon(path)
    
    def title(self,text=''):
        if not text:
            text = _('Paste a special symbol')
        self.gui.title(text)
        
    def reset(self,items=(),title='',icon=''):
        ''' It is better to run the whole class once again instead of
            doing the reset because frame sizes will not be restored
            after filling a different number of symbols.
        '''
        if not items:
            items = ['1','2','3','4','5']
        items = [lg.com.sanitize(item) for item in items]
        items = [item for item in items if item]
        self.title(title)
        self.icon(icon)
        if self.frm_prm:
            self.frm_prm.kill()
        self.frm_prm = Frame(self.parent)
        for i in range(len(items)):
            if i % 10 == 0:
                self.frm_row = Frame(self.frm_prm)
            self.gui.insert (frame = self.frm_row
                            ,items = items
                            ,i     = i
                            )

    def bindings(self):
        com.bind (obj      = self.parent
                 ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                 ,action   = self.close
                 )

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()



class OptionMenu:
    ''' - 'action' parameter defines an action triggered any time we
          select an OptionMenu item. Use 'com.bind' to set an action
          each time the entire OptionMenu (and not an item) is clicked.
          These bindings do not interfere with each other.
        - tk.OptionMenu will convert integers to strings, but we better
          do this here to avoid problems with iterating ("in requires
          int as the left operand") later (this happens when we pass
          a sequence of chars instead of a list of strings).
        - 'expand' seems to has no effect at the time, but I leave it
          for testing purposes.
    '''
    def __init__ (self
                 ,parent
                 ,items   = ('1','2','3','4','5')
                 ,side    = 'left'
                 ,anchor  = 'center'
                 ,action  = None
                 ,tfocus  = 1
                 ,default = None
                 ,Combo   = False
                 ,expand  = False
                 ,fill    = None
                 ,font    = None
                 ):
        self.parent  = parent
        self.items   = items
        self.action  = action
        self.default = default
        self.Combo   = Combo
        self.side    = side
        self.anchor  = anchor
        self.expand  = expand
        self._fill   = fill
        # Take focus; must be 1/True to be operational from keyboard
        self.tfocus  = tfocus
        self.font    = font
        
        self.gui = gi.OptionMenu (parent = self.parent
                                 ,Combo  = self.Combo
                                 ,side   = self.side
                                 ,anchor = self.anchor
                                 ,expand = self.expand
                                 ,fill   = self._fill
                                 ,tfocus = self.tfocus
                                 ,font   = self.font
                                 )
        self.widget = self.gui.widget
        if self.Combo:
            com.bind (obj      = self
                     ,bindings = '<<ComboboxSelected>>'
                     ,action   = self.trigger
                     )
        
        self.reset (items   = self.items
                   ,default = self.default
                   ,action  = self.action
                   )
    
    def convert2str(self):
        if not self.items:
            # An error is thrown if 'items' is ()
            self.items = ('1','2','3','4','5')
        self.items = list(self.items)
        self.items = [lg.com.sanitize(item) for item in self.items]
    
    def enable(self):
        self.gui.enable()
    
    def disable(self):
        self.gui.disable()
    
    def trigger(self,event=None):
        f = '[shared] shared.OptionMenu.trigger'
        self._get()
        if self.Combo:
            self.gui.clear_selection()
        if self.action:
            self.action()
        else:
            com.lazy(f)

    def _default_set(self):
        if len(self.items) > 0:
            self.gui.set(self.items[0])
            ''' Return a default value instead of 'None' if there was
                no interaction with the widget.
            '''
            self.choice = self.items[0]
            self.index  = 0

    def default_set(self):
        f = '[shared] shared.OptionMenu.default_set'
        if self.default is None:
            self._default_set()
        else:
            if self.default in self.items:
                self.gui.set(self.default)
                ''' Return a default value instead of 'None' if there
                    was no interaction with the widget.
                '''
                self.choice = self.default
                self.index  = self.items.index(self.choice)
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(self.default,self.items)
                objs.mes(f,mes,True).error()
                self._default_set()

    def set(self,item,event=None):
        f = '[shared] shared.OptionMenu.set'
        item = str(item)
        if item in self.items:
            self.gui.set(item)
            self.choice = item
            self.index  = self.items.index(self.choice)
        else:
            mes = _('Wrong input data: "{}"!').format(item)
            objs.mes(f,mes,True).error()

    def fill(self):
        self.gui.fill (items  = self.items
                      ,action = self.trigger
                      )

    def reset (self,items=('1','2','3','4','5')
              ,default=None,action=None
              ):
        self.choice = None
        self.index  = 0
        self.items  = items
        if action:
            self.action = action
        self.convert2str()
        self.fill()
        if default is None:
            if self.choice in self.items:
                default = self.choice
        if default is not None:
            self.default = str(default)
        self.default_set()
        if len(self.items) == 1:
            self.gui.disable()
        else:
            self.gui.enable()

    # Auto updated (after selecting an item)
    def _get(self,event=None):
        f = '[shared] shared.OptionMenu._get'
        self.choice = self.gui.get()
        try:
            self.index = self.items.index(self.choice)
        except ValueError:
            mes = _('Wrong input data: "{}"!').format(self.choice)
            objs.mes(f,mes,True).error()

    def set_prev(self,event=None):
        if self.index == 0:
            self.index = len(self.items) - 1
        else:
            self.index -= 1
        self.choice = self.items[self.index]
        self.gui.set(self.choice)

    def set_next(self,event=None):
        if self.index == len(self.items) - 1:
            self.index = 0
        else:
            self.index += 1
        self.choice = self.items[self.index]
        self.gui.set(self.choice)

    def focus(self,event=None):
        self.gui.focus()



class ListBox:
    #todo: configure a font
    def __init__(self
                ,parent
                ,Multiple = False
                ,lst      = []
                ,action   = None
                ,side     = None
                ,expand   = True
                ,fill     = 'both'
                ):
        self.type     = 'ListBox'
        self.state    = 'normal'
        self.parent   = parent
        self.Multiple = Multiple
        self.expand   = expand
        self.side     = side
        self._fill    = fill
        ''' 'action': A user-defined function that is run when
            pressing Up/Down arrow keys and LMB. There is a problem
            binding it externally, so we bind it here.
        '''
        self.action = action
        
        self.gui = gi.ListBox (parent   = self.parent
                              ,Multiple = self.Multiple
                              ,side     = self.side
                              ,expand   = self.expand
                              ,fill     = self._fill
                              )
        self.widget = self.gui.widget
        self.bindings()
        if lst or action:
            self.reset (lst    = lst
                       ,action = action
                       )

    def focus(self,event=None):
        self.gui.focus()
    
    def trigger(self,event=None):
        if self.action:
            ''' Binding just to '<Button-1>' does not work. We do not
                need binding Return/space/etc. because the function will
                be called each time the selection is changed. However,
                we still need to bind Up/Down.
            '''
            self.action()
    
    def delete(self,event=None):
        f = '[shared] shared.ListBox.delete'
        # Set an actual value
        self.index()
        try:
            del self.lst[self._index]
            # Set this after 'del' to be triggered only on success
            mes = _('Remove item #{}').format(self._index)
            objs.mes(f,mes,True).debug()
        except IndexError:
            mes = _('No item #{}!').format(self._index)
            objs.mes(f,mes,True).warning()
        else:
            self.reset(lst=self.lst)

    def insert(self,string,Top=False):
        # Empty lists are allowed
        if Top:
            pos = 0
        else:
            pos = len(self.lst)
        self.lst.insert(pos,string)
        self.reset(lst=self.lst)
    
    def bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = '<<ListboxSelect>>'
                 ,action   = self.trigger
                 )
        if not self.Multiple:
            com.bind (obj      = self.gui
                     ,bindings = '<Up>'
                     ,action   = self.move_up
                     )
            com.bind (obj      = self.gui
                     ,bindings = '<Down>'
                     ,action   = self.move_down
                     )

    def resize(self):
        # Autofit to contents
        self.gui.resize()

    def activate(self):
        self.gui.activate(self._index)

    def clear(self):
        self.gui.clear()

    def clear_selection(self):
        self.gui.clear_selection()

    def reset(self,lst=[],action=None):
        self.clear()
        if lst is None:
            self.lst = []
        else:
            self.lst = list(lst)
        self.lst = [lg.com.sanitize(item) for item in self.lst if item]
        # Checking for None allows to keep an old function
        if action:
            self.action = action
        self.fill()
        self.resize()
        self._index = 0
        self.select()

    def select(self):
        self.clear_selection()
        self.gui.select(self._index)

    def set(self,item):
        f = '[shared] shared.ListBox.set'
        if item:
            if item in self.lst:
                self._index = self.lst.index(item)
                self.select()
            else:
                mes = _('Item "{}" is not in list!').format(item)
                objs.mes(f,mes,True).error()
        else:
            com.empty(f)

    def fill(self):
        for item in self.lst:
            self.gui.insert(item)

    def index(self):
        selection = self.gui.selection()
        if selection and len(selection) > 0:
            ''' #note: selection[0] is a number in Python 3.4, however,
                in older interpreters and builds based on them it is a
                string. In order to preserve compatibility, we convert
                it to a number.
            '''
            self._index = int(selection[0])
        else:
            self._index = 0
        return self._index

    def index_add(self):
        if self.index() < len(self.lst) - 1:
            self._index += 1
        else:
            self._index = 0

    def index_subtract(self):
        if self.index() > 0:
            self._index -= 1
        else:
            self._index = len(self.lst) - 1

    def get(self):
        result = [self.gui.get(idx) for idx in self.gui.selection()]
        if self.Multiple:
            return result
        elif len(result) > 0:
            return result[0]

    def move_down(self,event=None):
        self.index_add()
        self.select()
        self.trigger()

    def move_up(self,event=None):
        self.index_subtract()
        self.select()
        self.trigger()
        
    def move_top(self,event=None):
        if self.lst:
            self._index = 0
            self.select()
            self.trigger()
    
    def move_bottom(self,event=None):
        if self.lst:
            self._index = len(self.lst) - 1
            self.select()
            self.trigger()



class ListBoxC:
    ''' This widget is based on 'Top' which already sanitizes input and
        checks an icon path, so we don't do that.
    '''
    def __init__(self
                ,Multiple = False
                ,lst      = []
                ,action   = None
                ,side     = None
                ,expand   = True
                ,fill     = 'both'
                ,title    = 'Title:'
                ,icon     = None
                ,ScrollX  = True
                ,ScrollY  = True
                ):
        self.Save     = False
        self.Multiple = Multiple
        self.lst      = lst
        self.action   = action
        self.side     = side
        self.expand   = expand
        self._fill    = fill
        self._title   = title
        self._icon    = icon
        self.ScrollX  = ScrollX
        self.ScrollY  = ScrollY
        self.add_gui()
    
    def clear(self,event=None):
        self.lbx_prm.clear()
    
    def focus(self,event=None):
        self.gui.focus()
    
    def set(self,item):
        self.lbx_prm.set(item)
    
    def clear_selection(self,event=None):
        self.lbx_prm.clear_selection()
    
    def reset(self,lst=(1,2,3,4,5),action=None,title='',icon=''):
        self.Save = False
        self.lbx_prm.reset (lst    = lst
                           ,action = action
                           )
        self.title(title)
        self.icon(icon)
    
    def buttons(self):
        self.btn_cls = Button (parent = self.frm_btn
                              ,action = self.close
                              ,hint   = _('Reject and close')
                              ,text   = _('Close')
                              )
        self.btn_sav = Button (parent = self.frm_btn
                              ,action = self.save
                              ,hint   = _('Accept and close')
                              ,text   = _('Save and close')
                              ,side   = 'right'
                              )
    
    def get(self):
        if self.Save:
            return self.lbx_prm.get()
    
    def scrollx(self):
        if self.ScrollX:
            Scrollbar (parent = self.frm_hor
                      ,scroll = self.lbx_prm
                      ,Horiz  = True
                      )
    
    def scrolly(self):
        if self.ScrollY:
            Scrollbar (parent = self.frm_ver
                      ,scroll = self.lbx_prm
                      )
    
    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()

    def save(self,event=None):
        self.Save = True
        self.close()
    
    def frames(self):
        self.frm_prm = Frame(self.parent)
        self.frm_sec = Frame (parent = self.frm_prm
                             ,side   = 'top'
                             )
        self.frm_btn = Frame (parent = self.frm_prm
                             ,side   = 'bottom'
                             ,expand = False
                             ,fill   = 'x'
                             )
        self.frm_trt = Frame (parent = self.frm_sec
                             ,side   = 'left'
                             )
        self.frm_ver = Frame (parent = self.frm_sec
                             ,side   = 'right'
                             ,expand = False
                             ,fill   = 'y'
                             )
        self.frm_lbx = Frame (parent = self.frm_trt
                             ,side   = 'top'
                             )
        self.frm_hor = Frame (parent = self.frm_trt
                             ,side   = 'bottom'
                             ,expand = False
                             ,fill   = 'x'
                             )
    
    def add_gui(self):
        self.parent = Top()
        self.widget = self.parent.widget
        Geometry(self.parent).set('800x600')
        self.frames()
        self.lbx_prm = ListBox (parent   = self.frm_lbx
                               ,Multiple = self.Multiple
                               ,lst      = self.lst
                               ,action   = self.action
                               ,side     = self.side
                               ,expand   = self.expand
                               ,fill     = self._fill
                               )
        self.lbx_prm.focus()
        self.gui = gi.ListBoxC(self.parent)
        self.scrollx()
        self.scrolly()
        self.buttons()
        self.title()
        self.icon()
    
    def title(self,text=''):
        if text:
            self._title = text
        self.gui.title(self._title)
    
    def icon(self,path=''):
        if path:
            self._icon = path
        self.gui.icon(self._icon)



class Scrollbar:
    
    def __init__(self,parent,scroll,Horiz=False):
        self.type   = 'Scrollbar'
        self.parent = parent
        self.scroll = scroll
        self.Horiz  = Horiz
        self.gui = gi.Scrollbar (parent = self.parent
                                ,scroll = self.scroll
                                )
        if self.check():
            if self.Horiz:
                self.gui.create_x()
                self.gui.config_x()
            else:
                self.gui.create_y()
                self.gui.config_y()
    
    def check(self):
        f = '[shared] shared.Scrollbar.check'
        if self.parent and self.scroll:
            if hasattr(self.parent,'widget') \
            and hasattr(self.scroll,'widget'):
                return True
            else:
                mes = _('Wrong input data!')
                objs.mes(f,mes,True).error()
        else:
            com.empty(f)



# Pop-up tips; see also 'calltips'; based on idlelib.ToolTip
class ToolTipBase:

    def __init__(self,obj):
        self.obj    = obj
        self.widget = self.obj.widget
        self.gui    = gi.ToolTipBase(self.obj)
        self.tip    = None
        self.id     = None
        self.x      = 0
        self.y      = 0
        self.bindings()
    
    def bindings(self):
        self.bind_mouse()
                    
    def bind_mouse(self):
        com.bind (obj      = self.obj
                 ,bindings = '<Enter>'
                 ,action   = self.enter
                 )
        com.bind (obj      = self.obj
                 ,bindings = ('<Leave>','<ButtonPress>')
                 ,action   = self.leave
                 )

    def enter(self,event=None):
        self.schedule()

    def leave(self,event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.gui.schedule(self.delay,self.showtip)

    def unschedule(self):
        myid = self.id
        self.id = None
        if myid:
            self.gui.unschedule(myid)

    def showtip(self):
        f = '[shared] shared.ToolTipBase.showtip'
        if self.tip:
            return
        ''' The tip window must be completely outside the widget;
            otherwise, when the mouse enters the tip window we get
            a leave event and it disappears, and then we get an enter
            event and it reappears, and so on forever :-(
            Tip coordinates are calculated such that, despite different
            sizes, centers of a horizontal tip and button would match.
        '''
        x = self.gui.rootx() + self.gui.width()/2 - self.width/2
        if self.dir == 'bottom':
            y = self.gui.rooty() + self.gui.height() + 1
        elif self.dir == 'top':
            y = self.gui.rooty() - self.height - 1
        else:
            y = 0
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.dir,'top, bottom')
            objs.mes(f,mes,True).error()
        self.tip = Top(Lock=False)
        self.tip.widget.wm_overrideredirect(1)
        # "+%d+%d" is not enough!
        mes = _('Set the geometry to "{}x{}+{}+{}"').format (self.width
                                                            ,self.height
                                                            ,x,y
                                                            )
        objs.mes(f,mes,True).info()
        self.tip.widget.wm_geometry ("%dx%d+%d+%d" % (self.width
                                                     ,self.height
                                                     ,x, y
                                                     )
                                    )
        self.showcontents()

    def hidetip(self):
        tw = self.tip
        self.tip = None
        if tw:
            tw.widget.destroy()



class ToolTip(ToolTipBase):

    def __init__(self,obj,text='Sample text'
                ,delay=800,bg='#ffffe0'
                ,hdir='top',bwidth=1
                ,bcolor='navy',font='Sans 11'
                ):
        self.height = 0
        self.width  = 0
        self.text   = text
        self.delay  = delay
        self.dir    = hdir
        self.bg     = bg
        self.bcolor = bcolor
        self.bwidth = bwidth
        self.font   = font
        self.calc_hint()
        ToolTipBase.__init__(self,obj=obj)

    def calc_hint(self):
        f = '[shared] shared.ToolTip.calc_hint'
        if not self.width or not self.height:
            if self.text:
                if not self.font:
                    self.font = 'Sans 11'
                ifont = Font(self.font)
                ifont.set_text(self.text)
                self.width  = ifont.width()
                self.height = ifont.height()
            else:
                com.lazy(f)
    
    def showcontents(self):
        # Assign this boolean externally to stop showing hints
        self.frm = Frame (parent = self.tip
                         ,bg     = self.bcolor
                         ,bd     = self.bwidth
                         ,expand = False
                         )
        self.lbl = Label (parent  = self.frm
                         ,text    = self.text
                         ,bg      = self.bg
                         ,width   = self.width
                         ,height  = self.height
                         ,justify = 'center'
                         ,font    = self.font
                         )



class WaitBox:

    def __init__(self,icon=''):
        self.type   = 'WaitBox'
        self.parent = Top (Lock   = False
                          ,AutoCr = True
                          ,icon   = icon
                          )
        self.widget = self.parent.widget
        self.gui    = gi.WaitBox(self.parent)
        Geometry(self.parent).set('300x150')
        self.lbl_pls = Label (parent = self.parent
                             ,text   = _('Please wait...')
                             ,expand = True
                             )

    def icon(self,path=''):
        f = '[shared] shared.WaitBox.icon'
        if path:
            if os.path.exists(path):
                self.gui.icon(path)
            else:
                mes = _('File "{}" has not been found!').format(path)
                objs.mes(f,mes).warning()
        else:
            com.empty(f)
    
    def update(self):
        ''' Tkinter works differently in Linux in Windows. This allows
            to evade focus problems in 'mclient'.
        '''
        if objs.os().win():
            objs.root().idle()
        else:
            self.lbl_pls.widget.update()
    
    # Use tuple for 'args' to pass multiple arguments
    def reset(self,func='',message=''):
        self.title(func)
        self.message(message)

    def show(self):
        self.gui.show()
        self.update()

    def close(self):
        self.gui.close()

    def title(self,text=''):
        text = lg.com.sanitize(text)
        self.gui.title(text)

    def message(self,text=''):
        text = lg.com.sanitize(text)
        if text:
            text += '\n\n' + _('Please wait...')
        else:
            text = _('Please wait...')
        self.lbl_pls.text(text)



class Button:

    def __init__ (self
                 ,parent
                 ,action   = None
                 ,hint     = None
                 ,inactive = None
                 ,active   = None
                 ,text     = 'Press me'
                 ,height   = 36
                 ,width    = 36
                 ,side     = 'left'
                 ,expand   = 0
                 ,bg       = None
                 ,bg_focus = None
                 ,fg       = None
                 ,fg_focus = None
                 ,bd       = 0
                 ,hdelay   = 800
                 ,hbg      = '#ffffe0'
                 ,hdir     = 'top'
                 ,hbwidth  = 1
                 ,hbcolor  = 'navy'
                 ,bindings = []
                 ,fill     = 'both'
                 ,Focus    = False
                 ,font     = None
                 ):
        self.Status    = False
        self.type      = 'Button'
        self.parent    = parent
        self.family    = 'Sans'
        self.size      = 12
        self.action    = action
        self.bd        = bd
        self.bg        = bg
        self.bg_focus  = bg_focus
        self._bindings = bindings
        self.expand    = expand
        self.fg        = fg
        self.fg_focus  = fg_focus
        self.fill      = fill
        self.font      = font
        self.height    = height
        self.hbg       = hbg
        self.hdelay    = hdelay
        self.hdir      = hdir
        self.hint      = hint
        self.side      = side
        self.Focus     = Focus
        self.text      = lg.com.sanitize(text)
        self.width     = width
        if active:
            self.on_img = gi.com.image (path   = active
                                       ,width  = self.width
                                       ,height = self.height
                                       )
        else:
            self.on_img = None
        if inactive:
            self.off_img = gi.com.image (path   = inactive
                                        ,width  = self.width
                                        ,height = self.height
                                        )
        else:
            self.off_img = None
        self.gui = gi.Button (parent   = parent
                             ,height   = height
                             ,width    = width
                             ,side     = side
                             ,expand   = expand
                             ,bg       = bg
                             ,bg_focus = bg_focus
                             ,fg       = fg
                             ,fg_focus = fg_focus
                             ,bd       = bd
                             ,fill     = fill
                             ,font     = font
                             ,on_img   = self.on_img
                             ,off_img  = self.off_img
                             )
        self.widget = self.gui.widget
        self.title(self.text)
        self.bindings()
        if self.Focus:
            self.focus()
        self.set_hint()
    
    def bindings(self):
        com.bind (obj      = self
                 ,bindings = ('<ButtonRelease-1>','<space>'
                             ,'<Return>','<KP_Enter>'
                             )
                 ,action   = self.click
                 )

    def set_hint(self):
        if self.hint:
            if self._bindings:
                self.hextended = self.hint + '\n' \
                                 + lg.Hotkeys(self._bindings).run()
            else:
                self.hextended = self.hint
            self.tip = ToolTip (obj   = self.gui
                               ,text  = self.hextended
                               ,delay = self.hdelay
                               ,font  = self.font
                               ,bg    = self.hbg
                               ,hdir  = self.hdir
                               )
    
    def title(self,button_text='Press me'):
        button_text = lg.com.sanitize(button_text)
        self.gui.title(button_text)

    def click(self,*args):
        f = '[shared] shared.Button.click'
        if self.action:
            if len(args) > 0:
                self.action(args)
            else:
                self.action()
        else:
            com.lazy(f)

    def active(self):
        if not self.Status:
            self.Status = True
            if self.on_img:
                self.gui.active()

    def inactive(self):
        if self.Status:
            self.Status = False
            if self.off_img:
                self.gui.inactive()

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()

    def focus(self,event=None):
        self.gui.focus()
    
    def enable(self):
        self.gui.enable()
    
    def disable(self):
        self.gui.disable()



class Frame:

    def __init__ (self,parent,expand=1
                 ,fill='both',side=None,padx=None
                 ,pady=None,ipadx=None,ipady=None
                 ,bd=None,bg=None,width=None
                 ,height=None,propag=True
                 ):
        self.type   = 'Frame'
        self.parent = parent
        self.gui = gi.Frame (parent = parent
                            ,expand = expand
                            ,fill   = fill
                            ,side   = side
                            ,padx   = padx
                            ,pady   = pady
                            ,ipadx  = ipadx
                            ,ipady  = ipady
                            ,bd     = bd
                            ,bg     = bg
                            ,width  = width
                            ,height = height
                            ,propag = propag
                            )
        self.widget = self.gui.widget

    def height(self):
        return self.gui.height()
    
    def width(self):
        return self.gui.width()
    
    def reqheight(self):
        return self.gui.reqheight()
    
    def reqwidth(self):
        return self.gui.reqwidth()
    
    def kill(self):
        self.gui.kill()
    
    def title(self,text=None):
        text = lg.com.sanitize(text)
        self.gui.title(text)

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()



class AttachWidget:
    # Make widget 'obj2' immediately adjacent to 'obj1'
    def __init__ (self,obj1,obj2
                 ,anchor='N'
                 ):
        self.values()
        self.obj1   = obj1
        self.obj2   = obj2
        self.anchor = anchor
        self.check()
        
    def values(self):
        self.anchors = ('N','NE','NW','E','EN','ES','S','SE','SW','W'
                       ,'WN','WS'
                       )
        self.Success = True
        self.w1 = 0
        self.h1 = 0
        self.w2 = 0
        self.h2 = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
    
    def check(self):
        f = '[shared] shared.AttachWidget.check'
        if self.obj1 and self.obj2:
            if hasattr(self.obj1,'widget') \
            and hasattr(self.obj2,'widget'):
                self.widget1 = self.obj1.widget
                self.widget2 = self.obj2.widget
            else:
                self.Success = False
                mes = _('Wrong input data!')
                objs.mes(f,mes).warning()
        else:
            self.Success = False
            com.empty(f)
        if self.anchor not in self.anchors:
            self.Success = False
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".').format(self.anchor,self.anchors)
            objs.mes(f,mes).error()
    
    def _ne(self):
        self.x2 = self.x1
        self.y2 = self.y1 - self.h2
    
    def _n(self):
        self.x2 = self.x1 + self.w1/2 - self.w2/2
        self.y2 = self.y1 - self.h2
    
    def _nw(self):
        self.x2 = self.x1 + self.w1 - self.w2
        self.y2 = self.y1 - self.h2
                      
    def _en(self):
        self.x2 = self.x1 - self.w2
        self.y2 = self.y1
    
    def _e(self):
        self.x2 = self.x1 - self.w2
        self.y2 = self.y1 + self.h1/2 - self.h2/2
    
    def _es(self):
        self.x2 = self.x1 - self.w2
        self.y2 = self.y1 + self.h1 - self.h2
    
    def _se(self):
        self.x2 = self.x1
        self.y2 = self.y1 + self.h1

    def _s(self):
        self.x2 = self.x1 + self.w1/2 - self.w2/2
        self.y2 = self.y1 + self.h1
    
    def _sw(self):
        self.x2 = self.x1 + self.w1 - self.w2
        self.y2 = self.y1 + self.h1
    
    def _wn(self):
        self.x2 = self.x1 + self.w1
        self.y2 = self.y1
    
    def _w(self):
        self.x2 = self.x1 + self.w1
        self.y2 = self.y1 + self.h1/2 - self.h2/2
                      
    def _ws(self):
        self.x2 = self.x1 + self.w1
        self.y2 = self.y1 + self.h1 - self.h2
    
    def set(self):
        f = '[shared] shared.AttachWidget.set'
        if self.Success:
            if self.anchor == 'N':
                self._n()
            elif self.anchor == 'NE':
                self._ne()
            elif self.anchor == 'NW':
                self._nw()
            elif self.anchor == 'E':
                self._e()
            elif self.anchor == 'EN':
                self._en()
            elif self.anchor == 'ES':
                self._es()
            elif self.anchor == 'S':
                self._s()
            elif self.anchor == 'SE':
                self._se()
            elif self.anchor == 'SW':
                self._sw()
            elif self.anchor == 'W':
                self._w()
            elif self.anchor == 'WN':
                self._wn()
            elif self.anchor == 'WS':
                self._ws()
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".').format(self.anchor,self.anchors)
                objs.mes(f,mes).error()
            geom = Geometry(parent=self.obj2)
            ''' Do not use '.format' here since it produces floats
                and we need integers.
            '''
            geom._geom = '%dx%d+%d+%d' % (self.w2,self.h2
                                         ,self.x2,self.y2
                                         )
            geom.restore()
        else:
            com.cancel(f)
    
    def get(self):
        f = '[shared] sharedGUI.AttachWidget.get'
        if self.Success:
            self.x1 = self.widget1.winfo_rootx()
            self.x2 = self.widget2.winfo_rootx()
            self.y1 = self.widget1.winfo_rooty()
            self.y2 = self.widget2.winfo_rooty()
            self.w1 = self.widget1.winfo_width()
            self.w2 = self.widget2.winfo_width()
            self.h1 = self.widget1.winfo_height()
            self.h2 = self.widget2.winfo_height()
            mes = _('Widget 1 geometry: {}x{}+{}+{}').format (self.w1
                                                             ,self.h1
                                                             ,self.x1
                                                             ,self.y1
                                                             )
            objs.mes(f,mes,True).debug()
            mes = _('Widget 2 geometry: {}x{}+{}+{}').format (self.w2
                                                             ,self.h2
                                                             ,self.x2
                                                             ,self.y2
                                                             )
            objs.mes(f,mes,True).debug()
        else:
            com.cancel(f)
    
    def run(self,event=None):
        self.get()
        self.set()



class Label:
    ''' 1) Use fill='both' with 'expand=1', otherwise, 'expand' does
           not work
        2) Use 'anchor="w"' to left align text
        3) Parents are 'Top' and 'Root' (the last only with
           'wait_window()')
        4) Inappropriate use of 'config' may result in resetting 
           config options. List of them: http://effbot.org/tkinterbook/label.htm#Tkinter.Label.config-method
    '''
    def __init__ (self,parent,text='Text:'
                 ,font='Sans 11',side=None,fill=None
                 ,expand=False,ipadx=None,ipady=None
                 ,image=None,fg=None,bg=None
                 ,anchor=None,width=None
                 ,height=None,justify=None
                 ):
        self.type   = 'Label'
        self.parent = parent
        self.side   = side
        self.fill   = fill
        self.expand = expand
        self._text  = text
        self._font  = font
        self.ipadx  = ipadx
        self.ipady  = ipady
        self.image  = image
        self.bg     = bg
        self.fg     = fg
        self.anchor = anchor
        self.width  = width
        self.height = height
        # Usually the alignment is done by tuning the parent
        self.justify = justify
        self.gui = gi.Label (parent  = self.parent
                            ,side    = self.side
                            ,fill    = self.fill
                            ,expand  = self.expand
                            ,ipadx   = self.ipadx
                            ,ipady   = self.ipady
                            ,image   = self.image
                            ,fg      = self.fg
                            ,bg      = self.bg
                            ,anchor  = self.anchor
                            ,width   = self.width
                            ,height  = self.height
                            ,justify = self.justify
                            )
        self.widget  = self.gui.widget
        self.text(self._text)
        self.font(self._font)
    
    def reqheight(self,event=None):
        return self.gui.reqheight()
    
    def reqwidth(self,event=None):
        return self.gui.reqwidth()
    
    def kill(self,event=None):
        self.gui.kill()
    
    def disable(self,event=None):
        self.gui.disable()
    
    def enable(self,event=None):
        self.gui.enable()

    def text(self,arg=None):
        if arg:
            self._text = arg
        self._text = lg.com.sanitize(arg)
        self.gui.text(self._text)

    def font(self,arg=None):
        f = '[shared] shared.Label.font'
        if arg:
            self._font = arg
        if not self.gui.font(self._font):
            mes = _('Wrong font: "{}"!').format(self._font)
            objs.mes(f,mes,True).error()
            self._font = 'Sans 11'

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()

    def title(self,text=''):
        text = lg.com.sanitize(text)
        self.gui.title(text)
        
    def reset(self):
        ''' #note #todo For some reason, using 'config' externally may 
            reset config options. Use them altogether to prevent such 
            behavior.
        '''
        self.widget.config (text   = self._text
                           ,font   = self._font
                           ,ipadx  = self.ipadx
                           ,ipady  = self.ipady
                           #,image = self.image
                           ,bg     = self.bg
                           ,fg     = self.fg
                           ,anchor = self.anchor
                           ,width  = self.width
                           ,height = self.height
                           )



class Geometry:
    ''' Window behavior is not uniform through different platforms or
        even through different Windows versions.
    '''
    def __init__(self,parent=None,title=None,hwnd=None):
        self.parent = parent
        self._title = title
        self._hwnd  = hwnd
        self._geom  = None
        self.gui    = gi.Geometry(parent)

    def update(self):
        self.gui.update()

    def save(self):
        f = '[shared] shared.Geometry.save'
        if self.parent:
            self.update()
            self._geom = self.gui.geometry()
            mes = _('Save geometry: {}').format(self._geom)
            objs.mes(f,mes,True).info()
        else:
            com.empty(f)

    def restore(self):
        f = '[shared] shared.Geometry.restore'
        if self.parent:
            if self._geom:
                mes = _('Restore geometry: {}').format(self._geom)
                objs.mes(f,mes,True).info()
                self.gui.restore(self._geom)
            else:
                mes = _('Failed to restore geometry!')
                objs.mes(f,mes,True).warning()
        else:
            com.empty(f)

    def foreground(self,event=None):
        f = '[shared] shared.Geometry.foreground'
        if objs.os().win():
            if self.hwnd():
                ''' 'pywintypes.error', but needs to import this for
                    some reason
                '''
                try:
                    win32gui.SetForegroundWindow(self._hwnd)
                except:
                    ''' In Windows 'Message' can be raised foreground,
                        so we just log it
                    '''
                    mes = _('Failed to change window properties!')
                    objs.mes(f,mes,True).error()
            else:
                com.empty(f)
        elif self.parent:
            self.gui.foreground()
        else:
            com.empty(f)

    def minimize(self,event=None):
        f = '[shared] shared.Geometry.minimize'
        if self.parent:
            ''' # Does not always work
                if objs.os().win():
                    win32gui.ShowWindow(self.hwnd(),win32con.SW_MINIMIZE)
                else:
            '''
            self.gui.minimize()
        else:
            com.empty(f)

    def maximize(self,event=None):
        f = '[shared] shared.Geometry.maximize'
        if lg.objs.os().win():
            #win32gui.ShowWindow(self.hwnd(),win32con.SW_MAXIMIZE)
            self.gui.maximize_win()
        elif self.parent:
            self.gui.maximize_nix()
        else:
            com.empty(f)

    def focus(self,event=None):
        f = '[shared] shared.Geometry.focus'
        if lg.objs.os().win():
            win32gui.SetActiveWindow(self.hwnd())
        elif self.parent:
            self.gui.focus()
        else:
            com.empty(f)

    def lift(self,event=None):
        f = '[shared] shared.Geometry.lift'
        if self.parent:
            self.gui.lift()
        else:
            com.empty(f)

    def _activate(self):
        f = '[shared] shared.Geometry._activate'
        if self.parent:
            self.gui._activate()
        else:
            com.empty(f)

    def activate(self,event=None,MouseClicked=False):
        self._activate()
        if objs.os().win():
            #todo: learn how to properly import modules
            import ctypes
            self.parent.widget.wm_attributes('-topmost',1)
            self.parent.widget.wm_attributes('-topmost',0)
            ''' Without this, a button click will fire a button action
                where it is not needed.
            '''
            if MouseClicked:
                ''' It's an ugly hack, but we cannot set a focus on
                    a widget without this (we manage without this
                    in Linux/Windows XP, however, this is required in
                    Windows 7/8).
                '''
                # Emulate a mouse button click
                # left mouse button down
                ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
                # left mouse button up
                ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

    def hwnd(self,event=None):
        f = '[shared] shared.Geometry.hwnd'
        if not self._hwnd:
            if self._title:
                try:
                    self._hwnd = win32gui.FindWindow(None,self._title)
                except win32ui.error:
                    mes = _('Failed to get the window handle!')
                    objs.mes(f,mes,True).error()
            else:
                com.empty(f)
        return self._hwnd

    def set(self,arg='800x600'):
        self._geom = arg
        self.restore()



class Top:

    def __init__ (self,Maximize=False
                 ,AutoCr=True,Lock=True
                 ,icon='',title=''
                 ):
        ''' 'Lock = True': the further program execution is blocked
            until an attempt to close the widget. 'Lock = False' allows
            to create several widgets on the screen at the same time.
            They will be operational, however, the widget having
            'Lock = False' will be closed when closing with
            'Lock = True'. Moreover, if none of the widgets has
            'Lock = True', then they all will be shown and immediately
            closed.
        '''
        self.values()
        self.AutoCr = AutoCr
        self.gui    = gi.Top(Lock=Lock)
        self.widget = self.gui.widget
        if Maximize:
            Geometry(parent=self).maximize()
        if icon:
            self.icon(icon)
        if title:
            self.title(title)
        
    def idle(self,event=None):
        self.gui.idle()
    
    def icon(self,path=''):
        f = '[shared] shared.Top.icon'
        if path:
            if os.path.exists(path):
                self.gui.icon(path)
            else:
                mes = _('File "{}" has not been found!').format(path)
                objs.mes(f,mes).warning()
        else:
            com.empty(f)
    
    def title(self,text=''):
        text = lg.com.sanitize(text)
        self.gui.title(text)
    
    def values(self):
        self.type  = 'Toplevel'
        self.count = 0

    def close(self,event=None):
        self.gui.close()

    def show(self):
        ''' Changing geometry at a wrong time may prevent frames
            from autoresizing after 'pack_forget'.
        '''
        if self.count == 0 and self.AutoCr:
            self.center()
        self.count += 1
        self.gui.show()

    def resolution(self):
        return self.gui.resolution()

    def center(self):
        ''' Make child widget always centered at the first time and up
            to a user's choice any other time (if the widget is reused).
            Only 'tk.Tk' and 'tk.Toplevel' types are supported.
        '''
        width, height = self.resolution()
        size = tuple(int(item) for item \
                in self.gui.geometry().split('+')[0].split('x'))
        x = width/2 - size[0]/2
        y = height/2 - size[1]/2
        self.gui.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def focus(self,event=None):
        self.gui.focus()



class Objects(lg.Objects):
    
    def __init__(self):
        super().__init__()
        self._question = self._info = self._warning = self._debug \
                       = self._error = self._mes = self._waitbox \
                       = self._txt = None
    
    def txt(self):
        if self._txt is None:
            self._txt = TextBoxC(title=_('Test:'))
        return self._txt
    
    def mes (self,func='Logic error'
            ,message='Logic error'
            ,Silent=False
            ):
        if self._mes is None:
            self._mes = Message
        return self._mes(func,message,Silent)
    
    def waitbox(self,icon=''):
        if self._waitbox is None:
            self._waitbox = WaitBox(icon)
        return self._waitbox
    
    def root(self,Close=True):
        return gi.objs.root(Close)
    
    def error(self):
        if self._error is None:
            self._error = MessageBuilder (level  = _('ERROR')
                                         ,Single = True
                                         ,YesNo  = False
                                         )
        return self._error
    
    def warning(self):
        if self._warning is None:
            self._warning = MessageBuilder (level  = _('WARNING')
                                           ,Single = True
                                           ,YesNo  = False
                                           )
        return self._warning
    
    def debug(self):
        # Reusing the same 'info' object may result in GUI glitches
        if self._debug is None:
            self._debug = MessageBuilder (level  = _('INFO')
                                         ,Single = True
                                         ,YesNo  = False
                                         )
        return self._debug
    
    def info(self):
        if self._info is None:
            self._info = MessageBuilder (level  = _('INFO')
                                        ,Single = True
                                        ,YesNo  = False
                                        )
        return self._info
    
    def question(self):
        if self._question is None:
            self._question = MessageBuilder (level  = _('QUESTION')
                                            ,Single = False
                                            ,YesNo  = True
                                            )
        return self._question



class MessageBuilder:
    ''' Not using tkinter.messagebox because it blocks main GUI (even
        if we specify a non-root parent).
    '''
    def __init__(self,level,Single=True,YesNo=False):
        self.level  = level
        self.Single = Single
        self.YesNo  = YesNo
        self.logic  = lg.MessageBuilder(self.level)
        self.parent = Top()
        self.widget = self.parent.widget
        self.gui    = gi.MessageBuilder(self.parent)
        Geometry(parent=self.parent).set('400x250')
        self.frames()
        self.txt = TextBox(self.frm_tpr)
        self.buttons()
        self.icon()
        self.image()
        self.bindings()
    
    def update(self,text=''):
        #note: Control-c does not work with read-only fields
        self.txt.clear_text()
        ''' Setting 'MoveTop' to 'True' leads to a bug when
            proportions of 'MessageBuilder' change upon reset. 
        '''
        self.txt.insert(text,MoveTop=False)
    
    def bindings(self):
        com.bind (obj      = self
                 ,bindings = ('<Control-q>','<Control-w>','<Escape>')
                 ,action   = self.close_no
                 )
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
    
    def frames(self):
        self.frm_prm = Frame (parent = self.gui.parent)
        self.frm_top = Frame (parent = self.frm_prm
                             ,side   = 'top'
                             )
        self.frm_btm = Frame (parent = self.frm_prm
                             ,expand = False
                             ,side   = 'bottom'
                             )
        self.frm_tpl = Frame (parent = self.frm_top
                             ,expand = False
                             ,side   = 'left'
                             )
        self.frm_tpr = Frame (parent = self.frm_top
                             ,side   = 'right'
                             ,propag = False
                             )
        self.frm_btl = Frame (parent = self.frm_btm
                             ,side   = 'left'
                             )
        self.frm_btr = Frame (parent = self.frm_btm
                             ,side   = 'right'
                             )
    
    def buttons(self):
        if self.YesNo:
            YesName = _('Yes')
            NoName  = _('No')
        else:
            YesName = 'OK'
            NoName  = _('Cancel')
        if self.Single:
            self.btn_yes = Button (parent = self.frm_btl
                                  ,action = self.close_yes
                                  ,hint   = _('Accept and close')
                                  ,text   = YesName
                                  ,Focus  = 1
                                  ,side   = 'right'
                                  )
        else:
            self.btn_no  = Button (parent = self.frm_btl
                                  ,action = self.close_no
                                  ,hint   = _('Reject and close')
                                  ,text   = NoName
                                  ,side   = 'left'
                                  )
            self.btn_yes = Button (parent = self.frm_btr
                                  ,action = self.close_yes
                                  ,hint   = _('Accept and close')
                                  ,text   = YesName
                                  ,Focus  = 1
                                  ,side   = 'right'
                                  )
    
    def close_yes(self,event=None):
        self.Yes = True
        self.close()

    def close_no(self,event=None):
        self.Yes = False
        self.close()
    
    def ask(self,event=None):
        return self.Yes
    
    def show(self,event=None):
        self.btn_yes.focus()
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def reset(self,title='',text=''):
        self.logic.reset (text  = text
                         ,title = title
                         )
        self.update(self.logic._text)
        self.title()
    
    def title(self):
        self.gui.title(self.logic._title)
    
    def icon(self):
        f = '[shared] shared.MessageBuilder.icon'
        if self.logic._icon and os.path.exists(self.logic._icon):
            self.gui.icon(self.logic._icon)
        else:
            com.empty(f)

    def image(self,event=None):
        f = '[shared] shared.MessageBuilder.image'
        if self.logic._icon and os.path.exists(self.logic._icon):
            iimage = self.gui.image (path = self.logic._icon
                                    ,obj  = self.frm_tpl
                                    )
            ''' We need to assign self.variable to Label, otherwise,
                it gets destroyed.
            '''
            self.lbl_img = Label (parent = self.frm_tpl
                                 ,image  = iimage
                                 )
        else:
            com.empty(f)



class Message:

    def __init__(self,func,message,Silent=False):
        self.func    = func
        self.message = message
        self.Silent  = Silent

    def debug(self):
        if GUI_MES and not self.Silent:
            objs.debug().reset (title = self.func
                               ,text  = self.message
                               )
            objs._debug.show()
        # Duplicate the message to the console
        lg.Message (func    = self.func
                   ,message = self.message
                   ).debug()
    
    def error(self):
        if GUI_MES and not self.Silent:
            objs.error().reset (title = self.func
                               ,text  = self.message
                               )
            objs._error.show()
        # Duplicate the message to the console
        lg.Message (func    = self.func
                   ,message = self.message
                   ).error()

    def info(self):
        if GUI_MES and not self.Silent:
            objs.info().reset (title = self.func
                              ,text  = self.message
                              )
            objs._info.show()
        # Duplicate the message to the console
        lg.Message (func    = self.func
                   ,message = self.message
                   ).info()
                       
    def warning(self):
        if GUI_MES and not self.Silent:
            objs.warning().reset (title = self.func
                                 ,text  = self.message
                                 )
            objs._warning.show()
        # Duplicate the message to the console
        lg.Message (func    = self.func
                   ,message = self.message
                   ).warning()

    def question(self):
        if GUI_MES and not self.Silent:
            objs.question().reset (title = self.func
                                  ,text  = self.message
                                  )
            objs._question.show()
            lg.log.append (self.func
                          ,_('QUESTION')
                          ,self.message
                          )
            answer = objs._question.ask()
            lg.Message (func    = self.func
                       ,message = str(answer)
                       ).debug()
            return answer
        else:
            return lg.Message (func    = self.func
                              ,message = self.message
                              ).question()



class Commands(lg.Commands):
    
    def __init__(self):
        super().__init__()
    
    def mod_color(self,color,delta=76): # ~30%
        ''' Make a color (a color name (/usr/share/X11/rgb.txt) or
            a hex value) brighter (positive delta) or darker
            (negative delta).
        '''
        f = '[shared] shared.Commands.mod_color'
        if -255 <= delta <= 255:
            rgb = gi.com.mod_color(color)
            if rgb:
                return lg.com.mod_color(rgb,delta)
            else:
                mes = _('An unknown color "{}"!').format(color)
                objs.mes(f,mes).error()
        else:
            sub = '-255 <= {} <= 255'.format(delta)
            mes = _('The condition "{}" is not observed!').format(sub)
            objs.mes(f,mes).warning()
    
    def fast_txt(self,text):
        objs.txt().reset()
        objs._txt.insert(text)
        objs._txt.show()
    
    def dialog_save_file(self,types=()):
        f = '[shared] shared.Commands.dialog_save_file'
        options = lg.com.dialog_save_file()
        try:
            file = gi.com.dialog_save_file(options)
        except:
            file = ''
            mes = _('Failed to select a file!')
            objs.mes(f,mes).error()
        return file
    
    def bind(self,obj,bindings,action):
        ''' Bind keyboard or mouse keys to an action
            Input: object, str/list, function
        '''
        f = '[shared] shared.Commands.bind'
        if hasattr(obj,'widget'):
            if isinstance(bindings,str) or isinstance(bindings,list) \
            or isinstance(bindings,tuple):
                if isinstance(bindings,str):
                    bindings = [bindings]
                for binding in bindings:
                    if not gi.com.bind(obj,binding,action):
                        mes = _('Failed to enable key combination "{}"!')
                        mes = mes.format(binding)
                        objs.mes(f,mes,True).error()
            else:
                mes = _('Wrong input data: "{}"').format(bindings)
                objs.mes(f,mes,True).error()
        else:
            mes = _('Wrong input data!')
            objs.mes(f,mes,True).error()
    
    def start(self):
        gi.objs.start()
    
    def end(self):
        gi.objs.end()



class Font:
    
    def __init__(self,name,xborder=20,yborder=20):
        self._font = None
        self.gui   = gi.Font()
        self.logic = lg.Font (name    = name
                             ,xborder = xborder
                             ,yborder = yborder
                             )
    
    def reset(self,name,xborder=20,yborder=20):
        self.logic.reset (name    = name
                         ,xborder = xborder
                         ,yborder = yborder
                         )
    
    def set_text(self,text):
        self.logic.set_text(text)
    
    def font(self):
        f = '[shared] shared.Font.font'
        if not self._font:
            if self.logic._family and self.logic._size:
                self._font = self.gui.font (family = self.logic._family
                                           ,size   = self.logic._size
                                           )
            else:
                com.empty(f)
        return self._font
    
    def height(self):
        f = '[shared] shared.Font.height'
        if not self.logic._height:
            if self.font():
                try:
                    self.logic._height = self.gui.height(self._font)
                except Exception as e:
                    objs.mes(f,str(e),True).error()
                self.logic.height()
            else:
                com.empty(f)
        return self.logic._height
    
    def width(self):
        f = '[shared] shared.Font.width'
        if not self.logic._width:
            if self.font() and self.logic._text:
                try:
                    max_line = sorted (self.logic._text.splitlines()
                                      ,key     = len
                                      ,reverse = True
                                      )[0]
                    self.logic._width = self.gui.width (font     = self._font
                                                       ,max_line = max_line
                                                       )
                except Exception as e:
                    objs.mes(f,str(e),True).error()
                self.logic.width()
            else:
                com.empty(f)
        return self.logic._width


com  = Commands()
objs = Objects()
# Use GUI dialogs for logic-only modules
lg.objs._mes = Message


if __name__ == '__main__':
    f = '[shared] shared.__main__'
    com.start()
    lg.ReadTextFile('/tmp/aaa').get()
    com.end()
