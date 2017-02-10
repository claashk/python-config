#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .value import Value

class List(Value):
    """List Decorator
    
    Arguments:
        obj (:class:`object`): Destination object.
        attrName (:class:`str`): Attribute name in destination.
        attrType (type): Attribute type capable of converting a string. An
           unary functor accepting a string could be passed as well.
        maxCount (:class:`int`): Maximum number of occurences
    """
    def __str__(self):
        return ", ".join( map(str, getattr(self._obj, self._attr) ))

    def parse(self, content=None):
        """Convert buffered string to desired target type and clear buffer
        
        Arguments:
            content(str): Ignored argument.
            
        Return:
            Content string converted to desired type
        """
        retval= []
        for s in self._buffer.decode().split(","):
            retval.append(self._type(s))
        self._buffer.clear()        
        return retval
