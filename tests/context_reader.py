#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

import unittest
from StringIO import StringIO

from config import XmlWriter, ErrorHandler, DefaultWriter
from config.context import Group, Value, List, Map
from config.context.decorator import Help
from config import ContextReader


class ContextReaderTestCase(unittest.TestCase):

    def setUp(self):
        self.context= Group( {
  u"value1"
  : Help(u"Help message for value 1", Value(self, u"val1", int))
,
  u"value2"
  : Help(u"A longer help message\n"
         u"Value 2 allows to set another value apart from value 1",
         Value(self, u"val2", float))
,
  u"section"
  : Group( {
      u"value3"
      : Value(self, u"val3", Map({u"on" : True, u"off" : False}))
,
      u"value4" : List(self, u"val4", int) }) })                      
                          
        self.val1 = 1
        self.val2 = 0.
        self.val3 = False
        self.val4 = [1,2,3,4]
        
        self.out= StringIO()
        self.err= StringIO()        
        self.errorHandler= ErrorHandler(out= self.err, err=self.err )


    def test_case1(self):
        reader= ContextReader( handler=XmlWriter(os= self.out,
                                                 errorHandler= self.errorHandler ))
        reader(self.context)
        print self.out.getvalue()
        

    def test_case2(self):
        reader= ContextReader( handler=DefaultWriter(os= self.out,
                                                     errorHandler= self.errorHandler ))
        reader(self.context)
        print self.out.getvalue()


def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(ContextReaderTestCase)


if __name__ == u'__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )