#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys, os
import tkinter            as tk
import tkinter.filedialog as dialog
import tkinter.ttk        as ttk
import shared             as sh

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','../resources/locale')


# Привязать горячие клавиши или кнопки мыши к действию
# object, str/list, function
def bind(obj,bindings,action):
    f = '[shared] sharedGUI.bind'
    if hasattr(obj,'widget'):
        if isinstance(bindings,str) or isinstance(bindings,list):
            if isinstance(bindings,str):
                bindings = [bindings]
            for binding in bindings:
                try:
                    obj.widget.bind(binding,action)
                except tk.TclError:
                    Message (f,_('ERROR')
                            ,_('Failed to enable key combination "%s"!')\
                            % binding
                            )
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data: "%s"') \
                    % str(bindings)
                    )
    else:
        Message (f,_('ERROR')
                ,_('Wrong input data!')
                )

def dialog_save_file(filetypes=()):
    f = '[shared] sharedGUI.dialog_save_file'
    file = ''
    if not filetypes:
        filetypes = ((_('Plain text (UTF-8)'),'.txt' )
                    ,( _('Web-page')         ,'.htm' )
                    ,( _('Web-page')         ,'.html')
                    ,( _('All files')        ,'*'    )
                    )
    options                = {}
    options['initialfile'] = ''
    options['filetypes']   = filetypes
    options['title']       = _('Save As:')
    try:
        file = dialog.asksaveasfilename(**options)
    except:
        Message (f,_('ERROR')
                ,_('Failed to select a file!')
                )
    return file
    
def mod_color(color,delta=76): # ~30%
    ''' Make a color (a color name (/usr/share/X11/rgb.txt) or
        a hex value) brighter (positive delta) or darker
        (negative delta).
    '''
    f = '[shared] sharedGUI.mod_color'
    if -255 <= delta <= 255:
        try:
            rgb = objs.root().widget.winfo_rgb(color=color)
            rgb = list(max(min(255,x/256+delta),0) for x in rgb)
            # We need to have integers here. I had a float once.
            rgb = tuple(int(item) for item in rgb)
            return '#%02x%02x%02x' % rgb
        except tk._tkinter.TclError:
            Message (f,_('WARNING')
                    ,_('An unknown color "%s"!') % str(color)
                    )
    else:
        Message (f,_('WARNING')
                ,_('The condition "%s" is not observed!') \
                % ('-255 <= %d <= 255' % delta)
                )



class Root:

    def __init__(self):
        self.type = 'Root'
        self.widget = tk.Tk()

    def idle(self):
        self.widget.update_idletasks()
    
    def run(self):
        self.widget.mainloop()

    def show(self):
        self.widget.deiconify()

    def close(self):
        self.widget.withdraw()

    def destroy(self):
        self.kill()

    def kill(self):
        self.widget.destroy()

    def update(self):
        self.widget.update()
        
    def wait(self):
        self.widget.wait_window()



# Do not use graphical logging there
class WidgetShared:
    
    def disable(object):
        object.widget.config(state='disabled')
    
    def enable(object):
        object.widget.config(state='normal')
    
    def focus(object,event=None):
        object.widget.focus()

    def insert(object,text,pos):
        f = '[shared] sharedGUI.WidgetShared.insert'
        # Do not allow None
        if text:
            if object.type == 'TextBox' or object.type == 'Entry':
                try:
                    object.widget.insert(pos,text)
                except tk.TclError:
                    try:
                        object.widget.insert (pos
                                             ,_('Failed to insert the text!')
                                             )
                    except tk.TclError:
                        sh.log.append (f,_('ERROR')
                                      ,_('Failed to insert the text!')
                                      )
            else:
                sh.log.append (f,_('ERROR')
                              ,_('A logic error: unknown object type: "%s"!') \
                              % str(object.type)
                              )
        # Too frequent
        '''
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        '''

    # font_style, sh.globs['var']['menu_font']
    def font(object,font='Sans 11'):
        f = '[shared] sharedGUI.WidgetShared.font'
        if object.type == 'TextBox' or object.type == 'Entry':
            object.widget.config(font=font)
        else:
            sh.log.append (f,_('ERROR')
                          ,_('A logic error: unknown object type: "%s"!')\
                          % str(object.type)
                          )

    def set_state(object,ReadOnly=False):
        f = '[shared] sharedGUI.WidgetShared.set_state'
        if object.type == 'TextBox' or object.type == 'Entry':
            if ReadOnly:
                object.widget.config(state='disabled')
                object.state = 'disabled'
            else:
                object.widget.config(state='normal')
                object.state = 'normal'
        else:
            sh.log.append (f,_('ERROR')
                          ,_('A logic error: unknown object type: "%s"!')\
                          % str(object.type)
                          )

    # Родительский виджет
    def title(object,text=_('Text:'),my_program_title=''):
        f = '[shared] sharedGUI.WidgetShared.title'
        if object.type == 'Toplevel' or object.type == 'Root':
            object.widget.title(text + my_program_title)
        else:
            sh.log.append (f,_('ERROR')
                          ,_('A logic error: unknown object type: "%s"!')\
                          % str(object.type)
                          )

    def custom_buttons(object):
        f = '[shared] sharedGUI.WidgetShared.custom_buttons'
        if not object.Composite:
            if object.parent.type == 'Toplevel' \
            or object.parent.type == 'Root':
                if object.state == 'disabled':
                    object.parent.close_button.widget.config(text=_('Quit'))
                else:
                    object.parent.close_button.widget.config(text=_('Save and close'))
            else:
                sh.log.append (f,_('ERROR')
                              ,_('A logic error: unknown object type: "%s"!')\
                              % str(object.type)
                              )

    # Parent widget
    def icon(object,file):
        f = '[shared] sharedGUI.WidgetShared.icon'
        if object.type == 'Toplevel' or object.type == 'Root':
            if file and os.path.exists(file):
                object.widget.tk.call ('wm','iconphoto'
                                      ,object.widget._w
                                      ,tk.PhotoImage (master = object.widget
                                                     ,file   = file
                                                     )
                                      )
            else:
                sh.log.append (f,_('ERROR')
                              ,_('File "%s" has not been found!') \
                              % str(file)
                              )
        else:
            sh.log.append (f,_('ERROR')
                          ,_('A logic error: unknown object type: "%s"!')\
                          % str(object.type)
                          )



class Top:

    def __init__(self,parent,Maximize=False,AutoCenter=True):
        self.values()
        self.parent     = parent
        self.AutoCenter = AutoCenter
        self.widget     = tk.Toplevel(self.parent.widget)
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
        if Maximize:
            Geometry(parent=self).maximize()
        self.tk_trigger = tk.BooleanVar()
        
    def values(self):
        self.type  = 'Toplevel'
        ''' Lock = True - блокировать дальнейшее выполнение программы до
            попытки закрытия виджета. Lock = False позволяет создать
            одновременно несколько виджетов на экране. Они будут
            работать, однако, виджет с Lock = False будет закрыт при
            закрытии виджета с Lock = True. Кроме того, если ни один из
            виджетов не имеет Lock = True, то они все будут показаны и
            тут же закрыты.
        '''
        self.Lock  = False
        self.count = 0

    def close(self,event=None):
        self.widget.withdraw()
        if self.Lock:
            self.tk_trigger.set(True)

    def show(self,Lock=True):
        self.count += 1
        self.widget.deiconify()
        ''' Changing geometry at a wrong time may prevent frames from
            autoresizing after 'pack_forget'.
        '''
        if self.AutoCenter:
            self.center()
        self.Lock = Lock
        if self.Lock:
            self.tk_trigger = tk.BooleanVar()
            self.widget.wait_variable(self.tk_trigger)

    def title(self,text=_('Title:')):
        WidgetShared.title(self,text=text)

    def icon(self,path):
        WidgetShared.icon(self,path)

    def resolution(self):
        self.widget.update_idletasks()
        return (self.widget.winfo_screenwidth()
               ,self.widget.winfo_screenheight()
               )

    #todo: not centers without Force=True when Lock=False
    def center(self,Force=False):
        ''' Make child widget always centered at the first time and up
            to a user's choice any other time (if the widget is reused).
            Only 'tk.Tk' and 'tk.Toplevel' types are supported.
        '''
        if self.count == 1 or Force:
            width, height = self.resolution()
            size = tuple(int(item) for item \
                   in self.widget.geometry().split('+')[0].split('x'))
            x = width/2 - size[0]/2
            y = height/2 - size[1]/2
            self.widget.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def focus(self,event=None):
        self.widget.focus_set()



class SearchBox:
    ''' #todo (?): fix: if duplicate spaces/line breaks are not deleted,
        text with and without punctuation will have a different number
        of words; thus, tkinter will be supplied wrong positions upon
        Search.
    '''
    def __init__(self,obj):
        self.type    = 'SearchBox'
        self.obj     = obj
        self.parent  = self.obj.parent
        h_top        = Top(self.parent)
        self.h_entry = Entry(h_top)
        self.h_entry.title(text=_('Find:'))
        self.h_entry.close()
        self.h_sel   = Selection(self.obj)

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
            self.h_sel.reset_logic(words=self.words)
            self.h_search = sh.Search(text=self._text)
        else:
            self.Success = False

    def reset_data(self):
        f = '[shared] sharedGUI.SearchBox.reset_data'
        self.Success    = True
        self._prev_loop = self._next_loop = self._search = self._pos1 \
                        = self._pos2 = None
        self.i          = 0
        self.search()
        if self._text and self._search:
            self.h_search.reset(text=self._text,search=self._search)
            self.h_search.next_loop()
            # Prevents from calling self.search() once again
            if not self.h_search._next_loop:
                Message (f,_('INFO')
                        ,_('No matches!')
                        )
                self.Success = False
        else:
            self.Success = False
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def reset(self,mode='data',words=None,Strict=False):
        if mode == 'data':
            self.reset_data()
        else:
            self.reset_logic(words=words,Strict=Strict)

    def loop(self):
        f = '[shared] sharedGUI.SearchBox.loop'
        if self.Success:
            if not self.h_search._next_loop:
                self.reset()
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        return self.h_search._next_loop

    def add(self):
        f = '[shared] sharedGUI.SearchBox.add'
        if self.Success:
            if self.i < len(self.loop()) - 1:
                self.i += 1
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def subtract(self):
        f = '[shared] sharedGUI.SearchBox.subtract'
        if self.Success:
            if self.i > 0:
                self.i -= 1
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def new(self,event=None):
        self.reset_data()
        self.next()

    def select(self):
        f = '[shared] sharedGUI.SearchBox.select'
        if self.Success:
            if self.Strict:
                result1 = self.words.no_by_pos_p(pos=self.pos1())
                result2 = self.words.no_by_pos_p(pos=self.pos2())
            else:
                result1 = self.words.no_by_pos_n(pos=self.pos1())
                result2 = self.words.no_by_pos_n(pos=self.pos2())
            if result1 is None or result2 is None:
                sh.log.append (f,_('ERROR')
                              ,_('Wrong input data!')
                              )
            else:
                _pos1tk = self.words.words[result1].tf()
                _pos2tk = self.words.words[result2].tl()
                self.h_sel.reset (pos1tk     = _pos1tk
                                 ,pos2tk     = _pos2tk
                                 ,background = 'green2'
                                 )
                self.h_sel.set()
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def search(self):
        f = '[shared] sharedGUI.SearchBox.search'
        if self.Success:
            if self.words and not self._search:
                self.h_entry.focus()
                self.h_entry.select_all()
                self.h_entry.show()
                self._search = self.h_entry.get()
                if self._search and not self.Strict:
                    self._search = sh.Text (text = self._search
                                           ,Auto = False
                                           ).delete_punctuation()
                    self._search = sh.Text (text = self._search
                                           ,Auto = False
                                           ).delete_duplicate_spaces()
                    self._search = self._search.lower()
            return self._search
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def next(self,event=None):
        f = '[shared] sharedGUI.SearchBox.next'
        if self.Success:
            _loop = self.loop()
            if _loop:
                old_i = self.i
                self.add()
                if old_i == self.i:
                    if len(_loop) == 1:
                        Message (f,_('INFO')
                                ,_('Only one match has been found!')
                                )
                    else:
                        Message (f,_('INFO')
                                ,_('No more matches, continuing from the top!')
                                )
                        self.i = 0
                self.select()
            else:
                Message (f,_('INFO')
                        ,_('No matches!')
                        )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def prev(self,event=None):
        f = '[shared] sharedGUI.SearchBox.prev'
        if self.Success:
            _loop = self.loop()
            if _loop:
                old_i = self.i
                self.subtract()
                if old_i == self.i:
                    if len(_loop) == 1:
                        Message (f,_('INFO')
                                ,_('Only one match has been found!')
                                )
                    else:
                        Message (f,_('INFO')
                                ,_('No more matches, continuing from the bottom!')
                                )
                        # Not just -1
                        self.i = len(_loop) - 1
                self.select()
            else:
                Message (f,_('INFO')
                        ,_('No matches!')
                        )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def pos1(self):
        f = '[shared] sharedGUI.SearchBox.pos1'
        if self.Success:
            if self._pos1 is None:
                self.loop()
                self.i = 0
            _loop = self.loop()
            if _loop:
                self._pos1 = _loop[self.i]
            return self._pos1
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def pos2(self):
        f = '[shared] sharedGUI.SearchBox.pos2'
        if self.Success:
            if self.pos1() is not None:
                self._pos2 = self._pos1 + len(self.search())
            return self._pos2
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



class TextBox:

    def __init__ (self,parent,Composite=False
                 ,expand=1,side=None,fill='both'
                 ,words=None,font='Serif 14'
                 ,ScrollX=False,ScrollY=True
                 ,SpecialReturn=True,state='normal'
                 ):
        self.type      = 'TextBox'
        self.Composite = Composite
        self.ScrollX   = ScrollX
        self.ScrollY   = ScrollY
        self.font      = font
        ''' 'normal'   - обычный режим
            'disabled' - отключить редактирование
            выберите 'disabled', чтобы надпись на кнопке была другой
        '''
        self.state     = state
        self.SpecialReturn = SpecialReturn
        ''' (optional, external) Prevent resetting the active (already
            shown) widget
        '''
        self.Active    = False
        self.Save      = False
        self.tags      = []
        self.marks     = []
        self.parent    = parent
        self.expand    = expand
        self.side      = side
        self.fill      = fill
        self.selection = Selection(h_widget=self)
        self.gui()
        self.reset_logic(words=words)
        if not self.Composite:
            self.focus()

    def _gui_txt(self):
        if self.parent.type in ('Root','Toplevel'):
            self.widget = tk.Text (master = self.parent.widget
                                  ,font   = self.font
                                  ,wrap   = 'word'
                                  ,height = 1
                                  )
        else:
            self.widget = tk.Text (master = self.parent.widget
                                  ,font   = self.font
                                  ,wrap   = 'word'
                                  )
        self.widget.pack (expand = self.expand
                         ,fill   = self.fill
                         ,side   = self.side
                         )

    def _gui_scroll_hor(self):
        frame = Frame (parent = self.parent
                      ,expand = 0
                      ,fill   = 'x'
                      ,side   = 'top'
                      )
        self.scrollbar_hor = tk.Scrollbar (master    = frame.widget
                                          ,orient    = tk.HORIZONTAL
                                          ,jump      = 0
                                          ,takefocus = False
                                          )
        self.widget.config(xscrollcommand=self.scrollbar_hor.set)
        self.scrollbar_hor.config(command=self.widget.xview)
        self.scrollbar_hor.pack(expand=1,fill='x')

    def _gui_scroll_ver(self):
        self.scrollbar = tk.Scrollbar (master    = self.widget
                                      ,jump      = 0
                                      ,takefocus = False
                                      )
        self.widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.widget.yview)
        self.scrollbar.pack(side='right',fill='y')

    def gui(self):
        self._gui_txt()
        if self.ScrollY:
            self._gui_scroll_ver()
        if self.ScrollX:
            self._gui_scroll_hor()
        if not self.Composite and \
           not hasattr(self.parent,'close_button'):
            if self.parent.type == 'Toplevel' \
            or self.parent.type == 'Root':
                self.parent.close_button = \
                Button (parent = self.parent
                       ,text   = _('Quit')
                       ,hint   = _('Quit')
                       ,action = self.close
                       ,expand = 0
                       ,side   = 'bottom'
                       )
        self.search_box = SearchBox(self)
        WidgetShared.custom_buttons(self)
        self.bindings()

    def reset(self,words=None):
        self.reset_data()
        self.reset_logic(words=words)

    def reset_logic(self,words=None):
        self.words = words
        self.search_box.reset_logic(words=self.words)
        self.selection.reset_data()
        self.selection.reset_logic(words=self.words)

    # Delete text, tags, marks
    def reset_data(self,event=None):
        self.clear_text()
        self.clear_tags()
        self.clear_marks()

    def read_only(self,ReadOnly=True):
        ''' Setting ReadOnly state works only after filling text.
            Only tk.Text, tk.Entry and not tk.Toplevel are supported.
        '''
        WidgetShared.set_state(self,ReadOnly=ReadOnly)

    def show(self):
        self.Active = True
        self.parent.show()

    def close(self,event=None):
        self.Save   = True
        self.Active = False
        self.parent.close()
        return 'break'

    def bindings(self):
        bind (obj      = self
             ,bindings = ['<Control-f>','<Control-F3>']
             ,action   = self.search_box.new
             )
        bind (obj      = self
             ,bindings = '<F3>'
             ,action   = self.search_box.next
             )
        bind (obj      = self
             ,bindings = '<Shift-F3>'
             ,action   = self.search_box.prev
             )
        # Только для несоставных виджетов
        if not self.Composite:
            self.widget.unbind('<Return>')
            if self.state == 'disabled' or self.SpecialReturn:
                ''' Разрешать считывать текст после нажатия Escape
                    (в Entry запрещено)
                '''
                bind (obj      = self.parent
                     ,bindings = ['<Return>','<KP_Enter>','<Escape>']
                     ,action   = self.close
                     )
                ''' We need to bind 'Return' to the widget anyway even
                    if we have already bound this to 'parent',
                    because we need to return 'break'
                '''
                bind (obj      = self
                     ,bindings = ['<Return>','<KP_Enter>']
                     ,action   = self.close
                     )
            else:
                bind (obj      = self.parent
                     ,bindings = '<Escape>'
                     ,action   = self.close
                     )
        bind (obj      = self
             ,bindings = '<Control-a>'
             ,action   = self.select_all
             )
        bind (obj      = self
             ,bindings = '<Control-v>'
             ,action   = self.insert_clipboard
             )
        bind (obj      = self
             ,bindings = '<Key>'
             ,action   = self.clear_on_key
             )
        bind (obj      = self
             ,bindings = '<Control-Alt-u>'
             ,action   = self.toggle_case
             )
        if hasattr(self.parent,'type') \
            and self.parent.type == 'Toplevel':
            self.parent.widget.protocol ("WM_DELETE_WINDOW"
                                            ,self.close
                                            )

    def toggle_case(self,event=None):
        f = '[shared] sharedGUI.TextBox.toggle_case'
        text = sh.Text(text=self.selection.text()).toggle_case()
        pos1, pos2 = self.selection.get()
        self.clear_selection()
        self.insert(text=text,pos=self.cursor(),MoveTop=0)
        if pos1 and pos2:
            self.selection.reset (pos1tk     = pos1
                                 ,pos2tk     = pos2
                                 ,tag        = 'sel'
                                 ,background = 'gray'
                                 )
            self.selection.set(DeletePrevious=0,AutoScroll=0)
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        return 'break'

    def _get(self):
        f = '[shared] sharedGUI.TextBox._get'
        try:
            return self.widget.get('1.0','end')
        except tk._tkinter.TclError:
            # Do not use GUI
            sh.log.append (f,_('WARNING')
                          ,_('The parent has already been destroyed.')
                          )

    def get(self,Strip=True):
        result = self._get()
        if result:
            if Strip:
                return result.strip()
            else:
                return result.strip('\n')

    def insert(self,text='text',pos='1.0',MoveTop=True):
        WidgetShared.insert(self,text=text,pos=pos)
        if MoveTop:
            # Move to the beginning
            self.mark_add()
        else:
            self.scroll(mark='insert')

    def insert_clipboard(self,event=None):
        ''' Fix (probable) Tkinter bug(s) after pressing '<Control-v>':
            1) Fix weird scrolling
            2) Delete selected text before pasting
        '''
        self.clear_selection()
        # For some reason, 'self.insert' does not work here with 'break'
        #self.insert(text=Clipboard().paste(),MoveTop=False)
        self.widget.insert(self.cursor(),Clipboard().paste())
        return 'break'

    def select_all(self,event=None):
        self.tag_add()
        self.mark_add()
        return 'break'

    def _tag_remove(self,tag_name='sel',pos1tk='1.0',pos2tk='end'):
        f = '[shared] sharedGUI.TextBox._tag_remove'
        try:
            self.widget.tag_remove(tag_name,pos1tk,pos2tk)
        except tk.TclError:
            sh.log.append (f,_('WARNING')
                          ,_('Failed to remove the tag %s in the widget %s in positions %s-%s!')\
                          % (tag_name,str(widget),pos1tk,pos2tk)
                          )

    #todo: simplify
    def tag_remove(self,tag_name='sel',pos1tk='1.0',pos2tk='end'):
        f = '[shared] sharedGUI.TextBox.tag_remove'
        self._tag_remove(tag_name=tag_name,pos1tk=pos1tk,pos2tk=pos2tk)
        if self.tags:
            try:
                self.tags.remove(tag_name)
            except ValueError:
                #todo: Что тут не работает?
                sh.log.append (f,_('DEBUG-ERROR')
                              ,_('Element "%s" has not been found in fragment "%s"!')\
                              % (tag_name,str(self.tags))
                              )

    # Tk.Entry не поддерживает тэги и метки
    def tag_add (self,tag_name='sel',pos1tk='1.0'
                ,pos2tk='end',DeletePrevious=True
                ):
        f = '[shared] sharedGUI.TextBox.tag_add'
        if DeletePrevious:
            self.tag_remove(tag_name)
        try:
            self.widget.tag_add(tag_name,pos1tk,pos2tk)
        except tk.TclError:
            sh.log.append (f,_('ERROR')
                          ,_('Failed to add tag "%s" for positions %s-%s!')\
                          % (tag_name,pos1tk,pos2tk)
                          )
        self.tags.append(tag_name)

    def tag_config (self,tag_name='sel',background=None
                   ,foreground=None,font=None):
        f = '[shared] sharedGUI.TextBox.tag_config'
        if background:
            try:
                self.widget.tag_config(tag_name,background=background)
            except tk.TclError:
                sh.log.append (f,_('ERROR')
                              ,_('Failed to configure tag "%s" to have the background of color "%s"!')\
                              % (str(tag_name),str(background))
                              )
        if foreground:
            try:
                self.widget.tag_config(tag_name,foreground=foreground)
            except tk.TclError:
                sh.log.append (f,_('ERROR')
                              ,_('Failed to configure tag "%s" to have the foreground of color "%s"!')\
                              % (str(tag_name),str(foreground))
                              )
        if font:
            try:
                self.widget.tag_config(tag_name,font=font)
            except tk.TclError:
                sh.log.append (f,_('ERROR')
                              ,_('Failed to configure tag "%s" to have the font "%s"!')\
                              % (str(tag_name),str(font))
                              )

    # Tk.Entry не поддерживает тэги и метки
    def mark_add(self,mark_name='insert',postk='1.0'):
        f = '[shared] sharedGUI.TextBox.mark_add'
        try:
            self.widget.mark_set(mark_name,postk)
            '''
            sh.log.append (f,_('DEBUG')
                          ,_('Mark "%s" has been inserted in position "%s".')\
                          % (mark_name,postk)
                          )
            '''
        except tk.TclError:
            sh.log.append (f,_('ERROR')
                          ,_('Failed to insert mark "%s" in position "%s"!')\
                          % (mark_name,postk)
                          )
        self.marks.append(mark_name)

    def mark_remove(self,mark_name='insert'):
        f = '[shared] sharedGUI.TextBox.mark_remove'
        try:
            self.widget.mark_unset(mark_name)
            '''
            sh.log.append (f,_('DEBUG')
                          ,_('Mark "%s" has been removed.') % (mark_name)
                          )
            '''
        except tk.TclError:
            sh.log.append (f,_('ERROR')
                          ,_('Failed to remove mark "%s"!') % mark_name
                          )
        try:
            self.marks.remove(mark_name)
        except ValueError:
            sh.log.append (f,_('ERROR')
                          ,_('Element "%s" has not been found in fragment "%s"!')\
                          % (mark_name,str(self.marks))
                          )

    def clear_text(self,pos1='1.0',pos2='end'):
        f = '[shared] sharedGUI.TextBox.clear_text'
        try:
            self.widget.delete(pos1,pos2)
        except tk._tkinter.TclError:
            # Do not use GUI
            sh.log.append (f,_('WARNING')
                          ,_('The parent has already been destroyed.')
                          )

    #fix Tkinter limitations
    def clear_on_key(self,event=None):
        if event and event.char:
            if event.char.isspace() or event.char in sh.lat_alphabet \
            or event.char in sh.ru_alphabet or event.char in sh.digits \
            or event.char in sh.punc_array or event.char \
            in sh.punc_ext_array:
                ''' #todo: suppress excessive logging (Selection.get,
                    TextBox.clear_selection, TextBox.cursor,
                    Clipboard.paste, Words.no_by_tk)
                '''
                self.clear_selection()

    def clear_selection(self,event=None):
        f = '[shared] sharedGUI.TextBox.clear_selection'
        pos1tk, pos2tk = self.selection.get()
        if pos1tk and pos2tk:
            self.clear_text(pos1=pos1tk,pos2=pos2tk)
            return 'break'
        # Too frequent
        '''
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        '''

    def clear_tags(self):
        i = len(self.tags) - 1
        while i >= 0:
            self.tag_remove(self.tags[i])
            i -= 1

    def clear_marks(self):
        i = len(self.marks) - 1
        while i >= 0:
            self.mark_remove(self.marks[i])
            i -= 1

    def goto(self,GoTo=''):
        f = '[shared] sharedGUI.TextBox.goto'
        if GoTo:
            try:
                goto_pos = self.widget.search(GoTo,'1.0','end')
                self.mark_add('goto',goto_pos)
                self.mark_add('insert',goto_pos)
                self.widget.yview('goto')
            except:
                sh.log.append (f,_('ERROR')
                              ,_('Failed to shift screen to label "%s"!')\
                              % 'goto'
                              )

    # Scroll screen to a tkinter position or a mark (tags do not work)
    def scroll(self,mark):
        f = '[shared] sharedGUI.TextBox.scroll'
        try:
            self.widget.yview(mark)
        except tk.TclError:
            sh.log.append (f,_('WARNING')
                          ,_('Failed to shift screen to label "%s"!') \
                          % str(mark)
                          )

    def autoscroll(self,mark='1.0'):
        ''' Scroll screen to a tkinter position or a mark if they
            are not visible (tags do not work).
        '''
        if not self.visible(mark):
            self.scroll(mark)

    #todo: select either 'see' or 'autoscroll'
    def see(self,mark):
        f = '[shared] sharedGUI.TextBox.see'
        if mark is None:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        else:
            self.widget.see(mark)

    def title(self,text=_('Title:')):
        WidgetShared.title(self.parent,text)

    def icon(self,path):
        WidgetShared.icon(self.parent,path)

    def visible(self,tk_pos):
        if self.widget.bbox(tk_pos):
            return True

    def cursor(self,event=None):
        f = '[shared] sharedGUI.TextBox.cursor'
        try:
            self._pos = self.widget.index('insert')
            sh.log.append (f,_('DEBUG')
                          ,_('Got position: "%s"') % str(self._pos)
                          )
        except tk.TclError:
            self._pos = '1.0'
            sh.log.append (f,_('WARNING')
                          ,_('Cannot return a cursor position!')
                          )
        return self._pos

    def focus_set(self,event=None):
        self.focus()

    def focus(self,event=None):
        self.widget.focus_set()

    def spelling(self):
        ''' Tags can be marked only after text in inserted; thus, call
            this procedure separately before '.show'.
        '''
        f = '[shared] sharedGUI.TextBox.spelling'
        if self.words:
            self.words.sent_nos()
            result = []
            for i in range(self.words.len()):
                if not self.words.words[i].spell_ru():
                    result.append(i)
            if result:
                self.clear_tags()
                for i in range(len(result)):
                    no = self.words._no = result[i]
                    pos1tk = self.words.words[no].tf()
                    pos2tk = self.words.words[no].tl()
                    #todo: apply IGNORE_SPELLING
                    if pos1tk and pos2tk:
                        self.tag_add (tag_name       = 'spell'
                                     ,pos1tk         = pos1tk
                                     ,pos2tk         = pos2tk
                                     ,DeletePrevious = False
                                     )
                sh.log.append (f,_('DEBUG')
                              ,_('%d tags to assign') % len(result)
                              )
                self.tag_config(tag_name='spell',background='red')
            else:
                sh.log.append (f,_('INFO')
                              ,_('Spelling seems to be correct.')
                              )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Not enough input data!')
                          )



class Entry:

    def __init__(self,parent,Composite=False
                ,side=None,ipadx=None,ipady=None
                ,fill=None,width=None,expand=None
                ,font='Sans 11',bg=None,fg=None
                ):
        self.type      = 'Entry'
        self.Composite = Composite
        # 'disabled' - disable editing
        self.state     = 'normal'
        self.Save      = False
        self.parent    = parent
        self.widget    = tk.Entry (master = self.parent.widget
                                  ,font   = font
                                  ,bg     = bg
                                  ,fg     = fg
                                  ,width  = width
                                  )
        bind (obj      = self
             ,bindings = '<Control-a>'
             ,action   = self.select_all
             )
        self.widget.pack (side   = side
                         ,ipadx  = ipadx
                         ,ipady  = ipady
                         ,fill   = fill
                         ,expand = expand
                         )
        if not self.Composite:
            # Parent widget type can be any
            if not hasattr(self.parent,'close_button'):
                self.parent.close_button = Button (parent = self.parent
                                                  ,text   = _('Quit')
                                                  ,hint   = _('Quit')
                                                  ,action = self.close
                                                  ,expand = 0
                                                  ,side   = 'bottom'
                                                  )
            WidgetShared.custom_buttons(self)
        self.bindings()

    def read_only(self,ReadOnly=True):
        ''' Setting ReadOnly state works only after filling text. Only
            tk.Text, tk.Entry and not tk.Toplevel are supported.
        '''
        WidgetShared.set_state(self,ReadOnly=ReadOnly)

    def bindings(self):
        if self.Composite:
            self.clear_text()
        else:
            bind (obj      = self
                 ,bindings = ['<Return>','<KP_Enter>']
                 ,action   = self.close
                 )
            bind (obj      = self
                 ,bindings = '<Escape>'
                 ,action   = self.parent.close
                 )

    def show(self,event=None):
        self.parent.show()

    def close(self,event=None):
        self.Save = True
        self.parent.close()

    def _get(self):
        f = '[shared] sharedGUI.Entry._get'
        try:
            return self.widget.get()
        except tk._tkinter.TclError:
            # Do not use GUI
            sh.log.append (f,_('WARNING')
                          ,_('The parent has already been destroyed.')
                          )

    def get(self,Strip=False):
        f = '[shared] sharedGUI.Entry.get'
        # None != 'None' != ''
        result = sh.Input (title = f
                          ,value = self._get()
                          ).not_none()
        if Strip:
            return result.strip()
        else:
            return result.strip('\n')

    def insert(self,text='text',pos=0):
        WidgetShared.insert(self,text=text,pos=pos)

    def select_all(self,event=None):
        self.widget.select_clear()
        self.widget.select_range(0,'end')
        return 'break'

    def clear_text(self,event=None,pos1=0,pos2='end'):
        f = '[shared] sharedGUI.Entry.clear_text'
        try:
            self.widget.selection_clear()
            self.widget.delete(pos1,pos2)
        except tk._tkinter.TclError:
            # Do not use GUI
            sh.log.append (f,_('WARNING')
                          ,_('The parent has already been destroyed.')
                          )

    def icon(self,path):
        WidgetShared.icon(self.parent,path)

    def title(self,text='Title:'):
        WidgetShared.title(self.parent,text)

    def focus_set(self,event=None):
        self.focus()
        # Manual Tab focus (left to right widget)
        return 'break'

    def focus(self,event=None):
        self.widget.focus_set()
        # Manual Tab focus (left to right widget)
        return 'break'



class Frame:

    def __init__ (self,parent,expand=1
                 ,fill='both',side=None,padx=None
                 ,pady=None,ipadx=None,ipady=None
                 ,bd=None,bg=None,width=None
                 ,height=None,propag=True
                 ):
        self.type   = 'Frame'
        self.parent = parent
        self.widget = tk.Frame (master = self.parent.widget
                               ,bd     = bd
                               ,bg     = bg
                               ,width  = width
                               ,height = height
                               )
        ''' 'pack_propagate' should be set before 'pack' to 'False'
            if you want to set widget sizes manually. 'height' and
            'width' options will not work otherwise. If there are two
            frames packed one after another, and we need to set sizes
            of the second frame, then we should apply 'pack_propagate',
            'width' and 'height' to the first frame too.
        '''
        self.widget.pack_propagate(propag)
        self.widget.pack (expand = expand
                         ,fill   = fill
                         ,side   = side
                         ,padx   = padx
                         ,pady   = pady
                         ,ipadx  = ipadx
                         ,ipady  = ipady
                         )

    def title(self,text=None):
        if text:
            self.parent.title(text)
        else:
            self.parent.title()

    def show(self):
        self.parent.show()

    def close(self):
        self.parent.close()



class Button:

    def __init__ (self
                 ,parent
                 ,action      = None
                 ,hint        = None
                 ,inactive    = None
                 ,active      = None
                 ,text        = 'Press me'
                 ,height      = 36
                 ,width       = 36
                 ,side        = 'left'
                 ,expand      = 0
                 ,bg          = None
                 ,bg_focus    = None
                 ,fg          = None
                 ,fg_focus    = None
                 ,bd          = 0
                 ,hint_delay  = 800
                 ,hint_width  = 280
                 ,hint_height = 40
                 ,hint_bg     = '#ffffe0'
                 ,hint_dir    = 'top'
                 ,hint_bwidth = 1
                 ,hint_bcolor = 'navy'
                 ,bindings    = []
                 ,fill        = 'both'
                 ,TakeFocus   = False
                 ,font        = None
                 ):
        self.Status         = False
        self.parent         = parent
        self.action         = action
        self.height         = height
        self.width          = width
        self.side           = side
        self.expand         = expand
        self.fill           = fill
        self.text           = text
        self._bindings      = bindings
        self.TakeFocus      = TakeFocus
        self.bd             = bd
        self.bg             = bg
        self.bg_focus       = bg_focus
        self.fg             = fg
        self.fg_focus       = fg_focus
        self.hint           = hint
        self.hint_delay     = hint_delay
        self.hint_width     = hint_width
        self.hint_height    = hint_height
        self.hint_bg        = hint_bg
        self.hint_dir       = hint_dir
        self.side           = side
        self.inactive_image = self.image(inactive)
        self.active_image   = self.image(active)
        self.font           = font
        self.gui()
        
    def bindings(self):
        bind (obj      = self
             ,bindings = ['<ButtonRelease-1>','<space>','<Return>'
                         ,'<KP_Enter>'
                         ]
             ,action   = self.click
             )
    
    def gui(self):
        if self.inactive_image:
            self.widget = tk.Button (master           = self.parent.widget
                                    ,image            = self.inactive_image
                                    ,height           = self.height
                                    ,width            = self.width
                                    ,bd               = self.bd
                                    ,bg               = self.bg
                                    ,fg               = self.fg
                                    ,activebackground = self.bg_focus
                                    ,activeforeground = self.fg_focus
                                    ,font             = self.font
                                    )
        else:
            ''' A text button does not require setting a default width
                and height in most cases, they are defined
                automatically. Moreover, a border should be used for
                text buttons in a majority of cases.
            '''
            self.widget = tk.Button (master           = self.parent.widget
                                    ,bd               = 1
                                    ,bg               = self.bg
                                    ,fg               = self.fg
                                    ,activebackground = self.bg_focus
                                    ,activeforeground = self.fg_focus
                                    ,font             = self.font
                                    )
        self.title(button_text=self.text)
        self.set_hint()
        self.widget.pack (expand = self.expand
                         ,side   = self.side
                         ,fill   = self.fill
                         )
        self.bindings()
        if self.TakeFocus:
            self.widget.focus_set()

    def set_hint(self):
        if self.hint:
            if self._bindings:
                self.hint_extended = self.hint + '\n' + str(self._bindings).replace('[','').replace(']','').replace('<','').replace('>','').replace("'",'')
            else:
                self.hint_extended = self.hint
            self.tip = ToolTip (obj         = self
                               ,text        = self.hint_extended
                               ,hint_delay  = self.hint_delay
                               ,hint_width  = self.hint_width
                               ,hint_height = self.hint_height
                               ,hint_bg     = self.hint_bg
                               ,hint_dir    = self.hint_dir
                               )
    
    def title(self,button_text='Press me'):
        if button_text:
            self.widget.config(text=button_text)

    def image(self,button_image_path=None):
        # Без 'file=' не сработает!
        if button_image_path and os.path.exists(button_image_path):
            button_image = tk.PhotoImage (file   = button_image_path
                                         ,master = self.parent.widget
                                         ,width  = self.width
                                         ,height = self.height
                                         )
        else:
            button_image = None
        return button_image

    def click(self,*args):
        f = '[shared] sharedGUI.Button.click'
        if self.action:
            if len(args) > 0:
                self.action(args)
            else:
                self.action()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )

    def active(self):
        if not self.Status:
            self.Status = True
            if self.active_image:
                self.widget.config(image=self.active_image)
                self.widget.flag_img = self.active_image
            #self.widget.config(text="I'm Active")

    def inactive(self):
        if self.Status:
            self.Status = False
            if self.inactive_image:
                self.widget.config(image=self.inactive_image)
                self.widget.flag_img = self.inactive_image
            #self.widget.config(text="I'm Inactive")

    def show(self):
        self.parent.show()

    def close(self):
        self.parent.close()

    def focus(self,event=None):
        self.widget.focus_set()
    
    def enable(self):
        WidgetShared.enable(self)
    
    def disable(self):
        WidgetShared.disable(self)



# Pop-up tips; see also 'calltips'; based on idlelib.ToolTip
class ToolTipBase:

    def __init__(self,obj):
        self.obj    = obj
        self.widget = self.obj.widget
        self.tip    = None
        self.id     = None
        self.x      = 0
        self.y      = 0
        self.bindings()
    
    def bindings(self):
        self.bind_mouse()
                    
    def bind_mouse(self):
        bind (obj      = self.obj
             ,bindings = '<Enter>'
             ,action   = self.enter
             )
        bind (obj      = self.obj
             ,bindings = ['<Leave>','<ButtonPress>']
             ,action   = self.leave
             )

    def enter(self,event=None):
        self.schedule()

    def leave(self,event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.hint_delay,self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self):
        f = '[shared] sharedGUI.ToolTipBase.showtip'
        if self.tip:
            return
        ''' The tip window must be completely outside the widget;
            otherwise, when the mouse enters the tip window we get
            a leave event and it disappears, and then we get an enter
            event and it reappears, and so on forever :-(
            Tip coordinates are calculated such that, despite different
            sizes, centers of a horizontal tip and button would match.
        '''
        x = self.widget.winfo_rootx() + self.widget.winfo_width()/2 \
                                      - self.hint_width/2
        if self.hint_dir == 'bottom':
            y = self.widget.winfo_rooty() + self.widget.winfo_height() \
                                          + 1
        elif self.hint_dir == 'top':
            y = self.widget.winfo_rooty() - self.hint_height - 1
        else:
            y = 0
            Message (f,_('ERROR')
                    ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                    % (str(self.hint_dir),'top, bottom')
                    )
        self.tip = SimpleTop(parent=self.obj)
        self.tip.widget.wm_overrideredirect(1)
        # "+%d+%d" is not enough!
        sh.log.append (f,_('INFO')
                      ,_('Set the geometry to "%dx%d+%d+%d"') \
                      % (self.hint_width,self.hint_height,x,y)
                      )
        self.tip.widget.wm_geometry ("%dx%d+%d+%d" % (self.hint_width
                                                     ,self.hint_height
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
                ,hint_delay=800,hint_width=280
                ,hint_height=40,hint_bg='#ffffe0'
                ,hint_dir='top',hint_bwidth=1
                ,hint_bcolor='navy',hint_font='Sans 11'
                ):
        self.text        = text
        self.hint_delay  = hint_delay
        self.hint_dir    = hint_dir
        self.hint_bg     = hint_bg
        self.hint_bcolor = hint_bcolor
        self.hint_height = hint_height
        self.hint_width  = hint_width
        self.hint_bwidth = hint_bwidth
        self.hint_font   = hint_font
        ToolTipBase.__init__(self,obj=obj)

    def showcontents(self):
        self.frm = Frame (parent = self.tip
                         ,bg     = self.hint_bcolor
                         ,bd     = self.hint_bwidth
                         ,expand = False
                         )
        self.lbl = Label (parent  = self.frm
                         ,text    = self.text
                         ,bg      = self.hint_bg
                         ,width   = self.hint_width
                         ,height  = self.hint_height
                         ,justify = 'center'
                         ,Close   = False
                         ,font    = self.hint_font
                         )



class ListBox:
    #todo: configure a font
    def __init__(self
                ,parent
                ,Multiple        = False
                ,lst             = []
                ,title           = 'Title:'
                ,icon            = None
                ,SelectionCloses = True
                ,Composite       = False
                ,SingleClick     = True
                ,action          = None
                ,side            = None
                ,Scrollbar       = True
                ,expand          = 1
                ,fill            = 'both'
                ):
        # See 'WidgetShared'
        self.state = 'normal'
        self.type  = 'ListBox'
        ''' 'action': A user-defined function that is run when
            pressing Up/Down arrow keys and LMB. There is a problem
            binding it externally, so we bind it here.
        '''
        self.parent          = parent
        self.Multiple        = Multiple
        self.expand          = expand
        self.Composite       = Composite
        self.Scrollbar       = Scrollbar
        self.side            = side
        self._fill           = fill
        self.SelectionCloses = SelectionCloses
        self.SingleClick     = SingleClick
        self._icon           = icon
        # Set an initial value
        self.action          = action
        self.gui()
        self.reset (lst    = lst
                   ,title  = title
                   ,action = action
                   )

    def focus(self,event=None):
        self.widget.focus_set()
    
    def trigger(self,event=None):
        if self.action:
            ''' Binding just to '<Button-1>' does not work. We do not
                need binding Return/space/etc. because the function will
                be called each time the selection is changed. However,
                we still need to bind Up/Down.
            '''
            self.action()
    
    def delete(self,event=None):
        f = '[shared] sharedGUI.ListBox.delete'
        # Set an actual value
        self.index()
        try:
            del self.lst[self._index]
            # Set this after 'del' to be triggered only on success
            sh.log.append (f,_('DEBUG')
                          ,_('Remove item #%d') % self._index
                          )
        except IndexError:
            sh.log.append (f,_('WARNING')
                          ,_('No item #%d!') % self._index
                          )
        else:
            self.reset(lst=self.lst,title=self._title)

    def insert(self,string,Top=False):
        # Empty lists are allowed
        if Top:
            pos = 0
        else:
            pos = len(self.lst)
        self.lst.insert(pos,string)
        self.reset(lst=self.lst,title=self._title)
    
    def bindings(self):
        bind (obj      = self
             ,bindings = '<<ListboxSelect>>'
             ,action   = self.trigger
             )
        if self.SelectionCloses:
            #todo: test <KP_Enter> in Windows
            bind (obj      = self
                 ,bindings = ['<Return>','<KP_Enter>'
                             ,'<Double-Button-1>'
                             ]
                 ,action   = self.close
                 )
            if self.SingleClick and not self.Multiple:
                ''' Binding to '<Button-1>' does not allow to select
                    an entry before closing
                '''
                bind (obj      = self
                     ,bindings = '<<ListboxSelect>>'
                     ,action   = self.close
                     )
        if not self.Multiple:
            bind (obj      = self
                 ,bindings = '<Up>'
                 ,action   = self.move_up
                 )
            bind(self,'<Down>',self.move_down)
        #todo: test
        if not self.Composite:
            bind (obj      = self
                 ,bindings = ['<Escape>','<Control-q>','<Control-w>']
                 ,action   = self.interrupt
                 )
            if hasattr(self.parent,'type') and \
               self.parent.type == 'Toplevel':
                self.parent.widget.protocol ("WM_DELETE_WINDOW"
                                            ,self.interrupt
                                            )

    def gui(self):
        self._scroll()
        if self.Multiple:
            self.widget = tk.Listbox (master          = self.parent.widget
                                     ,exportselection = 0
                                     ,selectmode      = tk.MULTIPLE
                                     )
        else:
            self.widget = tk.Listbox (master          = self.parent.widget
                                     ,exportselection = 0
                                     ,selectmode      = tk.SINGLE
                                     )
        self.widget.pack (expand = self.expand
                         ,fill   = self._fill
                         ,side   = self.side
                         )
        self._resize()
        self._scroll_config()
        self.icon(path=self._icon)
        self.bindings()
        if not self.Composite:
            self.widget.focus_set()
            # Parent widget type can be any
            if not hasattr(self.parent,'close_button'):
                self.parent.close_button = Button (
                    parent = self.parent
                   ,text   = _('Quit')
                   ,hint   = _('Quit')
                   ,action = self.close
                   ,expand = 0
                   ,side   = 'bottom'
                                                  )
            WidgetShared.custom_buttons(self)

    def _scroll(self):
        if self.Scrollbar:
            self.scrollbar = tk.Scrollbar(self.parent.widget)
            self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

    def _scroll_config(self):
        if self.Scrollbar:
            self.scrollbar.config(command=self.widget.yview)
            self.widget.config(yscrollcommand=self.scrollbar.set)

    def _resize(self):
        # Autofit to contents
        self.widget.config(width=0,height=0)

    def activate(self):
        self.widget.activate(self._index)

    def clear(self):
        self.widget.delete(0,tk.END)

    def clear_selection(self):
        self.widget.selection_clear(0,tk.END)

    def reset(self,lst=[],title=None,action=None):
        self._title = title
        self.clear()
        if lst is None:
            self.lst = []
        else:
            self.lst = list(lst)
        # Checking for None allows to keep an old function
        if action:
            self.action = action
        self.title(text=self._title)
        self.fill()
        self._resize()
        ''' Do not set '_index' to 0, because we need 'self.interrupt'.
            Other functions use 'self.index()', which returns an actual
            value.
        '''
        self._get, self._index = '', None
        self.select()

    def select(self):
        f = '[shared] sharedGUI.ListBox.select'
        self.clear_selection()
        ''' Use an index changed with keyboard arrows. If it is not set,
            use current index (returned by 'self.index()').
        '''
        if self._index is None:
            self.index()
        if self._index is None:
            Message (f,_('ERROR')
                    ,_('Empty input is not allowed!')
                    )
        else:
            self._select()

    def _select(self):
        self.widget.selection_set(self._index)
        self.widget.see(self._index)

    def set(self,item):
        f = '[shared] sharedGUI.ListBox.set'
        if item:
            if item in self.lst:
                self._index = self.lst.index(item)
                self._select()
            else:
                Message (f,_('ERROR')
                        ,_('Item "%s" is not in list!') % str(item)
                        )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def show(self,event=None):
        self.parent.show()

    def interrupt(self,event=None):
        ''' Do not set '_index' to 0, because we need 'self.interrupt'.
            Other functions use 'self.index()', which returns an actual
            value.
        '''
        self._get, self._index = '', None
        self.parent.close()

    def close(self,event=None):
        self.index()
        self.get()
        self.parent.close()

    def fill(self):
        for item in self.lst:
            self.widget.insert(tk.END,item)

    def title(self,text=None):
        if text:
            self.parent.title(text=text)

    def icon(self,path=None):
        if path:
            WidgetShared.icon(self.parent,path)

    def index(self):
        ''' Read 'self._index' instead of calling this because we need 0
            in case of 'self.interrupt', and this always returns
            an actual value.
        '''
        selection = self.widget.curselection()
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
        ''' Read 'self._get' instead of calling this because we need ''
            in case of 'self.interrupt', and this always returns
            an actual value.
        '''
        result = [self.widget.get(idx) for idx \
                  in self.widget.curselection()
                 ]
        if self.Multiple:
            self._get = result
        elif len(result) > 0:
            self._get = result[0]
        return self._get

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



class OptionMenu:
    ''' tk.OptionMenu will convert integers to strings, but we better do
        this here to avoid problems with iterating ("in requires int as
        the left operand") later (this happens when we pass a sequence
        of chars instead of a list of strings).
    '''
    def __init__ (self
                 ,parent
                 ,items     = ('1','2','3','4','5')
                 ,side      = 'left'
                 ,anchor    = 'center'
                 ,action    = None
                 ,takefocus = 1
                 ,default   = None
                 ,Combo     = False
                 ):
        self.parent  = parent
        self.items   = items
        self.action  = action
        self.default = default
        self.Combo   = Combo
        self.choice  = None
        self.index   = 0
        self.var     = tk.StringVar(self.parent.widget)
        self.convert2str()
        if self.Combo:
            self.widget = ttk.Combobox (master       = self.parent.widget
                                       ,textvariable = self.var
                                       ,values       = self.items
                                       )
            bind (obj      = self
                 ,bindings = '<<ComboboxSelected>>'
                 ,action   = self.trigger
                 )
        else:
            # Cannot use a starred expression as a keyword argument
            self.widget = tk.OptionMenu (self.parent.widget
                                        ,self.var
                                        ,*self.items
                                        ,command = self.trigger
                                        )
        self.widget.pack(side=side,anchor=anchor)
        # Must be 1/True to be operational from keyboard
        self.widget.configure(takefocus=takefocus)
        self.default_set()

    # Allow to use digits at input
    def convert2str(self):
        if self.items:
            self.items = tuple(str(item) for item in self.items)
        else:
            # An error is thrown if 'items' is ()
            self.items = ('1','2','3','4','5')
        if self.default is not None:
            self.default = str(self.default)
    
    def enable(self):
        WidgetShared.enable(self)
    
    def disable(self):
        WidgetShared.disable(self)
    
    def trigger(self,event=None):
        f = '[shared] sharedGUI.OptionMenu.trigger'
        self._get()
        if self.Combo:
            self.widget.selection_clear()
        if self.action:
            self.action()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )

    def _default_set(self):
        if len(self.items) > 0:
            self.var.set(self.items[0])
            ''' Return a default value instead of 'None' if there was
                no interaction with the widget
            '''
            self.choice = self.items[0]
            self.index  = 0

    def default_set(self):
        f = '[shared] sharedGUI.OptionMenu.default_set'
        if self.default is None:
            self._default_set()
        else:
            if self.default in self.items:
                self.var.set(self.default)
                ''' Return a default value instead of 'None' if there
                    was no interaction with the widget
                '''
                self.choice = self.default
                self.index  = self.items.index(self.choice)
            else:
                Message (f,_('ERROR')
                        ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".')\
                        % (str(self.default),';'.join(self.items))
                        )
                self._default_set()

    def set(self,item,event=None):
        f = '[shared] sharedGUI.OptionMenu.set'
        item = str(item)
        if item in self.items:
            self.var.set(item)
            self.choice = item
            self.index  = self.items.index(self.choice)
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data: "%s"') % str(item)
                    )

    def _fill_menu(self):
        self.widget['menu'].delete(0,'end')
        for item in self.items:
            self.widget["menu"].add_command (label   = item
                                            ,command = tk._setit (self.var
                                                                 ,item
                                                                 ,self.trigger
                                                                 )
                                            )
                                            
    def _fill_combo(self):
        self.widget.config(values=self.items)
    
    def fill(self):
        if self.Combo:
            self._fill_combo()
        else:
            self._fill_menu()

    def reset (self,items=('1','2','3','4','5')
              ,default=None,action=None
              ):
        self.items = items
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
        if len(items) == 1:
            self.widget.config(state='disabled')
        else:
            self.widget.config(state='normal')

    # Auto updated (after selecting an item)
    def _get(self,event=None):
        f = '[shared] sharedGUI.OptionMenu._get'
        self.choice = self.var.get()
        # 'OptionMenu' always returns a string
        if self.choice not in self.items:
            self.choice = sh.Input (title = f
                                   ,value = self.choice
                                   ).integer()
        try:
            self.index = self.items.index(self.choice)
        except ValueError:
            Message (f,_('ERROR')
                    ,_('Wrong input data: "%s"') % str(self.choice)
                    )

    def set_prev(self,event=None):
        if self.index == 0:
            self.index = len(self.items) - 1
        else:
            self.index -= 1
        self.var.set(self.items[self.index])

    def set_next(self,event=None):
        if self.index == len(self.items) - 1:
            self.index = 0
        else:
            self.index += 1
        self.var.set(self.items[self.index])

    def focus(self,event=None):
        self.widget.focus_set()



# Selecting words only
class Selection:
    ''' Usage:
        bind(h_txt.widget,'<ButtonRelease-1>',action)

    def action(event=None):
        """ Refresh coordinates (or set h_selection._pos1tk,
        h_selection._pos2tk manually)
        """
        h_selection.get()
        h_selection.set()
    '''
    def __init__(self,h_widget,words=None):
        self.h_widget = h_widget
        self.reset_logic(words=words)
        self.reset_data()

    def reset (self
              ,mode       = 'data'
              ,words      = None
              ,pos1tk     = None
              ,pos2tk     = None
              ,background = None
              ,foreground = None
              ,tag        = 'tag'
              ):
        if mode == 'data':
            self.reset_data (pos1tk     = pos1tk
                            ,pos2tk     = pos2tk
                            ,background = background
                            ,foreground = foreground
                            ,tag        = tag
                            )
        else:
            self.reset_logic(words=words)

    def reset_logic(self,words):
        self.words = words

    def reset_data (self
                   ,pos1tk     = None
                   ,pos2tk     = None
                   ,background = None
                   ,foreground = None
                   ,tag        = 'tag'
                   ):
        self._pos1tk = pos1tk
        self._pos2tk = pos2tk
        self._text   = ''
        self._bg     = background
        self._fg     = foreground
        if not self._bg and not self._fg:
            self._bg = 'cyan'
        self._tag = tag

    def clear(self,tag_name='sel',pos1tk='1.0',pos2tk='end'):
        self.h_widget._tag_remove (tag_name = tag_name
                                  ,pos1tk   = pos1tk
                                  ,pos2tk   = pos2tk
                                  )

    def pos1tk(self):
        if self._pos1tk is None:
            self.get()
        return self._pos1tk

    def pos2tk(self):
        if self._pos2tk is None:
            self.get()
        return self._pos2tk

    def get(self,event=None):
        f = '[shared] sharedGUI.Selection.get'
        try:
            self._pos1tk = self.h_widget.widget.index('sel.first')
            self._pos2tk = self.h_widget.widget.index('sel.last')
        except tk.TclError:
            self._pos1tk, self._pos2tk = None, None
            # Too frequent
            '''
            sh.log.append (f,_('WARNING')
                          ,_('Nothing is selected in window %d, therefore, it is not possible to return coordinates!')\
                          % 1
                          )
            '''
        # Too frequent
        '''
        sh.log.append (f,_('DEBUG')
                      ,str((self._pos1tk,self._pos2tk))
                      )
        '''
        return(self._pos1tk,self._pos2tk)

    def text(self):
        f = '[shared] sharedGUI.Selection.text'
        try:
            self._text = self.h_widget.widget.get('sel.first','sel.last').replace('\r','').replace('\n','')
        except tk.TclError:
            self._text = ''
            sh.log.append (f,_('ERROR')
                          ,_('Failed to return selection in the Tkinter widget!')
                          )
        return self._text

    def cursor(self):
        return self.h_widget.cursor()

    def select_all(self):
        self.h_widget.select_all()

    def set(self,DeletePrevious=True,AutoScroll=True):
        if self.pos1tk() and self.pos2tk():
            mark = self._pos1tk
            self.h_widget.tag_add (pos1tk         = self._pos1tk
                                  ,pos2tk         = self._pos2tk
                                  ,tag_name       = self._tag
                                  ,DeletePrevious = DeletePrevious
                                  )
        else:
            # Just need to return something w/o warnings
            _cursor = mark = self.cursor()
            self.h_widget.tag_add (tag_name       = self._tag
                                  ,pos1tk         = _cursor
                                  ,pos2tk         = _cursor
                                  ,DeletePrevious = DeletePrevious
                                  )
        if self._bg:
            ''' This is not necessary for 'sel' tag which is hardcoded
                for selection and permanently colored with gray.
                A 'background' attribute cannot be changed for a 'sel'
                tag.
            '''
            self.h_widget.widget.tag_config (tagName    = self._tag
                                            ,background = self._bg
                                            )
        elif self._fg:
            self.h_widget.widget.tag_config (tagName    = self._tag
                                            ,foreground = self._fg
                                            )
        #todo: select either 'see' or 'autoscroll'
        if AutoScroll:
            #self.h_widget.see(mark)
            self.h_widget.autoscroll(mark)



class SymbolMap:

    def __init__(self,parent):
        self.symbol = 'EMPTY'
        self.parent = parent
        self.gui()
        self.bindings()
        
    def gui(self):
        self.obj    = Top(self.parent)
        self.widget = self.obj.widget
        self.frame  = Frame(self.obj,expand=1)
        self.obj.title(_('Paste a special symbol'))
        for i in range(len(sh.globs['var']['spec_syms'])):
            if i % 10 == 0:
                self.frame = Frame(self.obj,expand=1)
            ''' lambda will work properly only in case of an instant
                packing which is not supported by 'create_button'
                (the instant packing returns 'None' instead of a
                widget), therefore, we do not use this function.
                By the same reason, '<Return>' and '<KP_Enter>' cannot
                be bound to the buttons, only '<space>' and
                '<ButtonRelease-1>' that are bound by default will work.
            '''
            # width and height are required for Windows
            self.button = tk.Button (self.frame.widget
                                    ,text=sh.globs['var']['spec_syms'][i]
                                    ,command=lambda i=i:self.set(sh.globs['var']['spec_syms'][i])
                                    ,width=2,height=2).pack(side='left',expand=1)
        self.close()

    def bindings(self):
        bind (obj      = self.obj
             ,bindings = ['<Escape>','<Control-q>','<Control-w>']
             ,action   = self.close
             )
    
    def set(self,sym,event=None):
        self.symbol = sym
        self.close()

    def get(self,event=None):
        self.show()
        return self.symbol

    def show(self,event=None):
        self.obj.show()

    def close(self,event=None):
        self.obj.close()



class Geometry:
    ''' Window behavior is not uniform through different platforms or
        even through different Windows versions, so we bypass Tkinter's
        commands here.
    '''
    def __init__(self,parent=None,title=None,hwnd=None):
        self.parent = parent
        self._title = title
        self._hwnd  = hwnd
        self._geom  = None

    def update(self):
        objs.root().widget.update_idletasks()

    def save(self):
        f = '[shared] sharedGUI.Geometry.save'
        if self.parent:
            self.update()
            self._geom = self.parent.widget.geometry()
            sh.log.append (f,_('INFO')
                          ,_('Save geometry: %s') % self._geom
                          )
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )

    def restore(self):
        f = '[shared] sharedGUI.Geometry.restore'
        if self.parent:
            if self._geom:
                sh.log.append (f,_('INFO')
                              ,_('Restore geometry: %s') % self._geom
                              )
                self.parent.widget.geometry(self._geom)
            else:
                Message (f,_('WARNING')
                        ,_('Failed to restore geometry!')
                        )
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )

    def foreground(self,event=None):
        f = '[shared] sharedGUI.Geometry.foreground'
        if sh.oss.win():
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
                    sh.log.append (f,_('ERROR')
                                  ,_('Failed to change window properties!')
                                  )
            else:
                Message (f,_('ERROR')
                        ,_('Wrong input data!')
                        )
        elif self.parent:
            self.parent.widget.lift()
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )

    def minimize(self,event=None):
        f = '[shared] sharedGUI.Geometry.minimize'
        if self.parent:
            ''' # Does not always work
            if sh.oss.win():
                win32gui.ShowWindow(self.hwnd(),win32con.SW_MINIMIZE)
            else:
            '''
            self.parent.widget.iconify()
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )

    def maximize(self,event=None):
        f = '[shared] sharedGUI.Geometry.maximize'
        if sh.oss.win():
            #win32gui.ShowWindow(self.hwnd(),win32con.SW_MAXIMIZE)
            self.parent.widget.wm_state(newstate='zoomed')
        elif self.parent:
            self.parent.widget.wm_attributes('-zoomed',True)
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )

    def focus(self,event=None):
        f = '[shared] sharedGUI.Geometry.focus'
        if sh.oss.win():
            win32gui.SetActiveWindow(self.hwnd())
        elif self.parent:
            self.parent.widget.focus_set()
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )

    def lift(self,event=None):
        f = '[shared] sharedGUI.Geometry.lift'
        if self.parent:
            self.parent.widget.lift()
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )

    def _activate(self):
        f = '[shared] sharedGUI.Geometry._activate'
        if self.parent:
            self.parent.widget.deiconify()
            #self.parent.widget.focus_set()
            self.parent.widget.lift()
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )

    def activate(self,event=None,MouseClicked=False):
        self._activate()
        if sh.oss.win():
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
        f = '[shared] sharedGUI.Geometry.hwnd'
        if not self._hwnd:
            if self._title:
                try:
                    self._hwnd = win32gui.FindWindow(None,self._title)
                except win32ui.error:
                    Message (f,_('ERROR')
                            ,_('Failed to get the window handle!')
                            )
            else:
                Message (f,_('ERROR')
                        ,_('Not enough input data!')
                        )
        return self._hwnd

    def set(self,arg='800x600'):
        self._geom = arg
        self.restore()



class WaitBox:

    def __init__(self,parent):
        self.type   = 'WaitBox'
        self.parent = parent
        self._func  = self._title = self._args = self._message = None
        ''' For some reason, using common 'Top' may further cause
            problems in Windows with focusing.
        '''
        self.obj    = SimpleTop(parent=self.parent)
        self.widget = self.obj.widget
        self.widget.geometry('300x150')
        self.label = Label (parent = self
                           ,text   = _('Please wait...')
                           ,expand = True
                           ,Close  = True
                           )

    def update(self):
        ''' Tkinter works differently in Linux in Windows. This allows
            to evade focus problems in 'mclient'.
        '''
        if sh.oss.win():
            objs.root().idle()
        else:
            self.label.widget.update()
    
    # Use tuple for 'args' to pass multiple arguments
    def reset (self,func_title=None,func=None
              ,args=None,message=None
              ):
        self._func    = func
        self._title   = func_title
        self._args    = args
        self._message = message
        self.title()
        self.message()

    def run(self):
        f = '[shared] sharedGUI.WaitBox.run'
        self.show()
        if self._func:
            if self._args:
                func_res = self._func(self._args)
            else:
                func_res = self._func()
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )
        self.close()
        return func_res

    def show(self):
        self.obj.show()
        self.obj.center()
        self.update()

    def close(self):
        self.obj.close()

    def title(self,text=None):
        if text:
            self._title = text
        if self._title:
            self.obj.title(self._title)

    def message(self,message=None):
        if message:
            self._message = message
        if self._message:
            self.label.text (self._message + '\n\n' \
                            + _('Please wait...')
                            )
        else:
            self.label.text(_('Please wait...'))



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
                 ,anchor=None,Close=True,width=None
                 ,height=None,justify=None
                 ):
        self.type    = 'Label'
        self.parent  = parent
        self.side    = side
        self.fill    = fill
        self.expand  = expand
        self._text   = text
        self._font   = font
        self.ipadx   = ipadx
        self.ipady   = ipady
        self.image   = image
        self.bg      = bg
        self.fg      = fg
        self.anchor  = anchor
        self.width   = width
        self.height  = height
        # Usually the alignment is done by tuning the parent
        self.justify = justify
        self.gui()
        if Close:
            self.close()
    
    def gui(self):
        self.widget = tk.Label (master = self.parent.widget
                               ,image  = self.image
                               ,bg     = self.bg
                               ,fg     = self.fg
                               ,width  = self.width
                               ,height = self.height
                               )
        self.text()
        self.font()
        self.widget.pack (side   = self.side
                         ,fill   = self.fill
                         ,expand = self.expand
                         ,ipadx  = self.ipadx
                         ,ipady  = self.ipady
                         ,anchor = self.anchor
                         )

    def text(self,arg=None):
        if arg:
            self._text = arg
        self.widget.config(text=self._text)

    def font(self,arg=None):
        f = '[shared] sharedGUI.Label.font'
        if arg:
            self._font = arg
        try:
            self.widget.config(font=self._font)
        except tk.TclError:
            Message (f,_('ERROR')
                    ,_('Wrong font: "%s"!') % str(self._font)
                    )
            self._font = 'Sans 11'

    def show(self):
        self.parent.show()

    def close(self):
        self.parent.close()

    def title(self,text='Title:'):
        self.parent.title(text=text)
        
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
        self.status = tk.IntVar()
        self.gui()
        self.reset(Active=Active)

    def reset(self,Active=False,action=None):
        if Active:
            self.enable()
        else:
            self.disable()
        if action:
            self.action = action
            self.widget.config(command=self.action)

    def gui(self):
        self.widget = tk.Checkbutton (master   = self.parent.widget
                                     ,variable = self.status
                                     ,command  = self.action
                                     )
        self.widget.pack(side=self.side)
        self.obj = self

    def show(self):
        self.parent.show()

    def close(self):
        self.parent.close()

    def focus(self,event=None):
        self.widget.focus_set()

    def enable(self):
        self.widget.select()

    def disable(self):
        self.widget.deselect()

    def get(self,event=None):
        return self.status.get()

    def toggle(self,event=None):
        self.widget.toggle()



class Message:

    def __init__ (self,func='MAIN',level=_('WARNING')
                 ,message=_('Message'),Silent=False
                 ):
        f = '[shared] sharedGUI.Message.__init__'
        self.Success = True
        self.Yes     = False
        self.func    = func
        self.message = message
        self.level   = level
        self.Silent  = Silent
        if not self.func or not self.message:
            self.Success = False
            sh.log.append (f,_('ERROR')
                          ,_('Not enough input data!')
                          )
        if self.level == _('INFO'):
            self.info()
        elif self.level == _('WARNING'):
            self.warning()
        elif self.level in (_('ERROR'),_('CRITICAL')):
            self.error()
        elif self.level == _('QUESTION'):
            self.question()
        else:
            sh.log.append (f,_('ERROR')
                          ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                          % (str(self.level)
                            ,_('INFO') + ', ' + _('WARNING') + ', ' \
                            + _('ERROR') + ', ' + _('QUESTION')
                            )
                          )

    def error(self):
        f = '[shared] sharedGUI.Message.error'
        if self.Success:
            if not self.Silent:
                objs.error().reset (title = self.func + ':'
                                   ,text  = self.message
                                   ).show()
            sh.log.append (self.func
                          ,_('ERROR')
                          ,self.message
                          )
        else:
            sh.log.append (f,_('ERROR')
                          ,_('Operation has been canceled.')
                          )

    def info(self):
        f = '[shared] sharedGUI.Message.info'
        if self.Success:
            if not self.Silent:
                objs.info().reset (title = self.func + ':'
                                  ,text  = self.message
                                  ).show()
            sh.log.append (self.func
                          ,_('INFO')
                          ,self.message
                          )
        else:
            sh.log.append (f,_('INFO')
                          ,_('Operation has been canceled.')
                          )

    def question(self):
        f = '[shared] sharedGUI.Message.question'
        if self.Success:
            objs.question().reset (title = self.func + ':'
                                  ,text  = self.message
                                  ).show()
            self.Yes = objs._question.Yes
            sh.log.append (self.func
                          ,_('QUESTION')
                          ,self.message
                          )
            return self.Yes
        else:
            sh.log.append (f,_('QUESTION')
                          ,_('Operation has been canceled.')
                          )

    def warning(self):
        f = '[shared] sharedGUI.Message.warning'
        if self.Success:
            if not self.Silent:
                objs.warning().reset (title = self.func + ':'
                                     ,text  = self.message
                                     ).show()
            sh.log.append (self.func
                          ,_('WARNING')
                          ,self.message
                          )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



class MessageBuilder:
    ''' Not using tkinter.messagebox because it blocks main GUI (even
        if we specify a non-root parent).
    '''
    # Parent is root
    def __init__ (self,parent,level
                 ,Single=True,YesNo=False
                 ):
        self.Yes    = False
        self.YesNo  = YesNo
        self.Single = Single
        self.level  = level
        self.Lock   = False
        self.paths()
        self.parent = parent
        self.obj    = Top(parent=self.parent)
        self.widget = self.obj.widget
        self.icon()
        self.frames()
        self.picture()
        self.txt = TextBox (parent    = self.top_right
                           ,Composite = True
                           )
        self.buttons()
        self.bindings()
        Geometry(parent=self.obj).set('400x250')
        self.close()

    def bindings(self):
        bind (obj      = self
             ,bindings = ['<Control-q>','<Control-w>','<Escape>']
             ,action   = self.close_no
             )
        if hasattr(self.parent,'type') \
        and self.parent.type == 'Toplevel':
            self.widget.protocol("WM_DELETE_WINDOW",self.close)

    def paths(self):
        f = '[shared] sharedGUI.MessageBuilder.paths'
        if self.level == _('WARNING'):
            self.path = sh.objs.pdir().add ('..'
                                           ,'resources'
                                           ,'warning.gif'
                                           )
        elif self.level == _('INFO'):
            self.path = sh.objs.pdir().add ('..'
                                           ,'resources'
                                           ,'info.gif'
                                           )
        elif self.level == _('QUESTION'):
            self.path = sh.objs.pdir().add ('..'
                                           ,'resources'
                                           ,'question.gif'
                                           )
        elif self.level == _('ERROR'):
            self.path = sh.objs.pdir().add ('..'
                                           ,'resources'
                                           ,'error.gif'
                                           )
        else:
            sh.log.append (f,_('ERROR')
                          ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".')\
                          % (str(self.path)
                            ,', '.join ([_('WARNING'),_('ERROR')
                                        ,_('QUESTION'),_('INFO')
                                        ]
                                       )
                            )
                          )

    def icon(self,path=None):
        if path:
            self.obj.icon(path=path)
        else:
            self.obj.icon(path=self.path)

    def frames(self):
        frame = Frame (parent = self.obj
                      ,expand = 1
                      )
        top = Frame (parent = frame
                    ,expand = 1
                    ,side   = 'top'
                    )
        bottom = Frame (parent = frame
                       ,expand = 0
                       ,side   = 'bottom'
                       )
        self.top_left = Frame (parent = top
                              ,expand = 0
                              ,side   = 'left'
                              )
        self.top_right = Frame (parent = top
                               ,expand = 1
                               ,side   = 'right'
                               )
        self.bottom_left = Frame (parent = bottom
                                 ,expand = 1
                                 ,side   = 'left'
                                 )
        self.bottom_right = Frame (parent = bottom
                                  ,expand = 1
                                  ,side   = 'right'
                                  )

    def buttons(self):
        if self.YesNo or self.level == _('QUESTION'):
            YesName = _('Yes')
            NoName  = _('No')
        else:
            YesName = 'OK'
            NoName  = _('Cancel')
        if self.Single and self.level != _('QUESTION'):
            self.btn_yes = Button (parent    = self.bottom_left
                                  ,action    = self.close_yes
                                  ,hint      = _('Accept and close')
                                  ,text      = YesName
                                  ,TakeFocus = 1
                                  ,side      = 'right'
                                  )
        else:
            self.btn_no  = Button (parent = self.bottom_left
                                  ,action = self.close_no
                                  ,hint   = _('Reject and close')
                                  ,text   = NoName
                                  ,side   = 'left'
                                  )
            self.btn_yes = Button (parent    = self.bottom_right
                                  ,action    = self.close_yes
                                  ,hint      = _('Accept and close')
                                  ,text      = YesName
                                  ,TakeFocus = 1
                                  ,side      = 'right'
                                  )

    def title(self,text=None):
        if not text:
            text = _('Title:')
        self.obj.title(text=text)

    def update(self,text=_('Message')):
        #todo: Control-c does not work with 'ReadOnly=True'
        # Otherwise, updating text will not work
        #self.txt.read_only(ReadOnly=False)
        self.txt.clear_text()
        self.txt.insert(text=text)
        #self.txt.read_only(ReadOnly=True)

    def reset(self,text=_('Message'),title=_('Title:'),icon=None):
        self.update(text=text)
        self.title(text=title)
        self.icon(path=icon)
        return self

    def show(self,event=None,Lock=False):
        self.btn_yes.focus()
        self.obj.show()

    def close(self,event=None):
        self.obj.close()

    def close_yes(self,event=None):
        self.Yes = True
        self.close()

    def close_no(self,event=None):
        self.Yes = False
        self.close()

    def picture(self,event=None):
        f = '[shared] sharedGUI.MessageBuilder.picture'
        if os.path.exists(self.path):
            ''' We need to assign self.variable to Label, otherwise, it
                gets destroyed.
                Without explicitly indicating 'master', we get
                "image pyimage1 doesn't exist".
            '''
            self.label = Label (parent = self.top_left
                               ,image  = \
                         tk.PhotoImage (master = self.top_left.widget
                                       ,file   = self.path
                                       )
                               )
        else:
            sh.log.append (f,_('ERROR')
                          ,_('Picture "%s" was not found!') % self.path
                          )



class Clipboard:

    def __init__(self,Silent=False):
        self.Silent = Silent

    def copy(self,text,CopyEmpty=True):
        f = '[shared] sharedGUI.Clipboard.copy'
        if text or CopyEmpty:
            text = str(sh.Input (title = f
                                ,value = text
                                ).not_none()
                      )
            objs.root().widget.clipboard_clear()
            objs._root.widget.clipboard_append(text)
            try:
                objs._root.widget.clipboard_clear()
                objs._root.widget.clipboard_append(text)
            except tk.TclError:
                #todo: Show a window to manually copy from
                Message (func    = f
                        ,level   = _('ERROR')
                        ,message = _('A clipboard error has occurred!')
                        ,Silent  = self.Silent
                        )
            except tk._tkinter.TclError:
                # Do not use GUI
                sh.log.append (f,_('ERROR')
                              ,_('The parent has already been destroyed.')
                              )
            except:
                sh.log.append (f,_('ERROR')
                              ,_('An unknown error has occurred.')
                              )
            '''
            sh.log.append (f,_('DEBUG')
                          ,text
                          )
            '''
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def paste(self):
        f = '[shared] sharedGUI.Clipboard.paste'
        text = ''
        try:
            text = str(objs.root().widget.clipboard_get())
        except tk.TclError:
            Message (func    = f
                    ,level   = _('ERROR')
                    ,message = _('Failed to paste the clipboard contents!')
                    ,Silent  = self.Silent
                    )
        except tk._tkinter.TclError:
            # Do not use GUI
            sh.log.append (f,_('WARNING')
                          ,_('The parent has already been destroyed.')
                          )
        except:
            sh.log.append (f,_('ERROR')
                          ,_('An unknown error has occurred.')
                          )
        # Further possible actions: strip, delete double line breaks
        '''
        sh.log.append (f,_('DEBUG')
                      ,text
                      )
        '''
        return text



class Canvas:
    
    def __init__(self,parent,expand=True
                ,side=None,scrollregion=None
                ,width=None,height=None
                ,fill='both'
                ):
        self.type         = 'Canvas'
        self.parent       = parent
        self.expand       = expand
        self.side         = side
        self.scrollregion = scrollregion
        self.width        = width
        self.height       = height
        self.fill         = fill
        self.gui()
        
    def mouse_wheel(self,event=None):
        ''' Windows XP has the delta of -120, however, it differs
            depending on the version.
        '''
        if event.num == 5 or event.delta < 0:
            self.move_down()
        if event.num == 4 or event.delta > 0:
            self.move_up()
        return 'break'
    
    # These bindings are not enabled by default
    def top_bindings(self,top):
        f = '[shared] sharedGUI.Canvas.top_bindings'
        if top:
            if hasattr(top,'type') and top.type == 'Toplevel':
                bind (obj      = top
                     ,bindings = '<Down>'
                     ,action   = self.move_down
                     )
                bind (obj      = top
                     ,bindings = '<Up>'
                     ,action   = self.move_up
                     )
                bind (obj      = top
                     ,bindings = '<Left>'
                     ,action   = self.move_left
                     )
                bind (obj      = top
                     ,bindings = '<Right>'
                     ,action   = self.move_right
                     )
                bind (obj      = top
                     ,bindings = '<Next>'
                     ,action   = self.move_page_down
                     )
                bind (obj      = top
                     ,bindings = '<Prior>'
                     ,action   = self.move_page_up
                     )
                bind (obj      = top
                     ,bindings = '<End>'
                     ,action   = self.move_bottom
                     )
                bind (obj      = top
                     ,bindings = '<Home>'
                     ,action   = self.move_top
                     )
                bind (obj      = top
                     ,bindings = ['<MouseWheel>'
                                 ,'<Button 4>'
                                 ,'<Button 5>'
                                 ]
                     ,action   = self.mouse_wheel
                     )
            else:
                sh.log.append (f,_('WARNING')
                              ,_('Wrong input data!')
                              )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def move_up(self,event=None,value=-1):
        self.widget.yview_scroll(value,'units')
        
    def move_down(self,event=None,value=1):
        self.widget.yview_scroll(value,'units')
    
    def move_page_up(self,event=None,value=-1):
        self.widget.yview_scroll(value,'pages')
        
    def move_page_down(self,event=None,value=1):
        self.widget.yview_scroll(value,'pages')

    def move_left(self,event=None,value=-1):
        self.widget.xview_scroll(value,'units')
        
    def move_right(self,event=None,value=1):
        self.widget.xview_scroll(value,'units')
        
    def move_bottom(self,event=None):
        self.widget.yview_moveto('1.0')
        
    def move_top(self,event=None):
        self.widget.yview_moveto(0)
    
    def region (self,x=0,y=0
               ,x_border=0,y_border=0
               ):
        f = '[shared] sharedGUI.Canvas.region'
        # Both integer and float values are allowed at input
        if x and y:
            self.widget.configure (scrollregion = (-x/2 - x_border
                                                  ,-y/2 - y_border
                                                  , x/2 + x_border
                                                  , y/2 + y_border
                                                  )
                                  )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def scroll(self,event=None,x=0,y=0):
        self.widget.xview_moveto(x)
        self.widget.yview_moveto(y)
    
    def gui(self):
        self.widget = tk.Canvas (master       = self.parent.widget
                                ,scrollregion = self.scrollregion
                                ,width        = self.width
                                ,height       = self.height
                                )
        self.widget.pack (expand = self.expand
                         ,side   = self.side
                         ,fill   = self.fill
                         )
        
    def embed(self,obj):
        f = '[shared] sharedGUI.Canvas.embed'
        if hasattr(obj,'widget'):
            self.widget.create_window(0,0,window=obj.widget)
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )
        
    def focus(self,event=None):
        self.widget.focus_set()
    
    def show(self,event=None):
        self.parent.show()
        
    def close(self,event=None):
        self.parent.close()



class Objects:

    def __init__(self):
        self._root = self._warning = self._error = self._question \
                   = self._info = self._waitbox = self._txt \
                   = self._entry = self._clipboard = self._ig \
                   = self._it = self._io = self._txtnotes = None
        self._lst = []

    def txtnotes (self,text='',notes=''):
        if not self._txtnotes:
            self._txtnotes = TextBoxNotes()
            self._lst.append(self._txtnotes)
        self._txtnotes.reset(text=text,notes=notes)
        return self._txtnotes
    
    def io(self):
        if not self._io:
            import io
            self._io = io
        return self._io
    
    def ig(self):
        # Load PIL only after loading tkinter
        if not self._ig:
            from PIL import Image
            self._ig = Image
        return self._ig
        
    def it(self):
        # Load PIL only after loading tkinter
        if not self._it:
            from PIL import ImageTk
            self._it = ImageTk
        return self._it
    
    def root(self,Close=True):
        if not self._root:
            self._root = Root()
            if Close:
                self._root.close()
        return self._root

    def start(self,Close=True):
        self.root(Close=Close)

    def end(self):
        self.root().kill()
        self._root.run()

    def add(self,obj):
        f = '[shared] sharedGUI.Objects.add'
        sh.log.append (f,_('INFO')
                      ,_('Add %s') % type(obj)
                      )
        self._lst.append(obj)

    def warning(self):
        if not self._warning:
            self._warning = MessageBuilder (parent = self.root()
                                           ,level  = _('WARNING')
                                           )
            self._lst.append(self._warning)
        return self._warning

    def error(self):
        if not self._error:
            self._error = MessageBuilder (parent = self.root()
                                         ,level  = _('ERROR')
                                         )
            self._lst.append(self._error)
        return self._error

    def question(self):
        if not self._question:
            self._question = MessageBuilder (parent = self.root()
                                            ,level  = _('QUESTION')
                                            )
            self._lst.append(self._question)
        return self._question

    def info(self):
        if not self._info:
            self._info = MessageBuilder (parent = self.root()
                                        ,level  = _('INFO')
                                        )
            self._lst.append(self._info)
        return self._info

    def close_all(self):
        f = '[shared] sharedGUI.Objects.close_all'
        sh.log.append (f,_('INFO')
                      ,_('Close %d objs') % len(self._lst)
                      )
        for i in range(len(self._lst)):
            if hasattr(self._lst[i],'close'):
                self._lst[i].close()
            else:
                sh.log.append (f,_('ERROR')
                              ,_('Widget "%s" does not have a "close" action!')\
                              % type(self._lst[i])
                              )

    def new_top(self,Maximize=0,AutoCenter=1):
        return Top (parent     = self.root()
                   ,Maximize   = Maximize
                   ,AutoCenter = AutoCenter
                   )

    # It is better to use this for temporary widgets only
    def txt(self,Maximize=True,words=None):
        if not self._txt:
            h_top = Top (parent   = self.root()
                        ,Maximize = Maximize
                        )
            self._txt = TextBox (parent = h_top
                                ,words  = words
                                )
            self._txt.focus()
            self._lst.append(self._txt)
        return self._txt

    def entry(self):
        if not self._entry:
            h_top = Top(parent=self.root())
            self._entry = Entry(parent=h_top)
            self._entry.focus()
            self._lst.append(self._entry)
        return self._entry

    def waitbox(self):
        if not self._waitbox:
            self._waitbox = WaitBox(parent=self.root())
            self._lst.append(self._waitbox)
        return self._waitbox



class SimpleTop:
    
    def __init__(self,parent):
        self.type   = 'Toplevel'
        # Widget will be shown right after creation
        self.Active = True
        self.parent = parent
        self.gui()
        
    def destroy(self):
        self.kill()

    def kill(self):
        self.widget.destroy()
        
    # Identical to 'Top.resolution'
    def resolution(self):
        self.widget.update_idletasks()
        return (self.widget.winfo_screenwidth()
               ,self.widget.winfo_screenheight()
               )

    def center(self):
        ''' Make child widget always centered at the first time and up
            to a user's choice any other time (if the widget is reused).
            Basically the same as 'Top.center' (except for checking 
            the count of showing the widget).
            Only 'tk.Tk' and 'tk.Toplevel' types are supported.
            Use this only after setting widget sizes (e.g., by using
            'Geometry').
        '''
        width, height = self.resolution()
        size = tuple(int(item) for item \
               in self.widget.geometry().split('+')[0].split('x'))
        x = width/2 - size[0]/2
        y = height/2 - size[1]/2
        self.widget.geometry("%dx%d+%d+%d" % (size + (x, y)))
        
    def icon(self,path):
        WidgetShared.icon(self,path)
    
    def title(self,text=_('Title:')):
        WidgetShared.title(self,text=text)
    
    def gui(self):
        self.widget = tk.Toplevel(self.parent.widget)
        self.bindings()
        
    def bindings(self):
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
        
    def close(self,event=None):
        ''' Do not destroy widget: 'Label' may trigger closing with
            unwanted results
        '''
        f = '[shared] sharedGUI.SimpleTop.close'
        if self.Active:
            self.Active = False
            self.widget.withdraw()
        else:
            ''' This is a warning because, normally, closing this widget
                should not be triggered when it is not active
            '''
            sh.log.append (f,_('WARNING')
                          ,_('Nothing to do.')
                          )
        
    def show(self,event=None,Lock=False):
        f = '[shared] sharedGUI.SimpleTop.show'
        if self.Active:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do.')
                          )
        else:
            self.Active = True
            self.widget.deiconify()



class Scrollbar:
    
    def __init__(self,parent,scroll,Horizontal=False):
        self.type       = 'Scrollbar'
        self.parent     = parent
        self.scroll     = scroll
        self.Horizontal = Horizontal
        self.gui()
    
    def gui(self):
        f = '[shared] sharedGUI.Scrollbar.gui'
        if hasattr(self.parent,'widget'):
            if self.Horizontal:
                orient = tk.HORIZONTAL
                fill   = 'x'
                side   = None
            else:
                orient = tk.VERTICAL
                fill   = 'y'
                side   = 'right'
            self.widget = tk.Scrollbar (master = self.parent.widget
                                       ,orient = orient
                                       )
            self.widget.pack (expand = True
                             ,fill   = fill
                             ,side   = side
                             )
            if self.Horizontal:
                self.scroll.widget.config(xscrollcommand=self.widget.set)
                self.widget.config(command=self.scroll.widget.xview)
            else:
                self.scroll.widget.config(yscrollcommand=self.widget.set)
                self.widget.config(command=self.scroll.widget.yview)
        else:
            Message (f,_('ERROR')
                    ,_('Wrong input data!')
                    )



class Image:
    ''' Load an image from a file, convert this image to bytes and
        convert bytes back to the image.
        'it.PhotoImage' needs the 'tkinter' to be preloaded, so this
        class should be included in 'sharedGUI'.
    '''
    def __init__(self):
        self._image = self._bytes = self._loader = None
        
    def open(self,path):
        if sh.File(file=path).Success:
            self._loader = objs.ig().open(path)
            self._image  = objs.it().PhotoImage(self._loader)
        return self._image
            
    def loader(self):
        f = '[shared] sharedGUI.Image.loader'
        if not self._loader:
            if self._bytes:
                self._loader = \
                objs.ig().open(objs.io().BytesIO(self._bytes))
            else:
                sh.log.append (f,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        return self._loader
        
    def thumbnail(self,x,y):
        ''' Resize an image to x,y limits. PIL will keep an original
            aspect ratio.
        '''
        f = '[shared] sharedGUI.Image.thumbnail'
        if self._loader:
            try:
                self._loader.thumbnail([x,y])
            except Exception as e:
                sh.log.append (f,_('WARNING')
                              ,_('Third-party module has failed!\n\nDetails: %s')\
                              % str(e)
                              )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        return self._loader
    
    def image(self):
        f = '[shared] sharedGUI.Image.image'
        if not self._image:
            if self._loader:
                self._image = objs.it().PhotoImage(self._loader)
            else:
                sh.log.append (f,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        return self._image
        
    def bytes(self,ext='PNG'):
        if not self._bytes:
            if self._loader:
                self._bytes = objs.io().BytesIO()
                self._loader.save(self._bytes,format=ext)
                self._bytes = self._bytes.getvalue()
        return self._bytes



class Panes:
    
    def __init__(self,background='old lace',Extended=False):
        self._bg      = background
        self.Extended = Extended
        self.gui()
        
    def frames(self):
        self.frame1 = Frame (parent = self.obj
                            ,side   = 'top'
                            ,fill   = 'both'
                            )
        if self.Extended:
            self.frame2 = Frame (parent = self.obj
                                ,side   = 'bottom'
                                ,fill   = 'both'
                                )

    def panes(self):
        self.pane1 = TextBox (parent    = self.frame1
                             ,Composite = True
                             ,side      = 'left'
                             )
        self.pane2 = TextBox (parent    = self.frame1
                             ,Composite = True
                             ,side      = 'left'
                             )
        if self.Extended:
            self.pane3 = TextBox (parent    = self.frame2
                                 ,Composite = True
                                 ,side      = 'left'
                                 )
            self.pane4 = TextBox (parent    = self.frame2
                                 ,Composite = True
                                 ,side      = 'left'
                                 )
    
    def gui(self):
        self.obj = objs.new_top(Maximize=1)
        self.widget = self.obj.widget
        self.frames()
        self.panes()
        self.pane1.focus()
        #todo: reenable for 4 panes after GUI glitches are fixed
        if not self.Extended:
            self.pane1.widget.config(bg=self._bg)
        self.icon()
        self.title()
        self.bindings()
        
    def title(self,text=_('Compare texts:')):
        self.obj.title(text=text)
        
    def show(self,event=None):
        self.obj.show()
        
    def close(self,event=None):
        self.obj.close()
        
    def bindings(self):
        ''' We do not bind 'select1' to 'pane1' and 'select2' to 'pane3'
            since we need to further synchronize references by LMB
            anyway, and this further binding will rewrite the current
            binging.
        '''
        bind (obj      = self
             ,bindings = ['<Control-q>','<Control-w>']
             ,action   = self.close
             )
        bind (obj      = self
             ,bindings = '<Escape>'
             ,action   = Geometry(parent=self.obj).minimize
             )
        bind (obj      = self
             ,bindings = ['<Alt-Key-1>','<Control-Key-1>']
             ,action   = self.select1
             )
        bind (obj      = self
             ,bindings = ['<Alt-Key-2>','<Control-Key-2>']
             ,action   = self.select2
             )
        bind (obj      = self.pane2
             ,bindings = '<ButtonRelease-1>'
             ,action   = self.select2
             )
        if self.Extended:
            bind (obj      = self
                 ,bindings = ['<Alt-Key-3>','<Control-Key-3>']
                 ,action   = self.select3
                 )
            bind (obj      = self
                 ,bindings = ['<Alt-Key-4>','<Control-Key-4>']
                 ,action   = self.select4
                 )
            bind (obj      = self.pane4
                 ,bindings = '<ButtonRelease-1>'
                 ,action   = self.select4
                 )
             
    def decolorize(self):
        self.pane1.widget.config(bg='white')
        self.pane2.widget.config(bg='white')
        if self.Extended:
            self.pane3.widget.config(bg='white')
            self.pane4.widget.config(bg='white')
    
    def select1(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane1.focus()
        #todo: reenable for 4 panes after GUI glitches are fixed
        if not self.Extended:
            self.decolorize()
            self.pane1.widget.config(bg=self._bg)
        
    def select2(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane2.focus()
        #todo: reenable for 4 panes after GUI glitches are fixed
        if not self.Extended:
            self.decolorize()
            self.pane2.widget.config(bg=self._bg)
        
    def select3(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane3.focus()
        #fix: GUI glitches when doing this
        #self.decolorize()
        #self.pane3.widget.config(bg=self._bg)
        
    def select4(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane4.focus()
        #fix: GUI glitches when doing this
        #self.decolorize()
        #self.pane4.widget.config(bg=self._bg)
        
    def icon(self,path=None):
        if path:
            self.obj.icon(path)
        else:
            self.obj.icon (sh.objs.pdir().add ('..'
                                              ,'resources'
                                              ,'icon_64x64_cpt.gif'
                                              )
                          )
                          
    def reset(self,words1,words2,words3=None,words4=None):
        self.pane1.reset(words=words1)
        self.pane2.reset(words=words2)
        if self.Extended:
            self.pane3.reset(words=words3)
            self.pane4.reset(words=words4)



class ProgressBarItem:
    
    def __init__ (self,parent,orient='horizontal'
                 ,length=100,mode='determinate'
                 ):
        self.parent = parent
        self.orient = orient
        self.length = length
        self.mode   = mode
        self.gui()
        
    def gui(self):
        self.frames()
        self.labels()
        self.bar()
        self.text()
        
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
                           ,Close  = False
                           ,font   = 'Mono 11'
                           )

    def text (self,file='',cur_size=0
             ,total=0,rate=0,eta=0
             ):
        message = _('File: "%s"; %d/%d MB; Rate: %s kbps; ETA: %ss')\
                  % (file,cur_size,total,rate,eta)
        self.label.text(message)
                              
    def bar(self):
        self.widget = ttk.Progressbar (master = self.frame2.widget
                                      ,orient = self.orient
                                      ,length = self.length
                                      ,mode   = self.mode
                                      )
        self.widget.pack()



class ProgressBar:
    
    def __init__(self):
        self.values()
        self.gui()
        
    def values(self):
        self._items  = []
        self._item   = None
        self._height = 200
        self._width  = 750
        self._border = 80
    
    def frames(self):
        self.frm_prm = Frame (parent = self.obj)
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
    
    def title(self,text=None):
        if not text:
            text = _('Download progress')
        self.obj.title(text)
        
    def show(self,event=None):
        self.obj.show()
        
    def close(self,event=None):
        self.obj.close()
    
    def gui(self):
        self.obj = SimpleTop(parent=objs.root())
        self.widget = self.obj.widget
        Geometry(parent=self.obj).set ('%dx%d' % (self._width
                                                 ,self._height
                                                 )
                                      )
        self.title()
        self.frames()
        self.widgets()
        self.canvas.region (x = self._width
                           ,y = self._height
                           )
        self.canvas.scroll()
        self.bindings()
        
    def bindings(self):
        bind (obj      = self.obj
             ,bindings = ['<Control-q>','<Control-w>','<Escape>']
             ,action   = self.close
             )
        bind (obj      = self.obj
             ,bindings = '<Down>'
             ,action   = self.canvas.move_down
             )
        bind (obj      = self.obj
             ,bindings = '<Up>'
             ,action   = self.canvas.move_up
             )
        bind (obj      = self.obj
             ,bindings = '<Left>'
             ,action   = self.canvas.move_left
             )
        bind (obj      = self.obj
             ,bindings = '<Right>'
             ,action   = self.canvas.move_right
             )
        bind (obj      = self.obj
             ,bindings = '<End>'
             ,action   = self.canvas.move_bottom
             )
        bind (obj      = self.obj
             ,bindings = '<Home>'
             ,action   = self.canvas.move_top
             )
        bind (obj      = self.obj
             ,bindings = '<Prior>'
             ,action   = self.canvas.move_page_up
             )
        bind (obj      = self.obj
             ,bindings = '<Next>'
             ,action   = self.canvas.move_page_down
             )
    
    def widgets(self):
        self.canvas = Canvas(parent = self.frm_sec)
        self.label  = Label (parent = self.frm_sec
                            ,text   = 'ProgressBar'
                            ,expand = True
                            ,fill   = 'both'
                            )
        self.canvas.embed(self.label)
        self.yscroll = Scrollbar (parent = self.frm_ver
                                 ,scroll = self.canvas
                                 )
        self.canvas.focus()
        
    def add(self,event=None):
        f = '[shared] sharedGUI.ProgressBar.add'
        self._item = ProgressBarItem (parent = self.label
                                     ,length = self._width - self._border
                                     )
        self._items.append(self._item)
        objs.root().widget.update_idletasks()
        max_x = self.label.widget.winfo_reqwidth()
        max_y = self.label.widget.winfo_reqheight()
        '''
        sh.log.append (f,_('DEBUG')
                      ,_('Widget sizes: %s') \
                      % (str(max_x) + 'x' + str(max_y))
                      )
        '''
        self.canvas.region (x        = max_x
                           ,y        = max_y
                           ,x_border = 50
                           ,y_border = 20
                           )
        self.canvas.move_bottom()
        return self._item



class WidgetObject:
    
    def __init__(self,widget):
        self.widget = widget



# Make widget 'obj2' immediately adjacent to 'obj1'
class AttachWidget:
    
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
        f = '[shared] sharedGUI.AttachWidget.check'
        if self.obj1 and self.obj2:
            if hasattr(self.obj1,'widget') \
            and hasattr(self.obj2,'widget'):
                self.widget1 = self.obj1.widget
                self.widget2 = self.obj2.widget
            else:
                self.Success = False
                sh.log.append (f,_('WARNING')
                              ,_('Wrong input data!')
                              )
        else:
            self.Success = False
            sh.log.append (f,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        if self.anchor not in self.anchors:
            self.Success = False
            Message (f,_('ERROR')
                    ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".')\
                    % (str(self.anchor)
                      ,', '.join(self.anchors)
                      )
                    )
    
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
        f = '[shared] sharedGUI.AttachWidget.set'
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
                Message (f,_('ERROR')
                        ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                        % (str(self.anchor),', '.join(self.anchors))
                        )
            geom = Geometry(parent=self.obj2)
            geom._geom = '%dx%d+%d+%d' % (self.w2,self.h2
                                         ,self.x2,self.y2
                                         )
            geom.restore()
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def get(self):
        f = '[shared] sharedGUI.AttachWidget.get'
        if self.Success:
            self.x1 = self.widget1.winfo_rootx()
            self.y1 = self.widget1.winfo_rooty()
            self.x2 = self.widget2.winfo_rootx()
            self.y2 = self.widget2.winfo_rooty()
            self.w1 = self.widget1.winfo_width()
            self.h1 = self.widget1.winfo_height()
            self.w2 = self.widget2.winfo_width()
            self.h2 = self.widget2.winfo_height()
            sh.log.append (f,_('DEBUG')
                          ,_('Widget 1 geometry: %dx%d+%d+%d') \
                          % (self.w1,self.h1,self.x1,self.y1)
                          )
            sh.log.append (f,_('DEBUG')
                          ,_('Widget 2 geometry: %dx%d+%d+%d') \
                          % (self.w2,self.h2,self.x2,self.y2)
                          )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def run(self,event=None):
        self.get()
        self.set()



class MultCBoxes:

    def __init__(self,lst=[],width=350,height=300):
        self._width  = width
        self._height = height
        self.values()
        self.parent = Top(parent=objs.root())
        Geometry(parent=self.parent).set ('%dx%d' % (self._width
                                                    ,self._height
                                                    )
                                         )
        self.gui()
        self.reset(lst=lst)
        
    def selected(self,event=None):
        active = []
        for i in range(len(self._cboxes)):
            if self._cboxes[i].get():
                active.append(self._lbls[i]._text)
        return active
    
    def title(self,text=None):
        if not text:
            text = _('Select files:')
        self.parent.title(text)
    
    def region(self):
        f = '[shared] sharedGUI.MultCBoxes.region'
        if self._frms:
            self.cvs.region (x        = self._width
                            ,y        = 22 * len(self._frms)
                            ,x_border = 10
                            ,y_border = 20
                            )
            self.cvs.scroll()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
        
    def values(self):
        self._frms   = []
        self._cboxes = []
        self._lbls   = []
        
    
    def widgets(self):
        self.cvs  = Canvas(parent=self.frm1)
        self.frme = Frame(parent=self.frm1)
        self.cvs.embed(self.frme)
        self.btn1 = Button (parent = self.frmb
                           ,text   = _('Toggle all')
                           ,hint   = _('Mark/unmark all checkboxes')
                           ,side   = 'left'
                           ,action = self.toggle
                           )
        self.btn2 = Button (parent = self.frmb
                           ,text   = _('Close')
                           ,hint   = _('Close this window')
                           ,side   = 'right'
                           ,action = self.close
                           )
        
    def add_row(self,text):
        frm  = Frame (parent = self.frme
                     ,expand = False
                     )
        cbox = CheckBox (parent = frm
                        ,side   = 'left'
                        )
        lbl  = Label (parent = frm
                     ,text   = text
                     ,side   = 'left'
                     ,Close  = False
                     )
        bind (obj      = lbl
             ,bindings = '<ButtonRelease-1>'
             ,action   = cbox.toggle
             )
        self._frms.append(frm)
        self._cboxes.append(cbox)
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
    
    def reset(self,lst=[]):
        lst = [str(item) for item in lst]
        for frame in self._frms:
            frame.widget.destroy()
        self.values()
        for item in lst:
            self.add_row(item)
        self.region()
    
    def bindings(self):
        bind (obj      = self.parent
             ,bindings = ['<Control-q>','<Control-w>','<Escape>']
             ,action   = self.close
             )
        bind (obj      = self.parent
             ,bindings = '<Down>'
             ,action   = self.cvs.move_down
             )
        bind (obj      = self.parent
             ,bindings = '<Up>'
             ,action   = self.cvs.move_up
             )
        bind (obj      = self.parent
             ,bindings = '<Left>'
             ,action   = self.cvs.move_left
             )
        bind (obj      = self.parent
             ,bindings = '<Right>'
             ,action   = self.cvs.move_right
             )
        bind (obj      = self.parent
             ,bindings = '<Next>'
             ,action   = self.cvs.move_page_down
             )
        bind (obj      = self.parent
             ,bindings = '<Prior>'
             ,action   = self.cvs.move_page_up
             )
        bind (obj      = self.parent
             ,bindings = '<End>'
             ,action   = self.cvs.move_bottom
             )
        bind (obj      = self.parent
             ,bindings = '<Home>'
             ,action   = self.cvs.move_top
             )
        if sh.oss.win() or sh.oss.mac():
            bind (obj      = self.parent
                 ,bindings = '<MouseWheel>'
                 ,action   = self.mouse_wheel
                 )
        else:
            bind (obj      = self.parent
                 ,bindings = ['<Button 4>'
                             ,'<Button 5>'
                             ]
                 ,action   = self.mouse_wheel
                 )
    
    def mouse_wheel(self,event):
        ''' In Windows XP delta == -120 for scrolling up and 120
            for scrolling down, however, this value varies for different
            versions.
        '''
        if event.num == 5 or event.delta < 0:
            self.cvs.move_down()
        elif event.num == 4 or event.delta > 0:
            self.cvs.move_up()
        return 'break'
    
    def gui(self):
        self.frames()
        self.widgets()
        self.scrollbars()
        self.btn2.focus()
        self.bindings()
        self.title()
        
    def frames(self):
        self.frm  = Frame (parent = self.parent)
        self.frmy = Frame (parent = self.frm
                          ,expand = False
                          ,fill   = 'y'
                          ,side   = 'right'
                          )
        self.frmb = Frame (parent = self.parent
                          ,expand = False
                          ,fill   = 'both'
                          )
        self.frmx = Frame (parent = self.frm
                          ,expand = False
                          ,fill   = 'x'
                          ,side   = 'bottom'
                          )
        self.frm1 = Frame (parent = self.frm)
        
    def scrollbars(self):
        self.xscr = Scrollbar (parent     = self.frmx
                              ,scroll     = self.cvs
                              ,Horizontal = True
                              )
        self.yscr = Scrollbar (parent     = self.frmy
                              ,scroll     = self.cvs
                              )
                                 
    def show(self,event=None):
        self.parent.show()
        
    def close(self,event=None):
        self.parent.close()


def fast_txt(text):
    objs.txt().reset()
    objs._txt.insert(text)
    objs._txt.show()



''' If there are problems with import or tkinter's wait_variable, put
    this beneath 'if __name__'
'''
objs = Objects()


if __name__ == '__main__':
    objs.start()
    files = sh.Directory('/home/pete').rel_files()
    files.sort(key=lambda s:s.lower())
    cboxes = MultCBoxes(lst=files)
    cboxes.show()
    print('\n'.join(cboxes.selected()))
    objs.end()
