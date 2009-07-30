"""Unit tests for xml functions"""
import unittest
from xml.dom.minidom import parseString

from veliberator.xml_wrappers import xml_station_status_wrapper
from veliberator.xml_wrappers import xml_station_information_wrapper


class XmlFuncTestCase(unittest.TestCase):

    def test_XmlStationStatusWrapper(self):
        data_reference = {'total': 25, 'available': 23,
                          'free': 1, 'ticket': True}

        xml = parseString('<station>' \
                          '<available>23</available> <free>1</free>' \
                          '<total>25</total> <ticket>1</ticket>' \
                          '</station>')
        self.assertEquals(xml_station_status_wrapper(xml.firstChild), data_reference)

    def test_XmlStationInformationWrapper(self):
        data_reference = {'bonus': False, 'opened': True,
                          'postal_code': u'75020', 'city': u'PARIS', 
                          'address': u'69 RUE SAINT BLAISE',
                          'lat': u'48.8568139855',
                          'lng': u'2.40903293016',
                          'id': 20017}

        xml = parseString('<marker name="20017 - RUE SAINT BLAISE" number="20017" ' \
                          'address="69 RUE SAINT BLAISE -" ' \
                          'fullAddress="69 RUE SAINT BLAISE - 75020 PARIS" ' \
                          'lat="48.8568139855" lng="2.40903293016" open="1" bonus="0"/>')
        
        self.assertEquals(xml_station_information_wrapper(xml.firstChild), data_reference)

    def test_XmlStationInformationWrapperAdvanced(self):
        data_reference = {'bonus': False, 'opened': True,
                          'postal_code': u'94200', 'city': u'IVRY', 
                          'address': u'157-165 AVENUE DE VERDUN',
                          'lat': u'48.8067594749',
                          'lng': u'2.37550404031',
                          'id': 42009}

        xml = parseString('<marker name="42009 - VERDUN (IVRY)" number="42009" ' \
                          'address="157-165 AVENUE DE VERDUN -" ' \
                          'fullAddress="157-165 AVENUE DE VERDUN - 94200 IVRY" ' \
                          'lat="48.8067594749" lng="2.37550404031" open="1" bonus="0"/>')
        
        self.assertEquals(xml_station_information_wrapper(xml.firstChild), data_reference)


suite = unittest.TestLoader().loadTestsFromTestCase(XmlFuncTestCase)
