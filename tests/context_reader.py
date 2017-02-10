# -*- coding: utf-8 -*-

#TODO: This has to be renamed to schema_reader and adapted to the SchemaReader
# interface

import unittest

from config import XmlWriter, ErrorHandler, DefaultWriter, Dispatcher
from config.context import Group, Value, MultiValue, Map, List
from config.context.decorator import Help
from config import ContextReader

from io import StringIO


class Section(Group):
    def __init__(self, x=False, l=[], m=[]):
        self._x= bool(x)
        self._l= list(l)
        self._m= list(m)
        
        super().__init__( [("map", Value(self, "_x", Map({"on":True,
                                                          "off":False}) )),
                           ("mValue", MultiValue(self, "_m", int)),
                           ("list", List(self, "_l", float)) ] )
        
class TestContext(Group):
    def __init__(self, v1=0, v2=0, s=Section()):
        self.v1= v1
        self.v2= v2
        self.s = s
        
        super().__init__( [("value1", Help("Help message for value 1",
                                           Value(self, "v1", int))),
                           ("value2", Help("A longer help message.Value 2 allows to set "
                                           "another value apart from value 1. This sounds great or not ?",
                                           Value(self, "v2", float))),
                           ("section", s) ])
 
class ContextReaderTestCase(unittest.TestCase):

    def setUp(self):
        
        self.c1= TestContext(v1= 10, v2= 1.23e-4, s=Section( True,
                                                             l=[1.,2.,3.,4.],
                                                             m=[5, 6]))
        
        self.out= StringIO()
        self.err= StringIO()        
        self.errorHandler= ErrorHandler(out= self.err, err=self.err )


    def test_case1(self):
        reader= ContextReader(handler=XmlWriter(os= self.out,
                                                errorHandler= self.errorHandler))
        reader(self.c1)
        result= str(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<root>\n'
            '  <!--Help message for value 1-->\n'
            '  <value1>10</value1>\n'
            '  <!--A longer help message.Value 2 allows to set another value apart from value 1. This sounds great or not ?-->\n'
            '  <value2>0.000123</value2>\n'
            '  <section>\n'
            '    <map>on</map>\n'
            '    <mValue>5</mValue>\n'
            '    <mValue>6</mValue>\n'
            '    <list>1.0, 2.0, 3.0, 4.0</list>\n'
            '  </section>\n'
            '</root>\n' )
        #print(self.out.getvalue())
        self.assertEqual(result, self.out.getvalue() )


    def test_case2(self):
        reader= ContextReader( handler=DefaultWriter(os= self.out,
                                                     errorHandler= self.errorHandler ))
        reader(self.c1)
        result=str(
               "root {\n"
               "  #Help message for value 1\n"
               "  value1= 10\n"
               "  #A longer help message.Value 2 allows to set another value apart from value 1.\n"
               "  #This sounds great or not ?\n"
               "  value2= 0.000123\n"
               "  section {\n"
               "    map= on\n"
               "    mValue= 5\n"
               "    mValue= 6\n"
               "    list= 1.0, 2.0, 3.0, 4.0\n"
               "  }\n"
               "}\n" )
        #print(self.out.getvalue())
        self.assertEqual(result, self.out.getvalue() )


    def test_case3(self):
        c2= TestContext()
        reader= ContextReader(handler=Dispatcher(c2,
                                                 errorHandler= self.errorHandler))
        reader(self.c1)
        
        self.assertEqual(self.c1.s._x, c2.s._x)
        self.assertEqual(self.c1.s._l, c2.s._l)
        self.assertEqual(self.c1.s._m, c2.s._m)
        self.assertEqual(self.c1.v1, c2.v1)
        self.assertEqual(self.c1.v2, c2.v2)


def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(ContextReaderTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )