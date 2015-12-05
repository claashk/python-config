#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

import unittest
from io import StringIO
from xml.sax import parseString

from config import XmlWriter, XmlReader
from config import DefaultReader


class XmlWriterTestCase(unittest.TestCase):

    def setUp(self):
        self.stdout= StringIO()
        self.stderr= StringIO()
        self.handler1= XmlWriter()

                                                  
    def test_case1(self):
        str1= str(
            u'<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
            u'<root>\r\n'
            u'  <value1>5</value1>\r\n'
            u'  <value2>1.23</value2>\n'
            u'  <section first="1" second="long string">\n'
            u'    <value3>on</value3>\n'
            u'    <value4>1</value4>\n'
            u'    <value4>2</value4>\n'
            u'    <value4>42</value4>\n'
            u'  </section>\n'
            u'</root>'.encode(u"utf-8") )

        parseString(str1, XmlReader(self.handler1))


    def test_case2(self):
        str1= StringIO( 
            u'value1 = 5\n'
            u'value2 = 1.23 \n'
            u'section [first = "1",\n'
            u'         second= "long string"] { \n'
            u'  value3= on \n'
            u'  # A comment line\n'
            u'  value4= 1 \n'
            u'  value4 = 2 # With comment \n'
            u'  value4 = 42\n'
            u'  list = 1,2, 3, 4  , 5\n'
            u'}\n')

        reader= DefaultReader(self.handler1)
        reader.parse(str1)

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(XmlWriterTestCase)


if __name__ == u'__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )