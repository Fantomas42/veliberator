"""Station objects for veliberator"""
from xml.dom.minidom import parse

from veliberator.models import db_connection
from veliberator.models import StationInformation
from veliberator.status import StationStatus
from veliberator.geofinder import StationGeoFinder
from veliberator.settings import STATION_ALMOST_FULL
from veliberator.settings import STATION_ALMOST_EMPTY

STATUS_OPEN = u'open'
STATUS_CLOSE = u'close'
STATUS_BONUS = u'bonus'
STATUS_ERROR = u'api-error'
STATUS_BIKE_ONLY = u'bike-only'
STATUS_PARKING_ONLY = u'parking-only'
STATUS_ALMOST_FULL = u'almost-full'
STATUS_ALMOST_EMPTY = u'almost-empty'
STATUS_NO_SERVICE = u'no-service'

class UnknowStation(Exception):
    pass

class Station(object):
    """Station object,
    combinating informations and status"""

    def __init__(self, velib_id):
        self.id = int(velib_id)
        self.informations = self.acquire_informations()

        if not self.informations:
            raise UnknowStation('The Station ID does not exist.')

        self.status = StationStatus(self.id)
        self.finder = StationGeoFinder(self)

    def acquire_informations(self):
        """Default method for acquiring informations
        of a stations, by connecting to the database"""
        try:
            return StationInformation.get(self.id)
        except AttributeError:
            db_connection()
            return StationInformation.get(self.id)

    @property
    def is_open(self):
        """Property telling if the station is open"""
        return self.informations.opened

    @property
    def is_bonus(self):
        """Property telling if the station is bonus"""
        return self.informations.bonus

    def is_free(self, places=1):
        """Method property if the station
        has free places"""
        return self.is_open and self.status.free >= places

    def is_available(self, places=1):
        """Method property if the station
        has available places"""
        return self.is_open and self.status.available >= places

    @property
    def stations_around(self):
        """Find the stations around"""
        return self.finder.get_stations_around()

    @property
    def state(self):
        """Return the status for the station"""
        if not self.is_open:
            return STATUS_CLOSE

        free = self.status.free
        available = self.status.available
        total =  self.status.total

        if not available and not free:
            if not total:
                return STATUS_ERROR
            return STATUS_NO_SERVICE
        elif available and not free:
            return STATUS_BIKE_ONLY
        elif not available and free:
            return STATUS_PARKING_ONLY
        elif STATION_ALMOST_FULL >= free:
            return STATUS_ALMOST_FULL
        elif STATION_ALMOST_EMPTY >= available:
            return STATUS_ALMOST_EMPTY
        elif self.is_bonus:
            return STATUS_BONUS
        return STATUS_OPEN

    def __repr__(self):
        if self.informations:
            return '<Station "%s" (%s)>' % (self.id, self.informations.address)
        return '<Station "%s">' % self.id


