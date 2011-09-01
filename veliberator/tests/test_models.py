"""Unit tests for models object"""
import unittest

from veliberator.models import StationInformation


class StationInformationTestCase(unittest.TestCase):

    def tearDown(self):
        StationInformation.query.delete()

    def test_UpdateOrCreate(self):
        self.assertEquals(StationInformation.query.count(), 0)

        values = {'id': 42,
                  'address': '1 rue Kennedy',
                  'postal_code': '94200',
                  'city': 'Paris',
                  'lat': '42.000000000',
                  'lng': '42.000000000',
                  'opened': True,
                  'bonus': False}
        station = StationInformation.update_or_create(values, surrogate=False)
        self.assertEquals(StationInformation.query.count(), 1)
        self.assertEquals(station.postal_code, '94200')

        values['postal_code'] = '75000'
        station = StationInformation.update_or_create(values, surrogate=False)
        self.assertEquals(StationInformation.query.count(), 1)
        self.assertEquals(station.postal_code, '75000')

        values['id'] = 43
        station = StationInformation.update_or_create(values, surrogate=False)
        self.assertEquals(StationInformation.query.count(), 2)
        self.assertEquals(station.postal_code, '75000')

    def test_FullAddress(self):
        values = {'id': 42,
                  'address': '1 rue Kennedy',
                  'postal_code': '94200',
                  'city': 'Paris',
                  'lat': '42.000000000',
                  'lng': '42.000000000',
                  'opened': True,
                  'bonus': False}
        station = StationInformation.update_or_create(values, surrogate=False)
        self.assertEquals(station.full_address, '1 rue Kennedy, 94200 Paris')

    def test_repr(self):
        values = {'id': 42,
                  'address': '1 rue Kennedy',
                  'postal_code': '94200',
                  'city': 'Paris',
                  'lat': '42.000000000',
                  'lng': '42.000000000',
                  'opened': True,
                  'bonus': False}
        station = StationInformation.update_or_create(values, surrogate=False)
        self.assertEquals(repr(station),
                          '<StationInformation "42" (1 rue Kennedy)>')


suite = unittest.TestLoader().loadTestsFromTestCase(StationInformationTestCase)
