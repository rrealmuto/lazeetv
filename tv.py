from unc import UsenetCrawlerAPI
from db import TVDatabaseManager
from show import Show
from tvrage import TVRageAPI
import sqlite3

options = [
    'a -- Add a new show',
    's -- Search for NZBs',
    'd -- Delete show',
    'q -- Quit',


]

def new_show_function():
    showname = raw_input("Search for show: ")
    api = TVRageAPI()
    shows = api.search(showname)

    i = 0
    for show in shows:
        print str(i) + ": " + show.name
        i = i + 1
    done = False
    index = -1

    while not done:
        selection = raw_input("Which show? (Enter the number from above) ")
        try:
            index = int(selection)
            done = True
        except ValueError:
            done = False
            print "Try Again"

    show = shows[index]
    show.save()
    eps = api.episode_list(show.tvrage_id)
    for ep in eps:
        ep.save()
    return False

def search_for_nzbs_function():
    show = prompt_for_show()
    eps = show.getEpisodes()
    for ep in eps:
        print "Search for nzbs for S" + str(ep.season) +"E" + str(ep.episode)
        ep.startDownloading(update=True)


def delete_show_function():
    show = prompt_for_show()
    show.delete()

def prompt_for_show():
    myDB = TVDatabaseManager()
    shows = myDB.getShows()
    i = 0
    for show in shows:
        print str(i) + ": " + show.name
    index = -1
    done = False
    while not done:
        try:
            index = int(raw_input("Which show? "))
            done = True
        except ValueError:
            done = False
            print "Try again"
    show = shows[index]
    return show

def quit():
    return True

function_map = {
    'q':quit,
    'a': new_show_function,
    'd': delete_show_function,
    's': search_for_nzbs_function,
}

myDB = TVDatabaseManager()
try:  # try to create the tables
    myDB.createTables()
except sqlite3.OperationalError: #if we get an operational error, that should mean that the tables already existed
    print "Already exists"

done = False
while not done:
    for option in options:
        print option
    sel = raw_input("What would you like to do? ")
    try:
        done = function_map[sel]()
    except KeyError:
        print "Invalid command"
