"""Unit tests for GeoFinder objects"""
import unittest

from veliberator.station import Station
from veliberator.geofinder import global_geofinder_cache
from veliberator.geofinder import BaseGeoFinder
from veliberator.geofinder import StationGeoFinder
from veliberator.geofinder import AddressGeoFinder
from veliberator.geofinder import pythagor_distance
from veliberator.models import StationInformation
from veliberator.cartography import Cartography
from veliberator.settings import TEST_XML_URL_DATA_STATION

STATION_AROUND_RADIUS = 1200


class BaseGeoFinderTestCase(unittest.TestCase):

    def test_ComputeSquareArea(self):
        finder = BaseGeoFinder(1, 1)
        self.assertEquals(finder.compute_square_area(STATION_AROUND_RADIUS),
                          ((0.98922021659056569, 1.0, 1.0107797834094343),
                           (0.98922021659056569, 1.0, 1.0107797834094343)))
        finder.lat = '1'
        finder.lng = '1'
        self.assertEquals(finder.compute_square_area(STATION_AROUND_RADIUS),
                          ((0.98922021659056569, 1.0, 1.0107797834094343),
                           (0.98922021659056569, 1.0, 1.0107797834094343)))
        finder.lat = 4.897645
        finder.lng = 18.798923
        self.assertEquals(finder.compute_square_area(STATION_AROUND_RADIUS),
                          ((4.8868652165905653,
                            4.8976449999999998,
                            4.9084247834094343),
                           (18.788143216590566,
                            18.798922999999998,
                            18.809702783409431)))

    def test_ComputeStationDistances(self):
        finder = BaseGeoFinder(1, 1)

        si1 = StationInformation(id=42, lat=1, lng=1)
        result = finder.compute_station_distances([si1])
        self.assertEquals(result, [])

        si2 = StationInformation(id=43, lat=4, lng=5)
        result = finder.compute_station_distances([si2])
        self.assertEquals(result, [si2])

        self.assertEquals(result[0].distance, 556217.45145026874)
        result = finder.compute_station_distances([si2], pythagor_distance)
        self.assertEquals(result[0].distance, 556597.45396636787)

        si3 = StationInformation(id=44, lat=8, lng=10)
        si4 = StationInformation(id=45, lat=6, lng=5.5)
        result = finder.compute_station_distances([si1, si2, si3, si4])
        self.assertEquals(len(result), 3)

        StationInformation.query.delete()

    def test_GetStationsInArea(self):
        test_1 = (('4.89', '4.90', '4.91'), ('18.79', '18.80', '18.81'))
        test_2 = (('48.80', '48.81', '48.82'), ('2.37', '2.38', '2.39'))

        Cartography.synchronize(TEST_XML_URL_DATA_STATION)
        finder = BaseGeoFinder(1, 1)

        self.assertEquals(len(finder.get_stations_in_area(*test_1)), 0)
        self.assertEquals(len(finder.get_stations_in_area(*test_2)), 8)

        Cartography.flush()

    def test_GetStationsAround(self):
        Cartography.synchronize(TEST_XML_URL_DATA_STATION)

        finder = BaseGeoFinder(1, 1)
        self.assertEquals(len(finder.get_stations_around(
            STATION_AROUND_RADIUS)), 0)

        finder.lat = 48.81
        finder.lng = 2.38
        self.assertEquals(
            [station.id for station in
             finder.get_stations_around(STATION_AROUND_RADIUS)],
            [42012, 42010, 42009, 42008, 42016, 42006, 42007, 42015])

        Cartography.flush()

    def test_Cache(self):
        key = (1, 1, STATION_AROUND_RADIUS)
        self.assertFalse(key in global_geofinder_cache)
        finder = BaseGeoFinder(key[0], key[1])
        finder.get_stations_around(key[2])
        self.assertTrue(key in global_geofinder_cache)


class StationGeoFinderTestCase(unittest.TestCase):

    def test_Init(self):
        Cartography.synchronize(TEST_XML_URL_DATA_STATION)

        station = Station(42008)
        geofinder = StationGeoFinder(station)
        self.assertEquals(geofinder.lat, station.informations.lat)
        self.assertEquals(geofinder.lng, station.informations.lng)

        Cartography.flush()


class AddressGeoFinderTestCase(unittest.TestCase):

    def test_Init(self):
        address = '1 place de la Bastille, 75012 Paris'
        geofinder = AddressGeoFinder(address)
        self.assertEquals(geofinder.precision, 'street_address')
        self.assertEquals(geofinder.lat, 48.8530318)
        self.assertEquals(geofinder.lng, 2.3687204)

    def test_GeoCompute(self):
        address = '1 place de la Bastille, 75012 Paris'
        geofinder = AddressGeoFinder(address)
        self.assertEquals(len(geofinder.geocompute(address)), 6)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(BaseGeoFinderTestCase),
    unittest.TestLoader().loadTestsFromTestCase(StationGeoFinderTestCase),
    unittest.TestLoader().loadTestsFromTestCase(AddressGeoFinderTestCase)])
