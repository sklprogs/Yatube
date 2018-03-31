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

sh.objs.mes(Silent=True)


class Commands:
    
    def __init__(self):
        lg.objs.lists().reset()
        
    def update_channels(self):
        for i in range(len(lg.objs.lists()._subsc_auth)):
            self.update_channel (author = lg.objs._lists._subsc_auth[i]
                                ,url    = lg.objs._lists._subsc_urls[i]
                                )
                                
    def update_channel(self,author,url):
        self._channel = lg.Channel(url=url)
        self._channel.run()



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



class Objects:
    
    def __init__(self):
        pass


objs = Objects()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        Help().print()
    else:
        #todo: implement
        print('Parse arguments')
