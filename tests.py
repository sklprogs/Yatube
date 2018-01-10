#!/usr/bin/python3

import shared    as sh
import sharedGUI as sg
import gui       as gi
import yatube    as ya
import db


class Tests:
    
    def menu(self):
        menu = gi.Menu()
        menu.show()
        print(menu.choice)
        
    def video_summary(self):
        video = ya.Video(url='Gasrlh1MD74')
        video.video()
        summary = video.summary()
        if summary:
            sg.objs.txt().reset_data()
            sg.objs._txt.insert(text=summary)
            sg.Clipboard().copy(text=summary)
            sg.objs._txt.show()
            
    def add_video(self):
        dbi = db.DB()
        url         = '9r0Eeo5_L8k'
        author      = 'Максим Шелков'
        title       = 'АВТОХЛАМ от ОФИЦИАЛОВ - ВСЁ ПРОВЕРЕНО! Но это НЕ ТОЧНО'
        date        = '2017-12-24 16:01:31'
        category    = 'Autos & Vehicles'
        description = 'Официальный дилер продает только проверенные автомобили?! Смотрите, как бывает!'
        duration    = '00:13:43'
        length      = 823
        views       = 601388
        likes       = 34835
        dislikes    = 570
        rating      = 4.93560218811
        Block       = False
        Ignore      = False
        thumb       = 'http://i.ytimg.com/vi/9r0Eeo5_L8k/default.jpg'
        data = (url,author,title,date,category,description,duration
               ,length,views,likes,dislikes,rating,Block,Ignore
               )
        dbi.add_video(data)
        dbi.save()
        dbi.close()
        
    def get_video(self):
        dbi = db.DB()
        result = dbi.get_video('9r0Eeo5_L8k')
        dbi.close()
        return result
        
    def print(self):
        dbi = db.DB()
        dbi.dbc.execute ('select AUTHOR,TITLE,DATE,DURATION,LIKES \
                                ,DISLIKES from VIDEOS'
                        )
        dbi.print(Selected=1,Shorten=1)
        dbi.close()
        
    def search(self):
        dbi = db.DB()
        dbi.dbc.execute ('select TITLE from VIDEOS where AUTHOR = ? \
                          order by DATE desc',('Анатолий Шарий',))
        result = dbi.dbc.fetchall()
        result = [item[0] for item in result if item]
        result = '\n'.join(list(result))
        sg.objs.txt().reset_data()
        sg.objs._txt.insert(result)
        sg.objs._txt.show()
        dbi.close()
        
    def get_channels(self):
        dbi = db.DB()
        print(dbi.get_channels())
        dbi.close()
        
    def add_channels(self):
        dbi = db.DB()
        channels = dbi.get_channels()
        if not channels:
            channels = []
        print('Original list of channels:',dbi.get_channels())
        # Анатолий Шарий
        Shariy = ('SuperSharij',False,)
        # Максим Шелков
        Shelkov = ('AvtoKriminalist',False,)
        Centestrain01 = ('Centerstrain01',False,)
        Nemagia = ('NEMAGIA',False,)
        starred = [Shariy,Shelkov,Centestrain01,Nemagia]
        for channel in starred:
            if not channel[0] in channels:
                dbi.add_channel(data=channel)
        dbi.save()
        print('Final list of channels:',dbi.get_channels())
        dbi.close()
        
    def drop_channels(self):
        dbi = db.DB()
        dbi.dbc.execute('drop table CHANNELS')
        dbi.save()
        dbi.close()
        
    def fill_channel(self):
        channel = gi.Channel(name='Максим Шелков')
        sg.Geometry(parent_obj=channel.obj).set('985x500')
        channel.center(max_x=986,max_y=500)
        
        image = sh.Get (url      = 'http://i.ytimg.com/vi/9r0Eeo5_L8k/default.jpg'
                       ,encoding = None
                       ).run()
        img = sg.Image()
        img._bytes = image
        img.loader()
        image = img.image()
        
        for i in range(10):
            channel.add(no=i)
            # Show default picture & video information
            sg.objs.root().widget.update_idletasks()

            # Simulate long loading
            count = 0
            for k in range(500000):
                count += k
            
            video = channel._videos[i]
            video.reset (no       = i + 1
                        ,author   = 'Максим Шелков'
                        ,title    = 'НАГЛЫЙ ОБМАН от ПЕРЕКУПА! Автомобиль - Ford АВТОХЛАМ!'
                        ,duration = '14:16'
                        ,image    = image
                        )
            ''' This does not work in 'Channel.__init__' for some reason, 
            calling this externally
            ''' 
            channel.update_scroll()
        # Move back to video #0
        channel.canvas.widget.yview_moveto(0)
        channel.show()
        
    def update_channel(self,user):
        ''' 'AvtoKriminalist'
            'UCIpvyH9GKI54X1Ww2BDnEgg' # Not supported
            'SuperSharij'
            'Centerstrain01'
            'NEMAGIA'
            'https://www.youtube.com/channel/UCIpvyH9GKI54X1Ww2BDnEgg/videos'
        '''
        channel = ya.Channel(user=user)
        channel.channel()
        channel.page()
        channel.links()
        
        for i in range(len(channel._links)):
            gi.objs.channel_gui().add(no=i)
            # Show default picture & video information
            sg.objs.root().widget.update_idletasks()
            video = ya.Video(url=channel._links[i])
            video.get()
            if video.Success:
                author    = sh.Text(text=video._author).delete_unsupported()
                title     = sh.Text(text=video._title).delete_unsupported()
                duration  = sh.Text(text=video._dur).delete_unsupported()
                video_gui = gi.objs._channel_gui._videos[i]
                video_gui.reset (no       = i + 1
                                ,author   = author
                                ,title    = title
                                ,duration = duration
                                ,image    = video._image
                                )
                ''' This does not work in 'Channel.__init__' for some reason, 
                calling this externally
                ''' 
                gi.objs._channel_gui.update_scroll()
        
        ya.objs.db().save()
        
        # Move back to video #0
        gi.objs._channel_gui.canvas.widget.yview_moveto(0)
        gi.objs._channel_gui.show()
        
        ya.objs._db.close()


if __name__ == '__main__':
    sg.objs.start()
    Tests().print()
    sg.objs.end()
