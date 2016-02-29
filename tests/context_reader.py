# -*- coding: utf-8 -*-
import unittest

from config import XmlWriter, ErrorHandler, DefaultWriter
from config.context import Group, Value, List, Map
from config.context.decorator import Help
from config import ContextReader

from io import StringIO

class ContextReaderTestCase(unittest.TestCase):

    def setUp(self):
        self.context= Group( {
  "value1"
  : Help("Help message for value 1", Value(self, "val1", int))
,
  "value2"
  : Help("A longer help message\n"
         "Value 2 allows to set another value apart from value 1",
         Value(self, "val2", float))
,
  "section"
  : Group( {
      "value3"
      : Value(self, "val3", Map({"on" : True, "off" : False}))
,
      "value4" : List(self, "val4", int) }) })                      
                          
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
        #print(self.out.getvalue())
        

    def test_case2(self):
        reader= ContextReader( handler=DefaultWriter(os= self.out,
                                                     errorHandler= self.errorHandler ))
        reader(self.context)
        #print(self.out.getvalue())


def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(ContextReaderTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )