#!/usr/bin/python
import sys, os
import unittest

sys.path.append(os.path.abspath('.'))

from veliberator.models import db_connection

from tests import global_test_suite

if __name__ == '__main__':
    db_connection('sqlite:///:memory:')
    unittest.TextTestRunner(verbosity=2).run(global_test_suite)
    
