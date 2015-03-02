import cherrypy
from Cheetah.Template import Template
from db import TVDatabaseManager
from tvrage import TVRageAPI
from show import Show
import sqlite3
import json
import os, os.path

class TV:
    def index(self):
        t = Template(file='templates/home.html')
        return t.respond()
    index.exposed=True

    def shows(self):
        db = TVDatabaseManager()
        myShows = db.getShows()
        myShowsPlus = []
        for show in myShows:
            myShowsPlus.append((show, len(show.getSuccessfulEpisodes()), len(show.getEpisodes())))
        print myShowsPlus
        context = {
            'shows':myShows
        }
        t = Template(file='templates/shows.html', searchList=context)
        return t.respond()
    shows.exposed=True

    def show(self, id):
        db = TVDatabaseManager()
        show = db.getShow(id)
        seasons = show.getEpisodesAsSeasons()
        print seasons
        context = {
            'show':show,
            'seasons':seasons
        }
        t = Template(file='templates/show.html', searchList=context)
        return t.respond()

    show.exposed=True
    def addshow(self, **kwargs):
        print dir(cherrypy.request)
        print cherrypy.request.method
        # Check if the request is a post
        if cherrypy.request.method == "POST":
            print dir(cherrypy.request.body)
            # it was a post, so get the show from the kwargs (in the 'show' parameter)
            show_json = kwargs['show']
            show_dict = json.loads(show_json)
            show = Show(tvrage_id=show_dict['tvrage_id'], show_name=show_dict['name'], country=show_dict['country'], started=show_dict['started'])
            show.save()
            show.refreshEpisodeList()
            raise cherrypy.HTTPRedirect("shows")
        t = Template(file='templates/addshow.html')
        return t.respond()
    addshow.exposed=True

    def findshows(self, search):
        print search
        api = TVRageAPI()
        shows = api.search(search)
        show_list = []
        for show in shows:
            show_list.append(show.as_dict())
        return json.dumps(show_list)
    findshows.exposed=True

    def downloadepisode(self, episode):
        db = TVDatabaseManager()
        episode_dict = json.loads(episode)
        ep = db.getEpisode(tvrage_id=episode_dict['tvrage_id'], season=episode_dict['season'], episode=episode_dict['episode'])
        ep.startDownloading(update=True)
        return ep.ep_name
    downloadepisode.exposed=True

    def refresh(self, showid):
        db = TVDatabaseManager()
        show = db.getShow(showid)
        show.refreshEpisodeList()
        raise cherrypy.HTTPRedirect("show?id="+showid)
        return "Done"
    refresh.exposed=True

myDB = TVDatabaseManager()
try:  # try to create the tables
    myDB.createTables()
except sqlite3.OperationalError, e: #if we get an operational error, that should mean that the tables already existed
    print e

conf = {
    '/':{
        'tools.staticdir.root':os.path.abspath(os.getcwd())
    },
    '/static':{
        'tools.staticdir.on':True,
        'tools.staticdir.dir':'./public'
    }
}

cherrypy.quickstart(TV(), '/', conf)