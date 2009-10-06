"""Grabber for collecting data"""
import urllib2
from random import sample

from veliberator.settings import PROXY_SERVERS

class Grabber(object):
    """Url encapsultation for making request throught HTTP"""
    page = None
    data = None

    def __init__(self, url, proxies=PROXY_SERVERS):
        """Init the grabber"""
        self.url = url
        self.proxies = proxies
        self.opener = self.build_opener()

    def build_opener(self):
        """Build the url opener"""
        handlers = []
        
        if self.proxies:
            server = sample(self.proxies, 1)[0]
            handlers.append(urllib2.ProxyHandler({"http" : server}))

        return urllib2.build_opener(*handlers)

    @property
    def content(self):
        """Return the data grabbed"""
        if self.data:
            return self.data
        else:
            self.page = self.opener.open(self.url)
            self.data = ''.join(self.page.readlines())
            self.page.close()        
        
        return self.data
