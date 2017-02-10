# -*- coding: utf-8 -*-
import unittest
from io import StringIO

from schema import node, Bool, Validator
from schema.mixins import ref, children, lst
from schema import IniReader


class IniReaderTestCase(unittest.TestCase):

    def setUp(self):
        self.log= StringIO()
        self.err= StringIO()        

        self.val1 = 0
        self.val2 = 0.
        self.val3 = False
        self.val4 = []

        self.context= node("root") << children()[
                        node("value1") << ref(self, "val1", int),
                        node("value2") << ref(self, "val2", float),
                        node("section") << children() [
                          node("value3") << ref(self, "val3", Bool()),
                          node("value4") << lst(self, "val4", int)
                        ]
                      ]
        self.validator= Validator(self.context)
        self.reader= IniReader(self.validator)
                    
    
    def test_case1(self):
        text=StringIO( "value1 = 5\n"
                       "value2= 4.2\n"
                       "\n"
                       " [section] "
                       "  value3= on \n"
                       "  value4  = 3\n"
                       "  value4\t= 4 \n"
                       "  value4 = 5\n"
                       "\n" )

        self.reader.parse(text)        
        self.assertEqual(self.val1, 5)
        self.assertEqual(self.val2, 4.2)
        self.assertEqual(self.val3, True)
        self.assertEqual(self.val4, [3, 4, 5])
        self.assertEqual(self.log.getvalue(), "")
        self.assertEqual(self.err.getvalue(), "")


def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(IniReaderTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )