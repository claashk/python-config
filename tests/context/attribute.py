# -*- coding: utf-8 -*-
import unittest
from config.context import Attribute, attr

class Data(object):
    pass

class AttributeTestCase(unittest.TestCase):

    def setUp(self):
        
        self.data= Data()
        self.data.int2= 1
        
        self.integer= 3
        
        self.int1= Attribute("int1", destObj= self.data, valueType=int)
        self.int2= Attribute("int2", destObj= self.data)
        self.int3= Attribute("integer", destObj= self)
        self.flt1= Attribute("flt",
                             destObj= self.data,
                             destName="float",
                             valueType=float )

        self.flt2= Attribute("value", valueType= float)
        self.str = Attribute("string", destObj=self.data)


    def test_construction(self):
        self.assertEqual(self.int1.name, "int1")
        self.assertEqual(self.int2.name, "int2")
        self.assertEqual(self.int3.name, "integer")
        self.assertEqual(self.flt1.name, "flt")
        self.assertEqual(self.flt2.name, "value")
        
        self.assertEqual(self.int1.data, self.data.int1)
        self.assertEqual(self.int2.data, self.data.int2)
        self.assertEqual(self.int3.data, self.integer)
        self.assertEqual(self.flt1.data, self.data.float)
        self.assertEqual(self.flt2.data, self.flt2.value)
        self.assertEqual(self.str.data, self.data.string)
        
    
    def test_fromString(self):
        value="123"
        x=int(value)
        
        self.int1.fromString(value)
        self.int2.fromString(value)
        self.int3.fromString(value)
        self.str.fromString(value)
        
        self.assertEqual(self.int1.data, x)
        self.assertEqual(self.int2.data, x)
        self.assertEqual(self.int3.data, x)
        self.assertEqual(self.data.int1, x)
        self.assertEqual(self.data.int2, x)
        self.assertEqual(self.integer, x)
        self.assertEqual(self.data.string, value)

        value="1.23"
        self.flt1.fromString(value)
        self.flt2.fromString(value)

        x= float(value)
        self.assertEqual(self.flt1.data, x)
        self.assertEqual(self.data.float, x)
        self.assertEqual(self.flt2.data, x)
        self.assertEqual(self.flt2.value, x)

        value="a1.23"
        self.assertRaises(ValueError, self.int1.fromString, value)
        
        
    def test_contextInterface(self):
        self.assertIsNone(self.int1.parent)
        self.assertIs(self.int1, self.int1.decorator)
        self.assertEqual(self.flt1.about, "")
        self.assertIsNone(self.flt2.default)
        self.int1.open()
        self.int1.close()
        self.int1.clear()
        
        self.assertRaises(NotImplementedError, self.int2.getContext, "xx")
        self.assertRaises(NotImplementedError, self.int2.insert, self.int3)
       

    def test_attr(self):
        dmc= attr("int1", destObj= self.data, valueType=int)
        self.assertIs(dmc._ctx.data, self.data.int1)
        
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(AttributeTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )