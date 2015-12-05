#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

import unittest
from io import StringIO
from xml.sax import parseString

from config.context import Value
from config.context import List
from config.context import Group
from config.context import Map
from config.context import Ignore
from config import XmlReader, ErrorHandler, Dispatcher
from config.error import ContextError


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
                u"value1"  : Value(self, u"val1", int),
                u"value2"  : Value(self, u"val2", float),
                u"section" : Group( {
                    u"value3" : Value(self, u"val3", Map({u"on":True, u"off":False})),
                    u"value4" : List(self, u"val4", int) }) }),
            errorHandler=ErrorHandler( out=self.stdout, err=self.stderr ))         

        self.handler2= Dispatcher(
             context= Group({
                u"value1"  : Value(self, u"val1", int),
                u"value2"  : Value(self, u"val2", float),
                None      : Ignore(),
                u"section" : Group( {
                    u"value3" : Value(self, u"val3", Map({u"on":True, u"off":False})),
                    u"value4" : List(self, u"val4", int) }) }),
             errorHandler= ErrorHandler(out=self.stdout, err=self.stderr))                      

                                                  
    def test_case1(self):
        str1= str(
            u'<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
            u'<root>\r\n'
            u'  <value1>5</value1>\r\n'
            u'  <value2>1.23</value2>\n'
            u'  <section>\n'
            u'    <value3>on</value3>\n'
            u'    <value4>1</value4>\n'
            u'    <value4>2</value4>\n'
            u'    <value4>42</value4>\n'
            u'  </section>\n'
            u'</root>'.encode(u"utf-8") )

        parseString(str1, XmlReader(self.handler1))
#        except Exception as ex:
#            print("In Line {0}:{1}:\n{2}".format(handler._parent.locator.getLineNumber(),
#                                                 handler._parent.locator.getColumnNumber(),
#                                                 ex))
        self.assertEqual(self.val1, 5)
        self.assertEqual(self.val2, 1.23)
        self.assertEqual(self.val3, True)
        self.assertEqual(self.val4, [1,2,42])
        self.assertEqual(self.stderr.getvalue(), u"")
        self.assertEqual(self.stdout.getvalue(), u"")


    def test_case2(self):
        str1= str(
            u'<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
            u'<root>\r\n'
            u'  <value1>5</value1>\r\n'
            u'  <value2>1.23</value2>\n'
            u'  <section>\n'
            u'    <value3>on</value3>\n'
            u'    <value4>1\n'
            u'    <value4>2</value4>\n'
            u'    <value4>42</value4>\n'
            u'  </section>\n'
            u'</root>'.encode(u"utf-8") )

        msg= u""
        try:
            parseString(str1, XmlReader(self.handler2))
        except ContextError, ex:
            msg= unicode(ex)
        self.assertTrue( u"Sub context not supported" in msg )
        
        self.assertEqual(self.stderr.getvalue(), u"")
        self.assertEqual(self.stdout.getvalue(), u"")



def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(XmlReaderTestCase)


if __name__ == u'__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )