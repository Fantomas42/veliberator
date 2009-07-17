"""Station objects for veliberator"""
from math import sqrt
from urllib import urlopen
from datetime import datetime, timedelta
from xml.dom.minidom import parse

from veliberator.models import db_connection
from veliberator.models import StationInformation
from veliberator.settings import VELIB_STATUS_XML_URL
from veliberator.settings import STATION_STATUS_RECENT
from veliberator.xml_wrappers import xml_station_status_wrapper

class UnknowStation(Exception):
    pass

def require_recent_status(meth):
    """Decorator for updating the status of a station"""
    def wrapper(self, *args, **kwargs):
        if not self.status:
            self.get_status()
        if self.status['datetime'] + \
               timedelta(minutes=STATION_STATUS_RECENT) < datetime.now():
            self.get_status()
        return meth(self, *args, **kwargs)    
    return wrapper

class Station(object):
    """Station object"""

    def __init__(self, velib_id):
        self.id = int(velib_id)
        self.status = None

        try:
            self.informations = StationInformation.get(self.id)
        except AttributeError:
            db_connection()
            self.informations = StationInformation.get(self.id)

        if not self.informations:
            raise UnknowStation('The Station ID does not exist.')

    @property
    def is_open(self):
        return self.informations.opened

    @property
    def is_bonus(self):
        return self.informations.bonus

    @property
    def address(self):
        return '%s, %s %s' % (self.informations.address,
                              self.informations.postal_code,
                              self.informations.city)

    @require_recent_status
    def is_free(self, places=1):        
        return self.is_open and self.status['free'] >= places

    @require_recent_status
    def is_available(self, places=1):
        return self.is_open and self.status['available'] >= places

    def __repr__(self):
        if self.informations:
            return '<Station "%s" (%s)>' % (self.id, self.informations.address)
        return '<Station "%s">' % self.id
        
    def get_status(self):
        dom = parse(urlopen(VELIB_STATUS_XML_URL % self.id))        
        self.status = xml_station_status_wrapper(dom.firstChild)
        self.status['datetime'] = datetime.now()

    def compute_distances(self, stations):
        distances = {}

        for station in stations:
            if station.id == self.id:
                continue
            l1 = float(self.informations.lat) - float(station.lat)
            l2 = float(self.informations.lng) - float(station.lng) 
            dist = sqrt(pow(l1, 2) + pow(l2, 2))
            distances[station] = dist

        return distances
        
    def get_stations_around(self, number=5):
        lat_orig = float(self.informations.lat)
        lat_pos = '%.2f' % (lat_orig + 0.01)
        lat_neg = '%.2f' % (lat_orig - 0.01)
        lat_orig = '%.2f' % lat_orig

        lng_orig = float(self.informations.lng)
        lng_pos = '%.2f' % (lng_orig + 0.01)
        lng_neg = '%.2f' % (lng_orig - 0.01)
        lng_orig = '%.2f' % lng_orig


        stations = StationInformation.query.filter(
            (StationInformation.lat.startswith(lat_orig) |
             StationInformation.lat.startswith(lat_pos) |
             StationInformation.lat.startswith(lat_neg)) &
            (StationInformation.lng.startswith(lng_orig) |
             StationInformation.lng.startswith(lng_pos) |
             StationInformation.lng.startswith(lng_neg))).all()

        station_distances = self.compute_distances(stations)
        station_distances_ordered = sorted(station_distances.iteritems(),
                                           key=lambda (k,v): (v,k))
        stations_id = [station.id for station, distance in station_distances_ordered]
        
        return stations_id[:number]


