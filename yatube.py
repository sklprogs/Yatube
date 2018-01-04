#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import pafy      as pf
import shared    as sh
import sharedGUI as sg
import gui       as gi
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','./locale')


AllOS = False


class Links:
    
    def __init__(self,text):
        self._root  = '<a href="/watch?v='
        self._pos   = 0
        self._links = []
        self._text  = text
        
    def poses(self):
        text = self._text
        search = sh.Search (text   = self._text
                           ,search = self._root
                           )
        loop = search.next_loop()
        for self._pos in loop:
            self.link()
            
    def link(self):
        pos = self._pos + len(self._root)
        if pos >= len(self._text):
            sh.log.append ('Links.link'
                          ,_('WARNING')
                          ,_('Unexpected end of text!')
                          )
        else:
            text = self._text[pos:]
            try:
                pos = text.index('"')
                self._links.append(text[:pos])
            except ValueError:
                sh.log.append ('Links.link'
                              ,_('WARNING')
                              ,_('Wrong input data!')
                              )
                              
    def run(self):
        if self._text:
            self.poses()
        else:
            sh.log.append ('Links.run'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )



class Video:
    
    def __init__(self,url):
        self.values()
        self._url = url
        
    def values(self):
        self._video    = None
        self._no       = 0
        self._author   = ''
        self._title    = ''
        self._duration = ''
        
    def supported_names(self):
        # todo: Delete unsupported chars from other attributes
        self._author   = sh.Text(text=self._author).delete_unsupported()
        self._title    = sh.Text(text=self._title).delete_unsupported()
        self._duration = sh.Text(text=self._duration).delete_unsupported()
    
    def video(self):
        try:
            self._video = pf.new (url   = self._url
                                 ,basic = True
                                 ,gdata = False
                                 )
        except:
            sh.log.append ('Videos.video'
                          ,_('WARNING')
                          ,_('Error adding "%s"!') % self._url
                          )
            
    def debug(self):
        message = ''
        try:
            message += 'Author: %s\n' % self._video.author
            message += 'Title: %s\n' % self._video.title
            message += 'Date: %s\n' % self._video.published
            message += 'Duration: %s\n' % str(self._video.duration)
            message += 'Views: %s\n' % str(self._video.viewcount)
            message += 'Likes/dislikes: %s/%s\n' \
                       % (str(self._video.likes)
                         ,str(self._video.dislikes)
                         )
            message += 'Small video picture URL: %s\n' \
                       % self._video.thumb
            message += '\n'
        except:
            sh.log.append ('Video.debug'
                          ,_('WARNING')
                          ,_('Error getting info for video #%d!') \
                          % self._no
                          )
        return message
        
    def summary(self):
        try:
            self._author   = self._video.author
            self._title    = self._video.title
            self._duration = self._video.duration
        except:
            sh.log.append ('Video.summary'
                          ,_('WARNING')
                          ,_('Error getting info for video #%d!') \
                          % self._no
                          )



class Channel:
       
    def __init__(self,user,download_dir='./Youtube'):
        self.values()
        self._user = user
        self._dir  = download_dir
        self.check()
        
    def check(self):
        if self._user and isinstance(self._user,str) and \
           self._dir and isinstance(self._dir,str) and \
           sh.Directory(path=self._dir,Silent=True).Success:
               self.Success = True
        else:
            self.Success = False
            
    def values(self):
        self.Success     = True
        # todo: localize
        self._not_found  = 'Такой канал не существует.'
        self._link_start = 'https://www.youtube.com/user/'
        self._link_end   = '/videos'
        self._channel    = ''
        self._html       = ''
        self._escaped    = ''
        self._links      = []
            
    def channel(self):
        if self.Success:
            self._channel = self._link_start + self._user \
                                             + self._link_end
            self._escaped = sh.FixBaseName (basename = self._user
                                           ,AllOS    = AllOS
                                           ,max_len  = 100
                                           ).run()
            if self._escaped:
                self._dir = os.path.join(self._dir,self._escaped)
            else:
                self.Success = False
                sh.log.append ('Channel.channel'
                              ,_('WARNING')
                              ,_('Empty output is not allowed!')
                              )
        else:
            sh.log.append ('Channel.channel'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def create(self):
        if self.Success:
            self.Success = sh.Path(path=self._dir).create()
        else:
            sh.log.append ('Channel.create'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def page(self):
        if self.Success:
            response = sh.Get(url=self._channel).run()
            if not response:
                self.Success = False
                sh.log.append ('Channel.page'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
            elif self._not_found in response:
                self.Success = False
                sg.Message (func_title = 'Channel.page'
                           ,level      = _('WARNING')
                           ,message    = _('Channel "%s" does not exist!') \
                                         % self._channel
                           )
            else:
                self._html = response
        else:
            sh.log.append ('Channel.page'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def links(self):
        if self.Success:
            result = Links(self._html)
            result.run()
            self._links = result._links
            sh.log.append ('Channel.links'
                          ,_('INFO')
                          ,_('Fetched %d links for the user "%s"') \
                          % (len(self._links),self._user)
                          )
        else:
            sh.log.append ('Channel.links'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def download(self):
        if self.Success:
            sh.log.append ('Channel.download'
                          ,_('INFO')
                          ,_('User "%s": %d recent videos') % (self._user
                                                              ,len(self._links)
                                                              )
                          )
            for i in range(len(self._links)):
                # todo: implement
                print('#',i,':','Download ',self._links[i])
        else:
            sh.log.append ('Channel.download'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def run(self):
        self.channel()
        self.page()
        self.create()
        self.links()
        self.download()
            
        


if __name__ == '__main__':
    #user = 'AvtoKriminalist'
    #user = 'UCIpvyH9GKI54X1Ww2BDnEgg' # Not supported
    user = 'Centerstrain01'
    sg.objs.start()
    channel_gui = gi.Channel(name=user)
    sg.Geometry(parent_obj=channel_gui.obj).set('985x500')
    channel_gui.center(max_x=986,max_y=500)
    
    channel = Channel(user=user)
    channel.channel()
    channel.page()
    channel.links()
    
    for i in range(len(channel._links)):
        channel_gui.add(no=i)
        # Show default picture & video information
        sg.objs.root().widget.update_idletasks()
        video = Video(url=channel._links[i])
        video.video()
        video.summary()
        video.supported_names()
        video_gui = channel_gui._videos[i]
        video_gui.reset (no       = i + 1
                        ,author   = video._author
                        ,title    = video._title
                        ,duration = video._duration
                        # todo: implement (video.thumb)
                        ,picture  = None
                        )
        ''' This does not work in 'Channel.__init__' for some reason, 
        calling this externally
        ''' 
        channel_gui.update_scroll()
    # Move back to video #0
    channel_gui.canvas.widget.yview_moveto(0)
    channel_gui.show()
    sg.objs.end()
