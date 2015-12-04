#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

import unittest
from config.context import Value
from config.context import Group

class CollectionTestCase(unittest.TestCase):

    def setUp(self):
        self.int  = 5
        self.str  = u"string"
        self.float= 5.1
        self.nestedInt= 0
        
        self.group= Group( { u"integer" : Value(self, u"int", int),
                             u"string"  : Value(self, u"str", unicode),
                             u"floater" : Value(self, u"float", float),
                             u"section" : Group({
                                 u"integer" : Value(self, u"nestedInt", int)}) })
        
    def test_construction(self):
        self.assertEqual(self.group.count, 0)
        
        count=0
        for name, ctx in self.group:
            count+= 1
            self.assertEqual(ctx.count, 0)

        self.assertEqual(count, 4)    
    
    
    def test_getContext(self):
        ctx=self.group.getContext(u"integer")        
        inputString= u"123"

        ctx.enter()
        ctx.addContent(inputString)
        ctx.leave()
        
        self.assertEqual(self.int, int(inputString))

        ctx=self.group.getContext(u"string")        
        inputString= u"a long string"
        ctx.enter()
        ctx.addContent(inputString)
        ctx.leave()
        self.assertEqual(self.str, inputString)

        ctx=self.group.getContext(u"floater")        
        inputString= u"1.234"
        ctx.enter()        
        ctx.addContent(inputString)
        ctx.leave()
        self.assertEqual(self.float, float(inputString))
        
        ctx=self.group.getContext(u"section")
        ctx.enter()
        ctx2= ctx.getContext(u"integer")        
        ctx2.enter()
        inputString= u"1234"
        ctx2.addContent(inputString)
        ctx2.leave()
        ctx.leave()        
        self.assertEqual(self.nestedInt, int(inputString))

        self.assertRaises(KeyError, self.group.getContext, u"xxx")
        
        count= 0
        for name, ctx in self.group:
            count+= 1            
            self.assertEqual(ctx.count, 1)
            
        self.assertEqual(count, 4)

        
    def test_itemAccess(self):
        ctx1= self.group.getContext(u"string")
        ctx2= self.group[u"string"]          
        self.assertTrue( ctx1 is ctx2 )

        self.assertRaises(KeyError, self.group.__getitem__, u"str")


    def test_contextInterface(self):
        self.group.enter()
        self.assertRaises(NotImplementedError,
                          self.group.addContent,
                          u"ctx")
        self.group.leave()
        
        self.assertRaises(IOError, self.group.enter)
        
        self.group.reset()        
        self.group.enter()
        self.group.addContent(u" \n \r\n \t")
        self.group.leave()
        self.assertEqual(self.group.count, 1)

        self.assertEqual(self.group.help, u"")
        

def suite():
    u"""Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(CollectionTestCase)


if __name__ == u'__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )