# -*- coding: utf-8 -*-
import unittest

from config import DefaultWriter, DefaultReader, IniReader
from config import XmlReader, ErrorHandler


from io import StringIO

from xml.sax import parseString

class DefaultWriterTestCase(unittest.TestCase):

    def setUp(self):
        self.err  = StringIO()
        self.out  = StringIO()
        errHandler= ErrorHandler(out=self.err, err=self.err)
        self.handler1= DefaultWriter(os=self.out, errorHandler=errHandler)
        self.maxDiff= None

                                                  
    def test_case1(self):
        str1= bytes(
            u'<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
            u'<root>\r\n'
            u'  <value1>5</value1>\r\n'
            u'  <value2>1.23</value2>\n'
            u'  <section first="1" second="long string">\n'
            u'    <value3>on</value3>\n'
            u'    <value4>1</value4> \n'
            u'    <value4>2</value4>  \n'
            u'    <value4>42</value4>   \n'
            u'    <value5>A very long string</value5>\n'
            u'    <value5>"A very long string"</value5>\n'
            u'    <value6></value6>\n'
            u'  </section>\n'
            u'  <f>sin(arg1= 1, arg2= 3)</f>\n'
            u'</root>'.encode("utf-8") )

        parseString(str1, XmlReader(self.handler1))

        expected=str(
            u"\n"
            u"  value1= 5\n"
            u"  value2= 1.23\n"
            u"  section[first='1', second='long string'] {\n"
            u"    value3= on\n"
            u"    value4= 1 \n"
            u"    value4= 2  \n"
            u"    value4= 42   \n"
            u"    value5= A very long string\n"
            u"    value5= \"A very long string\"\n"
            u"    value6= ''\n"
            u"  }\n"
            u"  f= sin(arg1= 1, arg2= 3)\n")

        self.assertEqual(self.out.getvalue(), expected)
        self.assertEqual(self.err.getvalue(), "")


    def test_case2(self):
        str1= StringIO(
            u'value1 = 5\r\n'
            u'value2 = 1.23 \n'
            u'section [first = "1",\n'
            u'         second= "long string"] {\n'
            u'  value3= "on"\n'
            u'  value4= 1 # with comment \n'
            u'  # A comment line \n'
            u'\n'
            u'  value4= 2 \n'
            u'  value4= 42  \n'
            u'  value5= \'A very long quoted string\' \n'
            u'  value6 {}\n'
            u'  func= sin(arg1=1, arg2=2)\n'
            u'  f= sin(arg1="xxx with space",  \n'
            u'         arg2= 55.123)  \n'
            u'} \n' )

        expected= str(
            "value1= 5\r\n"
            "value2= 1.23\n"
            "section[first='1', second='long string'] {\n"
            "  value3= 'on'\n"
            "  value4= 1# with comment \n"
            "  # A comment line \n"
            "\n"
            "  value4= 2\n"
            "  value4= 42\n"
            "  value5= \'A very long quoted string\' \n"
            "  value6= ''\n"
            "  func= sin(arg1=1,arg2=2)\n"
            "  f= sin(arg1='xxx with space',\n"
            "         arg2= 55.123)  \n"
            "}\n" )

        reader= DefaultReader(self.handler1)
        reader.parse(str1)
        self.assertEqual(self.out.getvalue(), expected)
        self.assertEqual(self.err.getvalue(), "")
        

    def test_case3(self):
        str1= StringIO(
            'value1 = 5\r\n'
            'value2 = 1.23 \n'
            '[section]\n'
            '  value3= "on"\n'
            '  value4= 1 ; with comment \n'
            '  ; A comment line \n'
            '  \n'
            '  value4= 2 \n'
            '  value4= 42  \n'
            '  value5= \'A very long quoted string\' \n' )

        expected= str(
            "value1= 5\r\n"
            "value2= 1.23 \n"
            "section{\n"
            "  value3= 'on'\n"
            "  value4= 1 # with comment \n"
            "  # A comment line \n"
            "  \n"
            "  value4= 2 \n"
            "  value4= 42  \n"
            "  value5= \'A very long quoted string\' \n"
            "}" )

        reader= IniReader(self.handler1)
        reader.parse(str1)
        self.assertEqual(self.out.getvalue(), expected)
        self.assertEqual(self.err.getvalue(), "")


def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(DefaultWriterTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )