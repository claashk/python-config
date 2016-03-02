# -*- coding: utf-8 -*-
import unittest
from config.context import Map
from config.context import Value
from config.context import MultiValue


class MapTestCase(unittest.TestCase):

    def setUp(self):
        self.bool= True
        self.list= []

        self.boolCtx= Value( self,
                             "bool",
                             Map({'Yes' : True, 'No' : False}),
                             maxCount=2 )
                            
        self.listCtx= MultiValue( self,
                                 "list",
                                 Map({'On' : True, 'Off' : False}),
                                 maxCount=3) 
        
       
    def test_construction(self):
        self.assertEqual(self.boolCtx.count, 0)
        self.assertEqual(self.listCtx.count, 0)
        self.assertRaises(ValueError, Map, {5: True})
                      
    
    def test_parse(self):
        self.boolCtx.enter()
        self.boolCtx.addContent("No")
        self.boolCtx.leave()
        
        self.boolCtx.enter()
        self.boolCtx.addContent("no")
        self.assertRaises(KeyError, self.boolCtx.leave)
        
        self.listCtx.enter()        
        self.listCtx.addContent("On")
        self.listCtx.leave()
        
        self.listCtx.enter()
        self.listCtx.addContent("Off")
        self.listCtx.leave()
        
        self.assertEqual(self.bool, False)
        self.assertEqual(self.list, [True, False])
        self.assertEqual(self.boolCtx.count, 2)
        self.assertEqual(self.listCtx.count, 2)

        
    def test_contextInterface(self):
        self.assertRaises(NotImplementedError, self.boolCtx.getContext, "ctx")
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(MapTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )