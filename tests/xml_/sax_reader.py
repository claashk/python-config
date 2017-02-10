# -*- coding: utf-8 -*-
import unittest

from schema import Validator, node
from schema.mixins import children, ref
from schema.xml import SaxReader
from schema import SchemaError

from io import StringIO
from xml.sax import parseString

class SaxReaderTestCase(unittest.TestCase):

    def setUp(self):
        self.stdout= StringIO()
        self.stderr= StringIO()
        
        self.val1= 0
        self.val2= 0.
        self.val3= False
        self.val4= []
        self.context= node("root") << children()[
                        node("value1") << ref(self, "val1", int),
                        node("value2") << ref(self, "val2", float),
                        node("section") << children() [
                          node("value3") << ref(self, "val3"),
                          node("value4") << ref(self, "val4", int)
                        ]
                      ]
        self.validator= Validator(self.context)
        self.reader= SaxReader(self.validator)

                                                  
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

        parseString(str1, self.reader)
#        except Exception as ex:
#            print("In Line {0}:{1}:\n{2}".format(handler._parent.locator.getLineNumber(),
#                                                 handler._parent.locator.getColumnNumber(),
#                                                 ex))
        self.assertEqual(self.val1, 5)
        self.assertEqual(self.val2, 1.23)
        self.assertEqual(self.val3, "on")
        self.assertEqual(self.val4, 42)
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

        with self.assertRaises(SchemaError) as env:
            parseString(str1, self.reader)

        ex= env.exception
        msg= str(ex)
        #print(msg)
        self.assertEqual(ex.line, 8)
        self.assertIn("Error accessing child 'value4'", msg)
        self.assertIn("Context 'value4' does not support children", msg)
        self.assertEqual(self.stderr.getvalue(), "")
        self.assertEqual(self.stdout.getvalue(), "")



def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(SaxReaderTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )