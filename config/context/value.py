#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .context import Context

class Value(Context):
    """Value Parser Context invoked to actually parse content
    
    Provides only a parse method and not sub-contexts. Contains a reference to
    an object member in terms of the object and the name of the member, which
    will be set to the parsed value after type conversion.
    
    Arguments:
        obj (:class:`object`): Destination object.
        attrName (:class:`str`): Attribute name in destination.
        attrType (type): Attribute type capable of converting a string. An
           unary functor accepting a string could be passed as well.
        maxCount (:class:`int`): Maximum number of occurences
    """
    def __init__(self, obj=None,
                       attr="value",
                       type=str,
                       maxCount=1 ) :
        super().__init__(maxCount)        
        self._obj  = obj
        self._attr = attr
        self._type = type
        self._buffer= bytearray()
       
        if self._obj is None:
            self._obj= self
        

    def __str__(self):
        """Convert current content to string"""
        return str(self.content)


    @property
    def content(self):
        """Access current value
        """
        return getattr(self._obj, self._attr)


    def reset(self):
        """Reset counter and clear internal buffer
        """
        super().reset()
        self._buffer.clear()


    def parse(self, content=None):
        """Convert buffered string to desired target type and clear buffer
        
        Arguments:
            content(str): Ignored argument.
            
        Return:
            Content string converted to desired type
        """
        retval= self._type( self._buffer.decode() )
        self._buffer.clear()        
        return retval


    def addContent(self, content):
        """Add content to this value
        
        Content is stored in a temporary buffer, to allow for several calls to
        this function.
        
        If maxCount equals unity, the value is directly assigned, otherwise it
        is appended to a list.
        
        Arguments:
            content(str): Content string            
        """
        self._buffer.extend( content.encode() )
            
            
    def leave(self):
        """Content is parsed, when leaving the context
        """
        setattr(self._obj, self._attr, self.parse())
        