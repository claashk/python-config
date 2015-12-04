# -*- coding: utf-8 -*-

from .value import Value
from itertools import imap

class List(Value):
    """List Decorator
    
    Arguments:
        obj (:class:`object`): Destination object.
        attrName (:class:`str`): Attribute name in destination.
        attrType (type): Attribute type capable of converting a string. An
           unary functor accepting a string could be passed as well.
        maxCount (:class:`int`): Maximum number of occurences
    """
    def __init__(self, obj=None,
                       attr=u"value",
                       type=unicode,
                       maxCount= -1 ) :
        super(List, self).__init__(obj=obj, attr=attr, type=type, maxCount=maxCount)        


    @property
    def content(self):
        """Access current value
        """
        return u",".join( imap(unicode, getattr(self._obj, self._attr) ))


    def leave(self):
        """Leave list context and assign content
        """
        getattr(self._obj, self._attr).append( self.parse() )
