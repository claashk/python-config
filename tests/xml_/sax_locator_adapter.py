# -*- coding: utf-8 -*-
import unittest
from schema.xml import SaxLocatorAdapter

class SaxLocatorProxy(object):
    
    def __init__(self, line=0, column=0):
        self.line= line
        self.column= column

        
    def getColumnNumber(self):
        return self.column


    def getLineNumber(self):
        return self.line
        


class SaxLocatorAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.saxLocator= SaxLocatorProxy()
        self.locator= SaxLocatorAdapter(self.saxLocator)

                                                  
    def test_line(self):
        self.assertEqual(0, self.locator.line)

        for line in range(0, 100):
            self.saxLocator.line= line
            self.assertEqual(line, self.locator.line)


    def test_column(self):
        self.assertEqual(0, self.locator.column)

        for col in range(1000, 1100):
            self.saxLocator.column= col
            self.assertEqual(col, self.locator.column)


def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(SaxLocatorAdapterTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )