"""Unit tests for Station object"""
import unittest

from veliberator.settings import TEST_XML_URL_DATA_STATION
from veliberator.station import UnknowStation, Station
from veliberator.models import StationInformation
from veliberator import Cartography

from veliberator.station import STATUS_OPEN, STATUS_CLOSE, STATUS_BONUS, \
     STATUS_ERROR, STATUS_BIKE_ONLY, STATUS_PARKING_ONLY, STATUS_NO_SERVICE

class StationTestCase(unittest.TestCase):

    def setUp(self):
        self.velib_id = 42008
        self.informations = StationInformation(id=self.velib_id,
                                               address='Test',
                                               bonus=True, opened=True)
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

    def test_Properties(self):
        station = Station(self.velib_id)
        self.assertTrue(station.is_open == station.informations.opened)
        self.assertTrue(station.is_bonus == station.informations.bonus)

    def test_IsFree(self):
        station = Station(self.velib_id)
        station.status.status['free'] = 5
        self.assertTrue(station.is_free())
        self.assertTrue(station.is_free(4))
        self.assertFalse(station.is_free(7))

    def test_IsAvailable(self):
        station = Station(self.velib_id)
        station.status.status['available'] = 5
        self.assertTrue(station.is_available())
        self.assertTrue(station.is_available(4))
        self.assertFalse(station.is_available(7))

    def test_GetStationsAround(self):
        Cartography.synchronize(TEST_XML_URL_DATA_STATION)
        
        station = Station(self.velib_id)

        stations_around = station.stations_around
        self.assertEquals(len(stations_around), 7)

        Cartography.flush()

    def test_State(self):
        status = {'total': 25, 'available': 0,
                  'free': 12, 'ticket': True}

        station = Station(self.velib_id)
        station.status.status = status

        self.assertEquals(station.state, STATUS_PARKING_ONLY)
        station.status.status['free'] = 0
        station.status.status['available'] = 2
        self.assertEquals(station.state, STATUS_BIKE_ONLY)
        station.status.status['available'] = 0
        self.assertEquals(station.state, STATUS_NO_SERVICE)
        station.status.status['total'] = 0
        self.assertEquals(station.state, STATUS_ERROR)
        station.status.status['total'] = station.status.status['free'] = \
                                         station.status.status['available'] = 10
        
        self.assertEquals(station.state, STATUS_BONUS)
        station.informations.bonus = False
        self.assertEquals(station.state, STATUS_OPEN)
        station.informations.opened = False
        self.assertEquals(station.state, STATUS_CLOSE)

        
suite = unittest.TestLoader().loadTestsFromTestCase(StationTestCase)
