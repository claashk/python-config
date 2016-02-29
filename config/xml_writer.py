#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.sax.saxutils import XMLGenerator
from sys import stdout

from .error_handler import ErrorHandler
from .writer_base import WriterBase



class XmlWriter(WriterBase):
    """Writer for XML files
    
    Fulfills the Dispatcher interface.

    Arguments:
        os: Output stream    
    """
    def __init__(self, os=stdout, errorHandler=ErrorHandler()):
        super().__init__(errorHandler)
        self._impl= XMLGenerator(os, encoding="utf-8")
        self._indent = 2;
        self._stack= []
                           

    def startDocument(self):
        """Start new document
        """
        super().startDocument()
        self._impl.startDocument()
        self._stack.clear()
    
    
    def endDocument(self):
        """End current document
        """
        super().endDocument()
        self._impl.endDocument()
    
    
    def enterLeaf(self, name, attrs=dict()):
        """Enter leaf node
        
        Arguments:
            name (:class:`str`): Name of node
            attrs (:class:`dict`): Optional attributes
        """
        self.indent()
        self._impl.startElement(name, attrs)
        self._stack.append(name)

        
    def enterBranch(self, name, attrs=dict()):
        """Enter branch node
        
        Arguments:
            name (:class:`str`): Name of node
            attrs (:class:`dict`): Optional attributes
        """
        self.enterLeaf(name, attrs)
        self._impl.ignorableWhitespace("\n")
        
        
    def exitLeaf(self):
        """Exit current leaf node
        """
        self._impl.endElement( self._stack.pop() )
        self._impl.ignorableWhitespace("\n")


    def exitBranch(self):
        """Exit current branch node
        """
        self.indent(-1)
        self.exitLeaf()


    def writeContent(self, content):
        """Add content to current context

        Arguments:
            content(:class:`str`): String containing content
        """
        self._impl.characters(content)
        
       
    def writeComment(self, comment):
        """Add comment to current context

        Arguments:
            comment(:class:`str`): String containing comment
        """
        self.indent()
        self._impl.ignorableWhitespace("<!--{0}-->\n".format(comment))
        

    def indent(self, shift=0):
        """Print indentation level
        
        Arguments:
           shift (:class:`int`) : Shift indentation level by this amount
        """
        self._impl.ignorableWhitespace( self._indent
                                        * (shift + len(self._stack) )
                                        * " " )
