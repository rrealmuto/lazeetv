import urllib2
import urllib

class sabNZBdAPI:

    def __init__(self, host,port,API_KEY):
        self.host=host
        self.port=port
        self.API_KEY = API_KEY

    def addNZBByLink(self, nzb, cat='Default'):
        url_ext = '/api'
        data = {
            'mode':'addurl',
            'name':nzb.nzb_link,
            'cat':cat,
            'apikey':self.API_KEY,
        }
        data_enc = urllib.urlencode(data)
        urllib2.urlopen('http://' + self.host + ':' + self.port + url_ext+'?'+data_enc)