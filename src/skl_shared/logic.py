#!/usr/bin/python3
# -*- coding: UTF-8 -*-

copyright = 'Copyright 2015-2019, Peter Sklyar'
license   = 'GPL v.3'
email     = 'skl.progs@gmail.com'

import re
import os, sys
import configparser
import calendar
import datetime
import os
import pickle
import re
import shlex
import shutil
import ssl
import subprocess
import sys
import tempfile
import time
import webbrowser
''' 'import urllib' does not work in Python 3, importing must be as
    follows:
'''
import urllib.request, urllib.parse
import difflib
import locale

import gettext
import skl_shared.gettext_windows as gettext_windows
gettext_windows.setup_env()
gettext.install('shared','../resources/locale')


gpl3_url_en = 'http://www.gnu.org/licenses/gpl.html'
gpl3_url_ru = 'http://antirao.ru/gpltrans/gplru.pdf'

globs = {'int':{},'bool':{},'var':{}}

nbspace = ' '

ru_alphabet        = '№АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЪЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщыъьэюя'
# Some vowels are put at the start for the faster search
ru_alphabet_low    = 'аеиоубявгдёжзйклмнпрстфхцчшщыъьэю№'
lat_alphabet       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
lat_alphabet_low   = 'abcdefghijklmnopqrstuvwxyz'
greek_alphabet     = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω'
greek_alphabet_low = 'αβγδεζηθικλμνξοπρστυφχψω'
other_alphabet     = 'ÀÁÂÆÇÈÉÊÑÒÓÔÖŒÙÚÛÜàáâæßçèéêñòóôöœùúûü'
other_alphabet_low = 'àáâæßçèéêñòóôöœùúûü'
digits             = '0123456789'

SectionBooleans        = 'Boolean'
SectionBooleans_abbr   = 'bool'
SectionFloatings       = 'Floating Values'
SectionFloatings_abbr  = 'float'
SectionIntegers        = 'Integer Values'
SectionIntegers_abbr   = 'int'
SectionLinuxSettings   = 'Linux settings'
SectionMacSettings     = 'Mac settings'
SectionVariables       = 'Variables'
SectionVariables_abbr  = 'var'
SectionWindowsSettings = 'Windows settings'

punc_array      = ['.',',','!','?',':',';']
#todo: why there were no opening brackets?
#punc_ext_array = ['"','”','»',']','}',')']
punc_ext_array  = ['"','“','”','','«','»','[',']'
                  ,'{','}','(',')','’',"'",'*'
                  ]

forbidden_win = '/\?%*:|"<>'
forbidden_lin = '/'
forbidden_mac = '/\?*:|"<>'
reserved_win  = ['CON','PRN','AUX','NUL','COM1','COM2','COM3','COM4'
                ,'COM5','COM6','COM7','COM8','COM9','LPT1','LPT2','LPT3'
                ,'LPT4','LPT5','LPT6','LPT7','LPT8','LPT9'
                ]
config_parser = configparser.SafeConfigParser()


class MessageBuilder:
    
    def __init__(self,level):
        self.values()
        self._level = level
        self.icon()
    
    def icon(self):
        f = '[shared] logic.MessageBuilder.icon'
        if not self._icon:
            if self._level in (_('INFO'),_('DEBUG')):
                prefix = 'info'
            elif self._level == _('WARNING'):
                prefix = 'warning'
            elif self._level == _('QUESTION'):
                prefix = 'question'
            else:
                prefix = 'error'
            self._icon = objs.pdir().add('..','resources',prefix+'.gif')
        if not os.path.exists(self._icon):
            self._icon = ''
            message = _('File {} was not found!').format(self._icon)
            Message (func    = f
                    ,message = message
                    ).error()
    
    def reset(self,text='',title=''):
        self._text  = text
        self._title = title
        self.sanitize()
    
    def values(self):
        self._text  = ''
        self._title = ''
        self._icon  = ''
        self._level = _('INFO')
    
    def sanitize(self):
        self._title = com.sanitize(self._title) + ':'
        self._text  = com.sanitize(self._text)



class Message:

    def __init__(self,func,message,Silent=True):
        self.func    = func
        self.message = message

    def error(self):
        log.append (self.func
                   ,_('ERROR')
                   ,self.message
                   )
    
    def warning(self):
        log.append (self.func
                   ,_('WARNING')
                   ,self.message
                   )
    
    def info(self):
        log.append (self.func
                   ,_('INFO')
                   ,self.message
                   )
    
    def debug(self):
        log.append (self.func
                   ,_('DEBUG')
                   ,self.message
                   )
    
    def question(self):
        log.append (self.func
                   ,_('QUESTION')
                   ,self.message
                   )
        try:
            answer = input()
        except (EOFError, KeyboardInterrupt):
            # The user pressed 'Ctrl-c' or 'Ctrl-d'
            answer = ''
        if answer.lower() == 'y':
            return True



class Font:
    
    def __init__(self,name,xborder=0,yborder=0):
        self.values()
        if name:
            self.reset (name    = name
                       ,xborder = xborder
                       ,yborder = yborder
                       )
    
    def set_text(self,text):
        f = '[shared] logic.Font.set_text'
        if text:
            self._text = text
        else:
            com.empty(f)
    
    def values(self):
        self._font   = None
        self._family = ''
        self._name   = ''
        self._text   = ''
        self._size   = 0
        self._height = 0
        self._width  = 0
        self.xborder = 0
        self.yborder = 0
    
    def width(self):
        f = '[shared] logic.Font.width'
        if self._width:
            self._width += self.xborder
            '''
            Message (func    = f
                    ,message = '%d' % self._width
                    ).debug()
            '''
    
    def height(self):
        f = '[shared] logic.Font.height'
        if self._height:
            lines = len(self._text.splitlines())
            if lines:
                self._height = self._height * lines
            self._height += self.yborder
            '''
            Message (func    = f
                    ,message = '%d' % self._height
                    ).debug()
            '''
        else:
            com.empty(f)
    
    def reset(self,name,xborder=0,yborder=0):
        self.values()
        self._name   = name
        self.xborder = xborder
        self.yborder = yborder
        self.attr()
    
    def attr(self):
        f = '[shared] logic.Font.attr'
        if self._name:
            match = re.match('([aA-zZ].*) (\d+)',self._name)
            if match:
                self._family = match.group(1)
                self._size   = int(match.group(2))
            else:
                message = _('Wrong input data: "{}"!').format(self._name)
                Message (func    = f
                        ,message = message
                        ).error()
        else:
            com.empty(f)



class Hotkeys:
    ''' Transform tkinter bindings to a human readable form
        Use the following key names:
        http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
        #todo: add remaining keypad key
    '''
    def __init__(self,hotkeys,sep='; '):
        self.Success  = True
        self._hotkeys = hotkeys
        self._sep     = sep
        self.check()
    
    def check(self):
        f = '[shared] logic.Hotkeys.check'
        if self._hotkeys and self._sep:
            if not isinstance(self._hotkeys,str) \
            and not isinstance(self._hotkeys,tuple) \
            and not isinstance(self._hotkeys,list):
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(self._hotkeys)
                objs.mes(f,mes).warning()
        else:
            self.Success = False
            #todo: do we need this warning?
            com.empty(f)
    
    def _loop(self,pattern):
        self._hotkeys = [hotkey for hotkey in self._hotkeys \
                         if not pattern in hotkey
                        ]
    
    def keypad(self):
        ''' Both 'Return' (main key) and 'KP_Enter' (numeric keypad)
            usually do the same thing, so we just remove KP_Enter.
            The same relates to other keypad key.
        '''
        f = '[shared] logic.Hotkeys.keypad'
        if self.Success:
            if not isinstance(self._hotkeys,str):
                for hotkey in self._hotkeys:
                    ''' Do not use '<' and '>' signs here since
                        the combination can actually be
                        '<Control-KP_Enter>'.
                    '''
                    if 'Return' in hotkey:
                        self._loop('KP_Enter')
                    if 'Home' in hotkey:
                        self._loop('KP_Home')
                    if 'End' in hotkey:
                        self._loop('KP_End')
                    if 'Delete' in hotkey:
                        self._loop('KP_Delete')
                    if 'Insert' in hotkey:
                        self._loop('KP_Insert')
        else:
            com.cancel(f)
    
    def hotkeys(self):
        f = '[shared] logic.Hotkeys.hotkeys'
        if self.Success:
            self._hotkeys = [self.replace(hotkey) \
                             for hotkey in self._hotkeys
                            ]
            self._hotkeys = [hotkey for hotkey in self._hotkeys \
                             if hotkey
                            ]
        else:
            com.cancel(f)
    
    def run(self):
        f = '[shared] logic.Hotkeys.run'
        result = ''
        if self.Success:
            if isinstance(self._hotkeys,str):
                result = self.replace(self._hotkeys)
            else:
                self.keypad()
                self.hotkeys()
                result = self._sep.join(self._hotkeys)
        else:
            com.cancel(f)
        return result
    
    def replace(self,key):
        f = '[shared] logic.Hotkeys.replace'
        if key:
            key = key.replace('<','').replace('>','')
            key = key.replace('Left','←').replace('Right','→')
            key = key.replace ('Button-1'
                              ,_('Left mouse button')
                              )
            key = key.replace ('ButtonRelease-1'
                              ,_('Left mouse button')
                              )
            key = key.replace ('Button-2'
                              ,_('Middle mouse button')
                              )
            key = key.replace ('ButtonRelease-2'
                              ,_('Middle mouse button')
                              )
            key = key.replace ('Button-3'
                              ,_('Right mouse button')
                              )
            key = key.replace ('ButtonRelease-3'
                              ,_('Right mouse button')
                              )
            key = key.replace ('space'
                              ,_('Space')
                              )
            key = key.replace('grave','~')
            # Left and right Alt and Shift are usually interchangeable
            key = key.replace('Alt_R','Alt_L')
            key = key.replace('Alt_L','Alt')
            key = key.replace('Control_L','Control')
            key = key.replace('Control_R','Control')
            key = key.replace('Control','Ctrl')
            key = key.replace('Shift_R','Shift_L')
            key = key.replace('Shift_L','Shift')
            key = key.replace('-Key-','')
            key = key.replace('Delete','Del')
            key = key.replace('Insert','Ins')
            key = key.replace('Scroll_Lock','ScrollLock')
            key = key.replace('Print','PrintScrn')
            key = key.replace('Up','↑').replace('Down','↓')
            key = key.replace('Execute','SysReq')
            key = key.replace('Num_Lock','NumLock')
            key = key.replace('Prior','PgUp')
            key = key.replace('Next','PgDn')
            key = key.replace('Escape','Esc')
            ''' We should leave only 1 key if there are key
                both for keyboard and keypad. Thus, we generally should
                not have to use keypad key without keyboard
                analogs. If we do, we should excplicitly indicate that
                it is keypad.
            '''
            key = key.replace('KP_Delete','Del (keypad)')
            key = key.replace('KP_Divide','/ (keypad)')
            key = key.replace('KP_Down','↓ (keypad)')
            ''' '<Control-S>' actually means 'Ctrl-Shift-s' in tkinter.
                Insert 'Shift' before making key upper-case.
            '''
            match = re.match('.*-([A-Z])$',key)
            if match:
                group = match.group(1)
                key   = key.replace ('-'       + group
                                    ,'-Shift-' + group
                                    )
            ''' We make letters upper-case in order to avoid confusion,
                e.g., when using 'i', 'l' and '1'.
            '''
            match = re.match('.*-([a-z])$',key)
            if match:
                group = match.group(1)
                key   = key.replace ('-' + group
                                    ,'-' + group.upper()
                                    )
            #key = key.replace('-','+')
        else:
            #todo: do we need this warning?
            self.empty(f)
        return key



class OSSpecific:

    def __init__(self):
        self._name = ''
        self.win_import()

    def shift_tab(self):
        if self.lin():
            return '<Shift-ISO_Left_Tab>'
        else:
            return '<Shift-KeyPress-Tab>'

    def win(self):
        return 'win' in sys.platform

    def lin(self):
        return 'lin' in sys.platform

    def mac(self):
        return 'mac' in sys.platform

    def name(self):
        if not self._name:
            if self.win():
                self._name = 'win'
            elif self.lin():
                self._name = 'lin'
            elif self.mac():
                self._name = 'mac'
            else:
                self._name = 'unknown'
        return self._name

    def win_import(self):
        if self.win():
            #http://mail.python.org/pipermail/python-win32/2012-July/012493.html
            _tz = os.getenv('TZ')
            if _tz is not None and '/' in _tz:
                os.unsetenv('TZ')
            import pythoncom, win32com, win32com.client, win32api
            # Required by 'Geometry'
            import win32gui, win32con, ctypes
            if win32com.client.gencache.is_readonly:
                win32com.client.gencache.is_readonly = False
                ''' Under p2exe/cx_freeze the call in gencache to
                    __init__() does not happen so we use Rebuild() to
                    force the creation of the gen_py folder.
                    The contents of library.zip\win32com shall be
                    unpacked to exe.win32 - 3.3\win32com.
                    See also the section where EnsureDispatch is called.
                '''
                win32com.client.gencache.Rebuild()
            ''' 'datetime' may have to be imported last due to
                the problems with TZ.
            '''



class Launch:
    #note: 'Block' works only a 'custom_app' is set
    def __init__(self,target='',Block=False):
        self.values()
        self.target = target
        self.Block  = Block
        # Do not shorten, Path is used further
        self.ipath  = Path(self.target)
        self.ext    = self.ipath.extension().lower()
        ''' We do not use the File class because the target can be a
            directory.
        '''
        if self.target and os.path.exists(self.target):
            self.TargetExists = True
        else:
            self.TargetExists = False

    def values(self):
        self.custom_app  = ''
        self.custom_args = []
    
    def _launch(self):
        f = '[shared] logic.Launch._launch'
        if self.custom_args:
            mes = _('Custom arguments: "{}"').format(self.custom_args)
            objs.mes(f,mes,True).debug()
            try:
                # Block the script till the called program is closed
                if self.Block:
                    subprocess.call(self.custom_args)
                else:
                    subprocess.Popen(self.custom_args)
            except:
                mes = _('Failed to run "{}"!').format(self.custom_args)
                objs.mes(f,mes).error()
        else:
            com.empty(f)

    def _lin(self):
        f = '[shared] logic.Launch._lin'
        try:
            os.system("xdg-open " + self.ipath.escape() + "&")
        except OSError:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            objs.mes(f,mes).error()

    def _mac(self):
        f = '[shared] logic.Launch._mac'
        try:
            os.system("open " + self.target)
        except:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            objs.mes(f,mes).error()

    def _win(self):
        f = '[shared] logic.Launch._win'
        try:
            os.startfile(self.target)
        except:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            objs.mes(f,mes).error()

    def app(self,custom_app='',custom_args=[]):
        self.custom_app  = custom_app
        self.custom_args = custom_args
        if self.custom_app:
            if self.custom_args and len(self.custom_args) > 0:
                self.custom_args.insert(0,self.custom_app)
                if self.TargetExists:
                    self.custom_args.append(self.target)
            else:
                self.custom_args = [self.custom_app]
        self._launch()

    def auto(self):
        ''' Starting third-party apps instead of default ones is no
            longer supported - it introduces an excessive complexity
            and is a potential security breach (programs run by default
            are usually installed with admin rights and cannot be
            compromised).
        '''
        self.default()

    def custom(self):
        f = '[shared] logic.Launch.custom'
        if self.TargetExists:
            self.custom_args = [self.custom_app,self.target]
            self._launch()
        else:
            com.cancel(f)

    def default(self):
        f = '[shared] logic.Launch.default'
        if self.TargetExists:
            if objs.os().lin():
                self._lin()
            elif objs._os.mac():
                self._mac()
            elif objs._os.win():
                self._win()
        else:
            com.cancel(f)



class WriteTextFile:

    def __init__(self,file,Rewrite=False):
        f = '[shared] logic.WriteTextFile.__init__'
        self.file    = file
        self.text    = ''
        self.Rewrite = Rewrite
        self.Success = True
        if not self.file:
            self.Success = False
            mes = _('Not enough input data!')
            objs.mes(f,mes).warning()

    def _write(self,mode='w'):
        f = '[shared] logic.WriteTextFile._write'
        if mode == 'w' or mode == 'a':
            mes = _('Write file "{}"').format(self.file)
            objs.mes(f,mes,True).info()
            try:
                with open(self.file,mode,encoding='UTF-8') as fl:
                    fl.write(self.text)
            except:
                self.Success = False
                mes = _('Unable to write file "{}"!').format(self.file)
                objs.mes(f,mes).error()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode,'a, w')
            objs.mes(f,mes).error()

    def append(self,text=''):
        f = '[shared] logic.WriteTextFile.append'
        if self.Success:
            self.text = text
            if self.text:
                ''' #todo: In the append mode the file is created if it
                    does not exist, but should we warn the user that we
                    create it from scratch?
                '''
                self._write('a')
            else:
                mes = _('Not enough input data!')
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)

    def write(self,text=''):
        f = '[shared] logic.WriteTextFile.write'
        if self.Success:
            self.text = text
            if self.text:
                if com.rewrite (file    = self.file
                               ,Rewrite = self.Rewrite
                               ):
                    self._write('w')
            else:
                mes = _('Not enough input data!')
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)



class Log:

    def __init__ (self,Use=True,Short=False
                 ):
        f = self.func = 'shared.Log.__init__'
        self.Success = True
        self.level   = _('INFO')
        self.message = 'Test'
        self.count   = 1
        self.Short   = Short
        if not Use:
            self.Success = False

    def print(self):
        if self.Success:
            if self.Short:
                if self.level in (_('WARNING'),_('ERROR')):
                    self._print()
            else:
                self._print()

    def _print(self):
        f = '[shared] logic.Log._print'
        try:
            print ('%d:%s:%s:%s' % (self.count,self.func,self.level
                                   ,self.message
                                   )
                  )
        except:
            ''' Rarely somehing like "UnicodeEncodeError: 'utf-8' codec
                can't encode character '\udce9' in position 175:
                surrogates not allowed" occurs. Since there are to many
                Unicode exceptions to except, we do not specify
                an exception type.
            '''
            print ('%s:%s:%s' % (f,_('WARNING')
                                ,_('Cannot print the message!')
                                )
                  )

    def append (self,func='shared.Log.append'
               ,level=_('INFO'),message='Test'
               ):
        if self.Success:
            if func and level and message:
                self.func    = func
                self.level   = level
                self.message = str(message)
                self.print()
                self.count += 1



#todo: Do we really need this?
class TextDic:

    def __init__(self,file,Sortable=False):
        self.file     = file
        self.Sortable = Sortable
        self.iread    = ReadTextFile(self.file)
        self.reset()

    ''' This is might be needed only for those dictionaries that
        already may contain duplicates (dictionaries with newly added
        entries do not have duplicates due to new algorithms)
    '''
    def _delete_duplicates(self):
        f = '[shared] logic.TextDic._delete_duplicates'
        if self.Success:
            if self.Sortable:
                old = self.lines()
                self._list = list(set(self.list()))
                new = self._lines = len(self._list)
                mes = _('Entries deleted: {} ({}-{})')
                mes = mes.format(old-new,old,new)
                objs.mes(f,mes,True).info()
                self.text = '\n'.join(self._list)
                # Update original and translation
                self._split()
                # After using set(), the original order was lost
                self.sort()
            else:
                mes = _('File "{}" is not sortable!').format(self.file)
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)

    # We can use this as an updater, even without relying on Success
    def _join(self):
        f = '[shared] logic.TextDic._join'
        if len(self.orig) == len(self.transl):
            self._lines = len(self.orig)
            self._list  = []
            for i in range(self._lines):
                self._list.append(self.orig[i]+'\t'+self.transl[i])
            self.text = '\n'.join(self._list)
        else:
            mes = _('Wrong input data!')
            objs.mes(f,mes).warning()

    def _split(self):
        ''' We can use this to check integrity and/or update original
            and translation lists.
        '''
        f = '[shared] logic.TextDic._split'
        if self.get():
            self.Success = True
            self.orig    = []
            self.transl  = []
            ''' Building lists takes ~0.1 longer without temporary
                variables (now self._split() takes ~0.256)
            '''
            for i in range(self._lines):
                tmp_lst = self._list[i].split('\t')
                if len(tmp_lst) == 2:
                    self.orig.append(tmp_lst[0])
                    self.transl.append(tmp_lst[1])
                else:
                    self.Success = False
                    # i+1: Count from 1
                    mes = _('Dictionary "{}": Incorrect line #{}: "{}"!')
                    mes = mes.format(self.file,i+1,self._list[i])
                    objs.mes(f,mes).warning()
        else:
            self.Success = False

    def append(self,original,translation):
        ''' #todo: skip repetitions
            #todo: write a dictionary in an append mode after appending
            to memory.
        '''
        f = '[shared] logic.TextDic.append'
        if self.Success:
            if original and translation:
                self.orig.append(original)
                self.transl.append(translation)
                self._join()
            else:
                com.empty(f)
        else:
            com.cancel(f)

    def delete_entry(self,entry_no): # Count from 1
        ''' #todo: #fix: an entry which is only one in a dictionary is
            not deleted.
        '''
        f = '[shared] logic.TextDic.delete_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.lines():
                del self.orig[entry_no]
                del self.transl[entry_no]
                self._join()
            else:
                sub = '0 <= {} < {}'.format(entry_no,self.lines())
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)

    def edit_entry(self,entry_no,orig,transl): # Count from 1
        ''' #todo: Add checking orig and transl (where needed) for
            a wrapper function.
        '''
        f = '[shared] logic.TextDic.edit_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.lines():
                self.orig[entry_no] = orig
                self.transl[entry_no] = transl
                self._join()
            else:
                sub = '0 <= {} < {}'.format(entry_no,self.lines())
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)

    def get(self):
        if not self.text:
            self.text = self.iread.load()
        return self.text

    def lines(self):
        if self._lines == 0:
            self._lines = len(self.list())
        return self._lines

    def list(self):
        if not self._list:
            self._list = self.get().splitlines()
        return self._list

    def reset(self):
        self.text   = self.iread.load()
        self.orig   = []
        self.transl = []
        self._list  = self.get().splitlines()
        self._lines = len(self._list)
        self._split()

    # Sort a dictionary with the longest lines going first
    def sort(self):
        f = '[shared] logic.TextDic.sort'
        if self.Success:
            if self.Sortable:
                tmp_list = []
                for i in range(len(self._list)):
                    tmp_list += [[len(self.orig[i])
                                 ,self.orig[i]
                                 ,self.transl[i]
                                 ]
                                ]
                tmp_list.sort(key=lambda x: x[0],reverse=True)
                for i in range(len(self._list)):
                    self.orig[i]   = tmp_list[i][1]
                    self.transl[i] = tmp_list[i][2]
                    self._list[i]  = self.orig[i] + '\t' \
                                                  + self.transl[i]
                self.text = '\n'.join(self._list)
            else:
                mes = _('File "{}" is not sortable!').format(self.file)
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)

    def tail(self):
        f = '[shared] logic.TextDic.tail'
        tail_text = ''
        if self.Success:
            tail_len = globs['int']['tail_len']
            if tail_len > self.lines():
                tail_len = self.lines()
            i = self.lines() - tail_len
            # We count from 1, therefore it is < and not <=
            while i < self.lines():
                # i+1 by the same reason
                tail_text += str(i+1) + ':' + '"' + self.list()[i] \
                                      + '"\n'
                i += 1
        else:
            com.cancel(f)
        return tail_text

    def write(self):
        f = '[shared] logic.TextDic.write'
        if self.Success:
            WriteTextFile (file    = self.file
                          ,Rewrite = True
                          ).write(self.get())
        else:
            com.cancel(f)



class ReadTextFile:

    def __init__(self,file):
        f = '[shared] logic.ReadTextFile.__init__'
        self.file    = file
        self._text   = ''
        self._list   = []
        self.Success = True
        if self.file and os.path.isfile(self.file):
            pass
        elif not self.file:
            self.Success = False
            mes = _('Empty input is not allowed!')
            objs.mes(f,mes).warning()
        elif not os.path.exists(self.file):
            self.Success = False
            mes = _('File "{}" has not been found!').format(self.file)
            objs.mes(f,mes).warning()
        else:
            self.Success = False
            mes = _('Wrong input data!')
            objs.mes(f,mes).warning()

    def _read(self,encoding):
        try:
            with open(self.file,'r',encoding=encoding) as fl:
                self._text = fl.read()
        except:
            ''' We can handle UnicodeDecodeError here, however, we just
                handle them all (there could be access errors, etc.)
            '''
            pass

    def delete_bom(self):
        f = '[shared] logic.ReadTextFile.delete_bom'
        if self.Success:
            self._text = self._text.replace('\N{ZERO WIDTH NO-BREAK SPACE}','')
        else:
            com.cancel(f)

    # Return the text from memory (or load the file first)
    def get(self):
        f = '[shared] logic.ReadTextFile.get'
        if self.Success:
            if not self._text:
                self.load()
        else:
            com.cancel(f)
        return self._text

    # Return a number of lines in the file. Returns 0 for an empty file.
    def lines(self):
        f = '[shared] logic.ReadTextFile.lines'
        if self.Success:
            return len(self.list())
        else:
            com.cancel(f)

    def list(self):
        f = '[shared] logic.ReadTextFile.list'
        if self.Success:
            if not self._list:
                self._list = self.get().splitlines()
        else:
            com.cancel(f)
        # len(None) causes an error
        return self._list

    def load(self):
        f = '[shared] logic.ReadTextFile.load'
        if self.Success:
            mes = _('Load file "{}"').format(self.file)
            Message(f,mes).info()
            ''' We can try to define an encoding automatically, however,
                this often spoils some symbols, so we just proceed with
                try-except and the most popular encodings.
            '''
            self._read('UTF-8')
            if not self._text:
                self._read('windows-1251')
            if not self._text:
                self._read('windows-1252')
            if not self._text:
                ''' The file cannot be read OR the file is empty (we
                    don't need empty files)
                    #todo: Update the message
                '''
                self.Success = False
                mes = _('Unable to read file "{}"!').format(self.file)
                objs.mes(f,mes).warning()
            self.delete_bom()
        else:
            com.cancel(f)
        return self._text



class Input:

    def __init__(self,value,title='Input'):
        self.title = title
        self.value = value

    def check_float(self):
        if isinstance(self.value,float):
            return self.value
        else:
            mes = _('Float is required at input, but found "{}"! Return 0.0')
            mes = mes.format(self.value)
            objs.mes(self.title,mes).warning()
            self.value = 0.0
        return self.value
    
    def list(self):
        if isinstance(self.value,list):
            return self.value
        else:
            mes = _('Wrong input data!')
            objs.mes(self.title,mes,True).warning()
            return []
    
    def integer(self):
        if isinstance(self.value,int):
            return self.value
        elif str(self.value).isdigit():
            self.value = int(self.value)
            mes = _('Convert "{}" to an integer').format(self.value)
            objs.mes(self.title,mes,True).debug()
        else:
            mes = _('Integer is required at input, but found "{}"! Return 0')
            mes = mes.format(self.value)
            objs.mes(self.title,mes).warning()
            self.value = 0
        return self.value

    # Insert '' instead of 'None' into text widgets
    def not_none(self):
        if not self.value:
            self.value = ''
        return self.value



class Text:

    def __init__(self,text,Auto=False):
        self.text = text
        self.text = Input (title = 'Text.__init__'
                          ,value = self.text
                          ).not_none()
        # This can be useful in many cases, e.g. after OCR
        if Auto:
            ''' This will remove symbols that cannot be shown in Tcl/Tk.
                Since in many cases we build 'Words' from the text, we
                need to synchronize this.
            '''
            self.delete_unsupported()
            self.convert_line_breaks()
            self.strip_lines()
            self.delete_duplicate_line_breaks()
            self.tabs2spaces()
            self.trash()
            self.replace_x()
            self.delete_duplicate_spaces()
            self.yo()
            self.text = OCR(text=self.text).common()
            self.delete_space_with_punctuation()
            ''' This is necessary even if we do strip for each line (we
                need to strip '\n' at the beginning/end).
            '''
            self.text = self.text.strip()

    def has_digits(self):
        for sym in self.text:
            if sym in digits:
                return True
    
    def delete_comments(self):
        self.text = self.text.splitlines()
        self.text = [line for line in self.text \
                     if not line.startswith('#')
                    ]
        self.text = '\n'.join(self.text)
        return self.text
    
    # Getting rid of some useless symbols
    def trash(self):
        self.text = self.text.replace('· ','').replace('• ','').replace('¬','')
    
    def toggle_case(self):
        if self.text == self.text.lower():
            self.text = self.text.upper()
        else:
            self.text = self.text.lower()
        return self.text

    def quotations(self):
        self.text = re.sub(r'"([a-zA-Z\d\(\[\{\(])',r'“\1',self.text)
        self.text = re.sub(r'([a-zA-Z\d\.\?\!\)])"',r'\1”',self.text)
        self.text = re.sub(r'"(\.\.\.[a-zA-Z\d])',r'“\1',self.text)
        return self.text

    def delete_space_with_figure(self):
        expr = '[-\s]\d+'
        match = re.search(expr,self.text)
        while match:
            old = self.text
            self.text = self.text.replace(match.group(0),'')
            if old == self.text:
                break
            match = re.search(expr,self.text)
        return self.text

    def country(self):
        if len(self.text) > 4:
            if self.text[-4:-2] == ', ':
                if self.text[-1].isalpha() and self.text[-1].isupper() \
                and self.text[-2].isalpha() and self.text[-2].isupper():
                    return self.text[-2:]

    def reset(self,text):
        self.text = text

    def replace_x(self):
        # \xa0 is a non-breaking space in Latin1 (ISO 8859-1)
        self.text = self.text.replace('\xa0',' ').replace('\x07',' ')
        return self.text

    #todo: check
    def delete_alphabetic_numeration(self):
        my_expr = ' [\(,\[]{0,1}[aA-zZ,аА-яЯ][\.,\),\]]( \D)'
        match = re.search(my_expr,self.text)
        while match:
            self.text = self.text.replace(match.group(0),match.group(1))
            match = re.search(my_expr,self.text)
        return self.text

    def delete_embraced_text(self,opening_sym='(',closing_sym=')'):
        ''' If there are some brackets left after performing this
            operation, ensure that all of them are in the right place
            (even when the number of opening and closing brackets is
            the same).
        '''
        f = '[shared] logic.Text.delete_embraced_text'
        if self.text.count(opening_sym) == self.text.count(closing_sym):
            opening_parentheses = []
            closing_parentheses = []
            for i in range(len(self.text)):
                if self.text[i] == opening_sym:
                    opening_parentheses.append(i)
                elif self.text[i] == closing_sym:
                    closing_parentheses.append(i)

            min_val = min (len(opening_parentheses)
                          ,len(closing_parentheses)
                          )

            opening_parentheses = opening_parentheses[::-1]
            closing_parentheses = closing_parentheses[::-1]

            # Ignore non-matching parentheses
            i = 0
            while i < min_val:
                if opening_parentheses[i] >= closing_parentheses[i]:
                    del closing_parentheses[i]
                    i -= 1
                    min_val -= 1
                i += 1

            self.text = list(self.text)
            for i in range(min_val):
                if opening_parentheses[i] < closing_parentheses[i]:
                    self.text = self.text[0:opening_parentheses[i]] \
                                + self.text[closing_parentheses[i]+1:]
            self.text = ''.join(self.text)
            ''' Further steps: self.delete_duplicate_spaces(),
                self.text.strip()
            '''
        else:
            mes = _('Different number of opening and closing brackets: "{}": {}; "{}": {}!')
            mes = mes.format (opening_sym
                             ,self.text.count(opening_sym)
                             ,closing_sym
                             ,self.text.count(closing_sym)
                             )
            objs.mes(f,mes).warning()
        return self.text

    def convert_line_breaks(self):
        self.text = self.text.replace('\r\n','\n').replace('\r','\n')
        return self.text

    # Apply 'convert_line_breaks' first
    def delete_line_breaks(self):
        self.text = self.text.replace('\n',' ')
        return self.text

    def delete_duplicate_line_breaks(self):
        while '\n\n' in self.text:
            self.text = self.text.replace('\n\n','\n')
        return self.text

    def delete_duplicate_spaces(self):
        while '  ' in self.text:
            self.text = self.text.replace('  ',' ')
        return self.text

    def delete_end_punc(self,Extended=False):
        ''' Delete a space and punctuation marks in the end of a line
            (useful when extracting features with CompareField).
        '''
        f = '[shared] logic.Text.delete_end_punc'
        if len(self.text) > 0:
            if Extended:
                while self.text[-1] == ' ' or self.text[-1] \
                in punc_array or self.text[-1] in punc_ext_array:
                    self.text = self.text[:-1]
            else:
                while self.text[-1] == ' ' or self.text[-1] \
                in punc_array:
                    self.text = self.text[:-1]
        else:
            com.empty(f)
        return self.text

    def delete_figures(self):
        self.text = re.sub('\d+','',self.text)
        return self.text

    def delete_cyrillic(self):
        self.text = ''.join ([sym for sym in self.text if sym not \
                              in ru_alphabet
                             ]
                            )
        return self.text

    def delete_punctuation(self):
        for i in range(len(punc_array)):
            self.text = self.text.replace(punc_array[i],'')
        for i in range(len(punc_ext_array)):
            self.text = self.text.replace(punc_ext_array[i],'')
        return self.text

    def delete_space_with_punctuation(self):
        # Delete duplicate spaces first
        for i in range(len(punc_array)):
            self.text = self.text.replace (' ' + punc_array[i]
                                          ,punc_array[i]
                                          )
        self.text = self.text.replace('“ ','“').replace(' ”','”').replace('( ','(').replace(' )',')').replace('[ ','[').replace(' ]',']').replace('{ ','{').replace(' }','}')
        return self.text

    # Only for pattern '(YYYY-MM-DD)'
    def extract_date(self):
        expr = '\((\d\d\d\d-\d\d-\d\d)\)'
        if self.text:
            match = re.search(expr,self.text)
            if match:
                return match.group(1)

    def enclose(self,sym='"'):
        open_sym = close_sym = sym
        if sym == '(':
            close_sym = ')'
        elif sym == '[':
            close_sym = ']'
        elif sym == '{':
            close_sym = '}'
        elif sym == '“':
            close_sym = '”'
        elif sym == '«':
            close_sym = '»'
        self.text = open_sym + self.text + close_sym
        return self.text
    
    # Shorten a string up to a max length
    def shorten (self,max_len=10,Enclose=False
                ,FromEnd=False,ShowGap=True,sym='"'
                ):
        if len(self.text) > max_len:
            if Enclose:
                enc_len = 2 * len(sym)
                if max_len > enc_len:
                    max_len -= enc_len
            if ShowGap:
                if max_len > 3:
                    gap = '...'
                    max_len -= 3
                else:
                    gap = ''
            else:
                gap = ''
            if FromEnd:
                self.text = gap + self.text[len(self.text)-max_len:]
            else:
                self.text = self.text[0:max_len] + gap
        if Enclose:
            self.enclose(sym=sym)
        return self.text
        
    def grow(self,max_len=20,FromEnd=False,sym=' '):
        delta = max_len - len(self.text)
        if delta > 0:
            if FromEnd:
                self.text += delta * sym
            else:
                self.text = delta * sym + self.text
        return self.text
        
    def fit(self,max_len=20,FromEnd=False,sym=' '):
        self.shorten (max_len = max_len
                     ,FromEnd = FromEnd
                     ,ShowGap = False
                     )
        self.grow (max_len = max_len
                  ,FromEnd = FromEnd
                  ,sym     = sym
                  )
        return self.text

    def split_by_comma(self):
        ''' Replace commas or semicolons with line breaks or line breaks
            with commas.
        '''
        f = '[shared] logic.Text.split_by_comma'
        if (';' in self.text or ',' in self.text) and '\n' in self.text:
            mes = _('Commas and/or semicolons or line breaks can be used, but not altogether!')
            objs.mes(f,mes).warning()
        elif ';' in self.text or ',' in self.text:
            self.text = self.text.replace(',','\n')
            self.text = self.text.replace(';','\n')
            self.strip_lines()
        elif '\n' in self.text:
            self.delete_duplicate_line_breaks()
            # Delete a line break at the beginning/end
            self.text.strip()
            self.text = self.text.splitlines()
            for i in range(len(self.text)):
                self.text[i] = self.text[i].strip()
            self.text = ', '.join(self.text)
            if self.text.endswith(', '):
                self.text = self.text.strip(', ')
        return self.text

    def str2int(self):
        f = '[shared] logic.Text.str2int'
        par = 0
        try:
            par = int(self.text)
        except(ValueError,TypeError):
            mes = _('Failed to convert "{}" to an integer!')
            mes = mes.format(self.text)
            objs.mes(f,mes,True).warning()
        return par

    def str2float(self):
        f = '[shared] logic.Text.str2float'
        par = 0.0
        try:
            par = float(self.text)
        except(ValueError,TypeError):
            mes = _('Failed to convert "{}" to a floating-point number!')
            mes = mes.format(self.text)
            objs.mes(f,mes,True).warning()
        return par

    def strip_lines(self):
        self.text = self.text.splitlines()
        for i in range(len(self.text)):
            self.text[i] = self.text[i].strip()
        self.text = '\n'.join(self.text)
        return self.text

    def tabs2spaces(self):
        self.text = self.text.replace('\t',' ')
        return self.text

    # This allows to shorten dictionaries
    def yo(self):
        self.text = self.text.replace('Ё','Е')
        self.text = self.text.replace('ё','е')
        return self.text

    # Delete everything but alphas and digits
    def alphanum(self):
        self.text = ''.join([x for x in self.text if x.isalnum()])
        return self.text
        
    def has_latin(self):
        for sym in self.text:
            if sym in lat_alphabet:
                return True
                
    def has_cyrillic(self):
        for sym in self.text:
            if sym in ru_alphabet:
                return True
                
    def delete_unsupported(self):
        ''' Remove characters from a range not supported by Tcl 
            (and causing a Tkinter error).
        '''
        self.text = ''.join ([char for char in self.text if ord(char) \
                              in range(65536)
                             ]
                            )
        return self.text



class List:

    def __init__(self,lst1=[],lst2=[]):
        if lst1 is None:
            self.lst1 = []
        else:
            self.lst1 = list(lst1)
        if lst2 is None:
            self.lst2 = []
        else:
            self.lst2 = list(lst2)

    def shared(self):
        return [item for item in self.lst2 if item in self.lst1]
    
    # Check if 'lst1' fully comprises 'lst2'
    def eats(self):
        for item in self.lst2:
            if not item in self.lst1:
                return False
        return True
    
    def duplicates_low(self):
        ''' Remove (case-insensitively) duplicate items (positioned
            after original items). Both lists must consist of strings.
        '''
        cilst = [item.lower() for item in self.lst1]
        i = len(cilst) - 1
        while i >= 0:
            ind = cilst.index(cilst[i])
            if ind < i:
                del cilst[i]
                del self.lst1[i]
            i -= 1
        return self.lst1
    
    # Remove duplicate items (positioned after original items)
    def duplicates(self):
        i = len(self.lst1) - 1
        while i >= 0:
            ind = self.lst1.index(self.lst1[i])
            if ind < i:
                del self.lst1[i]
            i -= 1
        return self.lst1
    
    # Add a space where necessary and convert to a string
    def space_items(self,MultSpaces=False):
        text = ''
        for i in range(len(self.lst1)):
            if not self.lst1[i] == '':
                if text == '':
                    text += self.lst1[i]
                elif self.lst1[i] and self.lst1[i][0] in punc_array \
                or self.lst1[i][0] in '”»])}':
                    text += self.lst1[i]
                elif len(text) > 1 and text[-2].isspace() \
                and text[-1] == '"':
                    ''' We do not know for sure where quotes should be
                        placed, but we cannot leave out cases like ' " '
                    '''
                    text += self.lst1[i]
                elif len(text) > 1 and text[-2].isspace() \
                and text[-1] == "'":
                    text += self.lst1[i]
                # Only after "text == ''"
                elif text[-1] in '“«[{(':
                    text += self.lst1[i]
                elif text[-1].isspace() and self.lst1[i] \
                and self.lst1[i][0].isspace() and not MultSpaces:
                    tmp = self.lst1[i].lstrip()
                    if tmp:
                        text += tmp
                elif text[-1].isspace():
                    text += self.lst1[i]
                elif i == len(self.lst1) - 1 and self.lst1[i] \
                in punc_array:
                    text += self.lst1[i]
                # Do not allow ' "' in the end
                elif i == len(self.lst1) - 1 and self.lst1[i] \
                in ('”','»',']',')','}','"',"'"):
                    text += self.lst1[i]
                else:
                    text += ' ' + self.lst1[i]
        return text

    # Сделать списки, указанные на входе, одинаковой длины
    def equalize(self):
        max_range = max(len(self.lst1),len(self.lst2))
        if max_range == len(self.lst1):
            for i in range(len(self.lst1)-len(self.lst2)):
                self.lst2.append('')
        else:
            for i in range(len(self.lst2)-len(self.lst1)):
                self.lst1.append('')
        return(self.lst1,self.lst2)

    # Find different elements (strict order)
    # Based on http://stackoverflow.com/a/788780
    def diff(self):
        seqm = difflib.SequenceMatcher(a=self.lst1,b=self.lst2)
        output = []
        for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
            if opcode != 'equal':
                output += seqm.a[a0:a1]
        return output



class Time:
    ''' We constantly recalculate each value because they depend on each
        other.
    '''
    def __init__ (self,_timestamp=None,pattern='%Y-%m-%d'
                 ,MondayWarning=False
                 ):
        self.reset (_timestamp    = _timestamp
                   ,pattern       = pattern
                   ,MondayWarning = MondayWarning
                   )

    def reset (self,_timestamp=None,pattern='%Y-%m-%d'
              ,MondayWarning=False
              ):
        self.Success       = True
        self.pattern       = pattern
        self.MondayWarning = MondayWarning
        self._timestamp    = _timestamp
        self._instance = self._date = self._year = self._month_abbr \
                       = self._month_name = ''
        # Prevent recursion
        if self._timestamp is None:
            self.todays_date()
        else:
            self.instance()

    def add_days(self,days_delta):
        f = '[shared] logic.Time.add_days'
        if self.Success:
            if not self._instance:
                self.instance()
            try:
                self._instance += datetime.timedelta(days=days_delta)
            except:
                self.Success = False
                mes = _('Set time parameters are incorrect or not supported.')
                objs.mes(f,mes).warning()
            self.monday_warning()
        else:
            com.cancel(f)

    def date(self):
        f = '[shared] logic.Time.date'
        if self.Success:
            if not self._instance:
                self.instance()
            try:
                self._date = self._instance.strftime(self.pattern)
            except:
                self.Success = False
                mes = _('Set time parameters are incorrect or not supported.')
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)
        return self._date

    def instance(self):
        f = '[shared] logic.Time.instance'
        if self.Success:
            if self._timestamp is None:
                self.timestamp()
            try:
                self._instance = datetime.datetime.fromtimestamp(self._timestamp)
            except Exception as e:
                self.Success = False
                mes = _('Set time parameters are incorrect or not supported.\n\nDetails: {}')
                mes = mes.format(e)
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)
        return self._instance

    def timestamp(self):
        f = '[shared] logic.Time.timestamp'
        if self.Success:
            if not self._date:
                self.date()
            try:
                self._timestamp = time.mktime(datetime.datetime.strptime(self._date,self.pattern).timetuple())
            except:
                self.Success = False
                mes = _('Set time parameters are incorrect or not supported.')
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)
        return self._timestamp

    def monday_warning(self):
        f = '[shared] logic.Time.monday_warning'
        if self.Success:
            if not self._instance:
                self.instance()
            if self.MondayWarning \
            and datetime.datetime.weekday(self._instance) == 0:
                mes = _('Note: it will be Monday!')
                objs.mes(f,mes).info()
        else:
            com.cancel(f)

    def month_name(self):
        f = '[shared] logic.Time.month_name'
        if self.Success:
            if not self._instance:
                self.instance()
            self._month_name = calendar.month_name \
                             [Text (text = self._instance.strftime("%m")
                                   ,Auto = False
                                   ).str2int()
                             ]
        else:
            com.cancel(f)
        return self._month_name

    def localize_month_abbr(self):
        f = '[shared] logic.Time.localize_month_abbr'
        if self._month_abbr == 'Jan':
            self._month_abbr = _('Jan')
        elif self._month_abbr == 'Feb':
            self._month_abbr = _('Feb')
        elif self._month_abbr == 'Mar':
            self._month_abbr = _('Mar')
        elif self._month_abbr == 'Apr':
            self._month_abbr = _('Apr')
        elif self._month_abbr == 'May':
            self._month_abbr = _('May')
        elif self._month_abbr == 'Jun':
            self._month_abbr = _('Jun')
        elif self._month_abbr == 'Jul':
            self._month_abbr = _('Jul')
        elif self._month_abbr == 'Aug':
            self._month_abbr = _('Aug')
        elif self._month_abbr == 'Sep':
            self._month_abbr = _('Sep')
        elif self._month_abbr == 'Oct':
            self._month_abbr = _('Oct')
        elif self._month_abbr == 'Nov':
            self._month_abbr = _('Nov')
        elif self._month_abbr == 'Dec':
            self._month_abbr = _('Dec')
        else:
            mes = _('Wrong input data!')
            objs.mes(f,mes,True).warning()
        return self._month_abbr
    
    def month_abbr(self):
        f = '[shared] logic.Time.month_abbr'
        if self.Success:
            if not self._instance:
                self.instance()
            self._month_abbr = calendar.month_abbr \
                             [Text (text = self._instance.strftime("%m")
                                   ,Auto = False
                                   ).str2int()
                             ]
        else:
            com.cancel(f)
        return self._month_abbr

    def todays_date(self):
        self._instance = datetime.datetime.today()

    def year(self):
        f = '[shared] logic.Time.year'
        if self.Success:
            if not self._instance:
                self.instance()
            try:
                self._year = self._instance.strftime("%Y")
            except:
                self.Success = False
                mes = _('Set time parameters are incorrect or not supported.')
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)
        return self._year



class File:

    def __init__(self,file,dest=None,Rewrite=False):
        f = '[shared] logic.File.__init__'
        self.Success = True
        self.Rewrite = Rewrite
        self.file    = file
        self.dest    = dest
        # This will allow to skip some checks for destination
        if not self.dest:
            self.dest = self.file
        self.atime = ''
        self.mtime = ''
        # This already checks existence
        if self.file and os.path.isfile(self.file):
            ''' If the destination directory does not exist, this will
                be caught in try-except while copying/moving
            '''
            if os.path.isdir(self.dest):
                self.dest = os.path.join (self.dest
                                         ,Path(self.file).basename()
                                         )
        elif not self.file:
            self.Success = False
            mes = _('Empty input is not allowed!')
            objs.mes(f,mes).warning()
        elif not os.path.exists(self.file):
            self.Success = False
            mes = _('File "{}" has not been found!').format(self.file)
            objs.mes(f,mes).warning()
        else:
            self.Success = False
            mes = _('The object "{}" is not a file!').format(self.file)
            objs.mes(f,mes).warning()

    def size(self,Follow=True):
        f = '[shared] logic.File.size'
        result = 0
        if self.Success:
            try:
                if Follow:
                    cond = not os.path.islink(self.file)
                else:
                    cond = True
                if cond:
                    result = os.path.getsize(self.file)
            except Exception as e:
                ''' Along with other errors, 'No such file or directory'
                    error will be raised if Follow=False and this is
                    a broken symbolic link.
                '''
                mes = _('Operation has failed!\nDetails: {}').format(e)
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)
        return result
    
    def _copy(self):
        f = '[shared] logic.File._copy'
        Success = True
        mes = _('Copy "{}" to "{}"').format(self.file,self.dest)
        objs.mes(f,mes,True).info()
        try:
            shutil.copyfile(self.file,self.dest)
        except:
            Success = False
            mes = _('Failed to copy file "{}" to "{}"!')
            mes = mes.format(self.file,self.dest)
            objs.mes(f,mes).error()
        return Success

    def _move(self):
        f = '[shared] logic.File._move'
        Success = True
        mes = _('Move "{}" to "{}"').format(self.file,self.dest)
        objs.mes(f,mes,True).info()
        try:
            shutil.move(self.file,self.dest)
        except:
            Success = False
            mes = _('Failed to move "{}" to "{}"!')
            mes = mes.format(self.file,self.dest)
            objs.mes(f,mes).error()
        return Success

    def access_time(self):
        f = '[shared] logic.File.access_time'
        if self.Success:
            try:
                self.atime = os.path.getatime(self.file)
                # Further steps: datetime.date.fromtimestamp(self.atime).strftime(self.pattern)
                return self.atime
            except:
                mes = _('Failed to get the date of the file "{}"!')
                mes = mes.format(self.file)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)

    def copy(self):
        f = '[shared] logic.File.copy'
        Success = True
        if self.Success:
            if self.file.lower() == self.dest.lower():
                mes = _('Unable to copy the file "{}" to iself!')
                mes = mes.format(self.file)
                objs.mes(f,mes).error()
            elif com.rewrite (file    = self.dest
                             ,Rewrite = self.Rewrite
                             ):
                Success = self._copy()
            else:
                mes = _('Operation has been canceled by the user.')
                objs.mes(f,mes,True).info()
        else:
            com.cancel(f)
        return Success

    def delete(self):
        f = '[shared] logic.File.delete'
        Success = True
        if self.Success:
            mes = _('Delete "{}"').format(self.file)
            objs.mes(f,mes,True).info()
            try:
                os.remove(self.file)
            except:
                Success = False
                mes = _('Failed to delete file "{}"!').format(self.file)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)
        return Success

    def modification_time(self):
        f = '[shared] logic.File.modification_time'
        if self.Success:
            try:
                self.mtime = os.path.getmtime(self.file)
                # Further steps: datetime.date.fromtimestamp(self.mtime).strftime(self.pattern)
                return self.mtime
            except:
                mes = _('Failed to get the date of the file "{}"!')
                mes = mes.format(self.file)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)

    def move(self):
        f = '[shared] logic.File.move'
        Success = True
        if self.Success:
            if self.file.lower() == self.dest.lower():
                mes = _('Moving is not necessary, because the source and destination are identical ({}).')
                mes = mes.format(self.file)
                objs.mes(f,mes).warning()
            elif com.rewrite (file    = self.dest
                             ,Rewrite = self.Rewrite
                             ):
                Success = self._move()
            else:
                mes = _('Operation has been canceled by the user.')
                objs.mes(f,mes,True).info()
        else:
            com.cancel(f)
        return Success

    def set_time(self):
        f = '[shared] logic.File.set_time'
        if self.Success:
            if self.atime and self.mtime:
                mes = _('Change the time of the file "{}" to {}')
                mes = mes.format(self.file,(self.atime,self.mtime))
                objs.mes(f,mes,True).info()
                try:
                    os.utime(self.file,(self.atime,self.mtime))
                except:
                    mes = _('Failed to change the time of the file "{}" to "{}"!')
                    mes = mes.format(self.file,(self.atime,self.mtime))
                    objs.mes(f,mes).error()
        else:
            com.cancel(f)



class Path:

    def __init__(self,path):
        self.reset(path)

    def free_space(self):
        f = '[shared] logic.Path.free_space'
        result = 0
        if self.path:
            if os.path.exists(self.path):
                try:
                    istat  = os.statvfs(self.path)
                    result = istat.f_bavail * istat.f_bsize
                except Exception as e:
                    mes = _('Operation has failed!\nDetails: {}')
                    mes = mes.format(e)
                    objs.mes(f,mes).error()
            else:
                mes = _('Wrong input data: "{}"!').format(self.path)
                objs.mes(f,mes).warning()
        else:
            com.empty(f)
        return result
    
    def _splitpath(self):
        if not self._split:
            self._split = os.path.splitext(self.basename())
        return self._split

    def basename(self):
        if not self._basename:
            self._basename = os.path.basename(self.path)
        return self._basename

    # This will recursively (by design) create self.path
    def create(self):
        f = '[shared] logic.Path.create'
        # We actually don't need to fail the class globally
        Success = True
        if self.path:
            if os.path.exists(self.path):
                if os.path.isdir(self.path):
                    mes = _('Directory "{}" already exists.')
                    mes = mes.format(self.path)
                    objs.mes(f,mes,True).info()
                else:
                    Success = False
                    mes = _('The path "{}" is invalid!')
                    mes = mes.format(self.path)
                    objs.mes(f,mes).warning()
            else:
                mes = _('Create directory "{}"').format(self.path)
                objs.mes(f,mes,True).info()
                try:
                    #todo: consider os.mkdir
                    os.makedirs(self.path)
                except:
                    Success = False
                    mes = _('Failed to create directory "{}"!')
                    mes = mes.format(self.path)
                    objs.mes(f,mes).error()
        else:
            Success = False
            com.empty(f)
        return Success

    def delete_inappropriate_symbols(self):
        ''' These symbols may pose a problem while opening files
            #todo: check whether this is really necessary
        '''
        return self.filename().replace("'",'').replace("&",'')

    def dirname(self):
        if not self._dirname:
            self._dirname = os.path.dirname(self.path)
        return self._dirname

    # In order to use xdg-open, we need to escape some characters first
    def escape(self):
        self.path = shlex.quote(self.path)
        return self.path

    # An extension with a dot
    def extension(self):
        if not self._extension:
            if len(self._splitpath()) > 1:
                self._extension = self._splitpath()[1]
        return self._extension

    def filename(self):
        if not self._filename:
            if len(self._splitpath()) >= 1:
                self._filename = self._splitpath()[0]
        return self._filename

    def reset(self,path):
        # Prevent 'NoneType'
        if path:
            self.path = path
        else:
            self.path = ''
        ''' Building paths in Windows:
            - Use raw strings (e.g., set path as r'C:\1.txt')
            - Use os.path.join(mydir,myfile) or os.path.normpath(path)
              instead of os.path.sep
            - As an alternative, import ntpath, posixpath
        '''
        ''' We remove a separator from the end, because basename and
            dirname work differently in this case ('' and the last
            directory, correspondingly)
        '''
        if self.path != '/':
            self.path = self.path.rstrip('//')
        self._basename = self._dirname = self._extension \
                       = self._filename = self._split = self._date = ''
        self.parts     = []

    def split(self):
        if not self.parts:
            #todo: use os.path.split
            self.parts = self.path.split(os.path.sep)
            i = 0
            tmp_str = ''
            while i < len(self.parts):
                if self.parts[i]:
                    self.parts[i] = tmp_str + self.parts[i]
                    tmp_str = ''
                else:
                    tmp_str += os.path.sep
                    del self.parts[i]
                    i -= 1
                i += 1
        return self.parts



class WriteBinary:

    def __init__(self,file,obj,Rewrite=True):
        f = '[shared] logic.WriteBinary.__init__'
        self.Success = True
        self.file    = file
        self.obj     = obj
        if self.file and self.obj:
            self.Rewrite = Rewrite
            self.fragm   = None
        else:
            self.Success = False
            com.empty(f)

    def _write(self,mode='w+b'):
        f = '[shared] logic.WriteBinary._write'
        mes = _('Write file "{}"').format(self.file)
        objs.mes(f,mes,True).info()
        if mode == 'w+b' or mode == 'a+b':
            try:
                with open(self.file,mode) as fl:
                    if mode == 'w+b':
                        pickle.dump(self.obj,fl)
                    elif mode == 'a+b':
                        pickle.dump(self.fragm,fl)
            except:
                self.Success = False
                mes = _('Unable to write file "{}"!').format(self.file)
                objs.mes(f,mes).error()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode,'w+b, a+b')
            objs.mes(f,mes).error()

    def append(self,fragm):
        f = '[shared] logic.WriteBinary.append'
        if self.Success:
            self.fragm = fragm
            if self.fragm:
                self._write(mode='a+b')
            else:
                com.empty(f)
        else:
            com.cancel(f)

    def write(self):
        f = '[shared] logic.WriteBinary.write'
        if self.Success:
            if com.rewrite (file    = self.file
                           ,Rewrite = self.Rewrite
                           ):
                self._write(mode='w+b')
            else:
                mes = _('Operation has been canceled by the user.')
                Message(f,mes).info()
        else:
            com.cancel(f)



class Dic:

    def __init__(self,file,Sortable=False):
        self.file     = file
        self.Sortable = Sortable
        self.errors   = []
        self.iread    = ReadTextFile(self.file)
        self.reset()

    def _delete_duplicates(self):
        ''' This is might be needed only for those dictionaries that
            already may contain duplicates (dictionaries with newly
            added entries do not have duplicates due to new algorithms).
        '''
        f = '[shared] logic.Dic._delete_duplicates'
        if self.Success:
            if self.Sortable:
                old = self.lines()
                self._list = list(set(self.list()))
                new = self._lines = len(self._list)
                mes = _('Entries deleted: {} ({}-{})')
                mes = mes.format(old-new,old,new)
                objs.mes(f,mes,True).info()
                self.text = '\n'.join(self._list)
                # Update original and translation
                self._split()
                # After using set(), the original order was lost
                self.sort()
            else:
                mes = _('File "{}" is not sortable!').format(self.file)
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)

    # We can use this as an updater, even without relying on Success
    def _join(self):
        f = '[shared] logic.Dic._join'
        if len(self.orig) == len(self.transl):
            self._lines = len(self.orig)
            self._list = []
            for i in range(self._lines):
                self._list.append(self.orig[i]+'\t'+self.transl[i])
            self.text = '\n'.join(self._list)
        else:
            mes = _('Wrong input data!')
            objs.mes(f,mes).warning()

    def _split(self):
        ''' We can use this to check integrity and/or update original
            and translation lists.
        '''
        if self.get():
            self.Success = True
            self.orig    = []
            self.transl  = []
            ''' Building lists takes ~0.1 longer without temporary
                variables (now self._split() takes ~0.256)
            '''
            for i in range(self._lines):
                tmp_lst = self._list[i].split('\t')
                if len(tmp_lst) == 2:
                    self.orig.append(tmp_lst[0])
                    self.transl.append(tmp_lst[1])
                else:
                    ''' Lines that were successfully parsed can be
                        further processed upon correcting 'self.lines'
                    '''
                    self.Success = False
                    self.errors.append(str(i))
            self.warn()
            if not self.orig or not self.transl:
                self.Success = False
        else:
            self.Success = False
            
    def warn(self):
        f = '[shared] logic.Dic.warn'
        if self.errors:
            message = ', '.join(self.errors)
            mes = _('The following lines cannot be parsed:')
            mes += '\n' + message
            objs.mes(f,mes).warning()

    def append(self,original,translation):
        ''' #todo: write a dictionary in an append mode after appending
                   to memory.
            #todo: skip repetitions
        '''
        f = '[shared] logic.Dic.append'
        if self.Success:
            if original and translation:
                self.orig.append(original)
                self.transl.append(translation)
                self._join()
            else:
                com.empty(f)
        else:
            com.cancel(f)

    # Count from 1
    def delete_entry(self,entry_no):
        ''' #todo: fix: an entry which is only one in a dictionary is
            not deleted.
        '''
        f = '[shared] logic.Dic.delete_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.lines():
                del self.orig[entry_no]
                del self.transl[entry_no]
                self._join()
            else:
                sub = '0 <= {} < {}'.format(entry_no,self.lines())
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)

    # Count from 1
    def edit_entry(self,entry_no,orig,transl):
        ''' #todo: Add checking orig and transl (where needed) for
            a wrapper function.
        '''
        f = '[shared] logic.Dic.edit_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.lines():
                self.orig[entry_no] = orig
                self.transl[entry_no] = transl
                self._join()
            else:
                sub = '0 <= {} < {}'.format(entry_no,self.lines())
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)

    def get(self):
        if not self.text:
            self.text = self.iread.load()
        return self.text

    def lines(self):
        if self._lines == 0:
            self._lines = len(self.list())
        return self._lines

    def list(self):
        if not self._list:
            self._list = self.get().splitlines()
        return self._list

    def reset(self):
        self.text   = self.iread.load()
        self.orig   = []
        self.transl = []
        self._list  = self.get().splitlines()
        # Delete empty and commented lines
        self._list  = [line for line in self._list if line \
                       and not line.startswith('#')
                      ]
        self.text   = '\n'.join(self._list)
        self._lines = len(self._list)
        self._split()

    # Sort a dictionary with the longest lines going first
    def sort(self):
        f = '[shared] logic.Dic.sort'
        if self.Success:
            if self.Sortable:
                tmp_list = []
                for i in range(len(self._list)):
                    tmp_list += [[len(self.orig[i])
                                 ,self.orig[i]
                                 ,self.transl[i]
                                 ]
                                ]
                tmp_list.sort(key=lambda x: x[0],reverse=True)
                for i in range(len(self._list)):
                    self.orig[i] = tmp_list[i][1]
                    self.transl[i] = tmp_list[i][2]
                    self._list[i] = self.orig[i] + '\t' + self.transl[i]
                self.text = '\n'.join(self._list)
            else:
                mes = _('File "{}" is not sortable!').format(self.file)
                objs.mes(f,mes).warning()
        else:
            com.cancel(f)

    def tail(self):
        f = '[shared] logic.Dic.tail'
        tail_text = ''
        if self.Success:
            tail_len = globs['int']['tail_len']
            if tail_len > self.lines():
                tail_len = self.lines()
            i = self.lines() - tail_len
            # We count from 1, therefore it is < and not <=
            while i < self.lines():
                # i+1 by the same reason
                tail_text += str(i+1) + ':' + '"' + self.list()[i] \
                             + '"\n'
                i += 1
        else:
            com.cancel(f)
        return tail_text

    def write(self):
        f = '[shared] logic.Dic.write'
        if self.Success:
            WriteTextFile (file    = self.file
                          ,Rewrite = True
                          ).write(self.get())
        else:
            com.cancel(f)



class ReadBinary:

    def __init__(self,file):
        self.file    = file
        self.obj     = None
        h_file       = File(self.file)
        self.Success = h_file.Success

    def _load(self):
        f = '[shared] logic.ReadBinary._load'
        mes = _('Load file "{}"').format(self.file)
        objs.mes(f,mes,True).info()
        try:
            ''' AttributeError means that a module using _load does not
                have a class that was defined while creating the binary
            '''
            with open(self.file,'r+b') as fl:
                self.obj = pickle.load(fl)
        except Exception as e:
            self.Success = False
            mes = _('Unable to read file "{}"!\n\nDetails: {}')
            mes = mes.format(self.file,e)
            objs.mes(f,mes).error()

    #todo: load fragments appended to a binary
    def load(self):
        f = '[shared] logic.ReadBinary.load'
        if self.Success:
            self._load()
        else:
            com.cancel(f)
        return self.obj

    def get(self):
        if not self.obj:
            self.load()
        return self.obj



# Do not forget to import this class if it was used to pickle an object
class CreateInstance:
    pass



#todo: fix: does not work with a root dir ('/')
class Directory:

    def __init__(self,path,dest=''):
        f = '[shared] logic.Directory.__init__'
        self.values()
        if path:
            ''' Remove trailing slashes and follow symlinks. No error is
                thrown for broken symlinks, but further checks will fail
                for them. Failing a real path (e.g., pointing to
                the volume that is not mounted yet) is more
                apprehensible than failing a symlink.
            '''
            self.dir = os.path.realpath(path)
        else:
            self.dir = ''
        if dest:
            self.dest = Path(dest).path
        else:
            self.dest = self.dir
        if not os.path.isdir(self.dir):
            self.Success = False
            mes = _('Wrong input data: "{}"!').format(self.dir)
            objs.mes(f,mes).warning()

    def size(self,Follow=True):
        f = '[shared] logic.Directory.size'
        result = 0
        if self.Success:
            try:
                for dirpath, dirnames, filenames in os.walk(self.dir):
                    for name in filenames:
                        obj = os.path.join(dirpath,name)
                        if Follow:
                            cond = not os.path.islink(obj)
                        else:
                            cond = True
                        if cond:
                            result += os.path.getsize(obj)
            except Exception as e:
                ''' Along with other errors, 'No such file or directory'
                    error will be raised if Follow=False and there are
                    broken symbolic links.
                '''
                mes = _('Operation has failed!\nDetails: {}').format(e)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)
        return result
    
    def values(self):
        self.Success = True
        # Assigning lists must be one per line
        self._list           = []
        self._rel_list       = []
        self._files          = []
        self._rel_files      = []
        self._dirs           = []
        self._rel_dirs       = []
        self._extensions     = []
        self._extensions_low = []
    
    def extensions(self): # with a dot
        f = '[shared] logic.Directory.extensions'
        if self.Success:
            if not self._extensions:
                for file in self.rel_files():
                    ext = Path(path=file).extension()
                    self._extensions.append(ext)
                    self._extensions_low.append(ext.lower())
        else:
            com.cancel(f)
        return self._extensions

    def extensions_low(self): # with a dot
        f = '[shared] logic.Directory.extensions_low'
        if self.Success:
            if not self._extensions_low:
                self.extensions()
        else:
            com.cancel(f)
        return self._extensions_low

    def delete_empty(self):
        f = '[shared] logic.Directory.delete_empty'
        if self.Success:
            # Do not delete nested folders
            if not os.listdir(self.dir):
                self.delete()
        else:
            com.cancel(f)
    
    def delete(self):
        f = '[shared] logic.Directory.delete'
        if self.Success:
            mes = _('Delete "{}"').format(self.dir)
            objs.mes(f,mes,True).info()
            try:
                shutil.rmtree(self.dir)
            except:
                mes = _('Failed to delete directory "{}"! Delete it manually.')
                mes = mes.format(self.dir)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)

    # Create a list of objects with a relative path
    def rel_list(self):
        if self.Success:
            if not self._rel_list:
                self.list()
        return self._rel_list

    # Create a list of objects with an absolute path
    def list(self):
        f = '[shared] logic.Directory.list'
        if self.Success:
            if not self._list:
                self._list = os.listdir(self.dir)
                self._list.sort(key=lambda x: x.lower())
                self._rel_list = list(self._list)
                for i in range(len(self._list)):
                    self._list[i] = os.path.join(self.dir,self._list[i])
        else:
            com.cancel(f)
        return self._list

    def rel_dirs(self):
        if self.Success:
            if not self._rel_dirs:
                self.dirs()
        return self._rel_dirs

    def rel_files(self):
        if self.Success:
            if not self._rel_files:
                self.files()
        return self._rel_files

    # Needs absolute path
    def dirs(self):
        f = '[shared] logic.Directory.dirs'
        if self.Success:
            if not self._dirs:
                for i in range(len(self.list())):
                    if os.path.isdir(self._list[i]):
                        self._dirs.append(self._list[i])
                        self._rel_dirs.append(self._rel_list[i])
        else:
            com.cancel(f)
        return self._dirs

    # Needs absolute path
    def files(self):
        f = '[shared] logic.Directory.files'
        if self.Success:
            if not self._files:
                for i in range(len(self.list())):
                    if os.path.isfile(self._list[i]):
                        self._files.append(self._list[i])
                        self._rel_files.append(self._rel_list[i])
        else:
            com.cancel(f)
        return self._files

    def copy(self):
        f = '[shared] logic.Directory.copy'
        if self.Success:
            if self.dir.lower() == self.dest.lower():
                mes = _('Unable to copy "{}" to iself!').format(self.dir)
                objs.mes(f,mes).error()
            elif os.path.isdir(self.dest):
                mes = _('Directory "{}" already exists.')
                mes = mes.format(self.dest)
                objs.mes(f,mes).info()
            else:
                self._copy()
        else:
            com.cancel(f)

    def _copy(self):
        f = '[shared] logic.Directory._copy'
        mes = _('Copy "{}" to "{}"').format(self.dir,self.dest)
        objs.mes(f,mes,True).info()
        try:
            shutil.copytree(self.dir,self.dest)
        except:
            self.Success = False
            mes = _('Failed to copy "{}" to "{}"!')
            mes = mes.format(self.dir,self.dest)
            objs.mes(f,mes).error()



class Config:

    def __init__(self):
        self.values()
        
    def values(self):
        self.Success          = True
        self.sections         = [SectionVariables]
        self.sections_abbr    = [SectionVariables_abbr]
        self.sections_func    = [config_parser.get]
        self.message          = _('The following sections and/or keys are missing:') + '\n'
        self.total_keys       = 0
        self.changed_keys     = 0
        self.missing_keys     = 0
        self.missing_sections = 0

    def load(self):
        f = '[shared] logic.Config.load'
        if self.Success:
            for i in range(len(self.sections)):
                for option in globs[self.sections_abbr[i]]:
                    new_val = self.sections_func[i](self.sections[i],option)
                    if globs[self.sections_abbr[i]][option] != new_val:
                        mes = _('New value of the key "{}" has been loaded.')
                        mes = mes.format(option)
                        Message(f,mes).info()
                        self.changed_keys += 1
                        globs[self.sections_abbr[i]][option] = new_val
            mes = _('Keys loaded in total: {}, whereas {} are modified.')
            mes = mes.format(self.total_keys,self.changed_keys)
            Message(f,mes).info()
        else:
            com.cancel(f)

    def check(self):
        f = '[shared] logic.Config.check'
        if self.Success:
            for i in range(len(self.sections)):
                if config_parser.has_section(self.sections[i]):
                    for option in globs[self.sections_abbr[i]]:
                        self.total_keys += 1
                        if not config_parser.has_option(self.sections[i]
                                                       ,option
                                                       ):
                            self.Success = False
                            self.missing_keys += 1
                            self.message += option + '; '
                else:
                    self.Success = False
                    self.missing_sections += 1
                    self.message += self.sections[i] + '; '
            if not self.Success:
                self.message += '\n'
                self.message += _('Missing sections: {}').format(self.missing_sections)
                self.message += '\n'
                self.message += _('Missing keys: {}').format(self.missing_keys)
                self.message += '\n'
                self.message += _('The default configuration has been loaded.')
                #cur
                #todo: set as GUI
                Message(f,self.message).warning()
                self._default()
        else:
            com.cancel(f)

    def open(self):
        f = '[shared] logic.Config.open'
        if self.Success:
            try:
                config_parser.read(self.path,'utf-8')
            except:
                Success = False
                mes = _('Failed to read the configuration file "{}". This file must share the same directory with the program and have UTF-8 encoding (no BOM) and UNIX line break type.')
                mes = mes.format(self.path)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)



class Online:
    ''' If you get 'TypeError("quote_from_bytes() expected bytes")',
        then you probably forgot to call 'self.reset' here or
        in children classes.
    '''
    def __init__ (self,base_str='%s',search_str=''
                 ,encoding='UTF-8'
                 ):
        self.reset (base_str   = base_str
                   ,search_str = search_str
                   ,encoding   = encoding
                   )

    def get_bytes(self):
        if not self._bytes:
            self._bytes = bytes (self.search_str
                                ,encoding = self.encoding
                                )
        return self._bytes

    # Open a URL in a default browser
    def browse(self):
        f = '[shared] logic.Online.browse'
        try:
            webbrowser.open (url       = self.url()
                            ,new       = 2
                            ,autoraise = True
                            )
        except Exception as e:
            mes = _('Failed to open URL "{}" in a default browser!\n\nDetails: {}')
            mes = mes.format(self._url,e)
            objs.mes(f,mes).error()

    # Create a correct online link (URI => URL)
    def url(self):
        f = '[shared] logic.Online.url'
        if not self._url:
            self._url = self.base_str % urllib.parse.quote(self.get_bytes())
            mes = str(self._url)
            objs.mes(f,mes,True).debug()
        return self._url

    def reset (self,base_str='',search_str=''
              ,encoding='UTF-8'
              ):
        self._bytes     = None
        self._url       = None
        self.encoding   = encoding
        self.base_str   = base_str
        self.search_str = search_str



class Diff:

    def __init__(self,text1='',text2='',file=None):
        self.Custom     = False
        ''' Some browsers update web-page as soon as we rewrite it, and
            some even do not open the same file again. So, we have to
            create a new temporary file each time.
        '''
        self.wda_html   = com.tmpfile(suffix='.htm',Delete=0)
        self.iwda_write = WriteTextFile (file    = self.wda_html
                                        ,Rewrite = True
                                        )
        if text1 or text2:
            self.reset (text1 = text1
                       ,text2 = text2
                       ,file  = file
                       )

    def reset(self,text1,text2,file=None):
        self._diff = ''
        self.text1 = text1
        self.text2 = text2
        if file:
            self.Custom  = True
            self.file    = file
            self._header = ''
            self.iwrite  = WriteTextFile (file    = self.file
                                         ,Rewrite = False
                                         )
            self.ipath   = Path(self.file)
        else:
            self.Custom  = False
            self.file    = self.wda_html
            self._header = '<title>%s</title>' % _('Differences:')
            self.iwrite  = self.iwda_write
        return self

    def diff(self):
        self.text1 = self.text1.split(' ')
        self.text2 = self.text2.split(' ')
        self._diff = difflib.HtmlDiff().make_file(self.text1,self.text2)
        # Avoid a bug in HtmlDiff()
        self._diff = self._diff.replace ('charset=ISO-8859-1'
                                        ,'charset=UTF-8'
                                        )

    def header(self):
        if self.Custom:
            self._header = self.ipath.basename().replace(self.ipath.extension(),'')
            self._header = '<title>' + self._header + '</title>'
        self._diff = self._diff.replace('<title></title>',self._header)\
                     + '\n'

    def compare(self):
        f = '[shared] logic.Diff.compare'
        if self.text1 and self.text2:
            if self.text1 == self.text2:
                mes = _('Texts are identical!')
                objs.mes(f,mes).info()
            else:
                self.diff()
                self.header()
                self.iwrite.write(self._diff)
                if self.iwrite.Success:
                    ''' Cannot reuse the class instance because the
                        temporary file might be missing
                    '''
                    Launch(target=self.file).default()
        else:
            com.empty(f)



class Shortcut:

    def __init__(self,symlink='',path=''):
        f = '[shared] logic.Shortcut.__init__'
        self.Success = True
        self.path    = path
        self.symlink = symlink
        if not self.path and not self.symlink:
            self.Success = False
            mes = _('Wrong input data!')
            objs.mes(f,mes).warning()

    # http://timgolden.me.uk/python/win32_how_do_i/read-a-shortcut.html
    def _get_win(self):
        link = pythoncom.CoCreateInstance (win32com.shell.shell.CLSID_ShellLink
                                          ,None
                                          ,pythoncom.CLSCTX_INPROC_SERVER
                                          ,win32com.shell.shell.IID_IShellLink
                                          )
        link.QueryInterface(pythoncom.IID_IPersistFile).Load(self.symlink)
        ''' GetPath returns the name and a WIN32_FIND_DATA structure
            which we're ignoring. The parameter indicates whether
            shortname, UNC or the "raw path" are to be returned.
            Bizarrely, the docs indicate that the flags can be combined.
        '''
        self.path,_=link.GetPath(win32com.shell.shell.SLGP_UNCPRIORITY)

    def _get_unix(self):
        self.path = os.path.realpath(self.symlink)

    def get(self):
        if self.Success and not self.path:
            if objs.os().win():
                self._get_win()
            else:
                self._get_unix()
        return self.path

    def _delete(self):
        f = '[shared] logic.Shortcut._delete'
        mes = _('Delete the symbolic link "{}"').format(self.symlink)
        objs.mes(f,mes,True).info()
        try:
            os.unlink(self.symlink)
        except:
            mes = _('Failed to remove shortcut "{}". Remove it manually and press OK.')
            mes = mes.format(self.symlink)
            objs.mes(f,mes).error()

    def delete(self):
        f = '[shared] logic.Shortcut.delete'
        if self.Success:
            if os.path.islink(self.symlink):
                self._delete()
        else:
            com.cancel(f)

    def _create_unix(self):
        f = '[shared] logic.Shortcut._create_unix'
        mes = _('Create a symbolic link "{}"').format(self.symlink)
        objs.mes(f,mes,True).info()
        try:
            os.symlink(self.path,self.symlink)
        except:
            mes = _('Failed to create shortcut "{}". Create it manually and press OK.')
            mes = mes.format(self.symlink)
            objs.mes(f,mes).error()

    def create_unix(self):
        f = '[shared] logic.Shortcut.create_unix'
        self.delete()
        if os.path.exists(self.symlink):
            if os.path.islink(self.symlink):
                com.lazy(f)
            else:
                self.Success = False
                mes = _('Wrong input data!')
                objs.mes(f,mes).warning()
        else:
            self._create_unix()

    def _create_win(self):
        f = '[shared] logic.Shortcut._create_win'
        mes = _('Create a symbolic link "{}"').format(self.symlink)
        objs.mes(f,mes,True).info()
        try:
            # The code will automatically add '.lnk' if necessary
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(self.symlink)
            shortcut.Targetpath = self.path
            shortcut.save()
        except:
            mes = _('Failed to create shortcut "{}". Create it manually and press OK.')
            mes = mes.format(self.symlink)
            objs.mes(f,mes).error()

    def create_win(self):
        ''' Using python 3 and windows (since 2009) it is possible to
            create a symbolic link, however, this will not be the same
            as a shortcut (.lnk). Therefore, in case the shortcut is
            used, os.path.islink() will always return False (not
            supported) (must use os.path.exists()), however, os.unlink()
            will work as expected.
        '''
        # Do not forget: windows paths must have a double backslash!
        f = '[shared] logic.Shortcut.create_win'
        if self.Success:
            if not Path(self.symlink).extension().lower() == '.lnk':
                self.symlink += '.lnk'
            self.delete()
            if os.path.exists(self.symlink):
                com.lazy(f)
            else:
                self._create_win()
        else:
            com.cancel(f)

    def create(self):
        f = '[shared] logic.Shortcut.create'
        if self.Success:
            if objs.os().win():
                self.create_win()
            else:
                self.create_unix()
        else:
            com.cancel(f)



class Email:
    ''' Invoke a default email client with the required input.
        Since there is no conventional way to programatically add
        an attachment in the default email client, we attempt to call
        Thunderbird, then Outlook, and finally mailto.
        Using 'webbrowser.open' has the following shortcomings:
        - A web browser is used to parse 'mailto' (we need to launch it
          first)
        - Instead of passing arguments to a mail agent, the web browser
          can search all input online which is a security breach
        - (AFAIK) Using this method, there is no standard way to add
          an attachment. Currently, I managed to add attachments only
          using CentOS6 + Palemoon + Thunderbird.
    '''
    def __init__ (self,email='',subject=''
                 ,message='',attachment=''
                 ):
        if email:
            self.reset (email      = email
                       ,subject    = subject
                       ,message    = message
                       ,attachment = attachment
                       )
    
    def reset (self,email,subject=''
              ,message='',attachment=''
              ):
        f = '[shared] logic.Email.reset'
        self.Success = True
        ''' A single address or multiple comma-separated addresses (not
            all mail agents support ';'). #note that, however, Outlook
            supports ONLY ';' and Evolution - only ','!
        '''
        self._email   = email
        self._subject = Input (title = f
                              ,value = subject
                              ).not_none()
        self._message = Input (title = f
                              ,value = message
                              ).not_none()
        self._attachment = attachment
        if not self._email:
            self.Success = False
            com.empty(f)
        if self._attachment:
            self.Success = File(file=self._attachment).Success
            if not self.Success:
                com.cancel(f)

    # Screen symbols that may cause problems when composing 'mailto'
    def sanitize(self,value):
        f = '[shared] logic.Email.sanitize'
        if self.Success:
            return str(Online(search_str=value).url())
        else:
            com.cancel(f)
    
    def browser(self):
        f = '[shared] logic.Email.browser'
        if self.Success:
            try:
                if self._attachment:
                    ''' - This is the last resort. Attaching a file
                          worked for me only with CentOS6 + Palemoon +
                          Thunderbird. Using another OS/browser/email
                          client will probably call a default email
                          client without the attachment.
                        - Quotes are necessary for attachments only,
                          they will stay visible otherwise.
                    '''
                    webbrowser.open ('mailto:%s?subject=%s&body=%s&attach="%s"'\
                                    % (self._email
                                      ,self._subject
                                      ,self._message
                                      ,self._attachment
                                      )
                                    )
                else:
                    webbrowser.open ('mailto:%s?subject=%s&body=%s' \
                                    % (self._email
                                      ,self._subject
                                      ,self._message
                                      )
                                    )
            except:
                mes = _('Failed to load an e-mail client.')
                objs.mes(f,mes).error()
        else:
            com.cancel(f)
    
    def create(self):
        f = '[shared] logic.Email.create'
        if self.Success:
            if not self.evolution() and not self.thunderbird() \
            and not self.outlook():
                self._subject    = self.sanitize(self._subject)
                self._message    = self.sanitize(self._message)
                self._attachment = self.sanitize(self._attachment)
                self.browser()
        else:
            com.cancel(f)
                       
    #note: this does not work in wine!
    def outlook(self):
        f = '[shared] logic.Email.outlook'
        if objs.os().win():
            try:
                import win32com.client
                #https://stackoverflow.com/a/51993450
                outlook       = win32com.client.dynamic.Dispatch('outlook.application')
                mail          = outlook.CreateItem(0)
                mail.To       = self._email.replace(',',';')
                mail.Subject  = self._subject
                mail.HtmlBody = '<html><body><meta http-equiv="Content-Type" content="text/html;charset=UTF-8">%s</body></html>'\
                                % self._message
                if self._attachment:
                    mail.Attachments.Add(self._attachment)
                mail.Display(True)
                return True
            except Exception as e:
                mes = _('Operation has failed!\nDetails: {}').format(e)
                objs.mes(f,mes).error()
        else:
            mes = _('This operation cannot be executed on your operating system.')
            objs.mes(f,mes).info()
    
    def thunderbird(self):
        f = '[shared] logic.Email.thunderbird'
        if self.Success:
            app = '/usr/bin/thunderbird'
            if os.path.isfile(app):
                if self._attachment:
                    self.custom_args = [app,'-compose'
                                       ,"to='%s',subject='%s',body='%s',attachment='%s'"\
                                       % (self._email,self._subject
                                         ,self._message,self._attachment
                                         )
                                       ]
                else:
                    self.custom_args = [app,'-compose'
                                       ,"to='%s',subject='%s',body='%s'"\
                                       % (self._email,self._subject
                                         ,self._message
                                         )
                                       ]
                try:
                    subprocess.Popen(self.custom_args)
                    return True
                except:
                    mes = _('Failed to run "{}"!')
                    mes = mes.format(self.custom_args)
                    objs.mes(f,mes).error()
        else:
            com.cancel(f)
    
    def evolution(self):
        f = '[shared] logic.Email.evolution'
        if self.Success:
            app = '/usr/bin/evolution'
            if os.path.isfile(app):
                if self._attachment:
                    self.custom_args = [app,'mailto:%s?subject=%s&body=%s&attach=%s'\
                                       % (self._email.replace(';',',')
                                         ,self._subject,self._message
                                         ,self._attachment
                                         )
                                       ]
                else:
                    self.custom_args = [app,'mailto:%s?subject=%s&body=%s'\
                                       % (self._email.replace(';',',')
                                         ,self._subject,self._message
                                         )
                                       ]
                try:
                    subprocess.Popen(self.custom_args)
                    return True
                except:
                    mes = _('Failed to run "{}"!')
                    mes = mes.format(self.custom_args)
                    objs.mes(f,mes).error()
        else:
            com.cancel(f)



class Grep:

    def __init__ (self,lst,start=[]
                 ,middle=[],end=[]
                 ):
        self._lst    = lst
        self._start  = start
        self._middle = middle
        self._end    = end
        self._found  = []
        self.i       = 0
        self.sanitize()

    def sanitize(self):
        ''' Get rid of constructs like [None] instead of checking
            arguments when parameterizing.
        '''
        if len(self._lst) == 1:
            if not self._lst[0]:
                self._lst = []
        if len(self._start) == 1:
            if not self._start[0]:
                self._start = []
        if len(self._middle) == 1:
            if not self._middle[0]:
                self._middle = []
        if len(self._end) == 1:
            if not self._end[0]:
                self._end = []

    def start(self):
        if not self._start:
            return True
        found = False
        for i in range(len(self._start)):
            if self._start[i] \
            and self._lst[self.i].startswith(self._start[i]):
                found = True
        return found

    def middle(self):
        if not self._middle:
            return True
        found = False
        for i in range(len(self._middle)):
            if self._middle[i] and self._middle[i] in self._lst[self.i]:
                found = True
        return found

    def end(self):
        if not self._end:
            return True
        found = False
        for i in range(len(self._end)):
            if self._end[i] \
            and self._lst[self.i].endswith(self._end[i]):
                found = True
        return found

    # Return all matches as a list
    def get(self):
        if not self._found:
            for i in range(len(self._lst)):
                self.i = i
                if self.start() and self.middle() and self.end():
                    self._found.append(self._lst[i])
        return self._found

    # Return the 1st match as a string
    def get_first(self):
        self.get()
        if self._found:
            return self._found[0]



class Word:

    def __init__(self):
        ''' _p: word with punctuation
            _n: _p without punctuation, lower case
            _nm: normal form of _n
            _pf: position of the 1st symbol of _p
            _pl: position of the last symbol of _p
            _nf: position of the 1st symbol of _n
            _nl: position of the last symbol of _n
            _nmf: position of the 1st symbol of _nm  # 'matches'
            _nml: position of the last symbol of _nm # 'matches'
        '''
        self._nm = self._nmf = self._nml = self._pf \
                     = self._pl = self._nf = self._nl = self._cyr \
                     = self._lat = self._greek = self._digit \
                     = self._empty = self._ref = self._sent_no \
                     = self._spell = self._sents_len = self._tf \
                     = self._tl = None

    def empty(self):
        if self._empty is None:
            self._empty = True
            for sym in self._p:
                if sym.isalpha():
                    self._empty = False
                    break
        return self._empty

    def digit(self):
        if self._digit is None:
            self._digit = False
            for sym in self._p:
                if sym.isdigit():
                    self._digit = True
                    break
        return self._digit

    def cyr(self):
        if self._cyr is None:
            self._cyr = False
            for sym in ru_alphabet_low:
                if sym in self._n:
                    self._cyr = True
                    break
        return self._cyr

    def lat(self):
        if self._lat is None:
            self._lat = False
            for sym in lat_alphabet_low:
                if sym in self._n:
                    self._lat = True
                    break
        return self._lat

    def greek(self):
        if self._greek is None:
            self._greek = False
            for sym in greek_alphabet_low:
                if sym in self._n:
                    self._greek = True
                    break
        return self._greek

    # Do only after Words.sent_nos
    def print(self,no=0):
        f = '[shared] logic.Word.print'
        mes = 'no: {}; _p: {}; _n: {}; _nm: {}; _pf: {}; _pl: {}; _nf: {}; _nl: {}; _cyr: {}; _lat: {}; _greek: {}; _digit: {}; _empty: {}; _ref: {}; _sent_no: {}; _sents_len: {}; _spell: {}; _nmf: {}; _nml: {}'
        mes = mes.format (no,self._p,self._n,self._nm,self._pf,self._pl
                         ,self._nf,self._nl,self._cyr,self._lat
                         ,self._greek,self._digit,self._empty,self._ref
                         ,self._sent_no,self._sents_len,self._spell
                         ,self._nmf,self._nml)
        objs.mes(f,mes,True).debug()

    def nm(self):
        if self._nm is None:
            if self.ref():
                ''' #note: Setting '_nm' to '' allows to find longer
                    matches (without references), but requires replacing
                    duplicate spaces in 'text_nm' with ordinary ones and
                    using another word numbering for '_nm'.
                '''
                #self._nm = ''
                self._nm = self._n
            else:
                result = Decline (text = self._n
                                 ,Auto = False
                                 ).normal().get()
                if result:
                    self._nm = result.replace('ё','е')
                else:
                    self._nm = self._n
        return self._nm

    def ref(self):
        ''' Criteria for setting the 'reference' mark:
            - The word has digits
            - The word has Greek characters (that are treated as
              variables. Greek should NOT be a predominant language)
            - The word has Latin characters in the predominantly Russian
              text (inexact)
            - The word has '-' (inexact) (#note: when finding matches,
              set the condition of ''.join(set(ref)) != '-')
        '''
        if self._ref is None:
            if self.lat() or self.digit() or self.greek():
                self._ref = True
            else:
                self._ref = False
        return self._ref

    def spell_ru(self):
        return objs.enchant(lang='ru').check(self._n)
    
    def spell_yo(self):
        words = []
        for i in range(len(self._n)):
            if self._n[i] == 'е':
                word    = list(self._n)
                word[i] = 'ё'
                word    = ''.join(word)
                words.append(word)
        for word in words:
            if objs.enchant(lang='ru').check(word):
                return True
    
    def spell_us(self):
        return objs.enchant(lang='us').check(self._n)
    
    def spell_gb(self):
        return objs.enchant(lang='gb').check(self._n)
    
    def spell(self):
        ''' Enchant:
            1) Lower-case, upper-case and words where the first letter
               is capital, are all accepted. Mixed case is not accepted;
            2) Punctuation is not accepted;
            3) Empty input raises an exception;
            4) 'е' instead of 'ё' returns False, however, 'ё' in
               a wrong place returns True.
        '''
        if self._spell is None:
            self._spell = False
            if self._n:
                if Text(self._n).has_digits():
                    self._spell = True
                elif Text(self._n).has_cyrillic():
                    if self.spell_ru() or self.spell_yo():
                        self._spell = True
                elif Text(self._n).has_latin():
                    if self.spell_us() or self.spell_gb():
                        self._spell = True
                else:
                    self._spell = True
            else:
                self._spell = True
        return self._spell

    # Wrong selection upon search: see an annotation to SearchBox
    def tf(self):
        f = '[shared] logic.Word.tf'
        if self._tf is None:
            self._tf = '1.0'
            # This could happen if double line breaks were not deleted
            if self._sent_no is None:
                com.empty(f)
            else:
                # This is easier, but assigning a tag throws an error
                #self._tf = '1.0+%dc' % (self._pf - self._sent_no)
                result = self._pf - self._sents_len
                if self._sent_no > 0 and result > 0:
                    result -= 1
                self._tf = '%d.%d' % (self._sent_no + 1,result)
                #objs.mes(f,str(self._tf),True).debug()
        return self._tf

    def tl(self):
        f = '[shared] logic.Word.tl'
        if self._tl is None:
            self._tl = '1.1'
            # This could happen if double line breaks were not deleted
            if self._sent_no is None:
                com.empty(f)
            else:
                # This is easier, but assigning a tag throws an error
                #self._tl = '1.0+%dc' % (self._pl - self._sent_no + 1)
                result = self._pl - self._sents_len
                if self._sent_no > 0 and result > 0:
                    result -= 1
                self._tl = '%d.%d' % (self._sent_no + 1,result + 1)
                #objs.mes(f,str(self._tl),True).debug()
        return self._tl



# Use cases: case-insensitive search; spellchecking; text comparison
# Requires Search, Text
class Words:

    def __init__(self,text,Auto=False):
        f = '[shared] logic.Words.__init__'
        self.Success = True
        self.Auto    = Auto
        self.values()
        if text:
            mes = _('Analyze the text')
            objs.mes(f,mes,True).info()
            ''' This is MUCH faster than using old symbol-per-symbol
                algorithm for finding words. We must, however, drop
                double space cases.
            '''
            self._text_orig   = Text(text=text,Auto=self.Auto).text
            self._line_breaks = Search(self._text_orig,'\n').next_loop()
            self._text_p      = Text(text=self._text_orig).delete_line_breaks()
            self._text_n      = Text(text=self._text_p).delete_punctuation().lower()
            self.split()
        else:
            self.Success = False
            com.cancel(f)
                       
    def values(self):
        self._no          = 0
        self.words        = []
        self._line_breaks = []
        self._list_nm     = []
        self._text_nm     = None
        self._text_orig   = ''
        self._text_p      = ''
        self._text_n      = ''

    def split(self):
        f = '[shared] logic.Words.split'
        if self.Success:
            if not self.len():
                lst_p = self._text_p.split(' ')
                lst_n = self._text_n.split(' ')
                assert len(lst_p) == len(lst_n)
                cur_len_p = cur_len_n = 0
                for i in range(len(lst_p)):
                    if i > 0:
                        cur_len_p += 2
                        cur_len_n += 2
                    cur_word = Word()
                    cur_word._p = lst_p[i]
                    cur_word._n = lst_n[i]
                    cur_word._pf = cur_len_p
                    cur_word._nf = cur_len_n
                    cur_len_p = cur_word._pl = cur_word._pf \
                                               + len(cur_word._p) - 1
                    cur_len_n = cur_word._nl = cur_word._nf \
                                               + len(cur_word._n) - 1
                    self.words.append(cur_word)
        else:
            com.cancel(f)

    def print(self):
        f = '[shared] logic.Words.print'
        if self.Success:
            for i in range(self.len()):
                self.words[i].print(no=i)
        else:
            com.cancel(f)

    # Running 'range(self.len())' does not re-run 'len'
    def len(self):
        return len(self.words)

    def _sent_nos(self):
        no = sents_len = 0
        for i in range(self.len()):
            condition1 = self.words[i]._pf - 1 in self._line_breaks
            if self.Auto:
                condition = condition1
            else:
                # In case duplicate spaces/line breaks were not deleted
                condition2 = self.words[i]._p == '\n' \
                             or self.words[i]._p == '\r' \
                             or self.words[i]._p == '\r\n'
                condition = condition1 or condition2
            if condition:
                no += 1
                sents_len = self.words[i]._pf - 1
            self.words[i]._sent_no = no
            self.words[i]._sents_len = sents_len

    def sent_nos(self):
        f = '[shared] logic.Words.sent_nos'
        if self.Success:
            if self.len() > 0:
                if self.words[self._no]._sent_no is None:
                    self._sent_nos()
        else:
            com.cancel(f)

    def sent_p(self):
        f = '[shared] logic.Words.sent_p'
        if self.Success:
            sent_no = self.sent_no()
            sent_no = Input (title = f
                            ,value = sent_no
                            ).integer()
            old = self._no
            result = []
            for self._no in range(self.len()):
                if self.words[self._no]._sent_no == sent_no:
                    result.append(self.words[self._no]._p)
            self._no = old
            return ' '.join(result)
        else:
            com.cancel(f)

    def sent_no(self):
        f = '[shared] logic.Words.sent_no'
        if self.Success:
            self.sent_nos()
            return self.words[self._no]._sent_no
        else:
            com.cancel(f)

    def next_ref(self):
        f = '[shared] logic.Words.next_ref'
        if self.Success:
            old = self._no
            Found = False
            while self._no < self.len():
                if self.words[self._no].ref():
                    Found = True
                    break
                else:
                    self._no += 1
            if not Found:
                self._no = old
            return self._no
        else:
            com.cancel(f)

    def prev_ref(self):
        f = '[shared] logic.Words.prev_ref'
        if self.Success:
            old = self._no
            Found = False
            while self._no >= 0:
                if self.words[self._no].ref():
                    Found = True
                    break
                else:
                    self._no -= 1
            if not Found:
                self._no = old
            return self._no
        else:
            com.cancel(f)

    def spellcheck(self):
        f = '[shared] logic.Words.spellcheck'
        if self.Success:
            if self.len() > 0:
                if self.words[0]._spell is None:
                    for i in range(self.len()):
                        self.words[i].spell()
        else:
            com.cancel(f)

    def _refs(self):
        for i in range(self.len()):
            self.words[i].ref()

    def refs(self):
        f = '[shared] logic.Words.refs'
        if self.Success:
            if self.len() > 0:
                if self.words[0]._ref is None:
                    self._refs()
        else:
            com.cancel(f)

    # Needed for text comparison
    def list_nm(self):
        f = '[shared] logic.Words.list_nm'
        if self.Success:
            if not self._list_nm:
                cur_len_nm = 0
                for i in range(self.len()):
                    self._list_nm.append(self.words[i].nm())
                    if i > 0:
                        cur_len_nm += 2
                    cur_word = self.words[i]
                    cur_word._nmf = cur_len_nm
                    cur_len_nm = cur_word._nml = cur_word._nmf \
                                               + len(cur_word._nm) - 1
            return self._list_nm
        else:
            com.cancel(f)

    # Needed for text comparison
    def text_nm(self):
        f = '[shared] logic.Words.text_nm'
        if self.Success:
            if not self._text_nm:
                self._text_nm = ' '.join(self.list_nm())
            return self._text_nm
        else:
            com.cancel(f)

    def no_by_pos_p(self,pos):
        f = '[shared] logic.Words.no_by_pos_p'
        if self.Success:
            result = self._no
            for i in range(self.len()):
                if self.words[i]._pf - 1 <= pos <= self.words[i]._pl + 1:
                    result = i
                    break
            return result
        else:
            com.cancel(f)

    def no_by_pos_n(self,pos):
        f = '[shared] logic.Words.no_by_pos_n'
        if self.Success:
            result = self._no
            for i in range(self.len()):
                if self.words[i]._nf - 1 <= pos <= self.words[i]._nl + 1:
                    result = i
                    break
            return result
        else:
            com.cancel(f)

    # Call 'list_nm()' first
    def no_by_pos_nm(self,pos):
        f = '[shared] logic.Words.no_by_pos_nm'
        if self.Success:
            result = self._no
            for i in range(self.len()):
                if self.words[i]._nmf - 1 <= pos <= self.words[i]._nml + 1:
                    result = i
                    break
            return result
        else:
            com.cancel(f)

    def no_by_tk(self,tkpos):
        f = '[shared] logic.Words.no_by_tk'
        if self.Success:
            if tkpos:
                lst = tkpos.split('.')
                if len(lst) == 2:
                    lst[0] = Text(text=lst[0]).str2int()
                    if lst[0] > 0:
                        lst[0] -= 1
                    lst[1] = Text(text=lst[1]).str2int()
                    result = None
                    for i in range(self.len()):
                        if self.words[i]._sent_no == lst[0]:
                            result = self.words[i]._sents_len
                            break
                    if result is not None:
                        if lst[1] == 0:
                            result += 1
                        elif lst[0] == 0:
                            result += lst[1]
                        else:
                            result += lst[1] + 1
                        mes = '{} -> {}'.format(tkpos,result)
                        objs.mes(f,mes,True).debug()
                        return self.no_by_pos_p(pos=result)
                else:
                    mes = _('Wrong input data: "{}"!').format(lst)
                    objs.mes(f,mes).warning()
            else:
                com.empty(f)
        else:
            com.cancel(f)

    def nos_by_sent_no(self,sent_no=0):
        f = '[shared] logic.Words.nos_by_sent_no'
        result = (0,0)
        if self.Success:
            sent_no = Input (title = f
                            ,value = sent_no
                            ).integer()
            old = self._no
            nos = []
            for self._no in range(self.len()):
                if sent_no == self.sent_no():
                    nos.append(self._no)
            self._no = old
            if nos:
                # Valid for one-word paragraph
                result = (min(nos),max(nos))
            else:
                mes = _('Failed to find words of paragraph #{}!')
                mes = mes.format(sent_no)
                objs.mes(f,mes,True).warning()
        else:
            com.cancel(f)
        return result

    def complete(self):
        f = '[shared] logic.Words.complete'
        if self.Success:
            self.sent_nos()
            for i in range(self.len()):
                self.words[i].empty()
                self.words[i].ref()
                self.words[i].nm()
                self.words[i].spell()
                self.words[i].tf()
                self.words[i].tl()
            self.text_nm()
        else:
            com.cancel(f)



class Search:

    def __init__(self,text=None,search=None):
        self.Success    = False
        self.i          = 0
        self._next_loop = []
        self._prev_loop = []
        if text and search:
            self.reset(text=text,search=search)

    def reset(self,text,search):
        f = '[shared] logic.Search.reset'
        self.Success    = True
        self.i          = 0
        self._next_loop = []
        self._prev_loop = []
        self._text      = text
        self._search    = search
        if not self._search or not self._text:
            self.Success = False
            mes = _('Wrong input data!')
            objs.mes(f,mes,True).warning()

    def add(self):
        f = '[shared] logic.Search.add'
        if self.Success:
            if len(self._text) > self.i + len(self._search) - 1:
                self.i += len(self._search)
        else:
            com.cancel(f)

    def next(self):
        f = '[shared] logic.Search.next'
        if self.Success:
            result = self._text.find(self._search,self.i)
            if result != -1:
                self.i = result
                self.add()
            return result
        else:
            com.cancel(f)

    def prev(self):
        f = '[shared] logic.Search.prev'
        if self.Success:
            ''' rfind, unlike find, does not include limits, so we can
                use it to search backwards
            '''
            result = self._text.rfind(self._search,0,self.i)
            if result != -1:
                self.i = result
            return result
        else:
            com.cancel(f)

    def next_loop(self):
        f = '[shared] logic.Search.next_loop'
        if self.Success:
            if not self._next_loop:
                self.i = 0
                while True:
                    result = self.next()
                    if result == -1:
                        break
                    else:
                        self._next_loop.append(result)
        else:
            com.cancel(f)
        return self._next_loop

    def prev_loop(self):
        f = '[shared] logic.Search.prev_loop'
        if self.Success:
            if not self._prev_loop:
                self.i = len(self._text)
                while True:
                    result = self.prev()
                    if result == -1:
                        break
                    else:
                        self._prev_loop.append(result)
        else:
            com.cancel(f)
        return self._prev_loop



class OCR:

    def __init__(self,text):
        self._text = text

    # Texts in Latin characters only
    def cyr2lat(self):
        ''' 'У' -> 'Y' is not actually an OCR error, but rather a human
            one.
        '''
        cyr = ['А','В','Е','К','М','Н','О','Р','С','Т','У','Х','Ь','а'
              ,'е','о','р','с','у'
              ]
        lat = ['A','B','E','K','M','H','O','P','C','T','Y','X','b','a'
              ,'e','o','p','c','y'
              ]
        for i in range(len(cyr)):
            self._text = self._text.replace(cyr[i],lat[i])
        return self._text

    # Digits only
    def letter2digit(self):
        self._text = self._text.replace('З','3').replace('з','3').replace('O','0').replace('О','0').replace('б','6')
        return self._text

    def common(self):
        # 100o => 100°
        self._text = re.sub(r'(\d+)[oо]',r'\1°',self._text)
        # 106а => 106a (Cyrillic)
        self._text = re.sub(r'(\d+)а',r'\1a',self._text)
        # 106е => 106e (Cyrillic)
        self._text = re.sub(r'(\d+)е',r'\1e',self._text)
        # 106Ь => 106b
        self._text = re.sub(r'(\d+)Ь',r'\1b',self._text)
        # А1 => A1 (Cyrillic)
        self._text = re.sub(r'А(\d+)',r'A\1',self._text)
        # 1А => 1A (Cyrillic)
        self._text = re.sub(r'(\d+)А',r'\1A',self._text)
        # В1 => B1 (Cyrillic)
        self._text = re.sub(r'В(\d+)',r'B\1',self._text)
        # 1В => 1B (Cyrillic)
        self._text = re.sub(r'(\d+)В',r'\1B',self._text)
        # С1 => C1 (Cyrillic)
        self._text = re.sub(r'С(\d+)',r'C\1',self._text)
        # 1С => 1C (Cyrillic)
        self._text = re.sub(r'(\d+)С',r'\1C',self._text)
        #fix a degree sign
        self._text = re.sub (r'[\s]{0,1}[°o][\s]{0,1}[CС](\W)'
                            ,r'°C',self._text
                            )
        return self._text



class Decline:
    ''' #note ABOUT PYMORPHY2:
        1) Input must be stripped of punctuation, otherwise, the program
           fails.
        2) Output keeps unstripped spaces to the left, however, spaces
           to the right fail the program.
        3) Input can have any register. The output is lower-case.
        4) Output can have 'ё' irrespectively of input.
    '''
    def __init__ (self,text='',number=''
                 ,case='',Auto=True):
        if text:
            self.reset (text   = text
                       ,number = number
                       ,case   = case
                       ,Auto   = Auto
                       )
        else:
            self.Auto    = Auto
            self._orig   = ''
            self._number = 'sing'
            self._case   = 'nomn'
            self._list   = []

    def reset(self,text,number='',case='',Auto=True):
        ''' #todo:
            1) Restore punctuation
            2) Optional leading/trailing spaces
        '''
        self._orig = text
        self._number = number
        # 'nomn', 'gent', 'datv', 'accs', 'ablt', 'loct'
        self._case = case
        self.Auto = Auto
        if self.Auto:
            result = Text(text=self._orig).delete_punctuation()
        else:
            result = self._orig
        self._list = result.split(' ')
        ''' Returning 'self' allows to call 'get' in the same line, e.g.
            Decline(text='текст').normal().get()
        '''
        return self

    def get(self):
        result = ' '.join(self._list)
        if self.Auto:
            result = result.replace('ё','е')
        return result

    def decline(self):
        f = '[shared] logic.Decline.decline'
        for i in range(len(self._list)):
            # Inflecting '', None, digits and Latin words *only* fails
            ''' mes = _('Decline "{}" in "{}" number and "{}" case')
                mes = mes.format (self._list[i]
                                 ,self.number()
                                 ,self.case()
                                 )
                objs.mes(f,mes,True).debug()
            '''
            try:
                self._list[i] = objs.morph().parse(self._list[i])[0].inflect({self.number(),self.case()}).word
            except AttributeError:
                self._list[i] = self._list[i]
        return self

    # If input is a phrase, 'normal' each word of it
    def normal(self):
        for i in range(len(self._list)):
            self._list[i] = objs.morph().parse(self._list[i])[0].normal_form
        return self

    def number(self):
        f = '[shared] logic.Decline.number'
        if not self._number:
            self._number = 'sing'
            # Needed by 'max'
            if self._list:
                tmp = []
                for i in range(len(self._list)):
                    if self._list[i]:
                        # Returns 'sing', 'plur' or None
                        tmp.append(objs.morph().parse(self._list[i])[0].tag.number)
                if tmp and max(tmp,key=tmp.count) == 'plur':
                    self._number = 'plur'
            ''' mes = str(self._number)
                objs.mes(f,mes,True).debug()
            '''
        return self._number

    def case(self):
        f = '[shared] logic.Decline.case'
        if not self._case:
            self._case = 'nomn'
            # Needed by 'max'
            if self._list:
                tmp = []
                for i in range(len(self._list)):
                    if self._list[i]:
                        tmp.append(objs.morph().parse(self._list[i])[0].tag.case)
                result = max(tmp,key=tmp.count)
                if result:
                    self._case = result
            mes = str(self._case)
            objs.mes(f,mes,True).debug()
        return self._case



class Objects:
    ''' Values here will be kept through different modules (but not
        through different programs both using 'shared.py').
    '''
    def __init__(self):
        self._enchant_ru = self._morph = self._pretty_table \
                         = self._pdir = self._online = self._tmpfile \
                         = self._os = self._mes = None

    def mes (self,func='Logic error'
            ,message='Logic error'
            ,Silent=False
            ):
        if self._mes is None:
            self._mes = Message
        return self._mes(func,message,Silent)
    
    def os(self):
        if self._os is None:
            self._os = OSSpecific()
        return self._os
    
    def tmpfile(self,suffix='.htm',Delete=0):
        if self._tmpfile is None:
            self._tmpfile = com.tmpfile (suffix = suffix
                                        ,Delete = Delete
                                        )
        return self._tmpfile
    
    def online(self):
        if self._online is None:
            self._online = Online()
        return self._online
    
    def pdir(self):
        if not self._pdir:
            self._pdir = ProgramDir()
        return self._pdir

    def enchant(self,lang='ru'):
        import enchant
        if not self._enchant_ru:
            self._enchant_ru = enchant.Dict('ru_RU')
            self._enchant_gb = enchant.Dict('en_GB')
            self._enchant_us = enchant.Dict('en_US')
        if lang == 'ru':
            return self._enchant_ru
        elif lang == 'gb':
            return self._enchant_gb
        elif lang == 'us':
            return self._enchant_us
        else:
            mes = 'An unknown mode "{}"!\n\nThe following modes are supported: "{}".'
            mes = mes.format(lang,'ru; gb; us')
            objs.mes(f,mes).error()
            return self._enchant_ru

    def morph(self):
        if not self._morph:
            import pymorphy2
            self._morph = pymorphy2.MorphAnalyzer()
        return self._morph

    def pretty_table(self):
        if not self._pretty_table:
            from prettytable import PrettyTable
            self._pretty_table = PrettyTable
        return self._pretty_table



class MessagePool:

    def __init__(self,max_size=5):
        self.max_size = max_size
        self.pool = []

    def free(self):
        if len(self.pool) == self.max_size:
            self.delete_first()

    def add(self,message):
        f = '[shared] logic.MessagePool.add'
        if message:
            self.free()
            self.pool.append(message)
        else:
            com.empty(f)

    def delete_first(self):
        f = '[shared] logic.MessagePool.delete_first'
        if len(self.pool) > 0:
            del self.pool[0]
        else:
            mes = _('The pool is empty!')
            objs.mes(f,mes,True).warning()

    def delete_last(self):
        f = '[shared] logic.MessagePool.delete_last'
        if len(self.pool) > 0:
            del self.pool[-1]
        else:
            mes = _('The pool is empty!')
            objs.mes(f,mes,True).warning()

    def clear(self):
        self.pool = []

    def get(self):
        return List(lst1=self.pool).space_items()



class ProgramDir:

    def __init__(self):
        self.dir = sys.path[0]
        # We run app, not interpreter
        if os.path.isfile(self.dir):
            self.dir = Path(path=self.dir).dirname()

    def add(self,*args):
        return os.path.join(self.dir,*args)



class Timer:

    def __init__(self,func_title='__main__'):
        self._start = self._end = 0
        self._func_title = func_title

    def start(self):
        self._start = time.time()

    def end(self):
        delta = float(time.time()-self._start)
        mes = _('The operation has taken {} s.').format(delta)
        objs.mes(self._func_title,mes,True).info()
        return delta



class Table:

    def __init__ (self,headers,rows
                 ,Shorten=True,MaxRow=18
                 ,MaxRows=20
                 ):
        f = '[shared] logic.Table.__init__'
        self._headers = headers
        self._rows    = rows
        self.Shorten  = Shorten
        self.MaxRow   = MaxRow
        self.MaxRows  = MaxRows
        if self._headers and self._rows:
            self.Success = True
        else:
            self.Success = False
            com.empty(f)

    def _shorten_headers(self):
        self._headers = [Text(text=header).shorten(max_len=self.MaxRow)\
                         for header in self._headers
                        ]
        # prettytable.py, 302: Exception: Field names must be unique!
        headers = list(set(self._headers))
        ''' prettytable.py, 818: Exception: Row has incorrect number of
            values
        '''
        if len(headers) != len(self._headers):
            result = List(lst1=headers,lst2=self._headers).equalize()
            if result:
                self._headers = result[0]

    def _shorten_rows(self):
        f = '[shared] logic.Table._shorten_rows'
        if self.MaxRows < 2 or self.MaxRows > len(self._rows):
            self.MaxRows = len(self._rows)
            mes = _('Set the max number of rows to {}')
            mes = mes.format(self.MaxRows)
            objs.mes(f,mes,True).info()
        self.MaxRows = int(self.MaxRows / 2)
        pos3 = len(self._rows)
        pos2 = pos3 - self.MaxRows
        self._rows = self._rows[0:self.MaxRows] + self._rows[pos2:pos3]

    def _shorten_row(self):
        # Will not be assigned without using 'for i in range...'
        for i in range(len(self._rows)):
            if isinstance(self._rows[i],tuple):
                self._rows[i] = list(self._rows[i])
            for j in range(len(self._rows[i])):
                if isinstance(self._rows[i][j],str):
                    if len(self._rows[i][j]) > self.MaxRow:
                        self._rows[i][j] = self._rows[i][j][0:self.MaxRow]

    def shorten(self):
        f = '[shared] logic.Table.shorten'
        if self.Success:
            if self.Shorten:
                self._shorten_headers()
                self._shorten_rows   ()
                self._shorten_row    ()
        else:
            com.cancel(f)

    def print(self):
        f = '[shared] logic.Table.print'
        if self.Success:
            self.shorten()
            obj = objs.pretty_table()(self._headers)
            for row in self._rows:
                obj.add_row(row)
            print(obj)
        else:
            com.cancel(f)



class FixBaseName:
    ''' Return a path base name that would comply with OS-specific
        rules. We should not use absolute paths at input because we
        cannot tell for sure that the path separator is actually
        a separator and not an illegal character.
    '''
    def __init__(self,basename,AllOS=False,max_len=0):
        self.AllOS    = AllOS
        self._name    = basename
        self._max_len = max_len
        
    def length(self):
        if self._max_len:
            self._name = self._name[:self._max_len]
    
    def win(self):
        self._name = [char for char in self._name if not char \
                      in forbidden_win
                     ]
        self._name = ''.join(self._name)
        if self._name.endswith('.'):
            self._name = self._name[:-1]
        self._name = self._name.strip()
        if self._name.upper() in reserved_win:
            self._name = ''
        
    def lin(self):
        self._name = [char for char in self._name if not char \
                      in forbidden_lin
                     ]
        self._name = ''.join(self._name)
        self._name = self._name.strip()
        
    def mac(self):
        self._name = [char for char in self._name if not char \
                      in forbidden_mac
                     ]
        self._name = ''.join(self._name)
        self._name = self._name.strip()
        
    def run(self):
        if self.AllOS:
            self.win()
            self.lin()
            self.mac()
        elif objs.os().win():
            self.win()
        elif objs._os.lin():
            self.lin()
        elif objs._os.mac():
            self.mac()
        else:
            self.win()
            self.lin()
            self.mac()
        self.length()
        return self._name



class Get:
    
    def __init__ (self,url,encoding='UTF-8'
                 ,Verbose=True,Verify=False
                 ,timeout=6
                 ):
        self._html     = ''
        self._timeout  = timeout
        self._url      = url
        self._encoding = encoding
        self.Verbose   = Verbose
        self.Verify    = Verify
        self.unverified()
    
    def read(self):
        ''' This is a dummy function to return the final result.
            It is needed merely to use 'json' which calls 'read'
            for input object.
        '''
        return self._html
    
    def unverified(self):
        ''' On *some* systems we can get urllib.error.URLError: 
            <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED].
            To get rid of this error, we use this small workaround.
        '''
        f = '[shared] logic.Get.unverified'
        if not self.Verify:
            if hasattr(ssl,'_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
            else:
                mes = _('Unable to use unverified certificates!')
                objs.mes(f,mes,True).warning()
        
    def _get(self):
        ''' Changing UA allows us to avoid a bot protection
            ('Error 403: Forbidden').
        '''
        f = '[shared] logic.Get._get'
        try:
            req = urllib.request.Request (url     = self._url
                                         ,data    = None
                                         ,headers = {'User-Agent': \
                                                     'Mozilla'
                                                    }
                                         )
            self._html = \
            urllib.request.urlopen(req,timeout=self._timeout).read()
            if self.Verbose:
                mes = _('[OK]: "{}"').format(self._url)
                objs.mes(f,mes,True).info()
        # Too many possible exceptions
        except Exception as e:
            mes = _('[FAILED]: "{}". Details: {}')
            mes = mes.format(self._url,e)
            objs.mes(f,mes,True).warning()
    
    def decode(self):
        ''' Set 'encoding' to None to cancel decoding. This is useful
            if we are downloading a non-text content.
        '''
        f = '[shared] logic.Get.decode'
        if self._encoding:
            if self._html:
                try:
                    self._html = \
                    self._html.decode(encoding=self._encoding)
                except UnicodeDecodeError:
                    self._html = str(self._html)
                    mes = _('Unable to decode "{}"!').format(self._url)
                    objs.mes(f,mes,True).warning()
            else:
                com.empty(f)
    
    def run(self):
        f = '[shared] logic.Get.run'
        if self._url:
            # Safely use URL as a string
            if isinstance(self._url,str):
                if self.Verbose:
                    timer = Timer(func_title=f)
                    timer.start()
                self._get()
                self.decode()
                if self.Verbose:
                    timer.end()
                return self._html
            else:
                mes = _('Wrong input data: {}!').format(self._url)
                objs.mes(f,mes).warning()
        else:
            com.empty(f)



class References:
    
    def __init__(self,words1,words2):
        f = '[shared] logic.References.__init__'
        self.words1 = words1
        self.words2 = words2
        if self.words1 and self.words2 and len(self.words1.words) \
        and len(self.words2.words):
            self.Success = True
            self.words1.sent_nos()
            self.words2.sent_nos()
            self.words1.refs()
        else:
            self.Success = False
            com.empty(f)
        
    def ref_before(self,word_no):
        f = '[shared] logic.References.ref_before'
        if self.Success:
            if word_no < len(self.words1.words):
                while word_no >= 0:
                    if self.words1.words[word_no]._ref:
                        break
                    else:
                        word_no -= 1
                return word_no
            else:
                sub = '{} < {}'.format(word_no,len(self.words1.words))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)
        
    def ref_after(self,word_no):
        f = '[shared] logic.References.ref_after'
        if self.Success:
            if word_no < len(self.words1.words):
                while word_no < len(self.words1.words):
                    if self.words1.words[word_no]._ref:
                        return word_no
                    else:
                        word_no += 1
                return -1
            else:
                sub = '{} < {}'.format(word_no,len(self.words1.words))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)
    
    def nearest_ref(self,word_no):
        f = '[shared] logic.References.nearest_ref'
        if self.Success:
            word_no1 = self.ref_before(word_no)
            word_no2 = self.ref_after(word_no)
            if word_no1 == -1 and word_no2 == -1:
                mes = _('No references have been found!')
                objs.mes(f,mes,True).info()
                return word_no
            elif word_no1 >= 0 and word_no2 == -1:
                mes = _('No references to the right!')
                objs.mes(f,mes,True).info()
                return word_no1
            elif word_no2 >= 0 and word_no1 == -1:
                mes = _('No references to the left!')
                objs.mes(f,mes,True).info()
                return word_no2
            else:
                delta_before = word_no - word_no1
                delta_after  = word_no2 - word_no
                if min(delta_before,delta_after) == delta_before:
                    return word_no1
                else:
                    return word_no2
        else:
            com.cancel(f)
                
    def repeated(self,word_no):
        f = '[shared] logic.References.repeated'
        if self.Success:
            if word_no < len(self.words1.words):
                count = 0
                for i in range(word_no+1):
                    if self.words1.words[i]._n == self.words1.words[word_no]._n:
                        count += 1
                return count
            else:
                sub = '{} < {}'.format(word_no,len(self.words1.words))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.mes(f,mes).error()
        else:
            com.cancel(f)
        
    def repeated2(self,word_n,count):
        f = '[shared] logic.References.repeated2'
        if self.Success:
            tmp = 0
            for i in range(len(self.words2.words)):
                if self.words2.words[i]._n == word_n:
                   tmp += 1
                   if tmp == count:
                       return i
        else:
            com.cancel(f)



class Links:
    
    def __init__(self,text,root='href="'):
        self.values()
        self._text = text
        # Some sites omit 'http(s):' for their links
        self._text = self._text.replace('"//www.','"http://www.')
        self._root = root
        
    def redirection(self):
        for i in range(len(self._links)):
            if '?url' in self._links[i]:
                self._links[i] = re.sub('.*\?url=','',self._links[i])
                # Replace '%3A%2F%2F' with '://' and so on
                self._links[i] = urllib.parse.unquote(self._links[i])
    
    def values(self):
        self._pos   = 0
        self._links = []
    
    def poses(self):
        text = self._text
        search = Search (text   = self._text
                        ,search = self._root
                        )
        loop = search.next_loop()
        for self._pos in loop:
            self.link()
            
    def link(self):
        f = '[shared] logic.Links.link'
        pos = self._pos + len(self._root)
        if pos >= len(self._text):
            mes = _('Unexpected end of text!')
            objs.mes(f,mes,True).warning()
        else:
            text = self._text[pos:]
            try:
                pos = text.index('"')
                self._links.append(text[:pos])
            except ValueError:
                mes = _('Wrong input data!')
                objs.mes(f,mes,True).warning()
                              
    def duplicates(self):
        ''' Sometimes there are duplicate URLs on a page - we delete
            them there. We may need to preserve an original sorting so
            do not use 'set'.
        '''
        i = len(self._links) - 1
        while i >= 0:
            ind = self._links.index(self._links[i])
            if ind < i:
                del self._links[i]
            i -= 1
        return self._links
    
    def add_root(self,root):
        for i in range(len(self._links)):
            if self._links[i].startswith('/'):
                self._links[i] = root + self._links[i]
        return self._links
        
    def valid(self):
        self._links = [link for link in self._links \
                       if link.startswith('http')
                      ]
        return self._links



class FilterList:
    ''' Filter base names (case-ignorant) of files & folders in a path.
        Blacklist is a list of patterns, not obligatory full names.
    '''
    def __init__(self,path,blacklist=[]):
        self._list   = []
        self._path   = path
        self._block  = blacklist
        self.Success = Directory(self._path).Success \
                       and isinstance(blacklist,list)
    
    def block(self):
        f = '[shared] logic.FilterList.block'
        if self.Success:
            # Actually, there is no reason to use 'strip' here
            self._block = [item.lower() for item in self._block if item]
        else:
            com.cancel(f)
    
    def list(self):
        f = '[shared] logic.FilterList.list'
        if self.Success:
            if not self._list:
                # Those are base names
                self._list = os.listdir(self._path)
            return self._list
        else:
            com.cancel(f)
    
    def filter(self):
        f = '[shared] logic.FilterList.filter'
        if self.Success:
            match = []
            for item in self._list:
                for pattern in self._block:
                    if pattern in item.lower():
                        match.append(item)
                        break
            # This allows us to return matches as well if necessary
            mismatch = list(set(self._list) - set(match))
            mismatch.sort()
            return [os.path.join(self._path,item) for item in mismatch]
        else:
            com.cancel(f)
        
    def run(self):
        self.block()
        self.list()
        return self.filter()



class Home:

    def __init__(self,app_name='myapp'):
        self._app_name = app_name
        self._conf_dir = self._share_dir = ''
        
    def add_share(self,*args):
        return os.path.join(self.share_dir(),*args)
    
    def create_share(self):
        return Path(path=self.share_dir()).create()
    
    def share_dir(self):
        if not self._share_dir:
            if objs.os().win():
                os_folder = 'Application Data'
            else:
                os_folder = os.path.join('.local','share')
            self._share_dir = os.path.join (self.home()
                                           ,os_folder
                                           ,self._app_name
                                           )
        return self._share_dir
    
    def create_conf(self):
        return Path(path=self.conf_dir()).create()
    
    def home(self):
        return os.path.expanduser('~')
        
    def conf_dir(self):
        if not self._conf_dir:
            if objs.os().win():
                os_folder = 'Application Data'
            else:
                os_folder = '.config'
            self._conf_dir = os.path.join (self.home()
                                          ,os_folder
                                          ,self._app_name
                                          )
        return self._conf_dir
    
    def add(self,*args):
        return os.path.join(self.home(),*args)
    
    def add_config(self,*args):
        return os.path.join(self.conf_dir(),*args)



class Commands:

    def __init__(self):
        self.lang()
    
    def sanitize(self,text):
        if text is None:
            text = ''
        else:
            text = Text(str(text)).delete_unsupported()
        return text
    
    def mod_color(self,rgb,delta):
        rgb = list(max(min(255,x/256+delta),0) for x in rgb)
        # We need to have integers here. I had a float once.
        rgb = tuple(int(item) for item in rgb)
        return '#%02x%02x%02x' % rgb
    
    def dialog_save_file(self,types=()):
        if not types:
            types = ((_('Plain text (UTF-8)'),'.txt' )
                    ,( _('Web-page')         ,'.htm' )
                    ,( _('Web-page')         ,'.html')
                    ,( _('All files')        ,'*'    )
                    )
        options                = {}
        options['initialfile'] = ''
        options['filetypes']   = types
        options['title']       = _('Save As:')
        return options
    
    def lazy(self,func):
        Message (func    = func
                ,message = _('Nothing to do!')
                ).info()
    
    def warning(self,func,message):
        objs.mes (func    = func
                 ,level   = _('WARNING')
                 ,message = message
                 )
    
    def info(self,func,message):
        objs.mes (func    = func
                 ,level   = _('INFO')
                 ,message = message
                 )
        
    # IEC standard
    def human_size(self,bsize,LargeOnly=False):
        result = '%d %s' % (0,_('B'))
        if bsize:
            tebibytes = bsize // pow(2,40)
            cursize   = tebibytes * pow(2,40)
            gibibytes = (bsize - cursize) // pow(2,30)
            cursize  += gibibytes * pow(2,30)
            mebibytes = (bsize - cursize) // pow(2,20)
            cursize  += mebibytes * pow(2,20)
            kibibytes = (bsize - cursize) // pow(2,10)
            cursize  += kibibytes * pow(2,10)
            rbytes    = bsize - cursize
            mes = []
            if tebibytes:
                mes.append('%d %s' % (tebibytes,_('TiB')))
            if gibibytes:
                mes.append('%d %s' % (gibibytes,_('GiB')))
            if mebibytes:
                mes.append('%d %s' % (mebibytes,_('MiB')))
            if not (LargeOnly and bsize // pow(2,20)):
                if kibibytes:
                    mes.append('%d %s' % (kibibytes,_('KiB')))
                if rbytes:
                    mes.append('%d %s' % (rbytes,_('B')))
            if mes:
                result = ' '.join(mes)
        return result
    
    def split_time(self,length=0):
        hours   = length // 3600
        all_sec = hours * 3600
        minutes = (length - all_sec) // 60
        all_sec += minutes * 60
        seconds = length - all_sec
        return(hours,minutes,seconds)
    
    def easy_time(self,length=0):
        f = '[shared] logic.Commands.easy_time'
        result = '00:00:00'
        if length:
            hours, minutes, seconds = self.split_time(length)
            mes = []
            if hours:
                mes.append(str(hours))
            item = str(minutes)
            if hours and len(item) == 1:
                item = '0' + item
            mes.append(item)
            item = str(seconds)
            if len(item) == 1:
                item = '0' + item
            mes.append(item)
            result = ':'.join(mes)
        else:
            com.empty(f)
        return result
    
    def yt_date(self,date):
        # Convert a date provided by Youtube API to a timestamp
        f = '[shared] logic.Commands.yt_date'
        if date:
            pattern = '%Y-%m-%dT%H:%M:%S'
            itime = Time(pattern=pattern)
            # Prevent errors caused by 'datetime' parsing microseconds
            tmp = date.split('.')
            if date != tmp[0]:
                ind  = date.index('.'+tmp[-1])
                date = date[0:ind]
            itime._instance = datetime.datetime.strptime(date,pattern)
            return itime.timestamp()
        else:
            self.empty(f)
    
    def yt_length(self,length):
        ''' Convert a length of a video provided by Youtube API (string)
            to seconds.
            Possible variants: PT%dM%dS, PT%dH%dM%dS, P%dDT%dH%dM%dS.
        '''
        f = '[shared] logic.Commands.yt_length'
        result = 0
        if length:
            if isinstance(length,str) and length[0] == 'P':
                days    = 0
                hours   = 0
                minutes = 0
                seconds = 0
                match = re.search(r'(\d+)D',length)
                if match:
                    days = int(match.group(1))
                match = re.search(r'(\d+)H',length)
                if match:
                    hours = int(match.group(1))
                match = re.search(r'(\d+)M',length)
                if match:
                    minutes = int(match.group(1))
                match = re.search(r'(\d+)S',length)
                if match:
                    seconds = int(match.group(1))
                result = days * 86400 + hours * 3600 + minutes * 60 \
                         + seconds
            else:
                mes = _('Wrong input data: "{}"!').format(length)
                objs.mes(f,mes).warning()
        else:
            self.empty(f)
        return result
    
    def rewrite(self,file,Rewrite=False):
        ''' - We do not put this into File class because we do not need
              to check existence.
            - We use 'Rewrite' just to shorten other procedures (to be
              able to use 'self.rewrite' silently in the code without
              ifs).
        '''
        f = '[shared] logic.Commands.rewrite'
        if not Rewrite and os.path.isfile(file):
            ''' We don't actually need to force rewriting or delete
                the file before rewriting.
            '''
            mes = _('ATTENTION: Do yo really want to rewrite file "{}"?')
            mes = mes.format(file)
            return objs.mes(f,mes).question()
        else:
            ''' We return True so we may proceed with writing
                if the file has not been found.
            '''
            return True
    
    def lang(self):
        result = locale.getdefaultlocale()
        if result and len(result) > 0 and result[0]:
            if 'ru' in result[0]:
                globs['ui_lang'] = 'ru'
                globs['license_url'] = gpl3_url_ru
            else:
                globs['ui_lang'] = 'en'
                globs['license_url'] = gpl3_url_en
        else:
            globs['ui_lang'] = 'en'
    
    def tmpfile(self,suffix='.htm',Delete=0):
        return tempfile.NamedTemporaryFile (mode     = 'w'
                                           ,encoding = 'UTF-8'
                                           ,suffix   = suffix
                                           ,delete   = Delete
                                           ).name
    
    def human_time(self,delta):
        f = '[shared] logic.Commands.human_time'
        result = '%d %s' % (0,_('sec'))
        # Allows to use 'None'
        if delta:
            if isinstance(delta,int) or isinstance(delta,float):
                # 'datetime' will output years even for small integers
                # https://kalkulator.pro/year-to-second.html
                years   = delta // 31536000.00042889
                all_sec = years * 31536000.00042889
                months  = (delta - all_sec) // 2592000.0000000005
                all_sec += months * 2592000.0000000005
                weeks   = (delta - all_sec) // 604800
                all_sec += weeks * 604800
                days    = (delta - all_sec) // 86400
                all_sec += days * 86400
                hours   = (delta - all_sec) // 3600
                all_sec += hours * 3600
                minutes = (delta - all_sec) // 60
                all_sec += minutes * 60
                seconds = delta - all_sec
                mes = []
                if years:
                    mes.append('%d %s' % (years,_('yrs')))
                if months:
                    mes.append('%d %s' % (months,_('mths')))
                if weeks:
                    mes.append('%d %s' % (weeks,_('wks')))
                if days:
                    mes.append('%d %s' % (days,_('days')))
                if hours:
                    mes.append('%d %s' % (hours,_('hrs')))
                if minutes:
                    mes.append('%d %s' % (minutes,_('min')))
                if seconds:
                    mes.append('%d %s' % (seconds,_('sec')))
                if mes:
                    result = ' '.join(mes)
            else:
                Message (func    = f
                        ,message = _('Wrong input data: "{}"!').format(delta)
                        ).warning()
        else:
            self.empty(f)
        return result
    
    def cancel(self,func):
        Message (func    = func
                ,message = _('Operation has been canceled.')
                ).warning()
    
    def empty(self,func):
        Message (func    = func
                ,message = _('Empty input is not allowed!')
                ).warning()
    
    def not_ready(self,func):
        Message (func    = func
                ,message = _('Not implemented yet!')
                ).info()


''' If there are problems with import or tkinter's wait_variable, put
    this beneath 'if __name__'
'''
com  = Commands()
log  = Log (Use   = True
           ,Short = False
           )
objs = Objects()


if __name__ == '__main__':
    f = '[shared] logic.__main__'
    ReadTextFile('/tmp/aaa').get()
