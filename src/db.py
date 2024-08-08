from pymongo import MongoClient
from config import DB_HOST, DB_PORT


class DBClient:

    def __init__(self):
        self._client = MongoClient(f"mongodb://{DB_HOST}:{DB_PORT}")
        self._db = self._client["database"]
        self._videos = self._db["videos"]
        self._tvshows = self._db["tvshows"]

    @property
    def videos_collection(self):
        return self._videos

    @property
    def tvshows_collection(self):
        return self._tvshows
