# -*- coding: utf-8 -*-
import unittest

from schema.mixins import children, lst
from schema import node

class ValueTestCase(unittest.TestCase):

    def setUp(self):
        self.ints= None
        self.floats= []
        
        self.group= node("root") << children() [
          node("iList") << lst(obj=self, attr="ints", cls=int),
          node("floats") << lst(obj=self, cls=float) ]
        

    def test_construction(self):
        self.assertEqual(self.ints, self.group.iList.value)
        self.assertEqual(self.floats, self.group.floats.value)
        
    
    def test_fromString(self):
        self.group.open() #this should reset
        self.group.iList.fromString("1")
        self.group.iList.fromString("2")
        self.group.iList.fromString("3")

        self.group.floats.fromString("1.1")
        self.group.floats.fromString("1.2")
        self.group.floats.fromString("1.3")
        self.group.close()
        
        
        self.assertEqual(self.ints, [1,2,3])
        self.assertEqual(self.floats, [1.1, 1.2, 1.3])

        self.group.open() #Should reset all children
        self.assertEqual(self.ints, [])
        self.assertEqual(self.floats, [])
        self.group.close()

        self.assertRaises(ValueError, self.group.iList.fromString, "12.5")

       
        
def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(ValueTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )