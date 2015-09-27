# -*- coding: utf-8 -*-

import unittest
from context import suite as contextSuite
from dispatcher import suite as dispatcherSuite
from xml_reader import suite as xmlReaderSuite
from default_reader import suite as defaultReaderSuite
from ini_reader import suite as iniReaderSuite
from default_writer import suite as defaultWriterSuite

def suite():
    return unittest.TestSuite([ contextSuite(),
                                dispatcherSuite(),
                                xmlReaderSuite(),
                                defaultReaderSuite(),
                                iniReaderSuite(),
                                defaultWriterSuite() ])


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )
