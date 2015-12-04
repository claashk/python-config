#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

from unittest import defaultTestLoader, TextTestRunner
import os

def suite():
    currentDir= os.path.dirname(__file__)
    topDir= os.path.dirname( os.path.join(currentDir, u"..") )
    return defaultTestLoader.discover( start_dir=currentDir,
                                       pattern=u"*.py",
                                       top_level_dir=topDir )


if __name__ == u'__main__':
    TextTestRunner(verbosity=2).run( suite() )
 