# -*- coding: utf-8 -*-
import unittest

from io import StringIO

from xml.sax import parseString
from schema.xml import SaxReader, XmlWriter


class XmlWriterTestCase(unittest.TestCase):

    def setUp(self):
        self.stdout= StringIO()
        self.stderr= StringIO()
        self.handler1= XmlWriter(os=self.stdout)

                                                  
    def test_case1(self):
        str1= bytes(
            '<?xml version="1.0" encoding="utf-8" standalone="no" ?>\n'
            '<root>\r\n'
            '  <value1>5</value1>\r\n'
            '  <value2>1.23</value2>\n'
            '  <section first="1" second="long string">\n'
            '    <value3>on</value3>\n'
            '    <value4>1</value4>\n'
            '    <value4>2</value4>\n'
            '    <value4>42</value4>\n'
            '  </section>\n'
            '</root>'.encode("utf-8") )

        expected= str(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<root>\n'
            '  <value1>5</value1>\n'
            '  <value2>1.23</value2>\n'
            '  <section first="1" second="long string">\n'
            '    <value3>on</value3>\n'
            '    <value4>1</value4>\n'
            '    <value4>2</value4>\n'
            '    <value4>42</value4>\n'
            '  </section>\n'
            '</root>\n' )

        parseString(str1, SaxReader(self.handler1))
        #print( self.stdout.getvalue() )
        #order of dict cannot be predicted -> replace commutation
        result= self.stdout.getvalue().replace('section second="long string" first="1"',
                                               'section first="1" second="long string"')
        self.assertEqual(result, expected)


    def test_case2(self):
        self.skipTest("YamlReader not yet functional")
        str1= StringIO( 
            'value1 = 5\n'
            'value2 = 1.23 \n'
            'section [first = "1",\n'
            '         second= "long string"] { \n'
            '  value3= on \n'
            '  # A comment line\n'
            '  value4= 1 \n'
            '  value4 = 2 # With comment \n'
            '  value4 = 42\n'
            '  list = 1,2, 3, 4  , 5\n'
            '}\n')

        result= str(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<root>\n'
            '  <value1>5</value1>\n'
            '  <value2>1.23</value2>\n'
            '  <section first="1" second="long string">\n'
            '    <value3>on</value3>\n'
            '    <!-- A comment line-->\n'
            '    <value4>1</value4>\n'
            '    <value4>2</value4>\n'
            '    <!-- With comment -->\n'
            '    <value4>42</value4>\n'
            '    <list>1,2,3,4,5</list>\n'
            '  </section>\n'
            '</root>\n' )

        reader= DefaultReader(self.handler1)
        reader.parse(str1)
        #print( self.stdout.getvalue() )
        self.assertEqual(result, self.stdout.getvalue() )


def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(XmlWriterTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )