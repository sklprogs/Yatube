#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import json
from googleapiclient.discovery import build
import skl_shared.shared as sh
from skl_shared.localize import _

API_KEY = ''
''' Default number of videos to be fetched: 5, max: 50.
    Default number of comments to be fetched: 20, max: 100.
'''
MAX_VIDEOS = 50
MAX_COMMENTS = 100


class Trending:
    
    def __init__(self,country=''):
        self.set_values()
        if country:
            self.reset(country)
    
    def check(self):
        if self.country:
            return True
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def fetch(self,token=''):
        f = '[Yatube] meta.Trending.fetch'
        if self.Success:
            try:
                self.resp = com.get_service().videos().list (chart = 'mostPopular'
                                                            ,regionCode = self.country
                                                            ,part = 'id,snippet'
                                                            ,maxResults = MAX_VIDEOS
                                                            ,pageToken = token
                                                            ).execute()
            except Exception as e:
                com.show_error(f,e)
            objs.get_stat().add_quota(3)
            if self.resp:
                try:
                    self.prev = self.resp['prevPageToken']
                except KeyError:
                    self.prev = ''
                try:
                    self.next = self.resp['nextPageToken']
                except KeyError:
                    mes = _('The end of the channel has been reached!')
                    sh.objs.get_mes(f,mes,True).show_info()
                    self.next = ''
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_next(self):
        f = '[Yatube] meta.Trending.fetch_next'
        if self.Success:
            if self.resp and self.next:
                self.fetch(token=self.next)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_prev(self):
        f = '[Yatube] meta.Trending.fetch_prev'
        if self.Success:
            if self.resp and self.prev:
                self.fetch(token=self.prev)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.fetch()
        self.set_videos()
    
    def set_videos(self):
        f = '[Yatube] meta.Trending.set_videos'
        if self.Success:
            for item in self.resp['items']:
                if item['kind'] == "youtube#video":
                    try:
                        video = Video()
                        video.id_ = item['id']
                        video.author = item['snippet']['channelTitle']
                        video.chid = item['snippet']['channelId']
                        video.ptime = sh.com.get_yt_date(item['snippet']['publishedAt'])
                        video.title = item['snippet']['title']
                        video.desc = item['snippet']['description']
                        video.thumb = item['snippet']['thumbnails']['default']['url']
                        objs.get_videos().add(video)
                    except KeyError as e:
                        mes = _('Missing key: "{}"!').format(e)
                        sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True
        self.resp = {}
        self.country = ''
        self.next = ''
        self.prev = ''
    
    def reset(self,country):
        f = '[Yatube] meta.Trending.reset'
        self.set_values()
        self.country = country
        self.check()



class PlayId:
    
    def __init__(self,myid=''):
        self.set_values()
        if myid:
            self.reset(myid)
    
    def get_by_user(self):
        f = '[Yatube] meta.PlayId.by_user'
        if self.Success:
            try:
                resp = com.get_service().channels().list (forUsername = self.id_
                                                         ,part = 'contentDetails'
                                                         ,maxResults = 1
                                                         ).execute()
            except Exception as e:
                com.show_error(f,e)
            objs.get_stat().add_quota(3)
            if resp:
                try:
                    return resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                except Exception:
                    ''' KeyError or IndexError can occur. The output can
                        be too ambiguous, so we just inform the user
                        about the wrong input (should be the real cause
                        of the error).
                    '''
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_by_channel_id(self):
        f = '[Yatube] meta.PlayId.get_by_channel_id'
        if self.Success:
            try:
                resp = com.get_service().channels().list (id = self.id_
                                                         ,part = 'contentDetails'
                                                         ,maxResults = 1
                                                         ).execute()
            except Exception as e:
                com.show_error(f,e)
            objs.get_stat().add_quota(3)
            if resp:
                try:
                    return resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                except Exception:
                    ''' KeyError or IndexError can occur. The output can
                        be too ambiguous, so we just inform the user
                        about the wrong input (should be the real cause
                        of the error).
                    '''
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[Yatube] meta.PlayId.check'
        if self.id_:
            return True
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def reset(self,myid):
        self.set_values()
        self.id_ = myid
        self.check()
    
    def set_values(self):
        self.Success = True
        self.id_ = ''



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
        
    def get_comments(self):
        f = '[Yatube] meta.Comments.get_comments'
        if self.Success:
            if self.resp:
                try:
                    message = ''
                    istr = io.StringIO()
                    for item in self.resp['items']:
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
                    if message not in self.texts:
                        self.texts.append(message)
                        return message
                except KeyError as e:
                    mes = _('Missing key: "{}"!').format(e)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        
    def set_values(self):
        self.Success = True
        self.resp = {}
        self.texts = []
        self.next = ''
        self.i = 0
        
    def reset(self):
        self.set_values()
        ''' We do not perform checks here since 'Videos.current'
            will create empty fields if they are missing.
        '''
    
    def fetch_next(self):
        f = '[Yatube] meta.Comments.fetch_next'
        if self.Success:
            if self.resp:
                self.i += 1
                if len(self.texts) > self.i:
                    result = self.texts[self.i]
                elif self.next:
                    result = self.fetch(token=self.next)
                else:
                    result = ''
                if self.i >= len(self.texts):
                    self.i = len(self.texts) - 1
                return result
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_prev(self):
        f = '[Yatube] meta.Comments.fetch_prev'
        if self.Success:
            ''' For some reason, there is no 'prevPageToken' in
                a comments output (even not documented), so we should
                allow an empty 'self.prev' to be able to navigate back
                to the first page.
            '''
            if self.resp:
                if self.i > 0:
                    self.i -= 1
                return self.texts[self.i]
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch(self,token=''):
        f = '[Yatube] meta.Comments.fetch'
        if self.Success:
            try:
                self.resp = com.get_service().commentThreads().list(
                                         part = 'snippet,replies'
                                        ,maxResults = MAX_COMMENTS
                                        ,videoId = objs.get_videos().get_current().id_
                                        ,textFormat = 'plainText'
                                        ,pageToken = token
                                        ).execute()
            except Exception as e:
                self.Success = False
                com.show_error(f,e)
            ''' The comments quota is not set in the quota calculator.
                According to documentation:
                https://developers.google.com/youtube/v3/docs/commentThreads/list#properties%23properties
                Quota: method: 1; replies: 2; snippet: 2
            '''
            objs.get_stat().add_quota(5)
            if self.resp:
                try:
                    self.next = self.resp['nextPageToken']
                except KeyError:
                    self.next = ''
                    mes = _('The end of the channel has been reached!')
                    sh.objs.get_mes(f,mes,True).show_info()
            return self.get_comments()
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
    
    def get_channel_id(self):
        f = '[Yatube] meta.VideoInfo.get_channel_id'
        video = objs.videos.get_current()
        if video.id_:
            resp = None
            try:
                resp = com.get_service().videos().list (id = video.id_
                                                       ,part = 'id,snippet'
                                                       ).execute()
            except Exception as e:
                com.show_error(f,e)
            objs.get_stat().add_quota(3)
            if resp:
                try:
                    for item in resp['items']:
                        if item['kind'] == "youtube#video":
                            video.chid = item['snippet']['channelId']
                            ''' We need other fields besides CHANID
                                if we extract URLs. This multi-purpose
                                procedure allows us to get those fields
                                by the same quota cost.
                            '''
                            if not video.author:
                                video.author = item['snippet']['channelTitle']
                                video.ptime = sh.com.get_yt_date(item['snippet']['publishedAt'])
                                video.title = item['snippet']['title']
                                video.desc = item['snippet']['description']
                                video.thumb = item['snippet']['thumbnails']['default']['url']
                            # We need only 1 suitable section
                            return video.chid
                except KeyError as e:
                    mes = _('Missing key: "{}"!').format(e)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
    
    def get_length(self):
        f = '[Yatube] meta.VideoInfo.get_length'
        video = objs.videos.get_current()
        if video.id_:
            resp = None
            try:
                resp = com.get_service().videos().list (id = video.id_
                                                       ,part = 'id,contentDetails'
                                                       ).execute()
            except Exception as e:
                com.show_error(f,e)
            objs.get_stat().add_quota(3)
            if resp:
                try:
                    for item in resp['items']:
                        if item['kind'] == "youtube#video":
                            length = item['contentDetails']['duration']
                            length = sh.com.get_yt_length(length)
                            if length:
                                if isinstance(length,(float,int)):
                                    video.len_ = length
                                    return video.len_
                                else:
                                    mes = _('Wrong input data: "{}"!')
                                    mes = mes.format(length)
                                    sh.objs.get_mes(f,mes).show_error()
                            else:
                                sh.com.rep_empty(f)
                except KeyError as e:
                    mes = _('Missing key: "{}"!').format(e)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
    
    def get_stat(self):
        f = '[Yatube] meta.VideoInfo.get_stat'
        video = objs.videos.get_current()
        if video.id_:
            resp = None
            try:
                resp = com.get_service().videos().list (id = video.id_
                                                       ,part = 'id,statistics'
                                                       ).execute()
            except Exception as e:
                com.show_error(f,e)
            objs.get_stat().add_quota(3)
            if resp:
                try:
                    for item in resp['items']:
                        if item['kind'] == "youtube#video":
                            video.views = sh.Input (title = f
                                                   ,value = item['statistics']['viewCount']
                                                   ).get_integer()
                            if 'likeCount' in item['statistics']:
                                video.likes = sh.Input (title = f
                                                       ,value = item['statistics']['likeCount']
                                                       ).get_integer()
                            else:
                                video.likes = -1
                            if 'dislikeCount' in item['statistics']:
                                video.dislikes = sh.Input (title = f
                                                          ,value = item['statistics']['dislikeCount']
                                                          ).get_integer()
                            else:
                                video.dislikes = -1
                            if 'commentCount' in item['statistics']:
                                video.com_num = sh.Input (title = f
                                                         ,value = item['statistics']['commentCount']
                                                         ).get_integer()
                            else:
                                video.com_num = -1
                            # We need only 1 suitable section
                            return True
                except KeyError as e:
                    mes = _('Missing key: "{}"!').format(e)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)



class Stat:
    
    def __init__(self):
        self.quota = 0
        ''' Timestamp when the program was started. This can be used
            to get a daily quota cost.
        '''
        self.started = sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp()
    
    def get_uptime(self):
        return sh.Time(pattern='%Y-%m-%d %H:%M:%S').get_timestamp() - self.started
    
    # Quota should be added even in case of invalid requests
    def add_quota(self,number):
        self.quota += number
    
    def report(self,Silent=False):
        f = '[Yatube] meta.Stat.report'
        sub = sh.com.get_human_time(self.get_uptime())
        mes = _('Uptime: {}').format(sub)
        mes += '\n'
        mes += _('Used quota: {}').format(self.quota)
        sh.objs.get_mes(f,mes,Silent).show_info()



class Playlist:
    
    def __init__(self,playid=None):
        self.set_values()
        if playid:
            self.reset(playid)
    
    def run(self):
        self.fetch()
        self.set_videos()
    
    def set_videos(self):
        f = '[Yatube] meta.Playlist.set_videos'
        if self.Success:
            if self.resp:
                try:
                    for item in self.resp['items']:
                        if item['snippet']['resourceId']['kind'] == "youtube#video":
                            video = Video()
                            video.id_ = item['snippet']['resourceId']['videoId']
                            video.author = item['snippet']['channelTitle']
                            video.chid = item['snippet']['channelId']
                            video.playid = item['snippet']['playlistId']
                            video.ptime = sh.com.get_yt_date(item['snippet']['publishedAt'])
                            video.title = item['snippet']['title']
                            video.desc = item['snippet']['description']
                            video.thumb = item['snippet']['thumbnails']['default']['url']
                            objs.get_videos().add(video)
                except KeyError as e:
                    mes = _('Missing key: "{}"!').format(e)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[Yatube] meta.Playlist.check'
        if self.playid:
            if self.playid.startswith('UU') and len(self.playid) == 24:
                return True
            else:
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(self.playid)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def reset(self,playid):
        f = '[Yatube] meta.Playlist.reset'
        self.set_values()
        self.playid = playid
        self.check()
        
    def set_values(self):
        self.Success = True
        self.resp = {}
        self.next = ''
        self.prev = ''
        self.playid = ''
    
    def fetch(self,token=''):
        f = '[Yatube] meta.Playlist.fetch'
        if self.Success:
            try:
                self.resp = com.get_service().playlistItems().list (playlistId = self.playid
                                                                   ,part = 'id,snippet'
                                                                   ,maxResults = MAX_VIDEOS
                                                                   ,pageToken = token
                                                                   ).execute()
            except Exception as e:
                com.show_error(f,e)
            objs.get_stat().add_quota(3)
            if self.resp:
                try:
                    self.prev = self.resp['prevPageToken']
                except KeyError:
                    self.prev = ''
                try:
                    self.next = self.resp['nextPageToken']
                except KeyError:
                    self.next = ''
                    mes = _('The end of the channel has been reached!')
                    sh.objs.get_mes(f,mes,True).show_info()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_next(self):
        f = '[Yatube] meta.Playlist.fetch_next'
        if self.Success:
            if self.resp and self.next:
                self.fetch(token=self.next)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_prev(self):
        f = '[Yatube] meta.Playlist.fetch_prev'
        if self.Success:
            if self.resp and self.prev:
                self.fetch(token=self.prev)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class Search:
    
    def __init__(self,query=''):
        self.set_values()
        if query:
            self.reset(query)
    
    def check(self):
        if self.query:
            return True
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def fetch(self,token=''):
        f = '[Yatube] meta.Search.fetch'
        if self.Success:
            try:
                self.resp = com.get_service().search().list (q = self.query
                                                            ,part = 'id,snippet'
                                                            ,maxResults = MAX_VIDEOS
                                                            ,safeSearch = 'none'
                                                            ,pageToken = token
                                                            ).execute()
            except Exception as e:
                com.show_error(f,e)
            objs.get_stat().add_quota(100)
            if self.resp:
                try:
                    self.prev = self.resp['prevPageToken']
                except KeyError:
                    self.prev = ''
                try:
                    self.next = self.resp['nextPageToken']
                except KeyError:
                    mes = _('The end of the channel has been reached!')
                    sh.objs.get_mes(f,mes,True).show_info()
                    self.next = ''
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_next(self):
        f = '[Yatube] meta.Search.fetch_next'
        if self.Success:
            if self.resp and self.next:
                self.fetch(token=self.next)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def fetch_prev(self):
        f = '[Yatube] meta.Search.fetch_prev'
        if self.Success:
            if self.resp and self.prev:
                self.fetch(token=self.prev)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.fetch()
        self.set_videos()
    
    def set_videos(self):
        f = '[Yatube] meta.Search.set_videos'
        if self.Success:
            try:
                for item in self.resp['items']:
                    if item['id']['kind'] == "youtube#video":
                        video = Video()
                        video.id_ = item['id']['videoId']
                        video.author = item['snippet']['channelTitle']
                        video.chid = item['snippet']['channelId']
                        video.ptime = sh.com.get_yt_date(item['snippet']['publishedAt'])
                        video.title = item['snippet']['title']
                        video.desc = item['snippet']['description']
                        video.thumb = item['snippet']['thumbnails']['default']['url']
                        objs.get_videos().add(video)
            except KeyError as e:
                mes = _('Missing key: "{}"!').format(e)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True
        self.resp = {}
        self.next = ''
        self.prev = ''
        self.query = ''
    
    def reset(self,query):
        f = '[Yatube] meta.Search.reset'
        self.set_values()
        self.query = query
        self.check()



