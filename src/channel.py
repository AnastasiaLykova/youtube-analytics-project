import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscribers = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.views = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """ Метод для операции сложения"""
        return int(self.subscribers) + int(other.subscribers)

    def __sub__(self, other):
        """ Метод для операции вычитания"""
        return int(self.subscribers) - int(other.subscribers)

    def __lt__(self, other):
        """ Метод для операции сравнения «меньше»"""
        if int(self.subscribers) < int(other.subscribers):
            return True
        else:
            return False

    def __le__(self, other):
        """ Метод для операции сравнения «меньше или равно»"""
        if int(self.subscribers) <= int(other.subscribers):
            return True
        else:
            return False

    def __gt__(self, other):
        """ Метод для операции сравнения «больше»"""
        if int(self.subscribers) > int(other.subscribers):
            return True
        else:
            return False

    def __ge__(self, other):
        """  Метод для операции сравнения «больше или равно»"""
        if int(self.subscribers) >= int(other.subscribers):
            return True
        else:
            return False

    def __eq__(self, other):
        """ Поведение оператора равенства"""
        if int(self.subscribers) == int(other.subscribers):
            return True
        else:
            return False

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, name_json):
        """
        Сохраняет в файл значения атрибутов экземпляра Channel
        """
        attribute_dict = {'channel_id': self.__channel_id,
                          'title': self.title,
                          'description': self.description,
                          'url': self.url,
                          'subscribers': self.subscribers,
                          'video_count': self.video_count,
                          'views': self.views,
                          }

        with open(name_json, "w", encoding="utf-8") as file:
            file.write(json.dumps(attribute_dict))
