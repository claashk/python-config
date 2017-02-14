# -*- coding: utf-8 -*-
#NOTE File has to be named schema_ to avoid name conflict with package schema
import unittest
from schema import Schema, node
from schema.mixins import children, ref


class SchemaTestCase(unittest.TestCase):

    def setUp(self):
        self.context= node("root") << children()[
                        node("value1") << ref(self, "val1", int),
                        node("value2") << ref(self, "val2", float),
                        node("section") << children() [
                          node("value3") << ref(self, "val3"),
                          node("value4") << ref(self, "val4")
                        ]
                      ]
        self.val1 = None
        self.val2 = None
        self.val3 = None
        self.val4 = None
        self.schema= Schema(self.context)
    
    def recurse(self):
        for ctxName in self.schema.children():
            self.schema.enter(ctxName)
            yield self.schema
            yield from self.recurse()
            self.schema.leave()

            
    def test_open(self):
        self.schema.open(self.context)
        self.assertFalse(self.schema.isActive)

        with self.assertRaises(IndexError):
            self.schema.activeContext.enter()
            

    def test_reset(self):
        self.schema.enter("root")
        self.schema.enter("section")
        self.assertTrue(self.schema.isActive)
        self.schema.reset()
        self.assertFalse(self.schema.isActive)
        self.schema.enter("root")
        self.assertIs(self.context, self.schema.activeContext)
        
        
    def test_iter(self):
        self.assertEqual([s.activeContext.name for s in self.recurse()],
                         ["root", "value1", "value2", "section", "value3",
                          "value4"])


    def test_traverse(self):
        self.schema.enter("root")
        self.schema.enter("value1")
        self.assertIs(self.context.value1, self.schema.activeContext)
        self.schema.leave()

        self.assertIs(self.context, self.schema.activeContext)
        self.schema.enter("value2")
        self.assertIs(self.context.value2, self.schema.activeContext)
        self.schema.leave()
        
        self.schema.enter("section")
        self.assertIs(self.context.section, self.schema.activeContext)
        self.schema.enter("value4")
        self.assertIs(self.context.section.value4, self.schema.activeContext)
        self.schema.leave()

        self.schema.enter("value3")
        self.assertIs(self.context.section.value3, self.schema.activeContext)
        self.schema.leave()
        self.schema.leave()
        self.assertIs(self.context, self.schema.activeContext)
        
        self.assertRaises(ValueError, self.schema.enter, "value666")
        
        self.schema.reset()
        with self.assertRaises(ValueError) as cm:
            self.schema.enter("wrong")
        
        self.assertIn("Invalid root context", str(cm.exception))
        
        schema= Schema()
        self.assertRaises(RuntimeError, schema.enter, "root")
        


    def test_assign(self):
        self.schema.enter("root")
        self.schema.enter("value1")
        self.assertIs(self.context.value1, self.schema.activeContext)
        
        self.schema.activeContext.fromString("42")
        self.schema.close()
        self.assertEqual(42, self.val1)
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(SchemaTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )