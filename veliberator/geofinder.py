"""Geo localizator objects"""
from functools import wraps
from math import sqrt, radians, sin, cos, atan2, pi
from urllib import quote_plus
from urllib import urlopen

import simplejson as json

from veliberator.models import StationInformation

EARTH_RADIUS = 6378137.0  # Earth radius in meters
EARTH_CIRCUMFERENCE = EARTH_RADIUS * 2 * pi
EARTH_METER_DEGREE = 360.0 / EARTH_CIRCUMFERENCE
EARTH_DEGREE_METER = EARTH_CIRCUMFERENCE / 360.0

global_geofinder_cache = {}


def cache_wrapper(method):
    @wraps(method)
    def cache(instance, around_radius):
        """Use a global cache for the results
        of stations around"""
        global global_geofinder_cache

        key_cache = (instance.lat, instance.lng, around_radius)
        if key_cache not in global_geofinder_cache.keys():
            global_geofinder_cache[key_cache] = method(instance, around_radius)

        return global_geofinder_cache[key_cache]
    return cache


def pythagor_distance(start, end):
    """Compute the distance between 2 points
    with Pythagor theorem"""
    l1 = float(start[0]) - float(end[0])
    l2 = float(start[1]) - float(end[1])
    return sqrt(pow(l1, 2) + pow(l2, 2)) * EARTH_DEGREE_METER


def haversine_distance(start, end):
    """Compute the distance between 2 points in meters
    with the haversine formula"""
    start_latt = radians(float(start[0]))
    start_long = radians(float(start[1]))
    end_latt = radians(float(end[0]))
    end_long = radians(float(end[1]))
    d_latt = end_latt - start_latt
    d_long = end_long - start_long
    a = sin(d_latt / 2) ** 2 + cos(start_latt) * \
        cos(end_latt) * sin(d_long / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS * c


class GeoFinderError(Exception):
    pass


class BaseGeoFinder(object):
    """Base GeoFinder object,
    for finding stations around"""
    lat = None
    lng = None

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def compute_square_area(self, radius):
        """Compute the GPS coordonates of a square,
        around the position"""
        radius_degree = radius * EARTH_METER_DEGREE

        lat_orig = float(self.lat)
        lat_pos = lat_orig + radius_degree
        lat_neg = lat_orig - radius_degree

        lng_orig = float(self.lng)
        lng_pos = lng_orig + radius_degree
        lng_neg = lng_orig - radius_degree

        return (lat_neg, lat_orig, lat_pos), \
               (lng_neg, lng_orig, lng_pos)

    def compute_station_distances(self, stations,
                                  distance_function=haversine_distance):
        """Return the stations ordered by their distance to the
        origin, with a distance property added"""
        station_distances = {}

        for station in stations:
            if station.lat == self.lat and station.lng == self.lng:
                continue
            distance = distance_function((self.lat, self.lng),
                                         (station.lat, station.lng))
            station.distance = distance
            station_distances[station] = distance

        stations_sorted_by_distance = sorted(station_distances.iteritems(),
                                             key=lambda (k, v): (v, k))
        return [s for s, d in stations_sorted_by_distance]

    def get_stations_in_area(self, lats, lngs):
        """Make a query to find the station with
        lat and lng matching with the area"""
        return StationInformation.query.filter(
            (StationInformation.lat >= lats[0]) &
            (StationInformation.lat <= lats[2]) &
            (StationInformation.lng >= lngs[0]) &
            (StationInformation.lng <= lngs[2])).all()

    @cache_wrapper
    def get_stations_around(self, around_radius):
        """Find the stations around the lat and lng,
        sorted by proximity"""
        lats, lngs = self.compute_square_area(around_radius)
        stations = self.get_stations_in_area(lats, lngs)
        stations_distanced = self.compute_station_distances(stations)
        return stations_distanced


class StationGeoFinder(BaseGeoFinder):

    def __init__(self, station):
        """Init the object with a Station object"""
        self.lat = station.informations.lat
        self.lng = station.informations.lng


class AddressGeoFinder(BaseGeoFinder):

    def __init__(self, address):
        """Init the object with an address
        who will be geocomputed"""
        self.address = address
        informations = self.geocompute(address)

        self.lat = informations['geometry']['location']['lat']
        self.lng = informations['geometry']['location']['lng']
        self.precision = informations['types'][0]
        self.clean_address = informations['formatted_address']

    def geocompute(self, address):
        """Geocompute an address with GMap"""
        address = quote_plus(address)
        request = 'https://maps.googleapis.com/maps/api/geocode/json' \
                  '?address=%s&region=fr' % address
        data = json.loads(urlopen(request).read())

        if data['status'] != 'OK':
            raise GeoFinderError('Geocoding service error')
        return data['results'][0]
