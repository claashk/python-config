#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

import unittest
from io import StringIO

from config.context import Value
from config.context import List
from config.context import Group
from config.context import Map
from config import IniReader, Dispatcher
from config import ErrorHandler

class IniReaderTestCase(unittest.TestCase):

    def setUp(self):
        self.context= Group( {
            u"value1"  : Value(self, u"val1", int),
            u"value2"  : Value(self, u"val2", float),
            u"section" : Group( {
                u"value3" : Value(self, u"val3", Map({u"on" : True,
                                                    u"off" : False})),
                u"value4" : List(self, u"val4", int) }) })                      
                          
        self.val1 = 0
        self.val2 = 0.
        self.val3 = False
        self.val4 = []
        
        self.log= StringIO()
        self.err= StringIO()        
        
        contentHandler= Dispatcher(self.context, ErrorHandler( out= self.log,
                                                               err= self.err))        
        self.reader= IniReader(contentHandler)
                    
    
    def test_case1(self):
        text=StringIO( u"value1 = 5\n"
                       u"value2= 4.2\n"
                       u"\n"
                       u" [section] "
                       u"  value3= on \n"
                       u"  value4  = 3\n"
                       u"  value4\t= 4 \n"
                       u"  value4 = 5\n"
                       u"\n" )

        self.reader.parse(text)        
        self.assertEqual(self.val1, 5)
        self.assertEqual(self.val2, 4.2)
        self.assertEqual(self.val3, True)
        self.assertEqual(self.val4, [3, 4, 5])
        self.assertEqual(self.context[u"section"].count, 1)
        self.assertEqual(self.context[u"value1"].count, 1)
        self.assertEqual(self.context[u"value2"].count, 1)
        self.assertEqual(self.context[u"section"][u"value3"].count, 1)
        self.assertEqual(self.context[u"section"][u"value4"].count, 3)
        self.assertEqual(self.log.getvalue(), u"")
        self.assertEqual(self.err.getvalue(), u"")



def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(IniReaderTestCase)


if __name__ == u'__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )