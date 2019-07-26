#!/usr/bin/python3

import re
import sre_constants
import shared as sh

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','../resources/locale')


class Record:
    ''' - This class is for both checking a regular expression and
          replacing matches through text (these actions require
          different arguments and are not necessarily interconnected).
        - Example:
          # Expressions must be raw strings, otherwise, there will be
            no match
          orig:       r'(\d+)[\s]{0,1}[–-][\s]{0,1}(\d+)'
          final:      r'\1-\2'
          what1:      'Figures 1 - 2 show that...'
          with1:      'Figures 1-2 show that...'
    '''
    def __init__(self,orig,final,what1=None
                ,with1=None,what2=None,with2=None
                ,what3=None,with3=None,what4=None
                ,with4=None,what5=None,with5=None
                ,_id='Unknown id'
                ):
        f = '[shared] regexp.Record.__init__'
        self.Success = True
        self._orig   = orig
        self._final  = final
        self._what1  = what1
        self._with1  = with1
        self._what2  = what2
        self._with2  = with2
        self._what3  = what3
        self._with3  = with3
        self._what4  = what4
        self._with4  = with4
        self._what5  = what5
        self._with5  = with5
        self._id     = _id
        self._what   = self._with = ''
        if not self._orig or not self._final:
            self.Success = False
            mes = _('Not enough input data!')
            sh.objs.mes(f,mes).warning()
    
    def apply(self,text):
        f = '[shared] regexp.Record.apply'
        if self.Success:
            try:
                result = re.sub(self._orig,self._final,text)
            except sre_constants.error:
                result = ''
                self.Success = False
                mes = _('A syntax error in the regular expression (id: {})!')
                mes = mes.format(self._id)
                sh.objs.mes(f,mes).warning()
            return result
        else:
            sh.com.cancel(f)
    
    def _check(self):
        f = '[shared] regexp.Record._check'
        if self.Success:
            result = self.apply(text=self._what)
            if self.Success and result != self._with:
                self.Success = False
                mes = _('Regular expression {} has failed: we were expecting\n"{}",\nbut received\n"{}".')
                mes = mes.format(self._id,self._with,result)
                sh.objs.mes(f,mes).warning()
        else:
            sh.com.cancel(f)
        return self.Success
    
    def check(self):
        f = '[shared] regexp.Record.check'
        if self.Success:
            cond1 = self._what1 and self._with1
            cond2 = self._what2 and self._with2
            cond3 = self._what3 and self._with3
            cond4 = self._what4 and self._with4
            cond5 = self._what5 and self._with5
            if cond1 or cond2 or cond3 or cond4 or cond5:
                if cond1:
                    self._what = self._what1
                    self._with = self._with1
                    self._check()
                if self.Success and cond2:
                    self._what = self._what2
                    self._with = self._with2
                    self._check()
                if self.Success and cond3:
                    self._what = self._what3
                    self._with = self._with3
                    self._check()
                if self.Success and cond4:
                    self._what = self._what4
                    self._with = self._with4
                    self._check()
                if self.Success and cond5:
                    self._what = self._what5
                    self._with = self._with5
                    self._check()
            else:
                self.Success = False
                mes = _('Not enough input data!')
                sh.objs.mes(f,mes).warning()
        else:
            sh.com.cancel(f)
        return self.Success



if __name__ == '__main__':
    orig = r'([Cc]laim|[Cc]olumn|[Pp]age|[Ss]heet|[Pp]aragraph|[Ll]ine)[s]{0,1}[\s]{0,1}(\d+[,-][\s]{0,1}\d+)'
    final = r'\1s \2'
    #text = 'Records 200 - 300 have undergone a regular procedure...'
    what1 = 'pages 1-2'
    with1 = 'pages 1-2'
    rec = Record (orig  = orig
                 ,final = final
                 ,what1 = what1
                 ,with1 = with1
                 )
    print(rec.check())
    #print(rec.apply(text=what1))
