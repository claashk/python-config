# -*- coding: utf-8 -*-
from .value import Value
from ..mixin import Mixin

class List(Value):
    """Appends rather than replaces new values
    
    Arguments:
        obj (:class:`object`): Destination object.
        attr (str): Attribute name in destination.
        cls (type): Attribute type capable of converting a string. An
           unary functor accepting a string could be passed as well.
    """
    def __init__(self, obj=None, attr=None, cls=str):
        super().__init__(obj=obj, attr=attr, cls=cls)

        
    def __str__(self):
        """Convert current content to string"""
        return str(self.value)


    @property
    def value(self):
        """Access current value
        
        Return:
            list: List containing items of this List
        """
        return getattr(self._obj, self._attr)


    @value.setter
    def value(self, val):
        """Append value to internal list
        """
        self.value.append(val)


    def reset(self):
        """Reset counter and clear internal buffer
        """
        super(Mixin, self).reset() #skip Value.reset
        setattr(self._obj, self._attr, list())



def lst(obj=None, attr=None, cls=str):
    return List(obj=obj, attr=attr, cls=cls)