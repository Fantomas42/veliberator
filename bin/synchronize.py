#!/usr/bin/python
import sys, os

sys.path.append(os.path.abspath('.'))

from veliberator.models import db_connection
from veliberator.cartography import Cartography

if __name__ == '__main__':
    db_connection()
    print 'Database open, now synchronizing...'
    Cartography.synchronize()
    print 'Synchronization completed !'
    

    
    
    
