import urllib2
import urllib
import xml.etree.ElementTree as ET
from show import Show
from episode import Episode

class TVRageAPI:
    API_URL = 'http://services.tvrage.com/feeds/'

    def search(self, show_name):
        url_ext = 'search.php'
        params = {
            'show':show_name
        }

        qs = urllib.urlencode(params)
        url = self.API_URL + url_ext + "?" + qs
        res = urllib2.urlopen(url)
        et = ET.parse(res)

        shows = et.getroot().findall('show')
        show_list = []
        for show in shows:
            tvrage_id = int(show.find('showid').text)
            name = show.find('name').text
            country = show.find('country').text
            started = int(show.find('started').text)
            show_list.append(Show(tvrage_id=tvrage_id, show_name=name,country=country,started=started))
        return show_list

    def episode_list(self, tvrage_id):
        url_ext = 'episode_list.php'
        params = {
            'sid':tvrage_id
        }

        qs = urllib.urlencode(params)
        url = self.API_URL + url_ext + "?" + qs
        res = urllib2.urlopen(url)
        et = ET.parse(res)
        seasons = et.getroot().find('Episodelist').findall('Season')
        eplist = []
        for season in seasons:
            season_num = int(season.get('no'))
            eps = season.findall('episode')
            for ep in eps:
                ep_num = ep.find('seasonnum').text
                name = ep.find('title').text
                eplist.append(Episode(tvrage_id=tvrage_id, season=season_num, episode=ep_num, ep_name=name))
        return eplist