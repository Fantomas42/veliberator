#!/usr/bin/python
import sys, os
import unittest

sys.path.append(os.path.abspath('.'))

from tests import global_test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(global_test_suite)
    
