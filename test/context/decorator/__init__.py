# -*- coding: utf-8 -*-

import unittest
from .help import suite as helpSuite

def suite():
    return unittest.TestSuite([ helpSuite() ])


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )
 