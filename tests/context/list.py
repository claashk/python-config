#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

import unittest
from config.context import List


class ListTestCase(unittest.TestCase):

    def setUp(self):
        self.list1=[]
        self.list2=[]

        self.list1Value= List( self, u"list1", int )
        self.list2Value= List( self, u"list2", float, maxCount=3)
        
        
    def test_construction(self):
        self.assertEqual(self.list1Value.count, 0)
        self.assertEqual(self.list2Value.count, 0)
        
    
    def test_parse(self):
        inputString=u"123"
        self.list1Value.enter()        
        self.list1Value.addContent(inputString)
        self.list1Value.leave()
        
        self.list2Value.enter()
        self.list2Value.addContent(inputString)
        self.list2Value.leave()
        
        self.assertEqual(self.list1, [int(inputString)])
        self.assertEqual(self.list2, [float(inputString)])
        self.assertEqual(self.list1Value.count, 1)
        self.assertEqual(self.list2Value.count, 1)

        self.list1Value.enter()
        self.list1Value.addContent(u"2")
        self.list1Value.leave()

        self.list1Value.enter()
        self.list1Value.addContent(u"3")
        self.list1Value.leave()

        self.list2Value.enter()        
        self.list2Value.addContent(u"2.0")
        self.list2Value.leave()
        
        self.list2Value.enter()
        self.list2Value.addContent(u"4.2")
        self.list2Value.leave()
        
        self.assertEqual(self.list1, [int(inputString), 2, 3])
        self.assertEqual(self.list2, [int(inputString), 2., 4.2])
        
        self.assertRaises(IOError, self.list2Value.enter)
        
        self.list1Value.enter()
        self.list1Value.addContent(u"4")
        self.list1Value.addContent(u"4")
        self.list1Value.leave()
        
        self.assertEqual(self.list1, [int(inputString), 2, 3, 44])
        
        
    def test_contextInterface(self):
        self.assertRaises(NotImplementedError, self.list1Value.getContext, u"ctx")
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(ListTestCase)


if __name__ == u'__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )