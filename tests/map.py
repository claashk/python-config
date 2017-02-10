# -*- coding: utf-8 -*-
import unittest
from schema import Map, Bool

class MapTestCase(unittest.TestCase):

    def test_map(self):
        m= Map(one=1, two= 2, three= 3)
        self.assertIsNone( m() )
        self.assertEqual(m("one"), 1)
        self.assertEqual(m("two"), 2)
        self.assertEqual(m("three"), 3)

        self.assertRaises(KeyError, m, "")
        self.assertRaises(KeyError, m, "four")


    def test_bool(self):
        b= Bool()
        self.assertFalse( b() )
        self.assertTrue( b("true") )
        self.assertTrue( b("on") )
        self.assertTrue( b("yes") )
        
        self.assertFalse( b("off") )
        self.assertFalse( b("no") )
        self.assertFalse( b("false") )

        self.assertRaises(KeyError, b, "")
        self.assertRaises(KeyError, b, "yup")
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(MapTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )