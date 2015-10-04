# -*- coding: utf-8 -*-

import unittest

def suite():
    return unittest.defaultTestLoader.discover(start_dir=".", pattern="*.py")


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )
 