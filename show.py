from db import TVDatabaseManager
class Show:
    def __init__(self, tvrage_id, show_name, country, started):
        self.tvrage_id = tvrage_id
        self.name = show_name
        self.country=country
        self.started = started

    def delete(self):
        myDB = TVDatabaseManager()
        myDB.deleteShow(self)

    def save(self):
        myDB = TVDatabaseManager()
        myDB.saveShow(self)

    def getSuccessfulEpisodes(self):
        myDB = TVDatabaseManager()
        return myDB.getEpisodes(self, status=2)

    def refreshEpisodeList(self):

        from tvrage import TVRageAPI
        api = TVRageAPI()
        eps = api.episode_list(self.tvrage_id)
        for ep in eps:
            ep.save()

    def getEpisodes(self):
        myDB = TVDatabaseManager()
        return myDB.getEpisodes(self)

    def getEpisodesAsSeasons(self):
        seasons = {}
        episodes = self.getEpisodes()
        for ep in episodes:
            try:
                seasons[ep.season].append(ep)
            except KeyError:
                seasons[ep.season] = []
                seasons[ep.season].append(ep)
        return seasons
    def getNeededEpisodes(self):
        myDB = TVDatabaseManager()
        return myDB.getNeededEpisodes(self)

    def setQualities(self, qualitiesWPriorities):
        myDB = TVDatabaseManager()
        myDB.deleteShowQualities(self)
        for qwp in qualitiesWPriorities:
            quality, priority =  qwp
            myDB.addShowQuality(self, quality, priority)

    def getQualities(self):
        myDB = TVDatabaseManager()
        return myDB.getShowQualities(self)

    def as_dict(self):
        return {
            'tvrage_id':self.tvrage_id,
            'name':self.name,
            'country':self.country,
            'started':self.started
        }