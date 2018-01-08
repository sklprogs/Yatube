#!/usr/bin/python3

import sharedGUI as sg
import yatube    as ya
import gui       as gi
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


if __name__ == '__main__':
    sg.objs.start()
    Tests().video_summary()
    sg.objs.end()
