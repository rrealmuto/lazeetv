from db import TVDatabaseManager
class Quality:

    def __init__(self,  quality_text, quality_id=None):
        self.quality_id = quality_id
        self.quality_text = quality_text

    def save(self):
        myDB = TVDatabaseManager()
        myDB.saveQuality(self)