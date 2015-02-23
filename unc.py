import urllib2
import urllib
import xml.etree.ElementTree as ET
from nzb import NZB

class UsenetCrawlerAPI:

    unc_url = 'https://www.usenet-crawler.com/api'

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def search(self, query, category=None, group=None, minsize=None, maxsize=None):
        params = {
        'apikey':self.API_KEY,
        't':'search',
        'q':query,
        }
        if category:
            params['cat']=category
        if group:
            params['group'] = group
        if minsize:
            params['minsize'] = minsize
        if maxsize:
            params['maxsize'] = maxsize
            
        qs = urllib.urlencode(params)
        
        url = self.unc_url + "?" + qs
        # print url
        res = urllib2.urlopen(url)
        # res_xml = res.read()
        et = ET.parse(res)
        return et
        # print et

    def tv_search(self, tvrage_id, season, ep):
        params = {
        'apikey':self.API_KEY,
        't':'tvsearch',
        'rid':tvrage_id
        }
        if season:
            params['season'] = season
        if ep:
            params['ep'] = ep
        

        qs = urllib.urlencode(params)
        
        url = self.unc_url + "?" + qs
        print url
        # print url
        res = urllib2.urlopen(url)
        # res_xml = res.read()
        et = ET.parse(res)
        items = et.find('channel').findall('item')
        found = []
        for item in items:
            item_dict = {

                'guid':item.find('guid').text,
                'title':item.find('title').text,
                'link':item.find('link').text,
            }
            nzb = NZB(tvrage_id=tvrage_id, season=season, episode=ep, nzb_name=item_dict['title'], nzb_link=item_dict['link'])
            # nzb.save()
            found.append(nzb)
        return found