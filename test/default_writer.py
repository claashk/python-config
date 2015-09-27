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
            '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
            '<root>\r\n'
            '  <value1>5</value1>\r\n'
            '  <value2>1.23</value2>\n'
            '  <section first="1" second="long string">\n'
            '    <value3>on</value3>\n'
            '    <value4>1</value4> \n'
            '    <value4>2</value4>  \n'
            '    <value4>42</value4>   \n'
            '    <value5>A very long string</value5>\n'
            '    <value5>"A very long string"</value5>\n'
            '    <value6></value6>\n'
            '  </section>\n'
            '  <f>sin(arg1= 1, arg2= 3)</f>\n'
            '</root>'.encode("utf-8") )

        parseString(str1, XmlReader(self.handler1))

        expected=str(
            "\n"
            "  value1= 5\n"
            "  value2= 1.23\n"
            "  section[first='1', second='long string'] {\n"
            "    value3= on\n"
            "    value4= 1 \n"
            "    value4= 2  \n"
            "    value4= 42   \n"
            "    value5= A very long string\n"
            "    value5= \"A very long string\"\n"
            "    value6= ''\n"
            "  }\n"
            "  f= sin(arg1= 1, arg2= 3)\n")

        self.assertEqual(self.out.getvalue(), expected)
        self.assertEqual(self.err.getvalue(), "")


    def test_case2(self):
        str1= StringIO(
            'value1 = 5\r\n'
            'value2 = 1.23 \n'
            'section [first = "1",\n'
            '         second= "long string"] {\n'
            '  value3= "on"\n'
            '  value4= 1 # with comment \n'
            '  # A comment line \n'
            '\n'
            '  value4= 2 \n'
            '  value4= 42  \n'
            '  value5= \'A very long quoted string\' \n'
            '  value6 {}\n'
            '  func= sin(arg1=1, arg2=2)\n'
            '  f= sin(arg1="xxx with space",  \n'
            '         arg2= 55.123)  \n'
            '} \n' )

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