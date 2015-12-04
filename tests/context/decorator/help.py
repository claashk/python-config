# -*- coding: utf-8 -*-
import unittest
from config.context.decorator import Help
from config.context import Value
from config.context import Group

class HelpDecoratorTestCase(unittest.TestCase):

    def setUp(self):
        self.int= 1
        self.intValue= Help( "This is an integer value",
                              Value(self, "int", int))

        self.group= Help( "This is a group",
                          Group({"value" : Help("Another int",
                                                           Value( self,
                                                                  "int",
                                                                  int) )}))
       

    def test_construction(self):
        self.assertEqual(self.intValue.count, 0)
        self.assertEqual(self.group.count, 0)
        
    
    def test_parse(self):
        inputString="123"
        self.intValue.enter()        
        self.intValue.addContent(inputString)
        self.intValue.leave()
        self.assertEqual(self.int, int(inputString))
        self.assertEqual(self.intValue.count, 1)
        

    def test_getValue(self):
        ctx= self.group.getContext("value")
        inputString= "12"
        ctx.enter()
        ctx.addContent(inputString)
        ctx.leave()
        self.assertEqual(self.int, int(inputString))
        self.assertEqual(ctx.count, 1)
        
        self.assertEqual(self.group.count, 0)
        self.group.enter()
        self.assertEqual(self.group.count, 1)
        self.group.leave()
        
        
    def test_contextInterface(self):
        self.assertRaises(NotImplementedError, self.intValue.getContext, "ctx")
        self.assertRaises(NotImplementedError, self.group.parse, "...")
        
        self.assertEqual(self.intValue.help, "This is an integer value")
        self.assertEqual(self.group.help, "This is a group")
        self.assertEqual(self.intValue.content, self.int)
        self.assertEqual(self.group.content, None)

        count=0
        for name, ctx in self.group:
            count+= 1
            self.assertEqual(ctx.count, 0)
            self.assertEqual(ctx.help, "Another int")
        self.assertEqual(count, 1)


def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(HelpDecoratorTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )