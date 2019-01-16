#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import json
from googleapiclient.discovery import build
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('yatube','../resources/locale')

API_KEY = 'AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo'
''' Default number of videos to be fetched: 5, max: 50.
    Default number of comments to be fetched: 20, max: 100.
'''
MAX_VIDEOS   = 50
MAX_COMMENTS = 100


class Trending:
    
    def __init__(self,country=''):
        self.values()
        if country:
            self.reset(country)
    
    def check(self):
        if self._country:
            return True
        else:
            self.Success = False
            sh.com.empty(f)
    
    def fetch(self,token=''):
        f = '[Yatube] meta.Trending.fetch'
        if self.Success:
            try:
                self._resp = com.service().videos().list (chart      = 'mostPopular'
                                                         ,regionCode = self._country
                                                         ,part       = 'id,snippet'
                                                         ,maxResults = MAX_VIDEOS
                                                         ,pageToken  = token
                                                         ).execute()
            except Exception as e:
                sh.objs.mes (f,_('WARNING')
                            ,_('Third-party module has failed!\n\nDetails: %s')\
                            % str(e)
                            )
            objs.stat().add_quota(3)
            if self._resp:
                try:
                    self._prev = self._resp['prevPageToken']
                except KeyError:
                    self._prev = ''
                try:
                    self._next = self._resp['nextPageToken']
                except KeyError:
                    sh.log.append (f,_('INFO')
                                  ,_('The end of the channel has been reached!')
                                  )
                    self._next = ''
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_next(self):
        f = '[Yatube] meta.Trending.fetch_next'
        if self.Success:
            if self._resp and self._next:
                self.fetch(token=self._next)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_prev(self):
        f = '[Yatube] meta.Trending.fetch_prev'
        if self.Success:
            if self._resp and self._prev:
                self.fetch(token=self._prev)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.fetch()
        self.videos()
    
    def videos(self):
        f = '[Yatube] meta.Trending.videos'
        if self.Success:
            for item in self._resp['items']:
                if item['kind'] == "youtube#video":
                    try:
                        video         = Video()
                        video._id     = item['id']
                        video._author = item['snippet']['channelTitle']
                        video._ptime  = sh.com.yt_date(item['snippet']['publishedAt'])
                        video._title  = item['snippet']['title']
                        video._desc   = item['snippet']['description']
                        video._thumb  = item['snippet']['thumbnails']['default']['url']
                        objs.videos().add(video)
                    except KeyError as e:
                        sh.objs.mes (f,_('WARNING')
                                    ,_('Missing key: "%s"!') % str(e)
                                    )
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success  = True
        self._resp    = {}
        self._country = ''
        self._next    = ''
        self._prev    = ''
    
    def reset(self,country):
        f = '[Yatube] meta.Trending.reset'
        self.values()
        self._country = country
        self.check()



class PlayId:
    
    def __init__(self,myid=''):
        self.values()
        if myid:
            self.reset(myid)
    
    def by_user(self):
        f = '[Yatube] meta.PlayId.by_user'
        if self.Success:
            try:
                resp = com.service().channels().list (forUsername = self._id
                                                     ,part        = 'contentDetails'
                                                     ,maxResults  = 1
                                                     ).execute()
            except Exception as e:
                sh.objs.mes (f,_('WARNING')
                            ,_('Third-party module has failed!\n\nDetails: %s')\
                            % str(e)
                            )
            objs.stat().add_quota(3)
            if resp:
                try:
                    return resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                except Exception:
                    ''' KeyError or IndexError can occur. The output can
                        be too ambiguous, so we just inform the user
                        about the wrong input (should be the real cause
                        of the error).
                    '''
                    sh.objs.mes (f,_('WARNING')
                                ,_('Wrong input data!')
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def by_channel_id(self):
        f = '[Yatube] meta.PlayId.by_channel_id'
        if self.Success:
            try:
                resp = com.service().channels().list (id         = self._id
                                                     ,part       = 'contentDetails'
                                                     ,maxResults = 1
                                                     ).execute()
            except Exception as e:
                sh.objs.mes (f,_('WARNING')
                            ,_('Third-party module has failed!\n\nDetails: %s')\
                            % str(e)
                            )
            objs.stat().add_quota(3)
            if resp:
                try:
                    return resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                except Exception:
                    ''' KeyError or IndexError can occur. The output can
                        be too ambiguous, so we just inform the user
                        about the wrong input (should be the real cause
                        of the error).
                    '''
                    sh.objs.mes (f,_('WARNING')
                                ,_('Wrong input data!')
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[Yatube] meta.PlayId.check'
        if self._id:
            return True
        else:
            self.Success = False
            sh.com.empty(f)
    
    def reset(self,myid):
        self.values()
        self._id = myid
        self.check()
    
    def values(self):
        self.Success = True
        self._id     = ''



# https://github.com/google/google-api-python-client/issues/325#issuecomment-274349841
class MemoryCache:
    _CACHE = {}
    
    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content



class Comments:
    
    def __init__(self):
        ''' From documentation: "Note that a commentThread resource does
            not necessarily contain all replies to a comment, and you
            need to use the comments.list method if you want to
            retrieve all replies for a particular comment".
            Thus, it seems there is no quota-efficient way to fetch all
            comments, so we should not rely on the number of comments
            returned by 'VideoInfo' and therefore we should not use
            number indicators in GUI.
        '''
        self.reset()
        
    def comments(self):
        f = '[Yatube] meta.Comments.comments'
        if self.Success:
            if self._resp:
                try:
                    message = ''
                    istr = io.StringIO()
                    for item in self._resp['items']:
                        istr.write(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                        istr.write(': ')
                        istr.write(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                        istr.write('\n')
                        try:
                            ''' For some reason, replies are fetched
                                backwards.
                            '''
                            subitems = list(item['replies']['comments'])
                            subitems = subitems[::-1]
                            for subitem in subitems:
                                istr.write('>>> ')
                                istr.write(subitem['snippet']['authorDisplayName'])
                                istr.write(': ')
                                istr.write(subitem['snippet']['textDisplay'])
                                istr.write('\n')
                            istr.write('\n')
                        except KeyError as e:
                            istr.write('\n')
                    message = istr.getvalue()
                    istr.close()
                    # This prevent from duplicating a page with no token
                    if message not in self._texts:
                        self._texts.append(message)
                        return message
                except KeyError as e:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Missing key: "%s"!') % str(e)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
        
    def values(self):
        self.Success = True
        self._resp   = {}
        self._texts  = []
        self._next   = ''
        self.i       = 0
        
    def reset(self):
        self.values()
        ''' We do not perform checks here since 'Videos.current'
            will create empty fields if they are missing.
        '''
    
    def fetch_next(self):
        f = '[Yatube] meta.Comments.fetch_next'
        if self.Success:
            if self._resp:
                self.i += 1
                if len(self._texts) > self.i:
                    result = self._texts[self.i]
                elif self._next:
                    result = self.fetch(token=self._next)
                else:
                    result = ''
                if self.i >= len(self._texts):
                    self.i = len(self._texts) - 1
                return result
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_prev(self):
        f = '[Yatube] meta.Comments.fetch_prev'
        if self.Success:
            ''' For some reason, there is no 'prevPageToken' in
                a comments output (even not documented), so we should
                allow an empty 'self._prev' to be able to navigate back
                to the first page.
            '''
            if self._resp:
                if self.i > 0:
                    self.i -= 1
                return self._texts[self.i]
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch(self,token=''):
        f = '[Yatube] meta.Comments.fetch'
        if self.Success:
            try:
                self._resp = com.service().commentThreads().list(
                                         part       = 'snippet,replies'
                                        ,maxResults = MAX_COMMENTS
                                        ,videoId    = objs.videos().current()._id
                                        ,textFormat = 'plainText'
                                        ,pageToken  = token
                                        ).execute()
            except Exception as e:
                e = str(e)
                self.Success = False
                if 'has disabled comments' in e:
                    sh.objs.mes (f,_('INFO')
                                ,_('Comments are disabled for this video.')
                                )
                else:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Third-party module has failed!\n\nDetails: %s')\
                                % str(e)
                                )
            ''' The comments quota is not set in the quota calculator.
                According to documentation:
                https://developers.google.com/youtube/v3/docs/commentThreads/list#properties%23properties
                Quota: method: 1; replies: 2; snippet: 2
            '''
            objs.stat().add_quota(5)
            if self._resp:
                try:
                    self._next = self._resp['nextPageToken']
                except KeyError:
                    sh.log.append (f,_('INFO')
                                  ,_('The end of the channel has been reached!')
                                  )
                    self._next = ''
            return self.comments()
        else:
            sh.com.cancel(f)



class VideoInfo:
    
    def __init__(self):
        ''' We do not perform checks here since 'Videos.current'
            will create empty fields if they are missing.
            #NOTE: suggestions, fileDetails and processingDetails parts
            are only available to the video's owner.
        '''
        pass
    
    def channel_id(self):
        f = '[Yatube] meta.VideoInfo.channel_id'
        video = objs._videos.current()
        if video._id:
            resp = None
            try:
                resp = com.service().videos().list (id   = video._id
                                                   ,part = 'id,snippet'
                                                   ).execute()
            except Exception as e:
                sh.objs.mes (f,_('WARNING')
                            ,_('Third-party module has failed!\n\nDetails: %s')\
                            % str(e)
                            )
            objs.stat().add_quota(3)
            if resp:
                try:
                    for item in resp['items']:
                        if item['kind'] == "youtube#video":
                            video._ch_id = item['snippet']['channelId']
                            # We need only 1 suitable section
                            return video._ch_id
                except KeyError as e:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Missing key: "%s"!') % str(e)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)
    
    def length(self):
        f = '[Yatube] meta.VideoInfo.length'
        video = objs._videos.current()
        if video._id:
            resp = None
            try:
                resp = com.service().videos().list (id   = video._id
                                                   ,part = 'id,contentDetails'
                                                   ).execute()
            except Exception as e:
                sh.objs.mes (f,_('WARNING')
                            ,_('Third-party module has failed!\n\nDetails: %s')\
                            % str(e)
                            )
            objs.stat().add_quota(3)
            if resp:
                try:
                    for item in resp['items']:
                        if item['kind'] == "youtube#video":
                            length = item['contentDetails']['duration']
                            length = sh.com.yt_length(length)
                            if length:
                                if isinstance(length,(float,int)):
                                    video._len = length
                                    return video._len
                                else:
                                    sh.objs.mes (f,_('ERROR')
                                                ,_('Wrong input data: "%s"!')\
                                                % str(length)
                                                )
                            else:
                                sh.com.empty(f)
                except KeyError as e:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Missing key: "%s"!') % str(e)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)
    
    def statistics(self):
        f = '[Yatube] meta.VideoInfo.statistics'
        video = objs._videos.current()
        if video._id:
            resp = None
            try:
                resp = com.service().videos().list (id   = video._id
                                                   ,part = 'id,statistics'
                                                   ).execute()
            except Exception as e:
                sh.objs.mes (f,_('WARNING')
                            ,_('Third-party module has failed!\n\nDetails: %s')\
                            % str(e)
                            )
            objs.stat().add_quota(3)
            if resp:
                try:
                    for item in resp['items']:
                        if item['kind'] == "youtube#video":
                            video._views = sh.Input (title = f
                                                    ,value = item['statistics']['viewCount']
                                                    ).integer()
                            video._likes = sh.Input (title = f
                                                    ,value = item['statistics']['likeCount']
                                                    ).integer()
                            video._dislikes = sh.Input (title = f
                                                       ,value = item['statistics']['dislikeCount']
                                                       ).integer()
                            video._com_num = sh.Input (title = f
                                                      ,value = item['statistics']['commentCount']
                                                      ).integer()
                            # We need only 1 suitable section
                            return True
                except KeyError as e:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Missing key: "%s"!') % str(e)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)



class Stat:
    
    def __init__(self):
        self._quota = 0
        ''' Timestamp when the program was started. This can be used
            to get a daily quota cost.
        '''
        self._started = sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp()
    
    def uptime(self):
        return sh.Time(pattern='%Y-%m-%d %H:%M:%S').timestamp() - self._started
    
    # Quota should be added even in case of invalid requests
    def add_quota(self,number):
        self._quota += number
    
    def report(self,Silent=False):
        f = '[Yatube] meta.Stat.report'
        message = _('Uptime:') + ' ' + sh.com.human_time(self.uptime())\
                               + '\n'
        message += _('Used quota:') + ' %d' % self._quota
        if Silent:
            sh.log.append (f,_('INFO')
                          ,message
                          )
        else:
            sh.objs.mes (f,_('INFO')
                        ,message
                        )



class Playlist:
    
    def __init__(self,play_id=None):
        self.values()
        if play_id:
            self.reset(play_id)
    
    def run(self):
        self.fetch()
        self.videos()
    
    def videos(self):
        f = '[Yatube] meta.Playlist.videos'
        if self.Success:
            if self._resp:
                try:
                    for item in self._resp['items']:
                        if item['snippet']['resourceId']['kind'] == "youtube#video":
                            video         = Video()
                            video._id     = item['snippet']['resourceId']['videoId']
                            video._author = item['snippet']['channelTitle']
                            video._ptime  = sh.com.yt_date(item['snippet']['publishedAt'])
                            video._title  = item['snippet']['title']
                            video._desc   = item['snippet']['description']
                            video._thumb  = item['snippet']['thumbnails']['default']['url']
                            objs.videos().add(video)
                except KeyError as e:
                    sh.objs.mes (f,_('WARNING')
                                ,_('Missing key: "%s"!') % str(e)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[Yatube] meta.Playlist.check'
        if self._play_id:
            if self._play_id.startswith('UU') \
            and len(self._play_id) == 24:
                return True
            else:
                self.Success = False
                sh.objs.mes (f,_('WARNING')
                            ,_('Wrong input data: "%s"!') \
                            % self._play_id
                            )
        else:
            self.Success = False
            sh.com.empty(f)
    
    def reset(self,play_id):
        f = '[Yatube] meta.Playlist.reset'
        self.values()
        self._play_id = play_id
        self.check()
        
    def values(self):
        self.Success  = True
        self._resp    = {}
        self._next    = ''
        self._prev    = ''
        self._play_id = ''
    
    def fetch(self,token=''):
        f = '[Yatube] meta.Playlist.fetch'
        if self.Success:
            try:
                self._resp = com.service().playlistItems().list (playlistId = self._play_id
                                                                ,part       = 'id,snippet'
                                                                ,maxResults = MAX_VIDEOS
                                                                ,pageToken  = token
                                                                ).execute()
            except Exception as e:
                sh.objs.mes (f,_('WARNING')
                            ,_('Third-party module has failed!\n\nDetails: %s')\
                            % str(e)
                            )
            objs.stat().add_quota(3)
            if self._resp:
                try:
                    self._prev = self._resp['prevPageToken']
                except KeyError:
                    self._prev = ''
                try:
                    self._next = self._resp['nextPageToken']
                except KeyError:
                    sh.log.append (f,_('INFO')
                                  ,_('The end of the channel has been reached!')
                                  )
                    self._next = ''
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_next(self):
        f = '[Yatube] meta.Playlist.fetch_next'
        if self.Success:
            if self._resp and self._next:
                self.fetch(token=self._next)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_prev(self):
        f = '[Yatube] meta.Playlist.fetch_prev'
        if self.Success:
            if self._resp and self._prev:
                self.fetch(token=self._prev)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class Search:
    
    def __init__(self,query=''):
        self.values()
        if query:
            self.reset(query)
    
    def check(self):
        if self._query:
            return True
        else:
            self.Success = False
            sh.com.empty(f)
    
    def fetch(self,token=''):
        f = '[Yatube] meta.Search.fetch'
        if self.Success:
            try:
                self._resp = com.service().search().list (q          = self._query
                                                         ,part       = 'id,snippet'
                                                         ,maxResults = MAX_VIDEOS
                                                         ,safeSearch = 'none'
                                                         ,pageToken  = token
                                                         ).execute()
            except Exception as e:
                sh.objs.mes (f,_('WARNING')
                            ,_('Third-party module has failed!\n\nDetails: %s')\
                            % str(e)
                            )
            objs.stat().add_quota(100)
            if self._resp:
                try:
                    self._prev = self._resp['prevPageToken']
                except KeyError:
                    self._prev = ''
                try:
                    self._next = self._resp['nextPageToken']
                except KeyError:
                    sh.log.append (f,_('INFO')
                                  ,_('The end of the channel has been reached!')
                                  )
                    self._next = ''
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_next(self):
        f = '[Yatube] meta.Search.fetch_next'
        if self.Success:
            if self._resp and self._next:
                self.fetch(token=self._next)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_prev(self):
        f = '[Yatube] meta.Search.fetch_prev'
        if self.Success:
            if self._resp and self._prev:
                self.fetch(token=self._prev)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.fetch()
        self.videos()
    
    def videos(self):
        f = '[Yatube] meta.Search.videos'
        if self.Success:
            for item in self._resp['items']:
                if item['id']['kind'] == "youtube#video":
                    try:
                        video         = Video()
                        video._id     = item['id']['videoId']
                        video._author = item['snippet']['channelTitle']
                        video._ptime  = sh.com.yt_date(item['snippet']['publishedAt'])
                        video._title  = item['snippet']['title']
                        video._desc   = item['snippet']['description']
                        video._thumb  = item['snippet']['thumbnails']['default']['url']
                        objs.videos().add(video)
                    except KeyError as e:
                        sh.objs.mes (f,_('WARNING')
                                    ,_('Missing key: "%s"!') % str(e)
                                    )
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success = True
        self._resp   = {}
        self._next   = ''
        self._prev   = ''
        self._query  = ''
    
    def reset(self,query):
        f = '[Yatube] meta.Search.reset'
        self.values()
        self._query = query
        self.check()



class Video:
    
    def __init__(self):
        self.Block     = False
        self.Saved     = None
        self._bytes    = None
        self._gui      = None
        self._image    = None
        self._com_num  = 0
        self._dtime    = 0
        self._ftime    = 0
        self._ltime    = 0
        self._ptime    = 0
        self._len      = 0
        self._views    = 0
        self._likes    = 0
        self._dislikes = 0
        self._com_num  = 0
        self._id       = ''
        self._play_id  = ''
        self._author   = ''
        self._title    = ''
        self._desc     = ''
        self._thumb    = ''
        self._search   = ''
        self._ch_id    = ''
        self._dir      = ''
        self._url      = ''
        self._path     = ''
        self._pathsh   = ''
        self._page     = ''



class Videos:
    
    def __init__(self):
        self.reset()
    
    def set_gui(self,gui):
        f = '[Yatube] meta.Videos.set_gui'
        if gui:
            for self.i in range(len(self._videos)):
                if self._videos[self.i]._gui == gui:
                    return True
        else:
            sh.com.empty(f)
    
    def current(self):
        f = '[Yatube] meta.Videos.current'
        if not self._videos:
            sh.com.empty(f)
            self.add(Video)
        if self.i < len(self._videos):
            return self._videos[self.i]
        else:
            sh.objs.mes (f,_('ERROR')
                        ,_('The condition "%s" is not observed!') \
                        % '%s < %d' % (str(self.i),len(self._videos))
                        )
            return Video()
    
    def add(self,video):
        f = '[Yatube] meta.Videos.video'
        if video:
            self._videos.append(video)
        else:
            sh.com.empty(f)
    
    def reset(self):
        self.values()
    
    def values(self):
        self._videos = []
        self.i = 0
    
    # Orphan, debug
    def summary(self):
        f = '[Yatube] meta.Videos.summary'
        if self._videos:
            istr = io.StringIO()
            for i in range(len(self._videos)):
                istr.write('#%d:' % (i+1))
                istr.write('\n')
                istr.write(_('ID:'))
                istr.write(' ')
                istr.write(self._videos[i]._id)
                istr.write('\n')
                istr.write(_('Author:'))
                istr.write(' ')
                istr.write(self._videos[i]._author)
                istr.write('\n')
                istr.write(_('Title:'))
                istr.write(' ')
                istr.write(self._videos[i]._title)
                istr.write('\n')
                istr.write(_('Date:'))
                istr.write(' ')
                itime = sh.Time (_timestamp = self._videos[i]._ptime
                                ,pattern    = '%Y-%m-%d %H:%M'
                                )
                istr.write(str(itime.date()))
                istr.write('\n')
                istr.write(_('Image:'))
                istr.write(' ')
                istr.write(self._videos[i]._thumb)
                istr.write('\n\n')
            message = istr.getvalue()
            istr.close()
            sh.objs.mes (f,_('INFO')
                        ,message
                        )
        else:
            sh.com.empty(f)



class Objects:
    
    def __init__(self):
        self._playlist = self._videos = self._search = self._stat \
                       = self._comments = self._playid = self._trending\
                       = None
    
    def trending(self):
        if self._trending is None:
            self._trending = Trending()
        return self._trending
    
    def playid(self):
        if self._playid is None:
            self._playid = PlayId()
        return self._playid
    
    def comments(self):
        if self._comments is None:
            self._comments = Comments()
        return self._comments
    
    def playlist(self):
        if self._playlist is None:
            self._playlist = Playlist()
        return self._playlist
    
    def stat(self):
        if self._stat is None:
            self._stat = Stat()
        return self._stat
    
    def search(self):
        if self._search is None:
            self._search = Search()
        return self._search
    
    def videos(self):
        if self._videos is None:
            self._videos = Videos()
        return self._videos



class Commands:
    
    def service(self):
        f = '[Yatube] meta.Commands.service'
        ''' Since this call quickly expires, we should rerun each time
            we use it.
        '''
        try:
            return build ('youtube','v3'
                         ,developerKey = API_KEY
                         ,cache        = MemoryCache()
                         )
        except Exception as e:
            sh.objs.mes (f,_('WARNING')
                        ,_('Third-party module has failed!\n\nDetails: %s')\
                        % str(e)
                        )


objs = Objects()
com  = Commands()


if __name__ == '__main__':
    f = 'meta.__main__'
    sg.objs.start()
    #author = 'Новости СВЕРХДЕРЖАВЫ'
    #objs.playid().reset(author)
    #print(objs._playid.by_user())
    video = Video()
    video._id = 'vjSohj-Iclc'
    objs.videos().add(video)
    VideoInfo().statistics()
    print('Views:',video._views)
    print('Likes:',video._likes)
    print('Dislikes:',video._dislikes)
    print('Comments:',video._com_num)
    sg.objs.end()
