# -*- coding: utf-8 -*-
import unittest
from config.context import Value
from config.context import Group

class GroupTestCase(unittest.TestCase):

    def setUp(self):
        self.int  = 5
        self.str  = "string"
        self.float= 5.1
        self.nestedInt= 0
        
        self.group= Group([ ("integer", Value(self, "int", int)),
                            ("string", Value(self, "str", str)),
                            ("floater", Value(self, "float", float)),
                            ("section",
                             Group([( "integer",
                                      Value(self, "nestedInt", int))  ])) ])
        

    def setValue(self, key, value, att, grp=None,):
        if grp is None:
            grp= self.group
            
        ctx= grp.getContext(key)
        ctx.enter()
        ctx.addContent( str(value) )
        ctx.leave()
        self.assertEqual(getattr(self, att), value)


    def test_construction(self):
        self.assertEqual(self.group.count, 0)
        
        count=0
        for name, ctx in self.group:
            count+= 1
            self.assertEqual(ctx.count, 0)

        self.assertEqual(count, 4)    
    
    
    def test_getContext(self):
        self.setValue("integer", 123, "int")
        self.setValue("string", "a long string", "str")
        self.setValue("floater", 1.234, "float")
        
        ctx=self.group.getContext("section")
        ctx.enter()
        self.setValue("integer", 321, "nestedInt", ctx)
        ctx.leave()        

        with self.assertRaises(KeyError):
            self.group.getContext("xxx")
        
        for count, (name, ctx) in enumerate(self.group, 1):
            self.assertEqual(ctx.count, 1)
        self.assertEqual(count, 4)

        
    def test_itemAccess(self):
        ctx1= self.group.getContext("string")
        ctx2= self.group["string"]          
        self.assertTrue( ctx1 is ctx2 )
        
        self.assertTrue("string" in self.group)
        self.assertTrue("integer" in self.group)
        self.assertFalse("Nothing" in self.group)

        self.assertRaises(TypeError, self.group.__getitem__, "str")


    def test_contextInterface(self):
        self.group.enter()
        with self.assertRaises(NotImplementedError):
            self.group.addContent("ctx")
        self.group.leave()
        
        self.assertRaises(IOError, self.group.enter)
        
        self.group.reset()        
        self.group.enter()
        self.group.addContent(" \n \r\n \t")
        self.group.leave()
        self.assertEqual(self.group.count, 1)
        self.assertEqual(self.group.help, "")


    def test_translation(self):
        d= {"str" : "string", "int" : "integer", "grp" : "section" }
        self.group.translate(d)
        self.setValue("int", 1234, "int")
        self.setValue("str", "What a string", "str")
        self.setValue("floater", 5.4321, "float")
        
        with self.assertRaises(KeyError):
            self.setValue("integer", 1234, "int")
                
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(GroupTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )