from db import TVDatabaseManager
from nzb import NZB
from unc import UsenetCrawlerAPI
from sab import sabNZBdAPI
import settings
import urllib2
import urllib

class Episode:

    def __init__(self, tvrage_id, season, episode, ep_name, status=NZB.NZB_STATUS_NOSTATUS, airdate=None):
        self.tvrage_id = tvrage_id
        self.season = season
        self.episode = episode
        self.ep_name = ep_name
        self.status = status
        self.airdate=airdate

    def save(self):
        myDB = TVDatabaseManager()
        myDB.saveEpisode(self)

    def getShow(self):
        myDB = TVDatabaseManager()
        return myDB.getShow(self.tvrage_id)

    def updateNZBs(self):
        api = UsenetCrawlerAPI('e16200fc2eae4735c00b1f703961febc')
        nzbs = api.tv_search(self.tvrage_id,self.season, self.episode)
        myDB = TVDatabaseManager()
        for nzb in nzbs:
            try:
                myDB.addNZB(nzb)
            except Exception, e:
                print e
                continue
        return nzbs

    def getNZBs(self, status=0):
        myDB = TVDatabaseManager()
        return myDB.getNZBs(self, status)

    def startDownloading(self, update=False):
        if update:
            print "Updating..."
            self.updateNZBs()
        nzb = self.getQualityNZB()
        if nzb:
            sab = sabNZBdAPI(settings.SAB_HOST, settings.SAB_PORT, settings.SAB_APIKEY)
            sab.addNZBByLink(nzb, settings.SAB_CAT)
            nzb.pending()
            nzb.setLastTried()
            self.pending()
        else: 
            # No NZBs left with the desired quality
            self.fail()

    def fail(self):
        self.status=NZB.NZB_STATUS_FAIL
        self.save()

    def pending(self):
        self.status=NZB.NZB_STATUS_DOWNLOADING
        self.save()

    def getQualityNZB(self):
        desiredQualities = self.getShow().getQualities()
        for q in desiredQualities:
            print q.quality_text
        nzbs = self.getNZBs(NZB.NZB_STATUS_NOSTATUS)
        quality_nzbs = []
        for quality in desiredQualities:
            for nzb in nzbs:
                if quality.quality_text in nzb.nzb_name:
                    quality_nzbs.append(nzb)
                    nzbs.remove(nzb)
                    return nzb
        return None