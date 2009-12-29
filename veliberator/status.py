"""Status objects for veliberator"""
from datetime import datetime, timedelta
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError

from veliberator.settings import STATION_STATUS_RECENT
from veliberator.settings import XML_URL_STATUS_STATION
from veliberator.xml_wrappers import xml_station_status_wrapper
from veliberator.grabber import Grabber

global_stationstatus_cache = {}

def cache_wrapper(method):
    def cache(instance):
        """Use a timed cache for result, and set
        the results into the instance"""
        global global_stationstatus_cache
        
        key_cache = instance.velib_id
        if not global_stationstatus_cache.has_key(key_cache) or \
               global_stationstatus_cache[key_cache]['datetime'] + \
               timedelta(minutes=STATION_STATUS_RECENT) < datetime.now():
            global_stationstatus_cache[key_cache] = method(instance)
        instance.status = global_stationstatus_cache[key_cache]
        return instance.status
    return cache

class StationStatus(object):
    """Status of a station, by opening an url
    providing a xml file, with cache"""
    status = {}

    def __init__(self, velib_id, xml_url=XML_URL_STATUS_STATION):
        """Init the status"""
        self.velib_id = velib_id
        self.xml_url = xml_url + str(self.velib_id)
        self.get_status()

    @cache_wrapper
    def get_status(self):
        """Get the status provided by an URL"""
        try:
            dom = parseString(Grabber(self.xml_url).content)        
            status = xml_station_status_wrapper(dom.firstChild)
        except (IOError, IndexError, ValueError, ExpatError):
            status = {'total': 0, 'available': 0,
                      'free': 0, 'ticket': False}
        status['closed'] = status['total'] - (status['available'] + status['free'])
        status['datetime'] = datetime.now()
        return status

    def __getattr__(self, name):
        """Allow direct access to self.status items"""
        if self.status.has_key(name):
            return self.status.get(name)
        return getattr(self, name)

    def __repr__(self):
        return '<StationStatus "%s">' % self.velib_id
