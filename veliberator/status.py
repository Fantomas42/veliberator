"""Status objects for veliberator"""
from urllib import urlopen
from datetime import datetime, timedelta
from xml.dom.minidom import parse

from veliberator.settings import STATION_STATUS_RECENT
from veliberator.settings import XML_URL_STATUS_STATION
from veliberator.xml_wrappers import xml_station_status_wrapper

global_station_status = {}

class StationStatus(object):
    """Status of a station, by opening an url
    providing a xml file, with cache"""
    status = {}

    def __init__(self, velib_id, xml_url=XML_URL_STATUS_STATION):
        self.velib_id = velib_id
        self.xml_url = xml_url + str(self.velib_id)
        self.get_status()

    def get_status(self):
        if global_station_status.has_key(self.velib_id):
            status = global_station_status[self.velib_id]

            if status['datetime'] + \
               timedelta(minutes=STATION_STATUS_RECENT) < datetime.now():
                self.set_status()
            else:
                self.status = status
        else:
            self.set_status()

    def set_status(self):
        global global_station_status
        self.status = self.get_status_xml()
        global_station_status[self.velib_id] = self.status
                
    def get_status_xml(self):
        dom = parse(urlopen(self.xml_url))        
        status = xml_station_status_wrapper(dom.firstChild)
        status['datetime'] = datetime.now()        

        return status

    def __getattr__(self, name):
        if self.status.has_key(name):
            return self.status.get(name)
        return getattr(self, name)

    def __repr__(self):
        return '<StationStatus "%s">' % self.velib_id
