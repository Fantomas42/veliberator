#!/usr/bin/python
import sys, os

sys.path.append(os.path.abspath('.'))

from veliberator.station import Station
from veliberator.models import db_connection

if __name__ == '__main__':
    db_connection()
    station = Station(sys.argv[1])
    station.show_status()
                        
    if not station.status['free']:
        print 'Pas de places disponibles...'
        print 'Calcul des places les plus proches.'
        
        for station_id in station.get_stations_around(3):
            station = Station(station_id)
            station.get_status()
            if station.status['free']:
                print '----------'
                station.show_status()
    
