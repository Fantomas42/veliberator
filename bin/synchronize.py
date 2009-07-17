#!/usr/bin/python
import sys, os
from optparse import OptionParser

sys.path.append(os.path.abspath('.'))

from veliberator import Cartography
from veliberator.models import db_connection
from veliberator.settings import DATABASE_URI

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-d', '--database', dest='database',
                      help='The SQLURI of the database', default=DATABASE_URI,
                      metavar='DATABASE')
    (options, args) = parser.parse_args()
    
    db_connection(options.database)
    print 'Database open, now synchronizing...'
    Cartography.synchronize()
    print 'Synchronization completed !'
    

    
    
    
