#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import io
import pafy      as pf
import shared    as sh
import sharedGUI as sg
import gui       as gi
import db
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('yatube','./locale')


product = 'Yatube'
version = '(alpha)'
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
        self.Success = True
        self._video  = self._image = self._bytes = None
        self._author = self._title = self._date = self._cat \
                     = self._desc = self._dur = ''
        self._len    = self._views = self._likes = self._dislikes = 0
        self._rating = 0.0
        
    def assign_online(self):
        if self._video:
            self._author   = self._video.author
            self._title    = self._video.title
            self._date     = self._video.published
            self._cat      = self._video.category
            self._desc     = self._video.description
            self._dur      = self._video.duration
            self._len      = self._video.length
            self._views    = self._video.viewcount
            self._likes    = self._video.likes
            self._dislikes = self._video.dislikes
            self._rating   = self._video.rating
        else:
            sh.log.append ('Video.assign_online'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def dump(self):
        if self.Success:
            ''' Do no write default data.
                Do not forget to commit where necessary.
            '''
            if self._video:
                data = (self._url,self._author,self._title,self._date
                       ,self._cat,self._desc,self._dur,self._len
                       ,self._views,self._likes,self._dislikes
                       ,self._rating,self._bytes,False,False
                       )
                objs.db().add_video(data)
            else:
                sh.log.append ('Video.dump'
                              ,_('INFO')
                              ,_('Nothing to do.')
                              )
        else:
            sh.log.append ('Video.dump'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        
    def assign_offline(self,data):
        if data:
            data_len = 12
            if len(data) >= data_len:
                self._author   = data[0]
                self._title    = data[1]
                self._date     = data[2]
                self._cat      = data[3]
                self._desc     = data[4]
                self._dur      = data[5]
                self._len      = data[6]
                self._views    = data[7]
                self._likes    = data[8]
                self._dislikes = data[9]
                self._rating   = data[10]
                self._bytes    = data[11]
                img = sg.Image()
                img._bytes = self._bytes
                img.loader()
                self._image = img.image()
            else:
                sg.Message ('Video.assign_offline'
                           ,_('ERROR')
                           ,_('The condition "%s" is not observed!') \
                            % '%d >= %d' % (len(data),data_len)
                           )
        else:
            sh.log.append ('Video.assign_offline'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        
    def video(self):
        if self.Success:
            if not self._video:
                try:
                    self._video = pf.new (url   = self._url
                                         ,basic = True
                                         ,gdata = False
                                         )
                except:
                    self.Success = False
                    sh.log.append ('Videos.video'
                                  ,_('WARNING')
                                  ,_('Error adding "%s"!') % self._url
                                  )
        else:
            sh.log.append ('Video.video'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def image(self):
        if self.Success:
            if self._video:
                image = sh.Get (url      = self._video.thumb
                               ,encoding = None
                               ).run()
                if image:
                    img = sg.Image()
                    self._bytes = img._bytes = image
                    img.loader()
                    self._image = img.image()
                else:
                    sh.log.append ('Video.image'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
            else:
                sh.log.append ('Video.image'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Video.image'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def get(self):
        if self.Success:
            result = objs.db().get_video(url=self._url)
            if result:
                self.assign_offline(result)
            else:
                self.video()
                self.assign_online()
                self.image()
                self.dump()
        else:
            sh.log.append ('Video.get'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def summary(self):
        if self.Success:
            tmp = io.StringIO()
            tmp.write(_('Author'))
            tmp.write(': ')
            tmp.write(self._author)
            tmp.write('\n')
            tmp.write(_('Title'))
            tmp.write(': ')
            tmp.write(self._title)
            tmp.write('\n')
            tmp.write(_('Date'))
            tmp.write(': ')
            tmp.write(self._date)
            tmp.write('\n')
            tmp.write(_('Category'))
            tmp.write(': ')
            tmp.write(self._cat)
            tmp.write('\n')
            tmp.write(_('Description'))
            tmp.write(': ')
            tmp.write(self._desc)
            tmp.write('\n')
            tmp.write(_('Duration'))
            tmp.write(': ')
            tmp.write(self._dur)
            tmp.write('\n')
            tmp.write(_('Length'))
            tmp.write(': ')
            tmp.write(str(self._len))
            tmp.write('\n')
            tmp.write(_('Views'))
            tmp.write(': ')
            tmp.write(str(self._views))
            tmp.write('\n')
            tmp.write(_('Likes'))
            tmp.write(': ')
            tmp.write(str(self._likes))
            tmp.write('\n')
            tmp.write(_('Dislikes'))
            tmp.write(': ')
            tmp.write(str(self._dislikes))
            tmp.write('\n')
            tmp.write(_('Rating'))
            tmp.write(': ')
            tmp.write(str(self._rating))
            tmp.write('\n')
            # todo: elaborate
            if self._video:
                tmp.write(_('Small video picture URL'))
                tmp.write(': ')
                tmp.write(str(self._video.thumb))
                tmp.write('\n')
            result = tmp.getvalue()
            result = sh.Text(text=result).delete_unsupported()
            tmp.close()
            return result
        else:
            sh.log.append ('Video.summary'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
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
                          ,_('User "%s": %d recent videos') \
                          % (self._user,len(self._links))
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



class Menu:
    
    def __init__(self):
        self.parent_obj = sg.objs.root()
        self.gui()
        
    def title(self,text=None):
        if text:
            self.parent_obj.title(text)
        else:
            text = sh.List(lst1=[product,version]).space_items()
            self.obj.title(text)
    
    def show(self,*args):
        self.obj.show()
    
    def close(self,*args):
        self.obj.close()
    
    def buttons(self):
        #todo: [cbox] Ignore videos older than ...
        ''' For some reason, separating the button text to a variable
            does not work correctly (the last action defined in such a
            way is selected).
        '''
        button = sg.Button (parent_obj = self.obj
                           ,text       = _('Update subscriptions')
                           ,action     = update_channels
                           ,side       = 'top'
                           )
        button.focus()
        sg.Button (parent_obj = self.obj
                  ,text       = _('Update trending')
                  ,action     = update_trending
                  ,side       = 'top'
                  )
        sg.Button (parent_obj = self.obj
                  ,text       = _('Manage subscriptions')
                  ,action     = manage_sub
                  ,side       = 'top'
                  )
        sg.Button (parent_obj = self.obj
                  ,text       = _('Manage blocklist')
                  ,action     = manage_block
                  ,side       = 'top'
                  )
        sg.Button (parent_obj = self.obj
                  ,text       = _('Quit')
                  ,action     = self.close
                  ,side       = 'top'
                  )
    
    def bindings(self):
        sg.bind (obj      = self.obj
                ,bindings = ['<Control-q>','<Control-w>','<Escape>']
                ,action   = self.close
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Down>'
                ,action   = self.focus_next
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Up>'
                ,action   = self.focus_prev
                )
        # Trying to pass lambda will result in an error
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
        
    def focus_next(self,event,*args):
        event.widget.tk_focusNext().focus()
        return 'break'
        
    def focus_prev(self,event,*args):
        event.widget.tk_focusPrev().focus()
        return 'break'
    
    def gui(self):
        self.obj = sg.objs.new_top(Maximize=False)
        self.widget = self.obj.widget
        self.buttons()
        self.title()
        self.bindings()



class Objects:
    
    def __init__(self):
        self._db = None
        
    def db(self):
        if not self._db:
            self._db = db.DB()
        return self._db


def update_channel(user='Centerstrain01'):
    channel = Channel(user=user)
    channel.channel()
    channel.page()
    channel.links()
    
    channel_gui = gi.Channel(name=user)
    sg.Geometry(parent_obj=channel_gui).set('985x500')
    channel_gui.center(max_x=986,max_y=500)
    
    for i in range(len(channel._links)):
        channel_gui.add(no=i)
        # Show default picture & video information
        sg.objs.root().widget.update_idletasks()
        video = Video(url=channel._links[i])
        video.get()
        if video.Success:
            author    = sh.Text(text=video._author).delete_unsupported()
            title     = sh.Text(text=video._title).delete_unsupported()
            duration  = sh.Text(text=video._dur).delete_unsupported()
            video_gui = channel_gui._videos[i]
            video_gui.reset (no       = i + 1
                            ,author   = author
                            ,title    = title
                            ,duration = duration
                            ,image    = video._image
                            )
            ''' This does not work in 'Channel.__init__' for some reason, 
            calling this externally
            ''' 
            channel_gui.update_scroll()
    objs.db().save()
    # Move back to video #0
    channel_gui.canvas.widget.yview_moveto(0)
    channel_gui.show()

def update_channels(*args):
    channels = objs.db().get_channels()
    for channel in channels:
        update_channel(user=channel)

def update_trending(*args):
    sg.Message ('update_trending'
               ,_('INFO')
               ,_('Not implemented yet!')
               )

def manage_sub(*args):
    old_channels = objs.db().get_channels()
    gi.objs.sub().fill(lst=old_channels)
    gi.objs._sub.show()
    channels = gi.objs._sub.get()
    if not channels:
        channels = []
    for channel in channels:
        if not channel in old_channels:
            objs._db.add_channel(data=(channel,False,))
    objs._db.save()
               
def manage_block(*args):
    channels = objs.db().get_channels(block=1)
    gi.objs.block().fill(lst=channels)
    gi.objs._block.show()
    channels = gi.objs._block.get()
    objs._db.block_channels(channels,block=0)
    objs._db.block_channels(channels)
    objs._db.save()


objs = Objects()



if __name__ == '__main__':
    sg.objs.start()
    menu = Menu()
    menu.show()
    sg.objs.end()
