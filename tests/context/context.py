# -*- coding: utf-8 -*-
import unittest
from config.context import Value

class ValueTestCase(unittest.TestCase):

    def setUp(self):
        self.int  = 5
        self.str  = "string"
        self.float= 5.1
        
        self.intValue= Value(obj=self, attr="int", type=int, maxCount=3)
        self.strValue= Value(obj=self, attr="str", type=str)
        self.floatValue= Value(obj=self, attr="float", type=float)


    def test_construction(self):
        self.assertEqual(self.intValue.count, 0)
        self.assertEqual(self.strValue.count, 0)
        self.assertEqual(self.floatValue.count, 0)
        
    
    def test_parse(self):
        inputString="123"
        self.intValue.enter()
        self.intValue.addContent(inputString)
        self.intValue.leave()
        self.assertEqual(self.int, int(inputString))
        self.assertEqual(self.intValue.count, 1)        
        
        inputString="12"
        self.intValue.enter()
        self.intValue.addContent(inputString)
        self.intValue.leave()
        self.assertEqual(self.int, int(inputString))
        self.assertEqual(self.intValue.count, 2)
        
        self.intValue.enter()
        self.intValue.addContent("12.5")
        self.assertRaises(ValueError, self.intValue.leave)

        self.assertRaises(IOError, self.intValue.enter)
        self.assertEqual(self.int, 12)
        self.assertEqual(self.intValue.count, 3)

        inputString="a string"
        self.strValue.enter()        
        self.strValue.addContent(inputString[:3])
        self.strValue.addContent(inputString[3:])
        self.strValue.leave()
        self.assertEqual(self.str, inputString)
        self.assertEqual(self.strValue.count, 1)

        inputString="12.123"
        self.floatValue.enter()
        self.floatValue.addContent(inputString[:4])
        self.floatValue.addContent(inputString[4:])
        self.floatValue.leave()
        
        self.assertEqual(self.float, float(inputString))
        self.assertEqual(self.floatValue.count, 1)        
        
        
    def test_contextInterface(self):
        self.assertRaises(NotImplementedError, self.intValue.getContext, "ctx")
        self.assertEqual(self.floatValue.help, "")
        
        x= 0
        for value in self.floatValue:
            x+= 1
        self.assertEqual(x, 0)
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(ValueTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )