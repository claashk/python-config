# -*- coding: utf-8 -*-
import unittest

from io import StringIO

from schema import Validator, node
from schema.mixins import children, ref
from schema import DefaultReader

class DefaultReaderTestCase(unittest.TestCase):

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
                          node("value3") << ref(self, "val3"),
                          node("value4") << ref(self, "val4", int)
                        ]
                      ]
        self.validator= Validator(self.context)
        self.reader= DefaultReader(self.validator)

    
    def test_case1(self):
        text=StringIO( "value1 = 5\n"
                       "# Comment line\n"
                       "value2= 4.2 # with comment\n"
                       "# value2= 500.\n"
                       "section { value3= on \n"
                       "  value4  = 3\n"
                       "  value4\t= 4 ; value4 = 5\n"
                       "}\n" )

        self.reader.parse(text)        
        self.assertEqual(self.val1, 5)
        self.assertEqual(self.val2, 4.2)
        self.assertEqual(self.val3, "on")
        self.assertEqual(self.val4, 5)
        self.assertEqual(self.log.getvalue(), "")
        self.assertEqual(self.err.getvalue(), "")


    def test_case2(self):
        self.skipTest("Warnings not implemented yet") #TODO
        text=StringIO( "value1 [att1=attr1, att2='attr2'] = 5\n"
                       "value2 [ att3='one', #comment\n"
                       "        # another comment\n"
                               " att4='two' ] = 4.2\n" )

        self.reader.parse(text)
        self.assertEqual(self.val1, 5)
        self.assertEqual(self.val2, 4.2)
        self.assertEqual(self.log.getvalue(), "")
        err= self.err.getvalue()
        # print(err)
        self.assertTrue("WARNING: In line 1" in err)
        self.assertTrue("WARNING: In line 4" in err)
        self.assertEqual(err.count("Ignored attributes"), 2)

        self.assertTrue("'att1' ('attr1')" in err)        
        self.assertTrue("'att2' ('attr2')" in err)        
        self.assertTrue("'att3' ('one')" in err)        
        self.assertTrue("'att4' ('two')" in err)        
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(DefaultReaderTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )