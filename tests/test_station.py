"""Unit tests for Station object"""
import unittest

from veliberator.settings import TEST_XML_CARTOGRAPHY
from veliberator.station import UnknowStation, Station
from veliberator.models import StationInformation
from veliberator.cartography import Cartography

class StationTestCase(unittest.TestCase):

    def setUp(self):
        self.velib_id = 42008
        self.informations = StationInformation(id=self.velib_id,
                                               address='Test')
        self.informations.save()

    def tearDown(self):
        self.informations = None
        StationInformation.query.delete()

    def test_InformationsErrorRaising(self):
        self.assertRaises(UnknowStation, Station, 0)

    def test_InformationsNoError(self):
        station = Station(self.velib_id)
        self.assertTrue(isinstance(station.informations, StationInformation))
        station = Station(str(self.velib_id))
        self.assertTrue(isinstance(station.informations, StationInformation))
        

    def test_GetStatus(self):
        station = Station(self.velib_id)
        self.assertEquals(station.status, None)

        station.get_status()
        self.assertTrue(isinstance(station.status, dict))

    def test_ComputeDistances(self):
        station = Station(self.velib_id)
        result = station.compute_distances([station.informations])
        self.assertEquals(result, {})

        station.informations.lat = 1
        station.informations.lng = 1
        si = StationInformation(id=42, lat=4, lng=5)
        
        result = station.compute_distances([si])
        self.assertEquals(result, {si: 5.0})

    def test_GetStationsAround(self):
        Cartography.synchronize(TEST_XML_CARTOGRAPHY)
        
        station = Station(self.velib_id)

        stations_around = station.get_stations_around(1)
        self.assertEquals(len(stations_around), 1)

        stations_around = station.get_stations_around(5)
        self.assertEquals(len(stations_around), 5)
        self.assertEquals(stations_around, [42006, 42010, 42012, 42014, 42016])

        Cartography.flush()


suite = unittest.TestLoader().loadTestsFromTestCase(StationTestCase)
