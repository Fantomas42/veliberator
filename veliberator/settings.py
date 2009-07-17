"""Settings for Veliberator"""

VELIB_DATA_XML_URL = 'http://www.velib.paris.fr/service/carto'
VELIB_STATUS_XML_URL = 'http://www.velib.paris.fr/service/stationdetails/%s'

STATION_STATUS_RECENT = 10

DATABASE_URI = 'sqlite:///db.sqlite'
DATABASE_ECHO = False

TEST_XML_CARTOGRAPHY = 'tests/data/carto_short.xml'
