# -*- coding: utf-8 -*-

from sys import stdout
from .writer_base import WriterBase


class DefaultWriter(WriterBase):
    """Default writer for ASCII files
    
    Fulfills the Dispatcher interface.

    Arguments:
        os: Output stream    
    """
    def __init__(self, os=stdout, assignChar= "=", commentChar= "#" ):
        super().__init__()
        self.indent        = 2
        self._os           = os
        self._assignChar   = assignChar
        self._commentChar  = commentChar
        self._currentIndent= ""


    def open(self):
        """Start new document
        """
        super().open()
        self._currentIndent= ""

    
    def enterLeaf(self, name, attrs=None):
        """Enter leaf node
        
        Arguments:
            name (:class:`str`): Name of node
            attrs (:class:`dict`): Optional attributes
        """
        self._indent()
        self._os.write(name)

        if attrs:
            self._os.write("[{0}]".format(", ".join(self._iterAttrs(attrs)) ))

        self._os.write("{0} ".format(self._assignChar) )
        
                   
    def enterBranch(self, name, **kwargs):
        """Enter branch node
        
        Arguments:
            name (:class:`str`): Name of node
            **kwargs: Optional keyword arguments
        """
        self._indent()
        self._os.write(name)

        if kwargs:
            self._os.write("[{0}]".format(", ".join(self._iterAttrs(kwargs)) ))

        self._os.write(" {\n")
        self._currentIndent= "".join([self._currentIndent, self.indent * " "])
        
        
    def exitLeaf(self):
        """Exit current leaf node
        """
        self._os.write("\n")

        
    def exitBranch(self):
        """Exit current branch node
        """
        self._currentIndent= self._currentIndent[:-self.indent]
        self._indent()
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
        for line in self.split(comment, maxLen= 80 - len(self._currentIndent)):
            self._indent()
            self._os.write("{0}{1}\n".format(self._commentChar, line))


    def _iterAttrs(self, attrs):
        """Iterate over attributes
        
        Yield:
            String containing key-value pair
        """
        for key, value in sorted(attrs.items()):
            yield "{0}=\"{1}\"".format(key, value)

            
    def _indent(self):
        """Print indentation level
        """
        self._os.write( self._currentIndent )
