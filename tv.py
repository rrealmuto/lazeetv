from unc import UsenetCrawlerAPI
from db import TVDatabaseManager
from show import Show
from quality import Quality
from tvrage import TVRageAPI
import sqlite3

options = [
    'a -- Add a new show',
    'aq -- Add a new quality',
    's -- Search for NZBs',
    'e -- Edit show',
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

def edit_show_function():
    
    show = prompt_for_show()
    allQualities = myDB.getQualities()
    
    selectedQualities=[]
    done = False
    priority = 0
    while not done:
        i = 0
        print "Selected Qualities:"
        for quality in selectedQualities:
            print quality[0].quality_text
        print ""
        for quality in allQualities:
            print str(i) + ": " + quality.quality_text
            i = i + 1

        try:    
            sel = int(raw_input("Select one of the above qualities (-1 to commit): "))
        except ValueError:
            print "Bad input"
            continue

        if sel == -1:
            done = True
        else:
            qual = allQualities[sel]
            selectedQualities.append((qual, priority))
            allQualities.remove(qual)
            priority = priority + 1
            done=False
    show.setQualities(selectedQualities)


def search_for_nzbs_function():
    show = prompt_for_show()
    eps = show.getNeededEpisodes()
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
        i += 1
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

def add_quality_function():
    myDB = TVDatabaseManager()
    newQualityText = raw_input("What's the text for this quality? ")
    qual = Quality(quality_text=newQualityText)
    qual.save()

def quit():
    return True

function_map = {
    'q':quit,
    'a': new_show_function,
    'e': edit_show_function,
    'aq':add_quality_function,
    'd': delete_show_function,
    's': search_for_nzbs_function,
}

myDB = TVDatabaseManager()
try:  # try to create the tables
    myDB.createTables()
except sqlite3.OperationalError, e: #if we get an operational error, that should mean that the tables already existed
    print e

done = False
while not done:
    for option in options:
        print option
    sel = raw_input("What would you like to do? ")
    try:
        done = function_map[sel]()
    except KeyError:
        print "Invalid command"