class Video:
    
    def __init__(self):
        self.Block = False
        self.Saved = None
        self.bytes_ = None
        self.gui = None
        self.image = None
        self.com_num = 0
        self.dislikes = 0
        self.len_ = 0
        self.likes = 0
        self.pause = 0
        self.views = 0
        self.dtime = 0.0
        self.fdtime = 0.0
        self.ftime = 0.0
        self.ltime = 0.0
        self.ptime = 0.0
        self.author = ''
        self.chid = ''
        self.desc = ''
        self.dir_ = ''
        self.id_ = ''
        self.playid = ''
        self.page = ''
        self.path = ''
        self.pathsh = ''
        self.search = ''
        self.thumb = ''
        self.title = ''
        self.url = ''



class Videos:
    
    def __init__(self):
        self.reset()
    
    def set_gui(self,gui):
        f = '[Yatube] meta.Videos.set_gui'
        if gui:
            for self.i in range(len(self.videos)):
                if self.videos[self.i].gui == gui:
                    return True
        else:
            sh.com.rep_empty(f)
    
    def get_current(self):
        f = '[Yatube] meta.Videos.get_current'
        if not self.videos:
            sh.com.rep_empty(f)
            self.add(Video)
        if self.i < len(self.videos):
            return self.videos[self.i]
        else:
            sub = '{} < {}'.format(self.i,len(self.videos))
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_error()
            return Video()
    
    def add(self,video):
        f = '[Yatube] meta.Videos.video'
        if video:
            self.videos.append(video)
        else:
            sh.com.rep_empty(f)
    
    def reset(self):
        self.set_values()
    
    def set_values(self):
        self.videos = []
        self.i = 0
    
    # Orphan, debug
    def show_summary(self):
        f = '[Yatube] meta.Videos.show_summary'
        if self.videos:
            istr = io.StringIO()
            for i in range(len(self.videos)):
                istr.write('#%d:' % (i+1))
                istr.write('\n')
                istr.write(_('ID:'))
                istr.write(' ')
                istr.write(self.videos[i].id_)
                istr.write('\n')
                istr.write(_('Author:'))
                istr.write(' ')
                istr.write(self.videos[i].author)
                istr.write('\n')
                istr.write(_('Title:'))
                istr.write(' ')
                istr.write(self.videos[i].title)
                istr.write('\n')
                istr.write(_('Date:'))
                istr.write(' ')
                itime = sh.Time (tstamp = self.videos[i].ptime
                                ,pattern = '%Y-%m-%d %H:%M'
                                )
                istr.write(str(itime.get_date()))
                istr.write('\n')
                istr.write(_('Image:'))
                istr.write(' ')
                istr.write(self.videos[i].thumb)
                istr.write('\n\n')
            message = istr.getvalue()
            istr.close()
            sh.objs.get_mes(f,message).show_info()
        else:
            sh.com.rep_empty(f)



class Objects:
    
    def __init__(self):
        self.playlist = self.videos = self.search = self.stat \
                      = self.comments = self.playid = self.trending\
                      = None
    
    def get_trending(self):
        if self.trending is None:
            self.trending = Trending()
        return self.trending
    
    def get_playid(self):
        if self.playid is None:
            self.playid = PlayId()
        return self.playid
    
    def get_comments(self):
        if self.comments is None:
            self.comments = Comments()
        return self.comments
    
    def get_playlist(self):
        if self.playlist is None:
            self.playlist = Playlist()
        return self.playlist
    
    def get_stat(self):
        if self.stat is None:
            self.stat = Stat()
        return self.stat
    
    def get_search(self):
        if self.search is None:
            self.search = Search()
        return self.search
    
    def get_videos(self):
        if self.videos is None:
            self.videos = Videos()
        return self.videos



class Commands:
    
    def get_service(self):
        f = '[Yatube] meta.Commands.get_service'
        ''' Since this call quickly expires, we should rerun each time
            we use it.
        '''
        try:
            return build ('youtube','v3'
                         ,developerKey = API_KEY
                         ,cache = MemoryCache()
                         )
        except Exception as e:
            self.show_error(f,e)
    
    def show_error(self,f,e):
        e = str(e)
        if 'you have exceeded your' in e and 'quota' in e \
        or 'Daily Limit Exceeded' in e:
            mes = _('Quota has been exceeded!')
            sh.objs.get_mes(f,mes).show_warning()
        elif 'has disabled comments' in e:
            mes = _('Comments are disabled for this video.')
            sh.objs.get_mes(f,mes).show_info()
        elif 'The playlist identified with the requests <code>playlistId</code> parameter cannot be found.' in e:
            mes = _('This channel is not available!')
            sh.objs.get_mes(f,mes).show_warning()
        else:
            mes = _('Third-party module has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f,mes).show_warning()


objs = Objects()
com = Commands()


if __name__ == '__main__':
    f = 'meta.__main__'
    sh.com.start()
    objs.get_playlist().reset('UU63-vXUchmKqP7K9WE2jCfg')
    objs.playlist.run()
    video = objs.get_videos().get_current()
    print('CHANID:',video.chid)
    print('PLAYID:',video.playid)
    sh.com.end()
