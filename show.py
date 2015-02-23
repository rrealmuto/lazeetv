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

    def getEpisodes(self):
        myDB = TVDatabaseManager()
        return myDB.getEpisodes(self)

    def setQualities(self, qualities):
        myDB = TVDatabaseManager()
        myDB.deleteShowQualities(self)
        for quality in qualities:
            myDB.addShowQuality(self, quality)

    def getQualities(self):
        myDB = TVDatabaseManager()
        return myDB.getShowQualities(self)