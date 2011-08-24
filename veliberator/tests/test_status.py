"""Unit tests for Status object"""
import unittest
from datetime import datetime, timedelta

from veliberator.status import StationStatus
from veliberator.status import global_stationstatus_cache
from veliberator.settings import STATION_STATUS_RECENT

class StationStatusTestCase(unittest.TestCase):

    def setUp(self):
        self.velib_id = 42008

    def tearDown(self):
        global global_stationstatus_cache
        global_stationstatus_cache = {}

    def test_Init(self):
        status = StationStatus(self.velib_id)
        self.assertTrue(isinstance(status.ticket, bool))
        self.assertTrue(isinstance(status.total, int))
        self.assertTrue(isinstance(status.available, int))
        self.assertTrue(isinstance(status.free, int))
        self.assertTrue(isinstance(status.closed, int))

    def test_Cache(self):
        global global_stationstatus_cache
        
        status = StationStatus(self.velib_id)
        data_compare = global_stationstatus_cache[self.velib_id].copy()
        status.get_status()
        self.assertEquals(status.status, data_compare)
        global_stationstatus_cache[self.velib_id][\
            'datetime'] = datetime.now() - timedelta(minutes=STATION_STATUS_RECENT + 5)
        status.get_status()
        self.assertNotEquals(status.status, data_compare)

    def test_GetStatus(self):
        status = StationStatus(self.velib_id)
        self.assertTrue(isinstance(status.get_status(), dict))

    def test_GetStatusError(self):
        status = StationStatus(self.velib_id - 1, 'http://example.com/badurl')
        self.assertTrue(isinstance(status.get_status(), dict))
        self.assertEquals(status.free, 0)

suite = unittest.TestLoader().loadTestsFromTestCase(StationStatusTestCase)

    
