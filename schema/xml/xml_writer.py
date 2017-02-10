# -*- coding: utf-8 -*-
from xml.sax.saxutils import XMLGenerator
from sys import stdout

from schema.writer_base import WriterBase


class XmlWriter(WriterBase):
    """SAX Writer for XML files
    
    XML writer implementing the :class:`~schema.ContentHandler` interface. The
    writer allows to produce XML output from content created by any reader
    exporting to :class:`~schema.ContentHandler` objects, such as 
    :class:`~schema.xml.SaxReader` or :class:`~schema.SchemaReader`.

    Arguments:
        os (stream): Output stream
        encoding (str): Output encoding.
    """
    def __init__(self, os=stdout, encoding="utf-8"):
        super().__init__()
        self._impl= XMLGenerator(os, encoding=encoding)
        self.indent= 2;
        self._stack= []
                           

    def open(self):
        """Start new document
        """
        super().open()
        self._impl.startDocument()
        self._stack.clear()
    
    
    def close(self):
        """End current document
        """
        super().close()
        self._impl.endDocument()
    
    
    def enterLeaf(self, name, **kwargs):
        """Enter leaf node
        
        Arguments:
            name (:class:`str`): Name of node
            **kwargs: Optional keyword arguments
        """
        self._indent()
        self._impl.startElement(name, kwargs)
        self._stack.append(name)

        
    def enterBranch(self, name, **kwargs):
        """Enter branch node
        
        Arguments:
            name (str): Name of node
            **kwargs: Optional keyword arguments
        """
        self.enterLeaf(name, **kwargs)
        self._impl.ignorableWhitespace("\n")
        
        
    def exitLeaf(self):
        """Exit current leaf node
        """
        self._impl.endElement( self._stack.pop() )
        self._impl.ignorableWhitespace("\n")


    def exitBranch(self):
        """Exit current branch node
        """
        self._indent(-1)
        self.exitLeaf()


    def writeContent(self, content):
        """Add content to current context

        Arguments:
            content(str): String containing content
        """
        self._impl.characters(content)
        
       
    def writeComment(self, comment):
        """Add comment to current context

        Arguments:
            comment(str): String containing comment
        """
        self._indent()
        self._impl.ignorableWhitespace("<!--{0}-->\n".format(comment))
        

    def _indent(self, shift=0):
        """Print indentation level
        
        Arguments:
           shift (int) : Shift indentation level by this amount
        """
        self._impl.ignorableWhitespace( self.indent * " "
                                        * (shift + len(self._stack) ) )
