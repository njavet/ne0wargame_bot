import pymongo
import datetime
import collections


class Storage(object):
    def __init__(self, host, dbuser, dbpasswd):
        self.db = self.setup_db(host, dbuser, dbpasswd)

    @staticmethod
    def setup_db(host, dbuser, dbpasswd):
        client = pymongo.MongoClient(host='localhost')
        return client.wargame

    def read_chats(self):
        col = self.db.chats
        cursor = col.find().sort('datetime', pymongo.DESCENDING)
        dix = {doc['chat_id']: doc['users'] for doc in cursor}
        if dix:
            return dix
        else:
            return collections.defaultdict(dict)

    def update_chats(self, chats):
        today = datetime.datetime.today()
        for chat_id, users in chats.items():
            self.db.chats.insert({'datetime': today,
                                  'chat_id': chat_id,
                                  'users': users})
