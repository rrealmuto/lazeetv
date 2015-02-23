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