"""
Veliberator script
"""
import os
import sys
import gettext
from optparse import OptionParser

import sqlalchemy

import veliberator
from veliberator.station import Station
from veliberator.station import UnknowStation
from veliberator.cartography import Cartography
from veliberator.models import db_connection
from veliberator.settings import DATABASE_URI
from veliberator.settings import STATION_AROUND_RADIUS
from veliberator.geofinder import GeoFinderError
from veliberator.geofinder import AddressGeoFinder
from veliberator.models import StationInformation


translation = gettext.translation(
    'veliberator',
    os.path.join(os.path.dirname(veliberator.__file__), 'locale'))
_ = translation.gettext
__ = translation.ngettext


def synchronization():
    print _('-> Online synchronization...')
    Cartography.synchronize()
    print _('-> Synchronization complete !')


def show_status(station, distance=None):
    print _("Station '%s'") % station.id
    if distance:
        print _('%(address)s (%(distance).2fm)') % {
            'address': station.informations.full_address,
            'distance': distance}
    else:
        print station.informations.full_address

    print __('%(available)s/%(total)s bike available',
             '%(available)s/%(total)s bikes available',
             station.status.available) % {
        'available': station.status.available,
        'total': station.status.total}
    print __('%s parking place', '%s parking places',
             station.status.free) % station.status.free


def display_free_stations(stations, places, max_display):
    displayed = 0

    for station_information in stations:
        if displayed == max_display:
            break
        station = Station(station_information.id)
        if station.is_free(places):
            print '----------'
            show_status(station, station_information.distance)
            displayed += 1


class VeliberatorOptionParser(OptionParser):
    """Customized OptionParser with
    correct gettext handling"""

    def _add_help_option(self):
        self.add_option('-h', '--help', action='help',
                        help=_('Show this help message and exit'))

    def _add_version_option(self):
        self.add_option('--version', action='version',
                        help=_("Show program's version number and exit"))

    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        file.write(self.format_help())


def cmdline():
    parser = VeliberatorOptionParser(
        usage=_('%prog [station_id] [address] [options]'),
        version='%s %s' % ('%prog', veliberator.__version__))
    parser.add_option('-d', '--database', dest='database',
                      help=_('The SQLURI of the database'),
                      default=DATABASE_URI)
    parser.add_option('-p', '--places', dest='places', type='int',
                      help=_('The number of places you want'), default=1)
    parser.add_option('-m', '--max-stations', dest='max_stations', type='int',
                      help=_('The maximun stations around proposed'),
                      default=5)
    parser.add_option('--synchronize', dest='synchronize', action='store_true',
                      help=_('Only do a synchronization of the cartography'))
    (options, args) = parser.parse_args()

    print '-==* Veliberator v%s *==-' % veliberator.__version__

    try:
        db_connection(options.database)
    except sqlalchemy.exc.OperationalError:
        if options.synchronize:
            sys.exit(_('-> The database %s is unreachable.') %
                     options.database)
        else:
            print _('-> The database is unreachable, switch on RAM.')
            print _('-> Edit the configuration file, '
                    'for removing this message.')
            db_connection('sqlite://')

    if options.synchronize:
        synchronization()
        sys.exit(0)

    if not StationInformation.query.count():
        synchronization()

    if args:
        user_input = args[0]
    else:
        user_input = raw_input(_('Station ID or complete address:\n'))

    if user_input.isdigit():
        try:
            station = Station(user_input)
        except UnknowStation:
            sys.exit(_('The Station ID does not exist.'))
        show_status(station)
        if not station.is_free(options.places):
            print _('Searching on the closest stations...')
            display_free_stations(station.stations_around,
                                  options.places, options.max_stations)
    else:
        try:
            finder = AddressGeoFinder(user_input)
        except GeoFinderError:
            sys.exit(_('The provided address is not valid or imprecise.'))
        display_free_stations(
            finder.get_stations_around(STATION_AROUND_RADIUS),
            options.places, options.max_stations)
