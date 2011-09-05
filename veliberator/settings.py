"""Settings for Veliberator"""
import os
from ConfigParser import SafeConfigParser

XML_SECTION = 'XML'
STATION_SECTION = 'STATION'
DATABASE_SECTION = 'DATABASE'
PROXY_SECTION = 'PROXY'

ALL_SECTIONS = [XML_SECTION, STATION_SECTION,
                DATABASE_SECTION, PROXY_SECTION]

DEFAULT_CONFIG = {
    'url_data_station': 'http://www.velib.paris.fr/service/carto',
    'url_status_station': 'http://www.velib.paris.fr/service/stationdetails/',
    'around_radius': '1200',
    'status_recent': '10',
    'almost_full': '3',
    'almost_empty': '3',
    'uri': 'sqlite:///~/.veliberator.db',
    'echo': 'False',
    'servers': ''}

config = SafeConfigParser(DEFAULT_CONFIG)

for section in ALL_SECTIONS:
    config.add_section(section)

config_read = config.read([os.path.expanduser('~/.veliberator.cfg'),
                           os.path.join(os.getcwd(), 'etc/veliberator.cfg')])

XML_URL_DATA_STATION = config.get(XML_SECTION, 'url_data_station')
XML_URL_STATUS_STATION = config.get(XML_SECTION, 'url_status_station')

STATION_AROUND_RADIUS = config.getint(STATION_SECTION, 'around_radius')
STATION_STATUS_RECENT = config.getint(STATION_SECTION, 'status_recent')
STATION_ALMOST_FULL = config.getint(STATION_SECTION, 'almost_full')
STATION_ALMOST_EMPTY = config.getint(STATION_SECTION, 'almost_empty')

DATABASE_URI = config.get(DATABASE_SECTION, 'uri')
if '~' in DATABASE_URI:
    protocol, source = DATABASE_URI.split('~')
    DATABASE_URI = '%s%s' % (protocol, os.path.expanduser('~' + source))

DATABASE_ECHO = config.getboolean(DATABASE_SECTION, 'echo')

PROXY_SERVERS = config.get(PROXY_SECTION, 'servers')
PROXY_SERVERS = PROXY_SERVERS and PROXY_SERVERS.split(';') or []

TEST_XML_URL_DATA_STATION = 'file:%s' % os.path.join(
    os.path.dirname(__file__), 'tests', 'data', 'carto_short.xml')
