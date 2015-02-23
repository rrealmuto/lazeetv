from db import TVDatabaseManager
from nzb import NZB
from unc import UsenetCrawlerAPI
from sab import sabNZBdAPI
import settings
import urllib2
import urllib

class Episode:

    def __init__(self, tvrage_id, season, episode, ep_name, status=NZB.NZB_STATUS_NOSTATUS):
        self.tvrage_id = tvrage_id
        self.season = season
        self.episode = episode
        self.ep_name = ep_name
        self.status = status

    def save(self):
        myDB = TVDatabaseManager()
        myDB.saveEpisode(self)

    def updateNZBs(self):
        api = UsenetCrawlerAPI('e16200fc2eae4735c00b1f703961febc')
        nzbs = api.tv_search(self.tvrage_id,self.season, self.episode)
        myDB = TVDatabaseManager()
        for nzb in nzbs:
            try:
                myDB.addNZB(nzb)
            except:
                continue
        return nzbs

    def getNZBs(self, status=0):
        myDB = TVDatabaseManager()
        return myDB.getNZBs(self, status)

    def startDownloading(self, update=False):
        if update:
            self.updateNZBs()
        nzbs = self.getNZBs(NZB.NZB_STATUS_NOSTATUS)
        if len(nzbs) > 0:
            sab = sabNZBdAPI(settings.SAB_HOST, settings.SAB_PORT, settings.SAB_APIKEY)
            sab.addNZBByLink(nzbs[0], settings.SAB_CAT)
            nzbs[0].pending()
            