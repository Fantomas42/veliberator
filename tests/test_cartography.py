"""Unit tests for Cartography object"""
import unittest

from veliberator.settings import TEST_XML_CARTOGRAPHY
from veliberator.cartography import Cartography
from veliberator.models import StationInformation

class CartographyTestCase(unittest.TestCase):

    def test_SynchronizeFlush(self):
        self.assertEquals(StationInformation.query.count(), 0)

        Cartography.synchronize(TEST_XML_CARTOGRAPHY)
        self.assertEquals(StationInformation.query.count(), 112)

        Cartography.flush()
        self.assertEquals(StationInformation.query.count(), 0)

    
suite = unittest.TestLoader().loadTestsFromTestCase(CartographyTestCase)
