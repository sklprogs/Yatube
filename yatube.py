#!/usr/bin/python3

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('yatube','./locale')

import os
import pafy      as pf
import shared    as sh
import sharedGUI as sg


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



class Videos:
    
    def __init__(self,urls):
        self._videos = []
        self._urls   = urls
        
    def videos(self):
        for url in self._urls:
            try:
                vid = pf.new (url   = url
                             ,basic = False
                             ,gdata = False
                             )
                self._videos.append(vid)
            except:
                url = 'https://www.youtube.com/watch?v=' + str(url)
                sh.log.append ('Videos.videos'
                              ,_('WARNING')
                              ,_('Error adding "%s"!') % url
                              )
            
    def summary(self):
        message = ''
        for i in range(len(self._videos)):
            try:
                message += 'Video #%d\n' % i
                message += 'Author: %s\n' % self._videos[i].author
                message += 'Title: %s\n' % self._videos[i].title
                message += 'Date: %s\n' % self._videos[i].published
                message += 'Duration: %s\n' % str(self._videos[i].duration)
                message += 'Views: %s\n' % str(self._videos[i].viewcount)
                message += 'Likes/dislikes: %s/%s\n' % (str(self._videos[i].likes)
                                                       ,str(self._videos[i].dislikes)
                                                       )
                message += 'Small video picture URL: %s\n' % self._videos[i].thumb
                message += '\n'
            except:
                sh.log.append ('Videos.summary'
                              ,_('WARNING')
                              ,_('Error getting info for video #%d!') % i
                              )
        return message



class Channel:
       
    def __init__(self,user,download_dir='./downloads'):
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
            self._channel = self._link_start + self._user + self._link_end
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
                          ,_('User "%s": %d recent videos') % self._user
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
    url = 'https://www.youtube.com/user/Centerstrain01/videos'
    
    Channel(user='Centerstrain01').run()


    '''
    videos = Videos(urls=links._links)
    videos.videos()
    print(videos.summary())
    '''
