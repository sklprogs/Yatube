#!/usr/bin/python3
# -*- coding: UTF-8 -*-

copyright = 'Copyright 2015-2018, Peter Sklyar'
license   = 'GPL v.3'
email     = 'skl.progs@gmail.com'

import re
import os, sys
import configparser
import calendar
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

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','../resources/locale')



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
            import pythoncom
            from win32com.shell import shell, shellcon
            import win32com.client, win32api
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
            import win32gui, win32con, ctypes # Required by 'Geometry'



config_parser = configparser.SafeConfigParser()

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
                  ,'{','}','(',')','’',"'"
                  ]

forbidden_win = '/\?%*:|"<>'
forbidden_lin = '/'
forbidden_mac = '/\?*:|"<>'
reserved_win  = ['CON','PRN','AUX','NUL','COM1','COM2','COM3','COM4'
                ,'COM5','COM6','COM7','COM8','COM9','LPT1','LPT2','LPT3'
                ,'LPT4','LPT5','LPT6','LPT7','LPT8','LPT9'
                ]

oss = OSSpecific()
if oss.win():
    import win32com
    import pythoncom
# Load last due to problems with TZ (see 'oss.win_import')
import datetime



class Launch:

    #note: 'Block' works only a 'custom_app' is set
    def __init__(self,target='',Block=False):
        self.values()
        self.target = target
        self.Block  = Block
        # Do not shorten, Path is used further
        self.h_path = Path(self.target)
        self.ext    = self.h_path.extension().lower()
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
        f = '[shared] shared.Launch._launch'
        if self.custom_args:
            log.append (f,_('DEBUG')
                       ,_('Custom arguments: "%s"') % ';'.join(self.custom_args)
                       )
            try:
                ''' Block the script till the called program is closed
                '''
                if self.Block:
                    subprocess.call(self.custom_args)
                else:
                    subprocess.Popen(self.custom_args)
            except:
                objs.mes (f,_('ERROR')
                         ,_('Failed to run "%s"!') \
                         % str(self.custom_args)
                         )
        else:
            log.append (f,_('ERROR')
                       ,_('Not enough input data!')
                       )

    def _lin(self):
        f = '[shared] shared.Launch._lin'
        try:
            os.system("xdg-open " + self.h_path.escape() + "&")
        except OSError:
            objs.mes (f,_('ERROR')
                     ,_('Unable to open the file in an external program. You should probably check the file associations.')
                     )

    def _mac(self):
        f = '[shared] shared.Launch._mac'
        try:
            os.system("open " + self.target)
        except:
            objs.mes (f,_('ERROR')
                     ,_('Unable to open the file in an external program. You should probably check the file associations.')
                     )

    def _win(self):
        f = '[shared] shared.Launch._win'
        try:
            os.startfile(self.target)
        except:
            objs.mes (f,_('ERROR')
                     ,_('Unable to open the file in an external program. You should probably check the file associations.')
                     )

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
        f = '[shared] shared.Launch.custom'
        if self.TargetExists:
            self.custom_args = [self.custom_app,self.target]
            self._launch()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def default(self):
        f = '[shared] shared.Launch.default'
        if self.TargetExists:
            if oss.lin():
                self._lin()
            elif oss.mac():
                self._mac()
            elif oss.win():
                self._win()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



class WriteTextFile:

    def __init__(self,file,Rewrite=False,UseLog=True):
        f = '[shared] shared.WriteTextFile.__init__'
        self.file    = file
        self.text    = ''
        self.Rewrite = Rewrite
        self.UseLog  = UseLog
        self.Success = True
        if not self.file:
            if self.UseLog:
                objs.mes (f,_('ERROR')
                         ,_('Not enough input data!')
                         )
            else:
                print(f+': Not enough input data!')
            self.Success = False

    def _write(self,mode='w'):
        f = '[shared] shared.WriteTextFile._write'
        if mode == 'w' or mode == 'a':
            if self.UseLog:
                log.append (f,_('INFO')
                           ,_('Write file "%s"') % self.file
                           )
            try:
                with open(self.file,mode,encoding='UTF-8') as fl:
                    fl.write(self.text)
            except:
                self.Success = False
                if self.UseLog:
                    objs.mes (f,_('ERROR')
                             ,_('Unable to write file "%s"!') \
                             % self.file
                             )
                else:
                    print(f+': Unable to write the file!')
        else:
            if self.UseLog:
                objs.mes (f,_('ERROR')
                         ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".')\
                         % (str(mode),'a, w')
                         )
            else:
                print(f+': An unknown mode!')

    def append(self,text=''):
        f = '[shared] shared.WriteTextFile.append'
        if self.Success:
            self.text = text
            if self.text:
                ''' #todo: In the append mode the file is created if it
                    does not exist, but should we warn the user that we
                    create it from scratch?
                '''
                self._write('a')
            else:
                if self.UseLog:
                    objs.mes (f,_('ERROR')
                             ,_('Not enough input data!')
                             )
                else:
                    print(f+': Not enough input data!')
        else:
            if self.UseLog:
                log.append (f,_('WARNING')
                           ,_('Operation has been canceled.')
                           )

    def write(self,text=''):
        f = '[shared] shared.WriteTextFile.write'
        if self.Success:
            self.text = text
            if self.text:
                if com.rewrite (file    = self.file
                               ,Rewrite = self.Rewrite
                               ):
                    self._write('w')
            else:
                if self.UseLog:
                    objs.mes (f,_('ERROR')
                             ,_('Not enough input data!')
                             )
                else:
                    print(f+': Not enough input data!')
        else:
            if self.UseLog:
                log.append (f,_('WARNING')
                           ,_('Operation has been canceled.')
                           )



class Log:

    def __init__(self,Use=True,Write=False
                ,Print=True,Short=False,file=None
                ):
        f = self.func = 'shared.Log.__init__'
        self.Success = True
        self.file    = file
        self.level   = _('INFO')
        self.message = 'Test'
        self.count   = 0
        self.Write   = Write
        self.Print   = Print
        self.Short   = Short
        if not Use:
            self.Success = False
        if self.Write:
            self.h_write = WriteTextFile (file    = self.file
                                         ,Rewrite = True
                                         ,UseLog  = False
                                         )
            self.Success = self.h_write.Success
            self.clear()

    def clear(self):
        if self.Success:
            self.h_write.write(text=_('***** Start of log. *****'))

    def _write(self):
        self.h_write.append (text='\n%d:%s:%s:%s' % (self.count
                                                    ,self.func
                                                    ,self.level
                                                    ,self.message
                                                    )
                            )

    def write(self):
        if self.Success and self.Write:
            if self.Short:
                if self.level == _('WARNING') \
                or self.level == _('ERROR'):
                    self._write()
            else:
                self._write()

    def print(self):
        if self.Success:
            if self.Print:
                if self.Short:
                    if self.level == _('WARNING') \
                    or self.level == _('ERROR'):
                        self._print()
                else:
                    self._print()

    def _print(self):
        f = '[shared] shared.Log._print'
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
                self.message = message
                self.print()
                self.write()
                self.count += 1

if oss.win():
    log = Log (Use   = True
              ,Write = False
              ,Print = True
              ,Short = False
              ,file  = r'C:\Users\pete\AppData\Local\Temp\log'
              )
else:
    log = Log (Use   = True
              ,Write = False
              ,Print = True
              ,Short = False
              ,file  = '/tmp/log'
              )



#todo: Do we really need this?
class TextDic:

    def __init__(self,file,Sortable=False):
        self.file     = file
        self.Sortable = Sortable
        self.h_read   = ReadTextFile(self.file)
        self.reset()

    ''' This is might be needed only for those dictionaries that
        already may contain duplicates (dictionaries with newly added
        entries do not have duplicates due to new algorithms)
    '''
    def _delete_duplicates(self):
        f = '[shared] shared.TextDic._delete_duplicates'
        if self.Success:
            if self.Sortable:
                old = self.lines()
                self._list = list(set(self.list()))
                new = self._lines = len(self._list)
                log.append (f,_('INFO')
                           ,_('Entries deleted: %d (%d-%d)') % (old-new
                                                               ,old
                                                               ,new
                                                               )
                           )
                self.text = '\n'.join(self._list)
                # Update original and translation
                self._split()
                # After using set(), the original order was lost
                self.sort()
            else:
                objs.mes (f,_('WARNING')
                         ,_('File "%s" is not sortable!') \
                         % self.file
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    # We can use this as an updater, even without relying on Success
    def _join(self):
        f = '[shared] shared.TextDic._join'
        if len(self.orig) == len(self.transl):
            self._lines = len(self.orig)
            self._list = []
            for i in range(self._lines):
                self._list.append(self.orig[i]+'\t'+self.transl[i])
            self.text = '\n'.join(self._list)
        else:
            objs.mes (f,_('WARNING')
                     ,_('Wrong input data!')
                     )

    def _split(self):
        ''' We can use this to check integrity and/or update original
            and translation lists.
        '''
        f = '[shared] shared.TextDic._split'
        if self.get():
            self.Success = True
            self.orig = []
            self.transl = []
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
                    objs.mes (f,_('WARNING')
                             ,_('Dictionary "%s": Incorrect line #%d: "%s"!')\
                             % (self.file,i+1,self._list[i])
                             )
        else:
            self.Success = False

    def append(self,original,translation):
        ''' #todo: skip repetitions
            #todo: write a dictionary in an append mode after appending
            to memory.
        '''
        f = '[shared] shared.TextDic.append'
        if self.Success:
            if original and translation:
                self.orig.append(original)
                self.transl.append(translation)
                self._join()
            else:
                objs.mes (f,_('WARNING')
                         ,_('Empty input is not allowed!')
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def delete_entry(self,entry_no): # Count from 1
        ''' #todo: #fix: an entry which is only one in a dictionary is
            not deleted.
        '''
        f = '[shared] shared.TextDic.delete_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.lines():
                del self.orig[entry_no]
                del self.transl[entry_no]
                self._join()
            else:
                objs.mes (f,_('ERROR')
                         ,_('The condition "%s" is not observed!') \
                         % ('0 <= ' + str(entry_no) + ' < %d' \
                           % self.lines()
                           )
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def edit_entry(self,entry_no,orig,transl): # Count from 1
        ''' #todo: Add checking orig and transl (where needed) for
            a wrapper function.
        '''
        f = '[shared] shared.TextDic.edit_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.lines():
                self.orig[entry_no] = orig
                self.transl[entry_no] = transl
                self._join()
            else:
                objs.mes (f,_('ERROR')
                         ,_('The condition "%s" is not observed!') \
                         % ('0 <= ' + str(entry_no) + ' < %d' \
                           % self.lines()
                           )
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def get(self):
        if not self.text:
            self.text = self.h_read.load()
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
        self.text = self.h_read.load()
        self.orig = []
        self.transl = []
        self._list = self.get().splitlines()
        self._lines = len(self._list)
        self._split()

    # Sort a dictionary with the longest lines going first
    def sort(self):
        f = '[shared] shared.TextDic.sort'
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
                objs.mes (f,_('WARNING')
                         ,_('File "%s" is not sortable!') % self.file
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def tail(self):
        f = '[shared] shared.TextDic.tail'
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return tail_text

    def write(self):
        f = '[shared] shared.TextDic.write'
        if self.Success:
            WriteTextFile (file    = self.file
                          ,Rewrite = True
                          ).write(self.get())
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



class ReadTextFile:

    def __init__(self,file):
        f = '[shared] shared.ReadTextFile.__init__'
        self.file    = file
        self._text   = ''
        self._list   = []
        self.Success = True
        if self.file and os.path.isfile(self.file):
            pass
        elif not self.file:
            self.Success = False
            objs.mes (f,_('ERROR')
                     ,_('Not enough input data!')
                     )
        elif not os.path.exists(self.file):
            self.Success = False
            objs.mes (f,_('WARNING')
                     ,_('File "%s" has not been found!') % self.file
                     )
        else:
            self.Success = False
            objs.mes (f,_('ERROR')
                     ,_('Wrong input data!')
                     )

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
        f = '[shared] shared.ReadTextFile.delete_bom'
        if self.Success:
            self._text = self._text.replace('\N{ZERO WIDTH NO-BREAK SPACE}','')
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    # Return the text from memory (or load the file first)
    def get(self):
        f = '[shared] shared.ReadTextFile.get'
        if self.Success:
            if not self._text:
                self.load()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._text

    # Return a number of lines in the file. Returns 0 for an empty file.
    def lines(self):
        f = '[shared] shared.ReadTextFile.lines'
        if self.Success:
            return len(self.list())
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def list(self):
        f = '[shared] shared.ReadTextFile.list'
        if self.Success:
            if not self._list:
                self._list = self.get().splitlines()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        # len(None) causes an error
        return self._list

    def load(self):
        f = '[shared] shared.ReadTextFile.load'
        if self.Success:
            log.append (f,_('INFO')
                       ,_('Load file "%s"') % self.file
                       )
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
                objs.mes (f,_('ERROR')
                         ,_('Unable to read file "%s"!') % self.file
                         )
            self.delete_bom()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._text



class Input:

    def __init__(self,value,title='Input'):
        self.title = title
        self.value = value

    def check_float(self):
        if isinstance(self.value,float):
            return self.value
        else:
            objs.mes (self.title
                     ,_('ERROR')
                     ,_('Float is required at input, but found "%s"! Return 0.0')\
                     % str(type(self.value))
                     )
            self.value = 0.0
        return self.value
    
    def list(self):
        if isinstance(self.value,list):
            return self.value
        else:
            log.append (self.title
                       ,_('WARNING')
                       ,_('Wrong input data!')
                       )
            return []
    
    def integer(self):
        if isinstance(self.value,int):
            return self.value
        elif str(self.value).isdigit():
            self.value = int(self.value)
            log.append (self.title
                       ,_('INFO')
                       ,_('Convert "%s" to an integer') % str(self.value)
                       )
        else:
            objs.mes (self.title
                     ,_('ERROR')
                     ,_('Integer is required at input, but found "%s"! Return 0')\
                     % str(type(self.value))
                     )
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

    def delete_autotranslate_markers(self):
        self.text = self.text.replace('[[','').replace(']]','').replace('{','').replace('}','').replace('_','')
        return self.text

    def delete_embraced_text(self,opening_sym='(',closing_sym=')'):
        ''' If there are some brackets left after performing this
            operation, ensure that all of them are in the right place
            (even when the number of opening and closing brackets is
            the same).
        '''
        f = '[shared] shared.Text.delete_embraced_text'
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
            objs.mes (f,_('WARNING')
                     ,_('Different number of opening and closing brackets: "%s": %d; "%s": %d!')\
                     % (opening_sym
                       ,self.text.count(opening_sym)
                       ,closing_sym
                       ,self.text.count(closing_sym)
                       )
                     )
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
        f = '[shared] shared.Text.delete_end_punc'
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
            log.append (f,_('WARNING')
                       ,_('Empty strings are not supported!')
                       )
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

    #todo: del
    def extract_date_hash(self):
        f = '[shared] shared.Text.extract_date_hash'
        hash = -1
        # Only strings at input
        result = self.text.split('-')
        if len(result) == 3:
            self.text = result[0]
            hash = self.str2int() * 365
            self.text = result[1]
            hash += self.str2int() * 12
            self.text = result[2]
            hash += self.str2int()
        '''
        else:
           objs.mes (f,_('WARNING')
                    ,_('Wrong input data!')
                    )
        '''
        return hash

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
        f = '[shared] shared.Text.split_by_comma'
        if (';' in self.text or ',' in self.text) and '\n' in self.text:
            objs.mes (f,_('WARNING')
                     ,_('Commas and/or semicolons or line breaks can be used, but not altogether!')
                     )
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
        f = '[shared] shared.Text.str2int'
        par = 0
        try:
            par = int(self.text)
        except(ValueError,TypeError):
            log.append (f,_('WARNING')
                       ,_('Failed to convert "%s" to an integer!') \
                       % str(self.text)
                       )
        return par

    def str2float(self):
        f = '[shared] shared.Text.str2float'
        par = 0.0
        try:
            par = float(self.text)
        except(ValueError,TypeError):
            log.append (f,_('WARNING')
                       ,_('Failed to convert "%s" to a floating-point number!')\
                       % str(self.text)
                       )
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

    def yo(self): # This allows to shorten dictionaries
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
                # We do not know for sure where quotes should be placed, but we cannot leave out cases like ' " '
                elif len(text) > 1 and text[-2].isspace() \
                and text[-1] == '"':
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
        if self._timestamp or self._timestamp == 0:
            self.instance()
        else:
            self.todays_date()

    def add_days(self,days_delta):
        f = '[shared] shared.Time.add_days'
        if self.Success:
            if not self._instance:
                self.instance()
            try:
                self._instance += datetime.timedelta(days=days_delta)
            except:
                self.Success = False
                objs.mes (f,_('WARNING')
                         ,_('Set time parameters are incorrect or not supported.')
                         )
            self.monday_warning()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def date(self):
        f = '[shared] shared.Time.date'
        if self.Success:
            if not self._instance:
                self.instance()
            try:
                self._date = self._instance.strftime(self.pattern)
            except:
                self.Success = False
                objs.mes (f,_('WARNING')
                         ,_('Set time parameters are incorrect or not supported.')
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._date

    def instance(self):
        f = '[shared] shared.Time.instance'
        if self.Success:
            if not self._timestamp:
                self.timestamp()
            try:
                self._instance = datetime.datetime.fromtimestamp(self._timestamp)
            except:
                self.Success = False
                objs.mes (f,_('WARNING')
                         ,_('Set time parameters are incorrect or not supported.')
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._instance

    def timestamp(self):
        f = '[shared] shared.Time.timestamp'
        if self.Success:
            if not self._date:
                self.date()
            try:
                self._timestamp = time.mktime(datetime.datetime.strptime(self._date,self.pattern).timetuple())
            except:
                self.Success = False
                objs.mes (f,_('WARNING')
                         ,_('Set time parameters are incorrect or not supported.')
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._timestamp

    def monday_warning(self):
        f = '[shared] shared.Time.monday_warning'
        if self.Success:
            if not self._instance:
                self.instance()
            if self.MondayWarning \
            and datetime.datetime.weekday(self._instance) == 0:
                objs.mes (f,_('INFO')
                         ,_('Note: it will be Monday!')
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def month_name(self):
        f = '[shared] shared.Time.month_name'
        if self.Success:
            if not self._instance:
                self.instance()
            self._month_name = calendar.month_name \
                             [Text (text = self._instance.strftime("%m")
                                   ,Auto = False
                                   ).str2int()
                             ]
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._month_name

    def localize_month_abbr(self):
        f = '[shared] shared.Time.localize_month_abbr'
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
            log.append (f,_('WARNING')
                       ,_('Wrong input data!')
                       )
        return self._month_abbr
    
    def month_abbr(self):
        f = '[shared] shared.Time.month_abbr'
        if self.Success:
            if not self._instance:
                self.instance()
            self._month_abbr = calendar.month_abbr \
                             [Text (text = self._instance.strftime("%m")
                                   ,Auto = False
                                   ).str2int()
                             ]
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._month_abbr

    def todays_date(self):
        self._instance = datetime.datetime.today()

    def year(self):
        f = '[shared] shared.Time.year'
        if self.Success:
            if not self._instance:
                self.instance()
            try:
                self._year = self._instance.strftime("%Y")
            except:
                self.Success = False
                objs.mes (f,_('WARNING')
                         ,_('Set time parameters are incorrect or not supported.')
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._year



class File:

    def __init__(self,file,dest=None,Rewrite=False):
        f = '[shared] shared.File.__init__'
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
            objs.mes (f,_('ERROR')
                     ,_('Empty input is not allowed!')
                     )
        elif not os.path.exists(self.file):
            self.Success = False
            objs.mes (f,_('WARNING')
                     ,_('File "%s" has not been found!') % self.file
                     )
        else:
            self.Success = False
            objs.mes (f,_('WARNING')
                     ,_('The object "%s" is not a file!') % self.file
                     )

    def _copy(self):
        f = '[shared] shared.File._copy'
        Success = True
        log.append (f,_('INFO')
                   ,_('Copy "%s" to "%s"') % (self.file,self.dest)
                   )
        try:
            shutil.copyfile(self.file,self.dest)
        except:
            Success = False
            objs.mes (f,_('ERROR')
                     ,_('Failed to copy file "%s" to "%s"!') \
                     % (self.file,self.dest)
                     )
        return Success

    def _move(self):
        f = '[shared] shared.File._move'
        Success = True
        log.append (f,_('INFO')
                   ,_('Move "%s" to "%s"') % (self.file,self.dest)
                   )
        try:
            shutil.move(self.file,self.dest)
        except:
            Success = False
            objs.mes (f,_('ERROR')
                     ,_('Failed to move "%s" to "%s"!') \
                     % (self.file,self.dest)
                     )
        return Success

    def access_time(self):
        f = '[shared] shared.File.access_time'
        if self.Success:
            try:
                self.atime = os.path.getatime(self.file)
                # Further steps: datetime.date.fromtimestamp(self.atime).strftime(self.pattern)
                return self.atime
            except:
                objs.mes (f,_('WARNING')
                         ,_('Failed to get the date of the file "%s"!') \
                         % self.file
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def copy(self):
        f = '[shared] shared.File.copy'
        Success = True
        if self.Success:
            if self.file.lower() == self.dest.lower():
                objs.mes (f,_('ERROR')
                         ,_('Unable to copy the file "%s" to iself!') \
                         % self.file
                         )
            elif com.rewrite (file    = self.dest
                             ,Rewrite = self.Rewrite
                             ):
                Success = self._copy()
            else:
                log.append (f,_('INFO')
                           ,_('Operation has been canceled by the user.')
                           )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return Success

    def delete(self):
        f = '[shared] shared.File.delete'
        Success = True
        if self.Success:
            log.append (f,_('INFO')
                       ,_('Delete "%s"') % self.file
                       )
            try:
                os.remove(self.file)
            except:
                Success = False
                objs.mes (f,_('WARNING')
                         ,_('Failed to delete file "%s"!') % self.file
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return Success

    def modification_time(self):
        f = '[shared] shared.File.modification_time'
        if self.Success:
            try:
                self.mtime = os.path.getmtime(self.file)
                # Further steps: datetime.date.fromtimestamp(self.mtime).strftime(self.pattern)
                return self.mtime
            except:
                objs.mes (f,_('WARNING')
                         ,_('Failed to get the date of the file "%s"!')\
                         % self.file
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def move(self):
        f = '[shared] shared.File.move'
        Success = True
        if self.Success:
            if self.file.lower() == self.dest.lower():
                objs.mes (f,_('WARNING')
                         ,_('Moving is not necessary, because the source and destination are identical (%s).')\
                         % self.file
                         )
            elif com.rewrite (file    = self.dest
                             ,Rewrite = self.Rewrite
                             ):
                Success = self._move()
            else:
                log.append (f,_('INFO')
                           ,_('Operation has been canceled by the user.')
                           )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return Success

    def set_time(self):
        f = '[shared] shared.File.set_time'
        if self.Success:
            if self.atime and self.mtime:
                log.append (f,_('INFO')
                           ,_('Change the time of the file "%s" to %s')\
                           % (self.file,str((self.atime,self.mtime)))
                           )
                try:
                    os.utime(self.file,(self.atime,self.mtime))
                except:
                    objs.mes (f,_('WARNING')
                             ,_('Failed to change the time of the file "%s" to "%s"!')\
                             % (self.file
                               ,str((self.atime,self.mtime))
                               )
                             )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



class Path:

    def __init__(self,path):
        self.reset(path)

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
        f = '[shared] shared.Path.create'
        # We actually don't need to fail the class globally
        Success = True
        if self.path:
            if os.path.exists(self.path):
                if os.path.isdir(self.path):
                    log.append (f,_('INFO')
                               ,_('Directory "%s" already exists.') \
                               % self.path
                               )
                else:
                    Success = False
                    objs.mes (f,_('WARNING')
                             ,_('The path "%s" is invalid!') % self.path
                             )
            else:
                log.append (f,_('INFO')
                           ,_('Create directory "%s"') % self.path
                           )
                try:
                    #todo: consider os.mkdir
                    os.makedirs(self.path)
                except:
                    Success = False
                    objs.mes (f,_('ERROR')
                             ,_('Failed to create directory "%s"!') \
                             % self.path
                             )
        else:
            Success = False
            objs.mes (f,_('ERROR')
                     ,_('Not enough input data!')
                     )
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
        self.path = path
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
        self.path      = self.path.rstrip('//')
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
        f = '[shared] shared.WriteBinary.__init__'
        self.Success = True
        self.file    = file
        self.obj     = obj
        if self.file and self.obj:
            self.Rewrite = Rewrite
            self.fragm   = None
        else:
            self.Success = False
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def _write(self,mode='w+b'):
        f = '[shared] shared.WriteBinary._write'
        log.append (f,_('INFO')
                   ,_('Write file "%s"') % self.file
                   )
        if mode == 'w+b' or mode == 'a+b':
            try:
                with open(self.file,mode) as fl:
                    if mode == 'w+b':
                        pickle.dump(self.obj,fl)
                    elif mode == 'a+b':
                        pickle.dump(self.fragm,fl)
            except:
                self.Success = False
                objs.mes (f,_('ERROR')
                         ,_('Unable to write file "%s"!') % self.file
                         )
        else:
            objs.mes (f,_('ERROR')
                     ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".')\
                     % (str(mode),'w+b, a+b')
                     )

    def append(self,fragm):
        f = '[shared] shared.WriteBinary.append'
        if self.Success:
            self.fragm = fragm
            if self.fragm:
                self._write(mode='a+b')
            else:
                objs.mes (f,_('ERROR')
                         ,_('Empty input is not allowed!')
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def write(self):
        f = '[shared] shared.WriteBinary.write'
        if self.Success:
            if com.rewrite (file    = self.file
                           ,Rewrite = self.Rewrite
                           ):
                self._write(mode='w+b')
            else:
                log.append (f,_('INFO')
                           ,_('Operation has been canceled by the user.')
                           )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



class Dic:

    def __init__(self,file,Sortable=False):
        self.file     = file
        self.Sortable = Sortable
        self.errors   = []
        self.h_read   = ReadTextFile(self.file)
        self.reset()

    def _delete_duplicates(self):
        ''' This is might be needed only for those dictionaries that
            already may contain duplicates (dictionaries with newly
            added entries do not have duplicates due to new algorithms).
        '''
        f = '[shared] shared.Dic._delete_duplicates'
        if self.Success:
            if self.Sortable:
                old = self.lines()
                self._list = list(set(self.list()))
                new = self._lines = len(self._list)
                log.append (f,_('INFO')
                           ,_('Entries deleted: %d (%d-%d)') % (old-new
                                                               ,old
                                                               ,new
                                                               )
                           )
                self.text = '\n'.join(self._list)
                # Update original and translation
                self._split()
                # After using set(), the original order was lost
                self.sort()
            else:
                objs.mes (f,_('WARNING')
                         ,_('File "%s" is not sortable!') % self.file
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    # We can use this as an updater, even without relying on Success
    def _join(self):
        f = '[shared] shared.Dic._join'
        if len(self.orig) == len(self.transl):
            self._lines = len(self.orig)
            self._list = []
            for i in range(self._lines):
                self._list.append(self.orig[i]+'\t'+self.transl[i])
            self.text = '\n'.join(self._list)
        else:
            objs.mes (f,_('WARNING')
                     ,_('Wrong input data!')
                     )

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
        f = '[shared] shared.Dic.warn'
        if self.errors:
            message = ', '.join(self.errors)
            objs.mes (f,_('WARNING')
                     ,_('The following lines cannot be parsed:') \
                     + '\n' + message
                     )

    def append(self,original,translation):
        ''' #todo: write a dictionary in an append mode after appending
                   to memory.
            #todo: skip repetitions
        '''
        f = '[shared] shared.Dic.append'
        if self.Success:
            if original and translation:
                self.orig.append(original)
                self.transl.append(translation)
                self._join()
            else:
                objs.mes (f,_('WARNING')
                         ,_('Empty input is not allowed!')
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    # Count from 1
    def delete_entry(self,entry_no):
        ''' #todo: fix: an entry which is only one in a dictionary is
            not deleted.
        '''
        f = '[shared] shared.Dic.delete_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.lines():
                del self.orig[entry_no]
                del self.transl[entry_no]
                self._join()
            else:
                objs.mes (f,_('ERROR')
                         ,_('The condition "%s" is not observed!') \
                         % ('0 <= ' + str(entry_no) + ' < %d' \
                           % self.lines()
                           )
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    # Count from 1
    def edit_entry(self,entry_no,orig,transl):
        ''' #todo: Add checking orig and transl (where needed) for
            a wrapper function.
        '''
        f = '[shared] shared.Dic.edit_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.lines():
                self.orig[entry_no] = orig
                self.transl[entry_no] = transl
                self._join()
            else:
                objs.mes (f,_('ERROR')
                         ,_('The condition "%s" is not observed!') \
                         % ('0 <= ' + str(entry_no) + ' < %d' \
                           % self.lines()
                           )
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def get(self):
        if not self.text:
            self.text = self.h_read.load()
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
        self.text   = self.h_read.load()
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
        f = '[shared] shared.Dic.sort'
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
                objs.mes (f,_('WARNING')
                         ,_('File "%s" is not sortable!') % self.file
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def tail(self):
        f = '[shared] shared.Dic.tail'
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return tail_text

    def write(self):
        f = '[shared] shared.Dic.write'
        if self.Success:
            WriteTextFile (file    = self.file
                          ,Rewrite = True
                          ).write(self.get())
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



class ReadBinary:

    def __init__(self,file):
        self.file    = file
        self.obj     = None
        h_file       = File(self.file)
        self.Success = h_file.Success

    def _load(self):
        f = '[shared] shared.ReadBinary._load'
        log.append (f,_('INFO')
                   ,_('Load file "%s"') % self.file
                   )
        try:
            ''' AttributeError means that a module using _load does not
                have a class that was defined while creating the binary
            '''
            with open(self.file,'r+b') as fl:
                self.obj = pickle.load(fl)
        except Exception as e:
            self.Success = False
            objs.mes (f,_('WARNING')
                     ,_('Unable to read file "%s"!\n\nDetails: %s') \
                     % (self.file,str(e))
                     )

    #todo: load fragments appended to a binary
    def load(self):
        f = '[shared] shared.ReadBinary.load'
        if self.Success:
            self._load()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
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
        f = '[shared] shared.Directory.__init__'
        self.values()
        if path:
            # Removes trailing slashes if necessary
            self.dir = Path(path).path
        else:
            self.dir = ''
        if dest:
            self.dest = Path(dest).path
        else:
            self.dest = self.dir
        if not os.path.isdir(self.dir):
            self.Success = False
            objs.mes (f,_('WARNING')
                     ,_('Wrong input data: "%s"') % self.dir
                     )

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
        f = '[shared] shared.Directory.extensions'
        if self.Success:
            if not self._extensions:
                for file in self.rel_files():
                    ext = Path(path=file).extension()
                    self._extensions.append(ext)
                    self._extensions_low.append(ext.lower())
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._extensions

    def extensions_low(self): # with a dot
        f = '[shared] shared.Directory.extensions_low'
        if self.Success:
            if not self._extensions_low:
                self.extensions()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._extensions_low

    def delete_empty(self):
        f = '[shared] shared.Directory.delete_empty'
        if self.Success:
            # Do not delete nested folders
            if not os.listdir(self.dir):
                self.delete()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
    
    def delete(self):
        f = '[shared] shared.Directory.delete'
        if self.Success:
            log.append (f,_('INFO')
                       ,_('Delete "%s"') % self.dir
                       )
            try:
                shutil.rmtree(self.dir)
            except:
                objs.mes (f,_('WARNING')
                         ,_('Failed to delete directory "%s"! Delete it manually.')\
                         % str(self.dir)
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    # Create a list of objects with a relative path
    def rel_list(self):
        if self.Success:
            if not self._rel_list:
                self.list()
        return self._rel_list

    # Create a list of objects with an absolute path
    def list(self):
        f = '[shared] shared.Directory.list'
        if self.Success:
            if not self._list:
                self._list = os.listdir(self.dir)
                self._list.sort(key=lambda x: x.lower())
                self._rel_list = list(self._list)
                for i in range(len(self._list)):
                    self._list[i] = os.path.join(self.dir,self._list[i])
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
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
        f = '[shared] shared.Directory.dirs'
        if self.Success:
            if not self._dirs:
                for i in range(len(self.list())):
                    if os.path.isdir(self._list[i]):
                        self._dirs.append(self._list[i])
                        self._rel_dirs.append(self._rel_list[i])
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._dirs

    # Needs absolute path
    def files(self):
        f = '[shared] shared.Directory.files'
        if self.Success:
            if not self._files:
                for i in range(len(self.list())):
                    if os.path.isfile(self._list[i]):
                        self._files.append(self._list[i])
                        self._rel_files.append(self._rel_list[i])
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._files

    def copy(self):
        f = '[shared] shared.Directory.copy'
        if self.Success:
            if self.dir.lower() == self.dest.lower():
                objs.mes (f,_('ERROR')
                         ,_('Unable to copy "%s" to iself!') % self.dir
                         )
            elif os.path.isdir(self.dest):
                objs.mes (f,_('INFO')
                         ,_('Directory "%s" already exists.') \
                         % self.dest
                         )
            else:
                self._copy()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def _copy(self):
        f = '[shared] shared.Directory._copy'
        log.append (f,_('INFO')
                   ,_('Copy "%s" to "%s"') % (self.dir,self.dest)
                   )
        try:
            shutil.copytree(self.dir,self.dest)
        except:
            self.Success = False
            objs.mes (f,_('WARNING')
                     ,_('Failed to copy "%s" to "%s"!') \
                     % (self.dir,self.dest)
                     )



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
        f = '[shared] shared.Config.load'
        if self.Success:
            for i in range(len(self.sections)):
                for option in globs[self.sections_abbr[i]]:
                    new_val = self.sections_func[i](self.sections[i],option)
                    if globs[self.sections_abbr[i]][option] != new_val:
                        log.append (f,_('INFO')
                                   ,_('New value of the key "%s" has been loaded.')\
                                   % option
                                   )
                        self.changed_keys += 1
                        globs[self.sections_abbr[i]][option] = new_val
            log.append (f,_('INFO')
                       ,_('Keys loaded in total: %d, whereas %d are modified.') \
                       % (self.total_keys,self.changed_keys)
                       )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def check(self):
        f = '[shared] shared.Config.check'
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
                self.message += '\n' + _('Missing sections: %d') \
                                % self.missing_sections
                self.message += '\n' + _('Missing keys: %d') \
                                % self.missing_keys
                self.message += '\n' + _('The default configuration has been loaded.')
                objs.mes (func    = 'Config.check'
                         ,level   = _('WARNING')
                         ,message = self.message
                         )
                self._default()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def open(self):
        f = '[shared] shared.Config.open'
        if self.Success:
            try:
                config_parser.read(self.path,'utf-8')
            except:
                Success = False
                objs.mes (f,_('WARNING')
                         ,_('Failed to read the configuration file "%s". This file must share the same directory with the program and have UTF-8 encoding (no BOM) and UNIX line break type.')\
                         % self.path
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



class Online:

    def __init__ (self,base_str='%s',search_str=''
                 ,encoding='UTF-8',MTSpecific=False
                 ):
        self.reset (base_str   = base_str
                   ,search_str = search_str
                   ,encoding   = encoding
                   ,MTSpecific = MTSpecific
                   )

    def bytes_common(self):
        if not self._bytes:
            self._bytes = bytes (self.search_str
                                ,encoding = self.encoding
                                )

    def bytes_multitran(self):
        if not self._bytes:
            # Otherwise, will not be able to encode 'Ъ'
            try:
                self._bytes = bytes (self.search_str
                                    ,encoding = globs['var']['win_encoding']
                                    )
            except:
                ''' Otherwise, will not be able to encode specific
                    characters
                '''
                try:
                    self._bytes = bytes (self.search_str
                                        ,encoding='UTF-8'
                                        )
                except:
                    self._bytes = ''

    def bytes(self):
        if self.MTSpecific:
            self.bytes_multitran()
        else:
            self.bytes_common()
        return self._bytes

    # Open a URL in a default browser
    def browse(self):
        f = '[shared] shared.Online.browse'
        try:
            webbrowser.open(self.url(),new=2,autoraise=True)
        except:
            objs.mes (f,_('ERROR')
                     ,_('Failed to open URL "%s" in a default browser!')\
                     % self._url
                     )

    # Create a correct online link (URI => URL)
    def url(self):
        f = '[shared] shared.Online.url'
        if not self._url:
            self._url = self.base_str % urllib.parse.quote(self.bytes())
            log.append (f,_('DEBUG')
                       ,str(self._url)
                       )
        return self._url

    def reset (self,base_str='',search_str=''
              ,encoding='UTF-8',MTSpecific=False
              ):
        self.encoding   = encoding
        self.MTSpecific = MTSpecific
        self.base_str   = base_str
        self.search_str = search_str
        self._bytes     = None
        self._url       = None



class Diff:

    def __init__(self):
        self.Custom      = False
        ''' Some browsers update web-page as soon as we rewrite it, and
            some even do not open the same file again. So, we have to
            create a new temporary file each time.
        '''
        self.wda_html    = com.tmpfile(suffix='.htm',Delete=0)
        self.h_wda_write = WriteTextFile (file    = self.wda_html
                                         ,Rewrite = True
                                         )

    def reset(self,text1,text2,file=None):
        self._diff = ''
        self.text1 = text1
        self.text2 = text2
        if file:
            self.Custom  = True
            self.file    = file
            self._header = ''
            self.h_write = WriteTextFile (file    = self.file
                                         ,Rewrite = False
                                         )
            self.h_path  = Path(self.file)
        else:
            self.Custom  = False
            self.file    = self.wda_html
            self._header = '<title>%s</title>' % _('Differences:')
            self.h_write = self.h_wda_write
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
            self._header = self.h_path.basename().replace(self.h_path.extension(),'')
            self._header = '<title>' + self._header + '</title>'
        self._diff = self._diff.replace('<title></title>',self._header)\
                     + '\n'

    def compare(self):
        f = '[shared] shared.Diff.compare'
        if self.text1 and self.text2:
            if self.text1 == self.text2:
                objs.mes (f,_('INFO')
                         ,_('Texts are identical!')
                         )
            else:
                self.diff()
                self.header()
                self.h_write.write(self._diff)
                if self.h_write.Success:
                    ''' Cannot reuse the class instance because the
                        temporary file might be missing
                    '''
                    Launch(target=self.file).default()
        else:
            objs.mes (f,_('WARNING')
                     ,_('Empty input is not allowed!')
                     )



class Shortcut:

    def __init__(self,symlink='',path=''):
        f = '[shared] shared.Shortcut.__init__'
        self.Success = True
        self.path    = path
        self.symlink = symlink
        if not self.path and not self.symlink:
            self.Success = False
            objs.mes (f,_('WARNING')
                     ,_('Wrong input data!')
                     )

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
            if oss.win():
                self._get_win()
            else:
                self._get_unix()
        return self.path

    def _delete(self):
        f = '[shared] shared.Shortcut._delete'
        log.append (f,_('INFO')
                   ,_('Delete the symbolic link "%s"') % self.symlink
                   )
        try:
            os.unlink(self.symlink)
        except:
            objs.mes (f,_('WARNING')
                     ,_('Failed to remove shortcut "%s". Remove it manually and press OK.')\
                     % self.symlink
                     )

    def delete(self):
        f = '[shared] shared.Shortcut.delete'
        if self.Success:
            if os.path.islink(self.symlink):
                self._delete()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def _create_unix(self):
        f = '[shared] shared.Shortcut._create_unix'
        log.append (f,_('INFO')
                   ,_('Create a symbolic link "%s"') % self.symlink
                   )
        try:
            os.symlink(self.path,self.symlink)
        except:
            objs.mes (f,_('ERROR')
                     ,_('Failed to create shortcut "%s". Create it manually and press OK.')\
                     % self.symlink
                     )

    def create_unix(self):
        f = '[shared] shared.Shortcut.create_unix'
        self.delete()
        if os.path.exists(self.symlink):
            if os.path.islink(self.symlink):
                log.append (f,_('INFO')
                           ,_('Nothing to do.')
                           )
            else:
                self.Success = False
                objs.mes (f,_('WARNING')
                         ,_('Wrong input data!')
                         )
        else:
            self._create_unix()

    def _create_win(self):
        f = '[shared] shared.Shortcut._create_win'
        log.append (f,_('INFO')
                   ,_('Create a symbolic link "%s"') % self.symlink
                   )
        try:
            # The code will automatically add '.lnk' if necessary
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(self.symlink)
            shortcut.Targetpath = self.path
            shortcut.save()
        except:
            objs.mes (f,_('ERROR')
                     ,_('Failed to create shortcut "%s". Create it manually and press OK.')\
                     % self.symlink
                     )

    def create_win(self):
        ''' Using python 3 and windows (since 2009) it is possible to
            create a symbolic link, however, this will not be the same
            as a shortcut (.lnk). Therefore, in case the shortcut is
            used, os.path.islink() will always return False (not
            supported) (must use os.path.exists()), however, os.unlink()
            will work as expected.
        '''
        # Do not forget: windows paths must have a double backslash!
        f = '[shared] shared.Shortcut.create_win'
        if self.Success:
            if not Path(self.symlink).extension().lower() == '.lnk':
                self.symlink += '.lnk'
            self.delete()
            if os.path.exists(self.symlink):
                log.append (f,_('INFO')
                           ,_('Nothing to do.')
                           )
            else:
                self._create_win()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def create(self):
        f = '[shared] shared.Shortcut.create'
        if self.Success:
            if oss.win():
                self.create_win()
            else:
                self.create_unix()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



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
    def __init__(self,email='',subject='',message='',attachment=''):
        if email:
            self.reset (email      = email
                       ,subject    = subject
                       ,message    = message
                       ,attachment = attachment
                       )
    
    def reset(self,email,subject='',message='',attachment=''):
        f = '[shared] shared.Email.reset'
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
            log.append (f,_('WARNING')
                       ,_('Empty input is not allowed!')
                       )
        if self._attachment:
            self.Success = File(file=self._attachment).Success
            if not self.Success:
                log.append (f,_('WARNING')
                           ,_('Operation has been canceled.')
                           )

    # Screen symbols that may cause problems when composing 'mailto'
    def sanitize(self,value):
        f = '[shared] shared.Email.sanitize'
        if self.Success:
            return str(Online(search_str=value).url())
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
    
    def browser(self):
        f = '[shared] shared.Email.browser'
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
                objs.mes (f,_('WARNING')
                         ,_('Failed to load an e-mail client.')
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
    
    def create(self):
        f = '[shared] shared.Email.create'
        if self.Success:
            if not self.evolution() and not self.thunderbird() \
            and not self.outlook():
                self._subject    = self.sanitize(self._subject)
                self._message    = self.sanitize(self._message)
                self._attachment = self.sanitize(self._attachment)
                self.browser()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
                       
    #note: this does not work in wine!
    def outlook(self):
        f = '[shared] shared.Email.outlook'
        if oss.win():
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
                objs.mes (f,_('WARNING')
                         ,_('Operation has failed!\nDetails: %s') % str(e)
                         )
        else:
            log.append (f,_('INFO')
                       ,_('This operation cannot be executed on your operating system.')
                       )
    
    def thunderbird(self):
        f = '[shared] shared.Email.thunderbird'
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
                    objs.mes (f,_('WARNING')
                             ,_('Failed to run "%s"!') \
                             % str(self.custom_args)
                             )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
    
    def evolution(self):
        f = '[shared] shared.Email.evolution'
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
                    objs.mes (f,_('WARNING')
                             ,_('Failed to run "%s"!') \
                             % str(self.custom_args)
                             )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



class Grep:

    def __init__(self,lst,start=[],middle=[],end=[]):
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
                     = self._spell_ru = self._sents_len = self._tf \
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
        f = '[shared] shared.Word.print'
        log.append (f,_('DEBUG')
                   ,'no: %d; _p: %s; _n: %s; _nm: %s; _pf: %s; _pl: %s; _nf: %s; _nl: %s; _cyr: %s; _lat: %s; _greek: %s; _digit: %s; _empty: %s; _ref: %s; _sent_no: %s; _sents_len: %s; _spell_ru: %s; _nmf: %s; _nml: %s' \
                   % (no,str(self._p),str(self._n)
                     ,str(self._nm),str(self._pf),str(self._pl)
                     ,str(self._nf),str(self._nl),str(self._cyr)
                     ,str(self._lat),str(self._greek),str(self._digit)
                     ,str(self._empty),str(self._ref)
                     ,str(self._sent_no),str(self._sents_len)
                     ,str(self._spell_ru),str(self._nmf),str(self._nml)
                     )
                   )

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
        ''' Enchant:
            1) Lower-case, upper-case and words where the first letter
               is capital, are all accepted. Mixed case is not accepted.
            2) Punctuation is not accepted
            3) Empty input raises an exception
        '''
        if self._spell_ru is None:
            self._spell_ru = True
            if self._n:
                self._spell_ru = objs.enchant().check(self._n)
        return self._spell_ru

    # Wrong selection upon search: see an annotation to SearchBox
    def tf(self):
        f = '[shared] shared.Word.tf'
        if self._tf is None:
            self._tf = '1.0'
            # This could happen if double line breaks were not deleted
            if self._sent_no is None:
                log.append (f,_('WARNING')
                           ,_('Not enough input data!')
                           )
            else:
                # This is easier, but assigning a tag throws an error
                #self._tf = '1.0+%dc' % (self._pf - self._sent_no)
                result = self._pf - self._sents_len
                if self._sent_no > 0 and result > 0:
                    result -= 1
                self._tf = '%d.%d' % (self._sent_no + 1,result)
                #log.append ('Word.tf',_('DEBUG'),self._tf)
        return self._tf

    def tl(self):
        f = '[shared] shared.Word.tl'
        if self._tl is None:
            self._tl = '1.1'
            # This could happen if double line breaks were not deleted
            if self._sent_no is None:
                log.append (f,_('WARNING')
                           ,_('Not enough input data!')
                           )
            else:
                # This is easier, but assigning a tag throws an error
                #self._tl = '1.0+%dc' % (self._pl - self._sent_no + 1)
                result = self._pl - self._sents_len
                if self._sent_no > 0 and result > 0:
                    result -= 1
                self._tl = '%d.%d' % (self._sent_no + 1,result + 1)
                #log.append(f,_('DEBUG'),self._tl)
        return self._tl



# Use cases: case-insensitive search; spellchecking; text comparison
# Requires Search, Text
class Words:

    def __init__(self,text,Auto=False):
        f = '[shared] shared.Words.__init__'
        self.Success = True
        self.Auto    = Auto
        self.values()
        if text:
            log.append (f,_('INFO')
                       ,_('Analyze the text')
                       )
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
                       
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
        f = '[shared] shared.Words.split'
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def print(self):
        f = '[shared] shared.Words.print'
        if self.Success:
            for i in range(self.len()):
                self.words[i].print(no=i)
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

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
        f = '[shared] shared.Words.sent_nos'
        if self.Success:
            if self.len() > 0:
                if self.words[self._no]._sent_no is None:
                    self._sent_nos()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def sent_p(self):
        f = '[shared] shared.Words.sent_p'
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def sent_no(self):
        f = '[shared] shared.Words.sent_no'
        if self.Success:
            self.sent_nos()
            return self.words[self._no]._sent_no
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def next_ref(self):
        f = '[shared] shared.Words.next_ref'
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def prev_ref(self):
        f = '[shared] shared.Words.prev_ref'
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def _spellcheck_ru(self):
        for i in range(self.len()):
            self.words[i].spell_ru()

    def spellcheck_ru(self):
        f = '[shared] shared.Words.spellcheck_ru'
        if self.Success:
            if self.len() > 0:
                if self.words[0]._spell_ru is None:
                    self._spellcheck_ru()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def _refs(self):
        for i in range(self.len()):
            self.words[i].ref()

    def refs(self):
        f = '[shared] shared.Words.refs'
        if self.Success:
            if self.len() > 0:
                if self.words[0]._ref is None:
                    self._refs()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    # Needed for text comparison
    def list_nm(self):
        f = '[shared] shared.Words.list_nm'
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    # Needed for text comparison
    def text_nm(self):
        f = '[shared] shared.Words.text_nm'
        if self.Success:
            if not self._text_nm:
                self._text_nm = ' '.join(self.list_nm())
            return self._text_nm
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def no_by_pos_p(self,pos):
        f = '[shared] shared.Words.no_by_pos_p'
        if self.Success:
            result = self._no
            for i in range(self.len()):
                if self.words[i]._pf - 1 <= pos <= self.words[i]._pl + 1:
                    result = i
                    break
            return result
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def no_by_pos_n(self,pos):
        f = '[shared] shared.Words.no_by_pos_n'
        if self.Success:
            result = self._no
            for i in range(self.len()):
                if self.words[i]._nf - 1 <= pos <= self.words[i]._nl + 1:
                    result = i
                    break
            return result
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    # Call 'list_nm()' first
    def no_by_pos_nm(self,pos):
        f = '[shared] shared.Words.no_by_pos_nm'
        if self.Success:
            result = self._no
            for i in range(self.len()):
                if self.words[i]._nmf - 1 <= pos <= self.words[i]._nml + 1:
                    result = i
                    break
            return result
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def no_by_tk(self,tkpos):
        f = '[shared] shared.Words.no_by_tk'
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
                        log.append (f,_('DEBUG')
                                   ,'%s -> %d' % (tkpos,result)
                                   )
                        return self.no_by_pos_p(pos=result)
                else:
                    objs.mes (f,_('WARNING')
                             ,_('Wrong input data: "%s"') % str(lst)
                             )
            else:
                objs.mes (f,_('WARNING')
                         ,_('Wrong input data: "%s"') % str(lst)
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def nos_by_sent_no(self,sent_no=0):
        f = '[shared] shared.Words.nos_by_sent_no'
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
                log.append (f,_('WARNING')
                           ,_('Failed to find words of paragraph #%d!')\
                           % sent_no
                           )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return result

    def complete(self):
        f = '[shared] shared.Words.complete'
        if self.Success:
            self.sent_nos()
            for i in range(self.len()):
                self.words[i].empty()
                self.words[i].ref()
                self.words[i].nm()
                self.words[i].spell_ru()
                self.words[i].tf()
                self.words[i].tl()
            self.text_nm()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



class Search:

    def __init__(self,text=None,search=None):
        self.Success    = False
        self.i          = 0
        self._next_loop = []
        self._prev_loop = []
        if text and search:
            self.reset(text=text,search=search)

    def reset(self,text,search):
        f = '[shared] shared.Search.reset'
        self.Success    = True
        self.i          = 0
        self._next_loop = []
        self._prev_loop = []
        self._text      = text
        self._search    = search
        if not self._search or not self._text:
            objs.mes (f,_('WARNING')
                     ,_('Wrong input data!')
                     )
            self.Success = False

    def add(self):
        f = '[shared] shared.Search.add'
        if self.Success:
            if len(self._text) > self.i + len(self._search) - 1:
                self.i += len(self._search)
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def next(self):
        f = '[shared] shared.Search.next'
        if self.Success:
            result = self._text.find(self._search,self.i)
            if result != -1:
                self.i = result
                self.add()
            return result
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def prev(self):
        f = '[shared] shared.Search.prev'
        if self.Success:
            ''' rfind, unlike find, does not include limits, so we can
                use it to search backwards
            '''
            result = self._text.rfind(self._search,0,self.i)
            if result != -1:
                self.i = result
            return result
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def next_loop(self):
        f = '[shared] shared.Search.next_loop'
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        return self._next_loop

    def prev_loop(self):
        f = '[shared] shared.Search.prev_loop'
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
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
        f = '[shared] shared.Decline.decline'
        for i in range(len(self._list)):
            # Inflecting '', None, digits and Latin words *only* fails
            ''' log.append (f,_('DEBUG')
                           ,_('Decline "%s" in "%s" number and "%s" case')\
                           % (str(self._list[i])
                             ,str(self.number())
                             ,str(self.case())
                             )
                           )
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
        f = '[shared] shared.Decline.number'
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
            ''' log.append (f,_('DEBUG')
                           ,str(self._number)
                           )
            '''
        return self._number

    def case(self):
        f = '[shared] shared.Decline.case'
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
            log.append (f,_('DEBUG')
                       ,str(self._case)
                       )
        return self._case



class Objects:
    ''' Values here will be kept through different modules (but not
        through different programs both using 'shared.py').
    '''
    def __init__(self):
        self._enchant = self._morph = self._pretty_table = self._diff \
                      = self._pdir = self._mes = self._online_mt \
                      = self._online_other = self._tmpfile = None

    def tmpfile(self,suffix='.htm',Delete=0):
        if self._tmpfile is None:
            self._tmpfile = com.tmpfile (suffix = suffix
                                        ,Delete = Delete
                                        )
        return self._tmpfile
    
    def online_mt(self):
        if self._online_mt is None:
            self._online_mt = Online(MTSpecific=True)
        return self._online_mt

    def online_other(self):
        if self._online_other is None:
            self._online_other = Online(MTSpecific=False)
        return self._online_other
    
    def mes (self,func='MAIN',level=_('DEBUG')
            ,message='',Silent=False
            ):
        ''' Call this externally for each GUI module like that:
            sh.objs.mes(Silent=False)
            Do not call this directly in 'sharedGUI' because
            cross-module import will fail ('sharedGUI' uses 'shared').
        '''
        if not self._mes:
            if Silent:
                self._mes = log.append
            else:
                import sharedGUI as sg
                self._mes = sg.Message
        if message:
            ''' Passing an empty message is useful for just setting
                GUI/non-GUI logging.
                Returning the function results may be useful if, for
                example, we need 'sg.Message.Yes' value.
            '''
            return self._mes (func    = func
                             ,level   = level
                             ,message = message
                             )
    
    def pdir(self):
        if not self._pdir:
            self._pdir = ProgramDir()
        return self._pdir

    def enchant(self):
        if not self._enchant:
            import enchant
            self._enchant = enchant.Dict("ru_RU")
        return self._enchant

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

    def diff(self):
        if not self._diff:
            self._diff = Diff()
        return self._diff



class MessagePool:

    def __init__(self,max_size=5):
        self.max_size = max_size
        self.pool = []

    def free(self):
        if len(self.pool) == self.max_size:
            self.delete_first()

    def add(self,message):
        f = '[shared] shared.MessagePool.add'
        if message:
            self.free()
            self.pool.append(message)
        else:
            log.append (f,_('WARNING')
                       ,_('Empty input is not allowed!')
                       )

    def delete_first(self):
        f = '[shared] shared.MessagePool.delete_first'
        if len(self.pool) > 0:
            del self.pool[0]
        else:
            log.append (f,_('WARNING')
                       ,_('The pool is empty!')
                       )

    def delete_last(self):
        f = '[shared] shared.MessagePool.delete_last'
        if len(self.pool) > 0:
            del self.pool[-1]
        else:
            log.append (f,_('WARNING')
                       ,_('The pool is empty!')
                       )

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
        log.append (self._func_title
                   ,_('INFO')
                   ,_('The operation has taken %f s.') \
                   % delta
                   )
        return delta



class Table:

    def __init__ (self,headers,rows
                 ,Shorten=True,MaxRow=18
                 ,MaxRows=20
                 ):
        f = '[shared] shared.Table.__init__'
        self._headers = headers
        self._rows    = rows
        self.Shorten  = Shorten
        self.MaxRow   = MaxRow
        self.MaxRows  = MaxRows
        if self._headers and self._rows:
            self.Success = True
        else:
            self.Success = False
            log.append (f,_('WARNING')
                       ,_('Empty input is not allowed!')
                       )

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
        f = '[shared] shared.Table._shorten_rows'
        if self.MaxRows < 2 or self.MaxRows > len(self._rows):
            self.MaxRows = len(self._rows)
            log.append (f,_('INFO')
                       ,_('Set the max number of rows to %d') \
                       % self.MaxRows
                       )
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
        f = '[shared] shared.Table.shorten'
        if self.Success:
            if self.Shorten:
                self._shorten_headers()
                self._shorten_rows   ()
                self._shorten_row    ()
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )

    def print(self):
        f = '[shared] shared.Table.print'
        if self.Success:
            self.shorten()
            obj = objs.pretty_table()(self._headers)
            for row in self._rows:
                obj.add_row(row)
            print(obj)
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



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
        elif oss.win():
            self.win()
        elif oss.lin():
            self.lin()
        elif oss.mac():
            self.mac()
        else:
            self.win()
            self.lin()
            self.mac()
        self.length()
        return self._name



class Get:
    
    def __init__(self,url,encoding='UTF-8',Verbose=True,Verify=False):
        self._timeout  = 6
        self._html     = ''
        self._url      = url
        self._encoding = encoding
        self.Verbose   = Verbose
        self.Verify    = Verify
        self.unverified()
        
    def unverified(self):
        ''' On *some* systems we can get urllib.error.URLError: 
            <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED].
            To get rid of this error, we use this small workaround.
        '''
        f = '[shared] shared.Get.unverified'
        if not self.Verify:
            if hasattr(ssl,'_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
            else:
                log.append (f,_('WARNING')
                           ,_('Unable to use unverified certificates!')
                           )
        
    def _get(self):
        ''' Changing UA allows us to avoid a bot protection
            ('Error 403: Forbidden').
        '''
        f = '[shared] shared.Get._get'
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
                log.append (f,_('INFO')
                           ,_('[OK]: "%s"') % self._url
                           )
        # Too many possible exceptions
        except Exception as e:
            log.append (f,_('WARNING')
                       ,_('[FAILED]: "%s". Details: %s') \
                       % (self._url,str(e))
                       )
    
    def decode(self):
        ''' Set 'encoding' to None to cancel decoding. This is useful
            if we are downloading a non-text content.
        '''
        f = '[shared] shared.Get.decode'
        if self._encoding:
            if self._html:
                try:
                    self._html = \
                    self._html.decode(encoding=self._encoding)
                except UnicodeDecodeError:
                    self._html = str(self._html)
                    log.append (f,_('WARNING')
                               ,_('Unable to decode "%s"!') \
                                % str(self._url)
                               )
            else:
                log.append (f,_('WARNING')
                           ,_('Empty input is not allowed!')
                           )
    
    def run(self):
        f = '[shared] shared.Get.run'
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
                log.append (f,_('WARNING')
                           ,_('Wrong input data!')
                           )
        else:
            log.append (f,_('WARNING')
                       ,_('Empty input is not allowed!')
                       )



class References:
    
    def __init__(self,words1,words2):
        f = '[shared] shared.References.__init__'
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
            log.append (f,_('WARNING')
                       ,_('Empty input is not allowed!')
                       )
        
    def ref_before(self,word_no):
        f = '[shared] shared.References.ref_before'
        if self.Success:
            if word_no < len(self.words1.words):
                while word_no >= 0:
                    if self.words1.words[word_no]._ref:
                        break
                    else:
                        word_no -= 1
                return word_no
            else:
                objs.mes (f,_('ERROR')
                         ,_('The condition "%s" is not observed!') \
                         % '%d < %d' % (word_no,len(self.words1.words))
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        
    def ref_after(self,word_no):
        f = '[shared] shared.References.ref_after'
        if self.Success:
            if word_no < len(self.words1.words):
                while word_no < len(self.words1.words):
                    if self.words1.words[word_no]._ref:
                        return word_no
                    else:
                        word_no += 1
                return -1
            else:
                objs.mes (f,_('ERROR')
                         ,_('The condition "%s" is not observed!') \
                         % '%d < %d' % (word_no,len(self.words1.words))
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
    
    def nearest_ref(self,word_no):
        f = '[shared] shared.References.nearest_ref'
        if self.Success:
            word_no1 = self.ref_before(word_no)
            word_no2 = self.ref_after(word_no)
            if word_no1 == -1 and word_no2 == -1:
                log.append (f,_('INFO')
                           ,_('No references have been found!')
                           )
                return word_no
            elif word_no1 >= 0 and word_no2 == -1:
                log.append (f,_('INFO')
                           ,_('No references to the right!')
                           )
                return word_no1
            elif word_no2 >= 0 and word_no1 == -1:
                log.append (f,_('INFO')
                           ,_('No references to the left!')
                           )
                return word_no2
            else:
                delta_before = word_no - word_no1
                delta_after  = word_no2 - word_no
                if min(delta_before,delta_after) == delta_before:
                    return word_no1
                else:
                    return word_no2
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
                
    def repeated(self,word_no):
        f = '[shared] shared.References.repeated'
        if self.Success:
            if word_no < len(self.words1.words):
                count = 0
                for i in range(word_no+1):
                    if self.words1.words[i]._n == self.words1.words[word_no]._n:
                        count += 1
                return count
            else:
                objs.mes (f,_('ERROR')
                         ,_('The condition "%s" is not observed!') \
                         % '%d < %d' % (word_no,len(self.words1.words))
                         )
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        
    def repeated2(self,word_n,count):
        f = '[shared] shared.References.repeated2'
        if self.Success:
            tmp = 0
            for i in range(len(self.words2.words)):
                if self.words2.words[i]._n == word_n:
                   tmp += 1
                   if tmp == count:
                       return i
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )



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
        f = '[shared] shared.Links.link'
        pos = self._pos + len(self._root)
        if pos >= len(self._text):
            log.append (f,_('WARNING')
                       ,_('Unexpected end of text!')
                       )
        else:
            text = self._text[pos:]
            try:
                pos = text.index('"')
                self._links.append(text[:pos])
            except ValueError:
                log.append (f,_('WARNING')
                           ,_('Wrong input data!')
                           )
                              
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
    ''' Filter base names (case-ignorant) of files and folders in a path
        Blacklist is a list of patterns, not obligatory full names
    '''

    def __init__(self,path,blacklist=[]):
        self._list   = []
        self._path   = path
        self._block  = blacklist
        self.Success = Directory(self._path).Success \
                       and isinstance(blacklist,list)
    
    def block(self):
        f = '[shared] shared.FilterList.block'
        if self.Success:
            # Actually, there is no reason to use 'strip' here
            self._block = [item.lower() for item in self._block if item]
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
    
    def list(self):
        f = '[shared] shared.FilterList.list'
        if self.Success:
            if not self._list:
                # Those are base names
                self._list = os.listdir(self._path)
            return self._list
        else:
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
    
    def filter(self):
        f = '[shared] shared.FilterList.filter'
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
            log.append (f,_('WARNING')
                       ,_('Operation has been canceled.')
                       )
        
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
            if oss.win():
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
            if oss.win():
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
    
    def rewrite(self,file,Rewrite=False):
        ''' - We do not put this into File class because we do not need
              to check existence.
            - We use 'Rewrite' just to shorten other procedures (to be
              able to use 'self.rewrite' silently in the code without
              ifs).
        '''
        f = '[shared] shared.Commands.rewrite'
        if not Rewrite and os.path.isfile(file):
            ''' We don't actually need to force rewriting or delete
                the file before rewriting.
            '''
            obj = objs.mes (f,_('QUESTION')
                            ,_('ATTENTION: Do yo really want to rewrite file "%s"?')\
                            % file
                            )
            # We do not have 'Yes' in a Silent mode
            if hasattr(obj,'Yes'):
                return obj.Yes
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
        f = 'Commands.human_time'
        if isinstance(delta,int) or isinstance(delta,float):
            hours   = delta // 3600
            minutes = (delta - hours * 3600) // 60
            seconds = delta - hours * 3600 - minutes * 60
            mes = []
            if hours:
                mes.append('%d %s' % (hours,_('hrs')))
            if minutes:
                mes.append('%d %s' % (minutes,_('min')))
            if seconds:
                mes.append('%d %s' % (seconds,_('sec')))
            if mes:
                return ' '.join(mes)
            else:
                return '%d %s' % (0,_('sec'))
        else:
            objs.mes (f,_('WARNING')
                     ,_('Wrong input data: "%s"!') % str(delta)
                     )
            return '%d %s' % (0,_('sec'))
    
    def cancel(self,func):
        log.append (func
                   ,_('WARNING')
                   ,_('Operation has been canceled.')
                   )
    
    def empty(self,func):
        log.append (func
                   ,_('WARNING')
                   ,_('Empty input is not allowed!')
                   )


''' If there are problems with import or tkinter's wait_variable, put
    this beneath 'if __name__'
'''
com  = Commands()
objs = Objects()


if __name__ == '__main__':
    ''' #note: Focusing on the widget is lost randomly (is assigned to
        root). This could be a Tkinter/DM bug.
    '''
    f = '[shared] shared.__main__'
    Silent = False
    if not Silent:
        import sharedGUI as sg
        sg.objs.start()
    objs = Objects()
    objs.mes (func    = f
             ,level   = _('INFO')
             ,message = _('Nothing to do!')
             ,Silent  = Silent
             )
    if not Silent:
        sg.objs.end()
