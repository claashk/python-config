#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

import unittest
from io import StringIO

from config.context import Value
from config.context import List
from config.context import Group
from config.context import Map
from config import DefaultReader, Dispatcher
from config import ErrorHandler

class DefaultReaderTestCase(unittest.TestCase):

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
        
        self.reader= DefaultReader( contentHandler=
            Dispatcher( context=self.context,
                        errorHandler=ErrorHandler(out= self.log,
                                                      err=self.err ) ))                    
    
    def test_case1(self):
        text=StringIO( u"value1 = 5\n"
                       u"# Comment line\n"
                       u"value2= 4.2 # with comment\n"
                       u"# value2= 500.\n"
                       u"section { value3= on \n"
                       u"  value4  = 3\n"
                       u"  value4\t= 4 ; value4 = 5\n"
                       u"}\n" )

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


    def test_case2(self):
        text=StringIO( u"value1 [att1=attr1, att2='attr2'] = 5\n"
                       u"value2 [ att3='one', #comment\n"
                       u"      # another comment\n"
                       u" att4='two' ] = 4.2\n" )

        self.reader.parse(text)
        self.assertEqual(self.val1, 5)
        self.assertEqual(self.val2, 4.2)
        self.assertEqual(self.log.getvalue(), u"")
        err= self.err.getvalue()
        # print(err)
        self.assertTrue(u"WARNING: In line 1" in err)
        self.assertTrue(u"WARNING: In line 4" in err)
        self.assertEqual(err.count(u"Ignored attributes"), 2)

        self.assertTrue(u"'att1' ('attr1')" in err)        
        self.assertTrue(u"'att2' ('attr2')" in err)        
        self.assertTrue(u"'att3' ('one')" in err)        
        self.assertTrue(u"'att4' ('two')" in err)        
        



def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(DefaultReaderTestCase)


if __name__ == u'__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )