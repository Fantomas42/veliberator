"""Global suite of tests"""
import unittest

from veliberator.models import db_connection

from tests.test_popchecker import suite as popchecker_suite
from tests.test_models import suite as models_suite
from tests.test_xml_wrappers import suite as xml_suite
from tests.test_station import suite as station_suite
from tests.test_cartography import suite as cartography_suite

db_connection('sqlite:///:memory:')

global_test_suite = unittest.TestSuite([popchecker_suite,
                                        models_suite,
                                        xml_suite,
                                        station_suite,
                                        cartography_suite,])


