# -*- coding: utf-8 -*-
import unittest

from schema.mixins import Proxy, proxy, ref, children, lst
from schema import node

class ProxyTestCase(unittest.TestCase):

    def setUp(self):

        self.nested= []

        self.group= node("root") << children() [
                        node("proxy") << proxy(key="id") [
                            node("i") << ref(self, cls=int),
                            node("f") << ref(self, cls=float),
                            node("g") << children() [
                                node("nested") << ref(self) << lst()
                            ]
                        ]
                    ]

    def test_construction(self):
        self.assertEqual(self.group.name, "root")
        self.assertTrue( isinstance(self.group.proxy, Proxy) )
        
    
    def test_contextInterface(self):
        self.group.open()
        self.group.proxy.open(id="i")
        self.group.proxy.fromString("1")
        self.group.proxy.close()
        self.assertEqual("1", str(self.group.proxy))

        self.group.proxy.open(id="f")
        self.group.proxy.fromString("1.2")
        self.group.proxy.close()
        self.assertEqual("1.2", str(self.group.proxy))

        self.group.proxy.open(id="g")
        self.group.proxy.nested.open()
        self.group.proxy.nested.fromString("one")
        self.group.proxy.nested.close()
        self.group.proxy.nested.open()
        self.group.proxy.nested.fromString("two")
        self.group.proxy.nested.close()
        self.assertEqual(self.group.proxy.nested.value, "two")

        self.assertEqual([x.name for x in self.group.proxy.children()],
                         ["nested"])

        self.assertEqual([x.value for x in self.group.proxy.nested],
                         ["one", "two"])
        
        self.group.proxy.close()
        self.group.close()

               

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(ProxyTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )