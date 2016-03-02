#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .value import Value

class MultiValue(Value):
    """Decorator for a value, which can occur more than once
    
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
                       maxCount= -1 ) :
        super().__init__(obj=obj, attr=attr, type=type, maxCount=maxCount)        




    def leave(self):
        """Leave list context and assign content
        """
        getattr(self._obj, self._attr).append( self.parse() )
