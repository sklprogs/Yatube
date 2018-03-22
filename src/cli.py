#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import io
import pafy   as pf
import shared as sh
import logic  as lg
import db

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')


class Objects:
    
    def __init__(self):
        pass


sh.objs.mes(Silent=True)
objs = Objects()


class Help:
    
    def __init__(self):
        self._summary = ''
        self.summary()
    
    def summary(self):
        tmp = io.StringIO()
        # -d
        tmp.write('-d')
        tmp.write('\t\t')
        tmp.write(_('Download updated subscriptions'))
        tmp.write('\n')
        # -n
        tmp.write('-n <integer>')
        tmp.write('\t')
        tmp.write(_('Filter by date. For example, "-n 3" means "select videos no older than 3 days"'))
        tmp.write('\n')
        # -u
        tmp.write('-u')
        tmp.write('\t\t')
        tmp.write(_('Update subscriptions in database'))
        tmp.write('\n')
        self._summary = tmp.getvalue()
        tmp.close()
        
    def print(self):
        print(self._summary)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        Help().print()
    else:
        #todo: implement
        print('Parse arguments')
