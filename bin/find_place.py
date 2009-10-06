#!/usr/bin/python
import sys, os
from optparse import OptionParser

sys.path.append(os.path.abspath('.'))

from veliberator import Station
from veliberator.models import db_connection
from veliberator.settings import DATABASE_URI
from veliberator.geofinder import GeoFinderError
from veliberator.geofinder import AddressGeoFinder

def show_status(station):
    print "Station '%s'" % station.id
    print station.informations.full_address
    print '%s/%s velo(s) disponible' % (station.status.available, station.status.total)
    print '%s place(s) disponible' % station.status.free

def display_free_stations(stations, places):
    for station_id in stations:
        station = Station(station_id)
        if station.is_free(places):
            print '----------'
            show_status(station)
        

if __name__ == '__main__':   
    parser = OptionParser(usage='usage: %prog [station_id] [options]')
    parser.add_option('-d', '--database', dest='database',
                      help='The SQLURI of the database', default=DATABASE_URI)
    parser.add_option('-p', '--places', dest='places', type='int',
                      help='The number of places you want', default=1)
    parser.add_option('-m', '--max_stations', dest='max_stations', type='int',
                      help='The maximun stations around proposed', default=4)
    (options, args) = parser.parse_args()
    
    db_connection(options.database)
    
    if args:
        user_input = args[0]
    else:
        user_input = raw_input('Identifiant de la station, ou adresse complete :\n')

    if user_input.isdigit():
        station = Station(user_input)
        show_status(station)
        if not station.is_free(options.places):
            print 'Calcul des places les plus proches...'
            display_free_stations(station.stations_around[:options.max_stations],
                                  options.places)
    else:
        try:
            finder = AddressGeoFinder(user_input)
        except GeoFinderError:
            sys.exit('Votre addresse n\'est pas valide ou imprecise.')
        display_free_stations(finder.get_stations_around()[:options.max_stations],
                              options.places)
