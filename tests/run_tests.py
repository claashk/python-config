#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import TextTestRunner, defaultTestLoader
import os, sys

def suite():
    testRoot= os.path.abspath( os.path.dirname(__file__) )
    libDir= os.path.dirname(testRoot)
    
    if libDir not in sys.path:
        sys.path.insert(0, libDir)

    return defaultTestLoader.discover(start_dir=testRoot, pattern="*.py")

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run( suite() )
