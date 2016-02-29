#! /usr/bin/env python
# -*- coding: utf-8 -*-
from sys import stdout

from .error_handler import ErrorHandler
from .writer_base import WriterBase


class DefaultWriter(WriterBase):
    """Default writer for ASCII files
    
    Fulfills the Dispatcher interface.

    Arguments:
        os: Output stream    
    """
    def __init__(self, os=stdout,
                       errorHandler=ErrorHandler(),
                       assignChar= "=",
                       commentChar= "#" ):

        super().__init__(errorHandler)
        self._os           = os
        self._assignChar   = assignChar
        self._commentChar  = commentChar
        self._indentSize   = 2
        self._currentIndent= ""


    def startDocument(self):
        """Start new document
        """
        super().startDocument()
        self._currentIndent= ""

    
    def enterLeaf(self, name, attrs=None):
        """Enter leaf node
        
        Arguments:
            name (:class:`str`): Name of node
            attrs (:class:`dict`): Optional attributes
        """
        self.indent()
        self._os.write(name)

        if attrs:
            self._os.write("[{0}]".format(", ".join(self._iterAttrs(attrs)) ))

        self._os.write("{0} ".format(self._assignChar) )
        
                   
    def enterBranch(self, name, attrs=None):
        """Enter branch node
        
        Arguments:
            name (:class:`str`): Name of node
            attrs (:class:`dict`): Optional attributes
        """
        self.indent()
        self._os.write(name)

        if attrs:
            self._os.write("[{0}]".format(", ".join(self._iterAttrs(attrs)) ))

        self._os.write(" {\n")
        self._currentIndent= "".join([ self._currentIndent,
                                       self._indentSize * " " ])
        
        
    def exitLeaf(self):
        """Exit current leaf node
        """
        self._os.write("\n")

        
    def exitBranch(self):
        """Exit current branch node
        """
        self._currentIndent= self._currentIndent[:-self._indentSize]
        self.indent()
        self._os.write("}\n")


    def writeContent(self, content):
        """Add content to current context

        Arguments:
            content(:class:`str`): String containing content
        """
        if not content or content.startswith(" ") or content.endswith(" "):
            self._os.write( "\"{0}\"".format(content) )
        else:
            self._os.write(content)
        
       
    def writeComment(self, comment):
        """Add comment to current context

        Arguments:
            comment(:class:`str`): String containing comment
        """
        self.indent()
        self._os.write("{0}{1}\n".format(self._commentChar, comment))


    def _iterAttrs(self, attrs):
        """Iterate over attributes
        
        Yield:
            String containing key-value pair
        """
        for key, value in sorted(attrs.items()):
            yield "{0}=\"{1}\"".format(key, value)

            
    def indent(self):
        """Print indentation level
        """
        self._os.write( self._currentIndent )
