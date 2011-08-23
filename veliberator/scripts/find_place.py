#!/usr/bin/python
import sys, os
from optparse import OptionParser

import sqlalchemy

sys.path.append(os.path.abspath('.'))

from veliberator import VERSION
from veliberator.station import Station
from veliberator.cartography import Cartography
from veliberator.models import db_connection
from veliberator.settings import DATABASE_URI
from veliberator.geofinder import GeoFinderError
from veliberator.geofinder import AddressGeoFinder
from veliberator.models import StationInformation

def check_database_content():
    if not StationInformation.query.count():
        print '-> Synchronisation en ligne...'
        Cartography.synchronize()
        print '-> Synchronisation complete !'

def show_status(station, distance=None):
    print "Station '%s'" % station.id
    if distance:
        print '%s (%.2fm)' % (station.informations.full_address, distance)
    else:
        print station.informations.full_address
    print '%s/%s velo(s) disponible' % (station.status.available, station.status.total)
    print '%s place(s) disponible' % station.status.free

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
    

if __name__ == '__main__':   
    parser = OptionParser(usage='usage: %prog [station_id] [options]')
    parser.add_option('-d', '--database', dest='database',
                      help='The SQLURI of the database', default=DATABASE_URI)
    parser.add_option('-p', '--places', dest='places', type='int',
                      help='The number of places you want', default=1)
    parser.add_option('-m', '--max_stations', dest='max_stations', type='int',
                      help='The maximun stations around proposed', default=5)
    (options, args) = parser.parse_args()

    print '-==* Veliberator Find Place v%s *==-' % VERSION

    try:
        db_connection(options.database)
    except sqlalchemy.exc.OperationalError:
        print '-> Database innacessible, switch sur la RAM.'
        print '-> Modifiez le fichier de configuration, pour enlever ce message.'
        db_connection('sqlite://')

    check_database_content()
    
    if args:
        user_input = args[0]
    else:
        user_input = raw_input('Identifiant de la station, ou adresse complete :\n')

    if user_input.isdigit():
        station = Station(user_input)
        show_status(station)
        if not station.is_free(options.places):
            print 'Calcul des places les plus proches...'
            display_free_stations(station.stations_around,
                                  options.places, options.max_stations)
    else:
        try:
            finder = AddressGeoFinder(user_input)            
        except GeoFinderError:
            sys.exit('Votre addresse n\'est pas valide ou imprecise.')
        display_free_stations(finder.get_stations_around(),
                              options.places, options.max_stations)
