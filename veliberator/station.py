"""Station objects for veliberator"""
from math import sqrt
from urllib import urlopen
from xml.dom.minidom import parse

from veliberator.models import StationInformation
from veliberator.settings import VELIB_STATUS_XML_URL
from veliberator.xml_wrappers import xml_station_status_wrapper

class UnknowStation(Exception):
    pass

class Station(object):
    """Station object"""

    def __init__(self, velib_id):
        self.id = int(velib_id)
        self.status = None
        self.informations = StationInformation.get(self.id)

        if not self.informations:
            raise UnknowStation('The Station ID does not exist.')

    def __repr__(self):
        if self.informations:
            return '<Station "%s" (%s)>' % (self.id, self.informations.address)
        return '<Station "%s">' % self.id
        
    def get_status(self):
        dom = parse(urlopen(VELIB_STATUS_XML_URL % self.id))        
        self.status = xml_station_status_wrapper(dom.firstChild)

    def show_status(self):
        if not self.status:
            self.get_status()
        print "Station '%s'" % self.id
        print '%s, %s %s' % (self.informations.address,
                             self.informations.postal_code,
                             self.informations.city)
        print '%s/%s velo(s) disponible' % (self.status['available'], self.status['total'])
        print '%s place(s) disponible' % self.status['free']

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
        
