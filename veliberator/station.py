"""Station objects for veliberator"""
from math import sqrt
from xml.dom.minidom import parse

from veliberator.models import db_connection
from veliberator.models import StationInformation
from veliberator.status import StationStatus

class UnknowStation(Exception):
    pass

class Station(object):
    """Station object,
    combinating informations and status"""

    def __init__(self, velib_id):
        self.id = int(velib_id)
        self.informations = self.acquire_informations()

        if not self.informations:
            raise UnknowStation('The Station ID does not exist.')

        self.status = StationStatus(self.id)

    def acquire_informations(self):
        """Default method for acquiring informations
        of a stations, by connecting to the database"""
        try:
            return StationInformation.get(self.id)
        except AttributeError:
            db_connection()
            return StationInformation.get(self.id)

    @property
    def is_open(self):
        """Property telling if the station is open"""
        return self.informations.opened

    @property
    def is_bonus(self):
        """Property telling if the station is bonus"""
        return self.informations.bonus

    def is_free(self, places=1):
        """Method property if the station
        has free places"""
        return self.is_open and self.status.free >= places

    def is_available(self, places=1):
        """Method property if the station
        has available places"""
        return self.is_open and self.status.available >= places

    def __repr__(self):
        if self.informations:
            return '<Station "%s" (%s)>' % (self.id, self.informations.address)
        return '<Station "%s">' % self.id

    def compute_distances(self, stations):
        """Compute the distance of the station,
        form other stations"""
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
        """Find the stations around"""
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


