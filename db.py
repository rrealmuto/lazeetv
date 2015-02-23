import sqlite3
# from show import Show

class TVDatabaseManager:
    dbName = 'database.db'
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

        shows_sql = "CREATE TABLE shows(tvrage_id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL, country TEXT NOT NULL, started INTEGER NOT NULL)"
        
        eps_sql = "CREATE TABLE episodes(show INTEGER NOT NULL, season INTEGER NOT NULL, episode INTEGER NOT NULL, ep_name TEXT, status INTEGER NOT NULL, PRIMARY KEY(show, season, episode), FOREIGN KEY(show) REFERENCES shows(tvrage_id) ON DELETE CASCADE);"
        nzbs_sql = "CREATE TABLE nzbs(show INTEGER NOT NULL, season INTEGER NOT NULL, episode INTEGER NOT NULL, nzb_name TEXT NOT NULL, nzb_link TEXT NOT NULL, status INTEGER NOT NULL, PRIMARY KEY(show, season, episode, nzb_link), FOREIGN KEY(show, season, episode) REFERENCES episodes(show, season, episode) ON DELETE CASCADE)"
        fk_sql = "PRAGMA foreign_keys = ON"
        self.connect()
        self.conn.execute(fk_sql)
        self.conn.execute(shows_sql)
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
        sql = "INSERT INTO episodes VALUES(?,?,?,?,?)"
        self.connect()
        try:
            self.conn.execute(sql, (episode.tvrage_id, episode.season, episode.episode, episode.ep_name, episode.status))
        except sqlite3.IntegrityError:
            sql = "UPDATE episodes SET ep_name=?, status=? WHERE (show=? AND season=? AND episode=?)"
            self.conn.execute(sql, (episode.ep_name, episode.status, episode.tvrage_id, episode.season, episode.episode))
        self.disconnect()

    def addNZB(self, nzb):
        sql = "INSERT INTO nzbs VALUES(?,?,?,?,?,?)"
        self.connect()
        self.conn.execute(sql, (nzb.tvrage_id, nzb.season, nzb.episode, nzb.nzb_name, nzb.nzb_link, nzb.status))

    def saveNZB(self, nzb):
        sql = "INSERT INTO nzbs VALUES(?,?,?,?,?,?)"
        self.connect()
        try:
            self.conn.execute(sql, (str(nzb.tvrage_id), str(nzb.season), str(nzb.episode), nzb.nzb_name, nzb.nzb_link, nzb.status))
        except sqlite3.IntegrityError:
            sql = "UPDATE nzbs SET nzb_name=?, status=? WHERE(show=? AND season=? AND episode=? AND nzb_link=?)"
            self.conn.execute(sql, (nzb.nzb_name, nzb.status, nzb.tvrage_id, nzb.season, nzb.episode, nzb.nzb_link))
        self.disconnect()

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

    def getEpisodes(self,show=None):
        from episode import Episode
        if show:
            sql = "SELECT * FROM episodes WHERE show=?"
        else:
            sql = "SELECT * FROM episodes"
        print sql
        self.connect()
        res = self.conn.execute(sql, (show.tvrage_id,))
        print res
        ep_list = []
        for r in res:
            ep = Episode(r[0],r[1],r[2],r[3],r[4])
            ep_list.append(ep)
        self.disconnect()
        return ep_list

    def getNZBs(self, episode=None, status=0):
        from nzb import NZB

        self.connect()
        if episode:
            print "using this"
            sql = "SELECT * FROM nzbs WHERE show=? AND season=? AND episode=? AND status=?"
            res = self.conn.execute(sql, (episode.tvrage_id, episode.season, episode.episode, status))
        else:
            sql = "SELECT * FROM nzbs"
            res = self.conn.execute(sql)
        nzb_list = []
        for r in res:

            nzb = NZB(r[0], r[1],r[2], r[3], r[4], r[5])
            nzb_list.append(nzb)
        self.disconnect()
        return nzb_list

    def deleteShow(self,show):
        sql = "DELETE FROM shows WHERE tvrage_id=?"
        self.connect()
        print show.tvrage_id
        res = self.conn.execute(sql, (show.tvrage_id,))
        self.disconnect()