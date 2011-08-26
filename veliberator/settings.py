"""Settings for Veliberator"""
import os
from ConfigParser import SafeConfigParser

config = SafeConfigParser()

config_read = config.read([os.path.expanduser('~/.veliberator.cfg'),
                           os.path.join(os.getcwd(), 'etc/veliberator.cfg')])

XML_URL_DATA_STATION = config.get('XML', 'url_data_station')
XML_URL_STATUS_STATION = config.get('XML', 'url_status_station')

STATION_STATUS_RECENT = config.getint('STATION', 'status_recent')
STATION_ALMOST_FULL = config.getint('STATION', 'almost_full')
STATION_ALMOST_EMPTY = config.getint('STATION', 'almost_empty')

DATABASE_URI = config.get('DATABASE', 'uri')
DATABASE_ECHO = config.getboolean('DATABASE', 'echo')

TEST_XML_URL_DATA_STATION = config.get('TEST', 'url_data_station')

PROXY_SERVERS = config.get('PROXY', 'servers')
PROXY_SERVERS = PROXY_SERVERS and PROXY_SERVERS.split(';') or []
