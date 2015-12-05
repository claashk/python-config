#!/usr/bin/env python2 
# -*- coding: utf-8 -*-

import unittest
from io import StringIO

from config.context import Value
from config.context import List
from config.context import Group
from config.context import Map
from config.context import Ignore
from config import Dispatcher, ErrorHandler
from config.error import ContextError


class DispatcherTestCase(unittest.TestCase):

    def setUp(self):
        self.stdout= StringIO()
        self.stderr= StringIO()
        
        self.handler  = Dispatcher( Group(
            { u"value1"  : Value(self, u"val1", int),
              u"value2"  : Value(self, u"val2", float),
              u"section" : Group( {
                  u"value3" : Value(self, u"val3", Map({u"on" : True,
                                                    u"off" : False})),
                  u"value4" : List(self, u"val4", int) }) }),
            errorHandler= ErrorHandler(self.stdout, self.stderr) )                      
                          
        self.val1 = 0
        self.val2 = 0.
        self.val3 = False
        self.val4 = []
                    
    
    def test_case1(self):
        handler= Dispatcher(context=None)
        self.assertRaises(ContextError, handler.startDocument)

        self.handler.startDocument()
        self.assertRaises(ContextError, handler.enterContext, u"")
        self.handler.endDocument()
        self.handler.startDocument()
        self.handler.endDocument()


    def test_case2(self):
        self.handler.startDocument()
        self.handler.enterContext(u"root")
        self.handler.enterContext(u"value1")
        self.handler.addContent(u"5")
        self.handler.leaveContext()
        self.assertEqual(self.val1, 5)
        self.handler.enterContext(u"section")
        self.handler.enterContext(u"value3")
        self.handler.addContent(u"on")
        self.handler.leaveContext()
        self.assertEqual(self.val3, True)
        self.handler.leaveContext()
        self.handler.leaveContext()
        self.handler.endDocument()
        self.assertEqual(self.stdout.getvalue(), u"")
        self.assertEqual(self.stderr.getvalue(), u"")

               
    def test_case3(self):
        self.handler.startDocument()
        self.handler.enterContext(u"root")
        self.handler.enterContext(u"section")
        self.handler.enterContext(u"value3")
        self.handler.addContent(u"on")
        self.handler.leaveContext()
        self.assertEqual(self.val3, True)
        self.handler.endDocument()

        msg= self.stderr.getvalue()
        self.stderr.truncate(0)
        self.stderr.seek(0)
        self.assertTrue(u"WARNING:" in msg )
        self.assertTrue(u"2 context(s) were not closed" in msg )
        
        self.handler.leaveContext()
        self.handler.endDocument()
        msg= self.stderr.getvalue()
        self.stderr.truncate(0)
        self.stderr.seek(0)
        self.assertTrue(u"WARNING:" in msg )
        self.assertTrue(u"1 context(s) were not closed" in msg )

        self.handler.leaveContext()
        self.handler.endDocument()
        
        self.assertEqual(self.stdout.getvalue(), u"")
        self.assertEqual(self.stderr.getvalue(), u"")


    def test_case4(self):
        self.handler.startDocument()
        self.handler.enterContext(u"root")
        self.assertRaises( ContextError,
                           self.handler.enterContext,
                           u"no_such_section" )
        self.handler.leaveContext()        
        self.handler.endDocument()

        self.handler._root.addContext(None, Ignore())
        self.handler.startDocument()
        self.handler.enterContext(u"root")
        self.handler.enterContext(u"no_such_selection")
        self.handler.enterContext(u"sub")
        self.handler.leaveContext()
        self.handler.leaveContext()
        self.handler.enterContext(u"section")
        self.handler.enterContext(u"value3")
        self.handler.addContent(u"on")
        self.handler.leaveContext()
        self.assertEqual(self.val3, True)
        self.handler.leaveContext()
        self.handler.leaveContext()
        self.handler.endDocument()

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(DispatcherTestCase)


if __name__ == u'__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )