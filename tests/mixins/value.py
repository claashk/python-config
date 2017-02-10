# -*- coding: utf-8 -*-
import unittest

from schema.mixins import children, ref
from schema import node

class ValueTestCase(unittest.TestCase):

    def setUp(self):
        self.int= 5
        self.str= "string"
        self.flt= 5.1
        
        self.group= node("root") << children() [
          node("integer") << ref(obj=self, attr="int", cls=int),
          node("otherInt") << ref(obj=self, cls=int),
          node("localInt") << ref(cls=int),
          node("string") << ref(obj=self, attr="str"),
          node("float") << ref(obj=self, attr="flt", cls=float) ]
        

    def test_construction(self):
        self.assertEqual(self.int, self.group.integer.value)
        self.assertEqual(self.str, self.group.string.value)
        self.assertEqual(self.flt, self.group.float.value)
        
    
    def test_fromString(self):
        inputString="123"
        self.group.integer.fromString(inputString)
        self.assertEqual(self.int, int(inputString))

        self.group.otherInt.fromString(inputString)
        self.assertEqual(self.otherInt, int(inputString))
        
        self.group.localInt.fromString(inputString)
        self.assertEqual(self.group.localInt.value, int(inputString))

        self.assertRaises(ValueError, self.group.integer.fromString, "12.5")

        inputString="a string"
        self.group.string.fromString(inputString)
        self.assertEqual(self.str, inputString)
        
        inputString="12.123"
        self.group.float.fromString(inputString)
        self.assertEqual(self.flt, float(inputString))
        
        
def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(ValueTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )