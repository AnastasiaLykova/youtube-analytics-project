from src.channel import Channel
import isodate
import datetime


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        youtube = Channel.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='snippet',
                                                       maxResults=50,
                                                       ).execute()
        channel_id = playlist_videos['items'][0]['snippet']['channelId']
        playlists = youtube.playlists().list(channelId=channel_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()
        for playlist in playlists['items']:
            if playlist['id'] == playlist_id:
                self.title = playlist['snippet']['title']

        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id

    @property
    def total_duration(self):
        """
        возвращает объект класса datetime.timedelta
        с суммарной длительность плейлиста
        """
        youtube = Channel.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        delta = datetime.timedelta()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            delta += duration
        return delta

    def show_best_video(self):
        """
        возвращает ссылку на самое популярное
        видео из плейлиста (по количеству лайков)
        """
        youtube = Channel.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        max_like = 0
        max_like_url = ''
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > max_like:
                max_like = int(video['statistics']['likeCount'])
                max_like_url = video['id']
        return f"https://youtu.be/" + max_like_url
