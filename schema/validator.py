# -*- coding: utf-8 -*-

from .content_handler import ContentHandler
from .content_buffer import ContentBuffer
from .context import Context
from .schema import Schema
from .error import SchemaError


#TODO need a validator test case ? Maybe validate this in combination with
# the SAX reader, as there is little functionality implemented here.

class Validator(ContentHandler):
    """Content handler implementing input validation against a Schema
    
    Allows validation of input data against a :class:`~schema.Schema`. Because
    Validator implements the :class:`~schema.ContentHandler` interface, it is
    well suited to validate data obtained from any reader exporting data
    through this interface such as
    
    * :class:`~schema.xml.SaxReader`
    * ...
    
    Arguments:
        schema (:class:~schema.Schema or :class:`~schema.Context`): Input
            schema against which to validate. If this is a context object,
            it will be converted to a schema using the :class:~schema.Schema
            constructor.
    """
    def __init__(self, schema):
        if isinstance(schema, Context):
            self._schema= Schema(context= schema)
        else:
            self._schema= schema
            
        self._buffer = ContentBuffer()
        self._locator= None


    @property
    def locator(self):
        """Return the currently used locator
        
        The locator is typically provided by the parser to track the current
        state of the parser.
        
        Return:
            :class:`~schema.Locator`: Locator object
        """
        return self._locator


    @locator.setter
    def locator(self, locator):
        """Set locator used by this handler
        
        Parsers are encourated to provide a locator through this interface.
        
        Arguments:
            locator(`schema.Locator`): Locator object.
        """
        self._locator= locator


    def open(self):
        """Open the schema
        
        Make sure the current schema is valid and the cursor is placed at the
        root node.
        """
        self._schema.reset()
        

    def close(self):
        """Close the current schema
        """
        self._schema.close()
        

    def enter(self, name, **kwargs):
        """Enter a sub context of the currently active context of the schema
        
        Arguments:
            name (str): Name of context to enter
            **kwargs: Keyword arguments passed verbatim to schema
            
        Raises:
            :class:`~schema.SchemaError`: If entering context fails
        """
        if self._schema.isActive:
            self.flushBuffer()
        try:        
            self._schema.enter(name, **kwargs)
        except Exception as ex:
            raise SchemaError(str(ex), self.locator)
            
    
    def leave(self):
        """Leave the current context for the parent context
        
        Directs all buffered content to the currently open context before
        leaving it. If a parent exists, the parent will become the currently
        active context.
        """
        self.flushBuffer()
        self._schema.leave()
            
    
    def content(self, content):
        """Add content chunk to internal content buffer

        Arguments:
            content(str): String containing content
        """
        self._buffer.add(content)
       
       
    def flushBuffer(self):
        """Flush all buffered content to currently active context
        
        Raises:
            :class:`~schema.SchemaError`: If passing content fails
        """
        try:        
            self._schema.content( self._buffer.flush() )
        except Exception as ex:
            raise SchemaError(str(ex), self.locator)
        
