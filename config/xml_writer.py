#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.sax.saxutils import XMLGenerator

from .error_handler import ErrorHandler
from .error import ContextError

from sys import stdout

class XmlWriter(object):
    """Writer for XML files
    
    Fulfills the Dispatcher interface.

    Arguments:
        os: Output stream    
    """
    def __init__(self, os=stdout, errorHandler=ErrorHandler()):
        self._errorHandler= errorHandler

        self._impl= XMLGenerator(os, encoding="utf-8")
        self._stack= []
                           

    @property
    def locator(self):
        return self._errorHandler.locator


    @locator.setter
    def locator(self, locator):
        self._errorHandler.locator= locator


    def startDocument(self):
        self._impl.startDocument()    
    
    
    def endDocument(self):
        self._impl.endDocument()
    
    
    def enterContext(self, name, attrs=dict()):
        self._impl.startElement(name, attrs)
        self._stack.append(name)            
        
        
    def leaveContext(self):
        self._impl.endElement( self._stack.pop() )


    def addContent(self, content):
        """Add content to current context

        Arguments:
            content(:class:`str`): String containing content
        """
        self._impl.characters(content)
        
       
    def addComment(self, comment):
        """Add comment to current context

        Arguments:
            comment(:class:`str`): String containing comment
        """
        self._impl.ignorableWhitespace("<!--{0}-->".format(comment))
        

    def ignoreContent(self, content):
        """Add ignorable content to current context

        Arguments:
            content(:class:`str`): String containing potentially ignorable
               content
        """
        self._impl.ignorableWhitespace(content)
               
        
    def warn(self, message, level=0):
        """Report warning messages

        Arguments:
            message (str): Error message. Passed verbatim to errorHandler
            level (int): Log level. Passed verbatim to errorHandler            
        """        
        self._errorHandler.warn(message, level)
        
        
    def error(self, message, level=0):
        """Report an error
        
        Arguments:
            message (str): Error message. Passed verbatim to errorHandler
            level (int): Log level. Passed verbatim to errorHandler            
        """
        self._errorHandler.error(message, level)
        
        
    def fatalError(self, message):
        """Report a fatal error

        Arguments:
            message (str): Error message
            
        Raise:
            ContextError
        """
        raise ContextError(message, self.locator)
            
        