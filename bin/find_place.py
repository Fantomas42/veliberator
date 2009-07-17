#!/usr/bin/python
import sys, os
from optparse import OptionParser

sys.path.append(os.path.abspath('.'))

from veliberator import Station
from veliberator.settings import DATABASE_URI
from veliberator.models import db_connection

def show_status(station):
    print "Station '%s'" % station.id
    print station.address
    print '%s/%s velo(s) disponible' % (station.status['available'], station.status['total'])
    print '%s place(s) disponible' % station.status['free']


if __name__ == '__main__':   
    parser = OptionParser(usage='usage: %prog station_id [options]')
    parser.add_option('-d', '--database', dest='database',
                      help='The SQLURI of the database', default=DATABASE_URI)
    parser.add_option('-p', '--place', dest='place', type='int',
                      help='The number of place you want', default=1)
    parser.add_option('-m', '--max_stations', dest='max_stations', type='int',
                      help='The maximun stations around proposed', default=4)
    (options, args) = parser.parse_args()
    
    db_connection(options.database)
    
    station = Station(args[0])
    station.get_status()
    show_status(station)
                        
    if not station.is_free(options.place):
        print 'Calcul des places les plus proches.'
        
        for station_id in station.get_stations_around(options.max_stations):
            station = Station(station_id)
            if station.is_free(options.place):
                print '----------'
                show_status(station)

