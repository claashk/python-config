# -*- coding: utf-8 -*-

import unittest

from .value import suite as valueSuite
from .list import suite as listSuite
from .map import suite as mapSuite
from .group import suite as groupSuite
from .ignore import suite as ignoreSuite
from .decorator import suite as decoratorSuite

def suite():
    return unittest.TestSuite([ valueSuite(),
                                listSuite(),
                                mapSuite(),
                                groupSuite(),
                                ignoreSuite(),
                                decoratorSuite() ])


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )
 