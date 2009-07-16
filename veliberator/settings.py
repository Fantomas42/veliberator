"""Settings for Veliberator"""

MAIL_SSL = True
MAIL_PORT = MAIL_SSL and 995 or 110
MAIL_SERVER = 'pop.gmail.com'
MAIL_ADDRESS = 'fantomas42@gmail.com'
MAIL_ACCOUNT = MAIL_ADDRESS
MAIL_PASSWORD = '.4il1>Y$'

VELIB_DATA_XML_URL = 'http://www.velib.paris.fr/service/carto'
VELIB_STATUS_XML_URL = 'http://www.velib.paris.fr/service/stationdetails/%s'

DATABASE_URI = 'sqlite:///db.sqlite'
DATABASE_ECHO = False

TEST_XML_CARTOGRAPHY = 'tests/data/carto_short.xml'
