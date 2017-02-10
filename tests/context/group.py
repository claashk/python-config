# -*- coding: utf-8 -*-
import unittest
from config.context import Attribute, attr
from config.context import Group, grp

class Data(object):
    pass

class GroupTestCase(unittest.TestCase):

    def setUp(self):
        self.data= Data()

        tmp= grp("root") [
                 attr("val1", destObj=self.data, valueType= int),
                 attr("val2", destObj=self.data, valueType= int),
                 attr("val3", destObj=self.data, valueType= int),
                 grp("sub1") [
                     attr("val4", destObj=self.data, valueType= int),
                     attr("val5", destObj=self.data, valueType= int)
                 ],
                 grp("sub2") [
                     attr("val6", destObj=self.data, valueType= int),
                     attr("val7", destObj=self.data, valueType= int)
                 ]
             ]

        self.group= tmp.context
        

    @staticmethod
    def recurse(g):
        for child in g:
            if isinstance(child, Attribute):
                yield child
            elif isinstance(child, Group):
                for grandChild in GroupTestCase.recurse(child):
                    yield grandChild
            else:
                raise RuntimeError("Undefined object")


    def test_construction(self):
        self.assertEqual(self.group.name, "root")
        

        for x, child in enumerate(self.recurse(self.group), 1):
            self.assertIsNone( getattr(self.data, "val{:d}".format(x)) )

        self.assertEqual(x, 7)
    
    
    def test_getContext(self):
        ctx= self.group.getContext("val1")
        ctx.fromString("321")
        self.assertEqual(self.data.val1, 321)
        
        with self.assertRaises(KeyError):
            ctx= self.group.getContext("doesNotExist")

        ctx= self.group.getContext("val3")
        ctx.fromString("465")
        self.assertEqual(self.data.val3, 465)

        ctx= self.group.getContext("sub2")
        ctx= ctx.getContext("val6")
        ctx.fromString("555")
        self.assertEqual(self.data.val6, 555)

        
    def test_itemAccess(self):
        ctx1= self.group.getContext("val1")
        ctx2= self.group["val1"]
        self.assertIs(ctx1, ctx2)
        
        self.assertTrue("val1" in self.group)
        self.assertTrue("val2" in self.group)
        self.assertFalse("Nothing" in self.group)

        with self.assertRaises(KeyError):
            ctx= self.group["doesNotExist"]



    def test_contextInterface(self):
        self.group.open()
        self.group.close()

        with self.assertRaises(NotImplementedError):
            self.group.count
            
        self.assertIsNone(self.group.maxCount)
        self.assertEqual(self.group.about, "")
        
        with self.assertRaises(NotImplementedError):
            self.group.data
                

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(GroupTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )