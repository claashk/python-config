# -*- coding: utf-8 -*-
import unittest
from config.context import Value
from config.context import List
from config.context import Group
from config.context import Map
from config.context import Ignore
from config import XmlReader, ErrorHandler, Dispatcher
from config.error import ContextError


from io import StringIO

from xml.sax import parseString

class XmlReaderTestCase(unittest.TestCase):

    def setUp(self):
        self.stdout= StringIO()
        self.stderr= StringIO()
        
        self.val1= 0
        self.val2= 0.
        self.val3= False
        self.val4= []
        
        self.handler1= Dispatcher(
            context= Group({
                "value1"  : Value(self, "val1", int),
                "value2"  : Value(self, "val2", float),
                "section" : Group( {
                    "value3" : Value(self, "val3", Map({"on":True, "off":False})),
                    "value4" : List(self, "val4", int) }) }),
            errorHandler=ErrorHandler( out=self.stdout, err=self.stderr ))         

        self.handler2= Dispatcher(
             context= Group({
                "value1"  : Value(self, "val1", int),
                "value2"  : Value(self, "val2", float),
                None      : Ignore(),
                "section" : Group( {
                    "value3" : Value(self, "val3", Map({"on":True, "off":False})),
                    "value4" : List(self, "val4", int) }) }),
             errorHandler= ErrorHandler(out=self.stdout, err=self.stderr))                      

                                                  
    def test_case1(self):
        str1= bytes(
            '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
            '<root>\r\n'
            '  <value1>5</value1>\r\n'
            '  <value2>1.23</value2>\n'
            '  <section>\n'
            '    <value3>on</value3>\n'
            '    <value4>1</value4>\n'
            '    <value4>2</value4>\n'
            '    <value4>42</value4>\n'
            '  </section>\n'
            '</root>'.encode("utf-8") )

        parseString(str1, XmlReader(self.handler1))
#        except Exception as ex:
#            print("In Line {0}:{1}:\n{2}".format(handler._parent.locator.getLineNumber(),
#                                                 handler._parent.locator.getColumnNumber(),
#                                                 ex))
        self.assertEqual(self.val1, 5)
        self.assertEqual(self.val2, 1.23)
        self.assertEqual(self.val3, True)
        self.assertEqual(self.val4, [1,2,42])
        self.assertEqual(self.stderr.getvalue(), "")
        self.assertEqual(self.stdout.getvalue(), "")


    def test_case2(self):
        str1= bytes(
            '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
            '<root>\r\n'
            '  <value1>5</value1>\r\n'
            '  <value2>1.23</value2>\n'
            '  <section>\n'
            '    <value3>on</value3>\n'
            '    <value4>1\n'
            '    <value4>2</value4>\n'
            '    <value4>42</value4>\n'
            '  </section>\n'
            '</root>'.encode("utf-8") )

        msg= ""
        try:
            parseString(str1, XmlReader(self.handler2))
        except ContextError as ex:
            msg= str(ex)
        self.assertTrue( "Sub context not supported" in msg )
        
        self.assertEqual(self.stderr.getvalue(), "")
        self.assertEqual(self.stdout.getvalue(), "")



def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(XmlReaderTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )