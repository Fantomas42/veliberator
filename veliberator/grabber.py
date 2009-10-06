"""Grabber for collecting data"""
import urllib2
from random import sample

from veliberator.settings import PROXY_USAGE
from veliberator.settings import PROXY_SERVERS

SERVERS = PROXY_SERVERS.split(';')

class Grabber(object):
    """Url encapsultation for making request throught HTTP"""

    def __init__(self, url):
        """Init the grabber"""
        self.url = url
        self.opener = self.build_opener()
        self.data = None

    def build_opener(self):
        """Build the url opener"""
        handlers = []

        if PROXY_USAGE:
            handlers.append(urllib2.ProxyHandler({"http" : sample(SERVERS, 1)[0]}))

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
