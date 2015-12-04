# -*- coding: utf-8 -*-
import unittest
from config.context import Value
from config.context import List
from config.context import Group
from config.context import Map
from config.context import Ignore
from config import Dispatcher, ErrorHandler

from config.error import ContextError

from io import StringIO

class DispatcherTestCase(unittest.TestCase):

    def setUp(self):
        self.stdout= StringIO()
        self.stderr= StringIO()
        
        self.handler  = Dispatcher( Group(
            { "value1"  : Value(self, "val1", int),
              "value2"  : Value(self, "val2", float),
              "section" : Group( {
                  "value3" : Value(self, "val3", Map({"on" : True,
                                                    "off" : False})),
                  "value4" : List(self, "val4", int) }) }),
            errorHandler= ErrorHandler(self.stdout, self.stderr) )                      
                          
        self.val1 = 0
        self.val2 = 0.
        self.val3 = False
        self.val4 = []
                    
    
    def test_case1(self):
        handler= Dispatcher(context=None)
        self.assertRaises(ContextError, handler.startDocument)

        self.handler.startDocument()
        self.assertRaises(ContextError, handler.enterContext, "")
        self.handler.endDocument()
        self.handler.startDocument()
        self.handler.endDocument()


    def test_case2(self):
        self.handler.startDocument()
        self.handler.enterContext("root")
        self.handler.enterContext("value1")
        self.handler.addContent("5")
        self.handler.leaveContext()
        self.assertEqual(self.val1, 5)
        self.handler.enterContext("section")
        self.handler.enterContext("value3")
        self.handler.addContent("on")
        self.handler.leaveContext()
        self.assertEqual(self.val3, True)
        self.handler.leaveContext()
        self.handler.leaveContext()
        self.handler.endDocument()
        self.assertEqual(self.stdout.getvalue(), "")
        self.assertEqual(self.stderr.getvalue(), "")

               
    def test_case3(self):
        self.handler.startDocument()
        self.handler.enterContext("root")
        self.handler.enterContext("section")
        self.handler.enterContext("value3")
        self.handler.addContent("on")
        self.handler.leaveContext()
        self.assertEqual(self.val3, True)
        self.handler.endDocument()

        msg= self.stderr.getvalue()
        self.stderr.truncate(0)
        self.stderr.seek(0)
        self.assertTrue("WARNING:" in msg )
        self.assertTrue("2 context(s) were not closed" in msg )
        
        self.handler.leaveContext()
        self.handler.endDocument()
        msg= self.stderr.getvalue()
        self.stderr.truncate(0)
        self.stderr.seek(0)
        self.assertTrue("WARNING:" in msg )
        self.assertTrue("1 context(s) were not closed" in msg )

        self.handler.leaveContext()
        self.handler.endDocument()
        
        self.assertEqual(self.stdout.getvalue(), "")
        self.assertEqual(self.stderr.getvalue(), "")


    def test_case4(self):
        self.handler.startDocument()
        self.handler.enterContext("root")
        self.assertRaises( ContextError,
                           self.handler.enterContext,
                           "no_such_section" )
        self.handler.leaveContext()        
        self.handler.endDocument()

        self.handler._root.addContext(None, Ignore())
        self.handler.startDocument()
        self.handler.enterContext("root")
        self.handler.enterContext("no_such_selection")
        self.handler.enterContext("sub")
        self.handler.leaveContext()
        self.handler.leaveContext()
        self.handler.enterContext("section")
        self.handler.enterContext("value3")
        self.handler.addContent("on")
        self.handler.leaveContext()
        self.assertEqual(self.val3, True)
        self.handler.leaveContext()
        self.handler.leaveContext()
        self.handler.endDocument()

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(DispatcherTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )