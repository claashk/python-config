# -*- coding: utf-8 -*-
import unittest

from schema.mixins import Group, children
from schema import node


class GroupTestCase(unittest.TestCase):

    def setUp(self):
        self.names= ["one", "two", "three", "four", "five", "six", "seven"]
        self.group= node("root") << children() [
                        node(self.names[0]),
                        node(self.names[1]),
                        node(self.names[2]) << children() [
                          node(self.names[3]),
                          node(self.names[4])
                        ],
                        node(self.names[5]),
                        node(self.names[6])
                    ]

        
    @staticmethod
    def recurse(g):
        for child in g:
            yield child

            if isinstance(child, Group):
                for grandChild in GroupTestCase.recurse(child):
                    yield grandChild


    def test_construction(self):
        self.assertEqual(self.group.name, "root")
        
        for name, element in zip(self.names, self.recurse(self.group)):
            self.assertEqual(name, element.name)
   
    
    def test_getChild(self):
        for name in (self.names[0:3] + self.names[5:7]):
            ctx= self.group.getChild(name)
            self.assertEqual(ctx.name, name)
            self.assertTrue(name in self.group)
            self.assertIs(self.group, ctx.parent)

        for name in self.names[3:5]:
            ctx= self.group.three.getChild(name)
            self.assertFalse(name in self.group)
            self.assertTrue(name in self.group.three)
            self.assertIs(self.group.three, ctx.parent)
            with self.assertRaises(ValueError):
                ctx= self.group.getContext(name)
        

    def test_contextInterface(self):
        self.group.open()
        self.group.close()
        
        self.assertEqual("", str(self.group))
        self.assertIsNone(self.group.parent)
        self.assertEqual("one", self.group.one.name)
        self.assertEqual("four", self.group.three.four.name)
                

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(GroupTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )