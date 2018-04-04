#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pafy   as pf
import shared as sh
import logic  as lg
import db

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')

sh.objs.mes(Silent=True)
idb = lg.idb


class Commands:
    
    def __init__(self):
        self._video     = None
        self._channel   = None
        self._timestamp = None
        lg.objs.lists().reset()
        
    def date_filter (self,days_delta=7
                    ,Newer=True,WithReady=False
                    ):
        itime = sh.Time()
        itime.add_days(days_delta=-days_delta)
        timestamp = itime.timestamp()
        return idb.date_filter (timestamp = timestamp
                               ,Newer     = Newer
                               ,WithReady = WithReady
                               )
        
    def report(self,data):
        if data:
            data = [(row[1],row[2],row[3]) for row in data]
            sh.Table (headers = ['AUTHOR','TITLE','DATE']
                     ,rows    = data
                     ,MaxRow  = 30
                     ,MaxRows = 50
                     ).print()
        else:
            sh.log.append ('Commands.report'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
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
        
    def download(self,data):
        if data:
            for row in data:
                video = lg.Video(url=row[0])
                video.video()
                video._author = row[1]
                video._title  = row[2]
                video.path()
                video.download()
                if video.Success:
                    idb.mark_downloaded(url=row[0])
        else:
            sh.log.append ('Commands.download'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )


if __name__ == '__main__':
    com = Commands()
    # Fetch metadata on new videos
    com.update_channels()
    ''' Select new videos
        'days_delta': 0 is today, 1 is tomorrow and today, 7 - for
        the entire week, etc. Beware: large subscribe lists will use
        a HUGE amount of traffic even when 'days_delta' is set to 0
        (today).
        'Newer': True  - select videos that are newer than 'days_delta'
                 False - select videos that are older than 'days_delta'
        'WithReady': True  - also process videos that were already
                             downloaded. May be useful if you lost your
                             video files or moved to another PC. Note
                             that video files that already exist will
                             be skipped.
                     False - do not process videos that were already
                             downloaded (default).
    '''
    data = com.date_filter (days_delta = 0
                           ,Newer      = True
                           ,WithReady  = False
                           )
    #com.download(data)
    com.report(data)
    idb.save()
    idb.close()
