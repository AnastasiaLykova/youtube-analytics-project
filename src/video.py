from src.channel import Channel


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        youtube = Channel.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        try:
            self.title: str = video_response['items'][0]['snippet']['title']
        except IndexError:
            self.url = None
            self.title = None
            self.view_count = None
            self.like_count = None
        else:
            video_data = video_response['items'][0]
            self.url = 'https://youtu.be/' + self.video_id
            self.title: str = video_data['snippet']['title']
            self.view_count: int = video_data['statistics']['viewCount']
            self.like_count: int = video_data['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
