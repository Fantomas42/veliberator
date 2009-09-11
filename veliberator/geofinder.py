"""Geo localizator objects"""
from math import sqrt
from urllib import quote_plus
from urllib import urlopen

import simplejson as json

from veliberator.models import StationInformation

global_geofinder_cache = {}

def cache_wrapper(method):
    def cache(instance):
        """Use a global cache for the results
        of stations around"""
        global global_geofinder_cache
        
        key_cache = (instance.lat, instance.lng)
        if not key_cache in global_geofinder_cache.keys():
            global_geofinder_cache[key_cache] = method(instance)
       
        return global_geofinder_cache[key_cache]
    return cache

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

    def compute_square_area(self):
        """Round the GPS coordonates to a wide area"""
        #to be refactored for configuring the area size
        lat_orig = float(self.lat)
        lat_pos = '%.2f' % (lat_orig + 0.01)
        lat_neg = '%.2f' % (lat_orig - 0.01)
        lat_orig = '%.2f' % lat_orig

        lng_orig = float(self.lng)
        lng_pos = '%.2f' % (lng_orig + 0.01)
        lng_neg = '%.2f' % (lng_orig - 0.01)
        lng_orig = '%.2f' % lng_orig

        return (lat_neg, lat_orig, lat_pos), (lng_neg, lng_orig, lng_pos)

    def compute_station_distances(self, stations):
        """Compute the distance from the coords,
        to the other stations, Pythagore powered"""
        distances = {}

        for station in stations:
            if station.lat == self.lat and station.lng == self.lng:
                continue
            l1 = float(self.lat) - float(station.lat)
            l2 = float(self.lng) - float(station.lng)
            dist = sqrt(pow(l1, 2) + pow(l2, 2))
            distances[station] = dist

        return distances

    def get_stations_in_area(self, lats, lngs):
        """Make a query to find the station with
        lat and lng matching with the area"""
        return StationInformation.query.filter(
            (StationInformation.lat.startswith(lats[0]) |
             StationInformation.lat.startswith(lats[1]) |
             StationInformation.lat.startswith(lats[2])) &
            (StationInformation.lng.startswith(lngs[0]) |
             StationInformation.lng.startswith(lngs[1]) |
             StationInformation.lng.startswith(lngs[2]))).all()


    @cache_wrapper
    def get_stations_around(self):
        """Find the stations around the lat and lng,
        sorted by proximity"""
        lats, lngs = self.compute_square_area()
        stations = self.get_stations_in_area(lats, lngs)
        station_distances = self.compute_station_distances(stations)
        station_distances_ordered = sorted(station_distances.iteritems(),
                                           key=lambda (k,v): (v,k))
        stations_id = [station.id for station, distance in station_distances_ordered]

        return stations_id


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

        self.lat = informations['Point']['coordinates'][1]
        self.lng = informations['Point']['coordinates'][0]
        self.precision = informations['AddressDetails']['Accuracy']
        self.clean_address = informations['address']   

        if self.precision <= 6:
            raise GeoFinderError('Your address is not available.')

    def geocompute(self, address):
        """Geocompute an address with GMap"""
        address = quote_plus(address)
        request = "http://maps.google.com/maps/geo?sensor=false&q=%s&output=%s&oe=utf8&gl=fr" % (
            address, 'json')
        data = json.loads(urlopen(request).read())
        
        if data['Status']['code'] != 200:
            raise GeoFinderError('Service unavailable')
        return data['Placemark'][0]


