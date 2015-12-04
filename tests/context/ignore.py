#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

import unittest

from config.context import Group
from config.context import Ignore

class IgnoreTestCase(unittest.TestCase):

    def setUp(self):
        self.int1 = 0
        self.int2 = 0
        self.grp= Group( { None      : Ignore() } )
        

    def test_contextInterface(self):
        ctx=self.grp.getContext(u"section")
        ctx.enter()
        ctx2= ctx.getContext(u"session2")
        ctx2.enter()
        ctx2.addContent(u"something")
        ctx2.leave()
        ctx.leave()
        
        
def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(IgnoreTestCase)


if __name__ == u'__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )