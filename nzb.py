from db import TVDatabaseManager
from datetime import datetime
import urllib2


class NZB:
    NZB_STATUS_NOSTATUS = 0
    NZB_STATUS_DOWNLOADING = 1
    NZB_STATUS_SUCCESS = 2
    NZB_STATUS_FAIL = 3

    def __init__(self, tvrage_id, season, episode, nzb_name, nzb_link, status=NZB_STATUS_NOSTATUS, last_tried=None):
        self.tvrage_id = tvrage_id
        self.season = season
        self.episode = episode
        self.nzb_name = nzb_name
        self.nzb_link = nzb_link
        self.status = status
        self.last_tried = last_tried

    def save(self):
        myDB = TVDatabaseManager()
        myDB.saveNZB(self)

    def pending(self):
        self.status = self.NZB_STATUS_DOWNLOADING
        self.save()

    def success(self):
        self.status = self.NZB_STATUS_SUCCESS
        self.save()

    def fail(self):
        self.status = self.NZB_STATUS_FAIL
        self.save()

    def setLastTried(self):
        self.last_tried = datetime.now()
        self.save()

    def getNZB(self):
        res = urllib2.urlopen(self.nzb_link).read()
        return res

    def getEpisode(self):
        myDB = TVDatabaseManager()
        return myDB.getNZBsEpisode(self)