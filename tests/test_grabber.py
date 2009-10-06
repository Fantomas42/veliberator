"""Unit tests for Status object"""
import unittest

from veliberator.grabber import Grabber
from veliberator.settings import PROXY_SERVERS
from veliberator.settings import TEST_XML_URL_DATA_STATION

class GrabberTestCase(unittest.TestCase):

    def test_Init(self):
        grabber = Grabber(TEST_XML_URL_DATA_STATION)
        self.assertEquals(grabber.url, TEST_XML_URL_DATA_STATION)
        self.assertEquals(grabber.proxies, PROXY_SERVERS)

    def test_ContentAndCache(self):
        grabber = Grabber(TEST_XML_URL_DATA_STATION)
        self.assertEquals(grabber.data, None)
        self.assertEquals(grabber.page, None)

        content = grabber.content
        page = grabber.page
        self.assertNotEquals(grabber.data, None)
        self.assertNotEquals(grabber.page, None)
        self.assertEquals(grabber.data, content)
        #Normaly does not reload the page when reaccessing to content
        self.assertEquals(grabber.content, content)
        self.assertEquals(grabber.page, page)
        

suite = unittest.TestLoader().loadTestsFromTestCase(GrabberTestCase)
