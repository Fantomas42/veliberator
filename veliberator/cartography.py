"""Objects for helping filling data"""
from xml.dom.minidom import parseString

from veliberator.grabber import Grabber
from veliberator.settings import XML_URL_DATA_STATION
from veliberator.xml_wrappers import xml_station_information_wrapper
from veliberator.models import StationInformation, session


class Cartography(object):
    """Grab the data and save it in db"""

    @staticmethod
    def synchronize(url=XML_URL_DATA_STATION):        
        dom = parseString(Grabber(url).content)
        for marker in dom.getElementsByTagName('marker'):
            values = xml_station_information_wrapper(marker)
            station = StationInformation.update_or_create(values, surrogate=False)

        session.commit()

    @staticmethod
    def flush():
        StationInformation.query.delete()

