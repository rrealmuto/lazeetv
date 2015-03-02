import sqlite3
import settings
# from show import Show

class TVDatabaseManager:
    dbName = settings.TV_DATABASE_FILE
    connected = False

    def connect(self):
        if not self.connected:
            self.conn = sqlite3.connect(self.dbName)
            self.conn.execute("PRAGMA foreign_keys=ON")
            self.connected = True
        return self.connected

    def disconnect(self):
        if self.connected:
            self.conn.commit()
            self.conn.close()
            self.connected = False

    def createTables(self):

        qualities_sql = "CREATE TABLE qualities(quality_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, quality_text TEXT NOT NULL)"
        shows_sql = "CREATE TABLE shows(tvrage_id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL, country TEXT NOT NULL, started INTEGER NOT NULL)"
        show_qualities_sql = "CREATE TABLE showqualities(show_id INTEGER NOT NULL, quality_id INTEGER NOT NULL, PRIORITY INTEGER NOT NULL, PRIMARY KEY(show_id, quality_id), FOREIGN KEY(show_id) REFERENCES shows(tvrage_id) ON DELETE CASCADE, FOREIGN KEY(quality_id) REFERENCES qualities(quality_id) ON DELETE CASCADE);"
        eps_sql = "CREATE TABLE episodes(show INTEGER NOT NULL, season INTEGER NOT NULL, episode INTEGER NOT NULL, ep_name TEXT, status INTEGER NOT NULL, airdate DATE, PRIMARY KEY(show, season, episode), FOREIGN KEY(show) REFERENCES shows(tvrage_id) ON DELETE CASCADE);"
        nzbs_sql = "CREATE TABLE nzbs(show INTEGER NOT NULL, season INTEGER NOT NULL, episode INTEGER NOT NULL, nzb_name TEXT NOT NULL, nzb_link TEXT NOT NULL, status INTEGER NOT NULL, last_tried DATE, PRIMARY KEY(show, season, episode, nzb_link), FOREIGN KEY(show, season, episode) REFERENCES episodes(show, season, episode) ON DELETE CASCADE)"
        self.connect()
        self.conn.execute(qualities_sql)
        self.conn.execute(shows_sql)
        self.conn.execute(show_qualities_sql)
        self.conn.execute(eps_sql)
        self.conn.execute(nzbs_sql)

        self.disconnect()

    def saveShow(self, show):

        sql = "INSERT INTO shows VALUES(?,?,?,?)"
        self.connect()
        try:
            self.conn.execute(sql, (str(show.tvrage_id), show.name, show.country, show.started))
        except sqlite3.IntegrityError:
            sql = "UPDATE shows SET name=?,country=?,started=? WHERE tvrage_id=?"
            self.conn.execute(sql, (show.name, show.country, show.started, str(show.tvrage_id)))
        self.disconnect()

    def saveEpisode(self, episode):
        sql = "INSERT INTO episodes VALUES(?,?,?,?,?,?)"
        self.connect()
        try:
            self.conn.execute(sql, (episode.tvrage_id, episode.season, episode.episode, episode.ep_name, episode.status, episode.airdate))
        except sqlite3.IntegrityError:
            sql = "UPDATE episodes SET ep_name=?, status=?, airdate=? WHERE (show=? AND season=? AND episode=?)"
            self.conn.execute(sql, (episode.ep_name, episode.status, episode.airdate, episode.tvrage_id, episode.season, episode.episode))
        self.disconnect()

    def getEpisode(self, tvrage_id, season, episode):
        from episode import Episode
        sql = "SELECT * FROM episodes WHERE show=? AND season=? and episode=?"
        self.connect()
        res = self.conn.execute(sql, (tvrage_id, season, episode))
        r = res.fetchone()
        self.disconnect()
        episode = Episode(r[0],r[1],r[2],r[3],r[4], r[5])
        return episode

    def addNZB(self, nzb):
        sql = "INSERT INTO nzbs VALUES(?,?,?,?,?,?,?)"
        self.connect()
        self.conn.execute(sql, (nzb.tvrage_id, nzb.season, nzb.episode, nzb.nzb_name, nzb.nzb_link, nzb.status, None))
        self.disconnect()

    def saveNZB(self, nzb):
        sql = "INSERT INTO nzbs VALUES(?,?,?,?,?,?,?)"
        self.connect()
        try:
            self.conn.execute(sql, (str(nzb.tvrage_id), str(nzb.season), str(nzb.episode), nzb.nzb_name, nzb.nzb_link, nzb.status, nzb.last_tried))
        except sqlite3.IntegrityError:
            sql = "UPDATE nzbs SET nzb_name=?, status=?, last_tried=? WHERE(show=? AND season=? AND episode=? AND nzb_link=?)"
            self.conn.execute(sql, (nzb.nzb_name, nzb.status, nzb.last_tried, nzb.tvrage_id, nzb.season, nzb.episode, nzb.nzb_link))
        self.disconnect()

    def getShow(self, tvrage_id):
        from show import Show
        sql = "SELECT * FROM shows WHERE tvrage_id=?"
        self.connect()
        res = self.conn.execute(sql, (tvrage_id,))
        r = res.fetchone()
        return Show(r[0], r[1], r[2], r[3])

    def getShows(self):
        from show import Show
        sql = "SELECT * FROM shows;"
        self.connect()
        res = self.conn.execute(sql)
        show_list = []
        for r in res:
            tvrage_id = r[0]
            name = r[1]
            country = r[2]
            started = r[3]
            show_list.append(Show(tvrage_id,name,country,started))
        return show_list

    def getNZBsEpisode(self, nzb):
        from episode import Episode
        from nzb import NZB
        sql = "SELECT * FROM episodes WHERE show=? AND season=? AND episode=?"
        self.connect()
        res = self.conn.execute(sql, (nzb.tvrage_id, nzb.season, nzb.episode))
        r = res.fetchone()
        self.disconnect()
        return Episode(r[0], r[1], r[2], r[3], r[4], r[5])

    def getEpisodes(self,show=None, status=None):
        from episode import Episode
        if show:
            if status is None:
                sql = "SELECT * FROM episodes WHERE show=?"
                qs = (show.tvrage_id,)
            else:
                sql = "SELECT * FROM episodes WHERE show=? AND status=?"
                qs = (show.tvrage_id, status)
        else:
            sql = "SELECT * FROM episodes"
            qs = (show.tvrage_id)
        print sql
        self.connect()
        res = self.conn.execute(sql, qs)
        print res
        ep_list = []
        for r in res:
            ep = Episode(r[0],r[1],r[2],r[3],r[4],r[5])
            ep_list.append(ep)
        self.disconnect()
        return ep_list

    def getNeededEpisodes(self, show):
        from episode import Episode
        from nzb import NZB
        sql = "SELECT * FROM episodes WHERE show=? AND NOT(status=?)"
        self.connect()
        res = self.conn.execute(sql, (show.tvrage_id, NZB.NZB_STATUS_SUCCESS))
        ep_list = []
        for r in res:
            ep = Episode(r[0],r[1],r[2],r[3],r[4],r[5])
            ep_list.append(ep)
        self.disconnect()
        return ep_list

    def getNZBs(self, episode=None, status=0):
        from nzb import NZB

        self.connect()
        if episode:
            sql = "SELECT * FROM nzbs WHERE show=? AND season=? AND episode=? AND status=?"
            res = self.conn.execute(sql, (episode.tvrage_id, episode.season, episode.episode, status))
        else:
            sql = "SELECT * FROM nzbs"
            res = self.conn.execute(sql)
        nzb_list = []
        for r in res:

            nzb = NZB(r[0], r[1],r[2], r[3], r[4], r[5], r[6])
            nzb_list.append(nzb)
        self.disconnect()
        return nzb_list

    def getNZB(self, nzb_name):
        from nzb import NZB
        sql = "SELECT * FROM nzbs WHERE nzb_name=?"
        self.connect()
        res = self.conn.execute(sql, (nzb_name,))
        r = res.fetchone()
        self.disconnect()

        return NZB(r[0], r[1], r[2], r[3],r[4], r[5], r[6])
        
    def deleteShow(self,show):
        sql = "DELETE FROM shows WHERE tvrage_id=?"
        self.connect()
        print show.tvrage_id
        res = self.conn.execute(sql, (show.tvrage_id,))
        self.disconnect()

    def addShowQuality(self, show, quality, priority):
        from quality import Quality
        sql = "INSERT INTO showqualities VALUES(?,?,?)"
        self.connect()
        self.conn.execute(sql, (show.tvrage_id, quality.quality_id, priority))
        self.disconnect()

    def getShowQualities(self, show):
        from quality import Quality
        sql = "SELECT Q.quality_id, Q.quality_text FROM qualities Q INNER JOIN showqualities SQ ON (Q.quality_id=SQ.quality_id) WHERE SQ.show_id=? ORDER BY priority"
        self.connect()
        res = self.conn.execute(sql, (show.tvrage_id,))
        quality_list = []
        for r in res:
            quality = Quality(quality_id=r[0], quality_text=r[1])
            quality_list.append(quality)
        self.disconnect()
        return quality_list

    def deleteShowQualities(self, show):
        print self.connected
        test = "DELETE FROM showqualities WHERE show_id=?"
        self.connect()

        self.conn.execute(test, (show.tvrage_id,))
        self.disconnect()


    def saveQuality(self, quality):
        from quality import Quality
        self.connect()
        if quality.quality_id:
            sql = "UPDATE qualities SET quality_text=? WHERE quality_id=?"
            self.conn.execute(sql, (quality.quality_text, quality.quality_id))
        else:
            sql = "INSERT INTO qualities(quality_text) VALUES(?)"
            self.conn.execute(sql, (quality.quality_text,))
        self.disconnect()

    def getQualities(self):
        from quality import Quality
        sql = "SELECT * FROM qualities"
        self.connect()
        res = self.conn.execute(sql)
        quality_list = []
        for r in res:
            quality = Quality(quality_id=r[0], quality_text=r[1])
            quality_list.append(quality)
        self.disconnect()
        return quality_list