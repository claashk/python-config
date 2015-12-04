#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

import unittest
from config.context import Map
from config.context import Value
from config.context import List


class MapTestCase(unittest.TestCase):

    def setUp(self):
        self.bool= True
        self.list= []

        self.boolCtx= Value( self,
                             u"bool",
                             Map({u'Yes' : True, u'No' : False}),
                             maxCount=2 )
                            
        self.listCtx= List( self,
                            u"list",
                            Map({u'On' : True, u'Off' : False}),
                            maxCount=3) 
        
       
    def test_construction(self):
        self.assertEqual(self.boolCtx.count, 0)
        self.assertEqual(self.listCtx.count, 0)
        self.assertRaises(ValueError, Map, {5: True})
                      
    
    def test_parse(self):
        self.boolCtx.enter()
        self.boolCtx.addContent(u"No")
        self.boolCtx.leave()
        
        self.boolCtx.enter()
        self.boolCtx.addContent(u"no")
        self.assertRaises(KeyError, self.boolCtx.leave)
        
        self.listCtx.enter()        
        self.listCtx.addContent(u"On")
        self.listCtx.leave()
        
        self.listCtx.enter()
        self.listCtx.addContent(u"Off")
        self.listCtx.leave()
        
        self.assertEqual(self.bool, False)
        self.assertEqual(self.list, [True, False])
        self.assertEqual(self.boolCtx.count, 2)
        self.assertEqual(self.listCtx.count, 2)

        
    def test_contextInterface(self):
        self.assertRaises(NotImplementedError, self.boolCtx.getContext, u"ctx")
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(MapTestCase)


if __name__ == u'__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )