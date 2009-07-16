"""Unit tests for PopChecker object"""
import unittest

from veliberator.popchecker import PopChecker

class PopCheckerTestCase(unittest.TestCase):

    def __test_ConfigPopChecker(self):
        pop_checker = PopChecker()
        pop_checker.authentificate()

    def __test_Authentificate(self):
        pop_checker = PopChecker('bla.gog', 45)
        pop_checker.authentificate()
        
        self.assertEquals(1, 1)

    

suite = unittest.TestLoader().loadTestsFromTestCase(PopCheckerTestCase)
