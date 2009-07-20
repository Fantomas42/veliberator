"""Objects for helping filling data"""
from urllib import urlopen
from xml.dom.minidom import parse

from veliberator.settings import XML_URL_DATA_STATION
from veliberator.xml_wrappers import xml_station_information_wrapper
from veliberator.models import StationInformation, session


class Cartography(object):
    """Grab the data and save it in db"""

    @staticmethod
    def synchronize(url=XML_URL_DATA_STATION):
        dom = parse(urlopen(url))
        for marker in dom.getElementsByTagName('marker'):
            values = xml_station_information_wrapper(marker)
            station = StationInformation.update_or_create(values, surrogate=False)

        session.commit()

    @staticmethod
    def flush():
        StationInformation.query.delete()

