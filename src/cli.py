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
        self._video     = None
        self._channel   = None
        self._timestamp = None
        lg.objs.lists().reset()
        
    def update_channels(self):
        delta = 0
        for i in range(len(lg.objs.lists()._subsc_auth)):
            delta += self.update_channel (author = lg.objs._lists._subsc_auth[i]
                                         ,url    = lg.objs._lists._subsc_urls[i]
                                         )
        sh.log.append ('Commands.update_channels'
                      ,_('INFO')
                      ,_('There are %d new videos in total') % delta
                      )
                                
    def update_channel(self,author,url):
        author = str(author)
        sh.log.append ('Commands.update_channel'
                      ,_('INFO')
                      ,_('Update channel "%s"') % author
                      )
        old_urls = idb.channel_videos(author=author)
        self._channel = lg.Channel(url=url)
        self._channel.run()
        self.channel_cli()
        new_urls = idb.channel_videos(author=author)
        old_urls = sh.Input (func_title = 'Commands.update_channel'
                            ,val        = old_urls
                            ).list()
        new_urls = sh.Input (func_title = 'Commands.update_channel'
                            ,val        = new_urls
                            ).list()
        delta_urls = []
        for url in new_urls:
            if not url in old_urls:
                delta_urls.append(url)
        sh.log.append ('Commands.update_channel'
                      ,_('INFO')
                      ,_('There are %d new videos for channel "%s"') \
                      % (len(delta_urls),author)
                      )
        return len(delta_urls)
        
    def channel_cli(self):
        for i in range(len(self._channel._links)):
            video = lg.Video(url=self._channel._links[i])
            video.get()
            if video.Success:
                self._video = video
                author    = sh.Text(text=self._video._author).delete_unsupported()
                title     = sh.Text(text=self._video._title).delete_unsupported()
                duration  = sh.Text(text=self._video._dur).delete_unsupported()
                if author in lg.objs.lists()._block_auth \
                or self._video._author in lg.objs._lists._block_auth:
                    author = title = _('BLOCKED')
                    self._video.Block = True
        idb.save()



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
idb  = lg.idb


if __name__ == '__main__':
    if len(sys.argv) == 1:
        Help().print()
    else:
        #todo: implement
        print('Parse arguments')
        Commands().update_channels()
        '''
        Commands().update_channel (author = 'Анатолий Шарий'
                                  ,url    = 'https://www.youtube.com/user/SuperSharij/videos'
                                  )
        '''
        idb.save()
        idb.close()
