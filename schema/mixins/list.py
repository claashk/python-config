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
        self._index= 0

        
    def __str__(self):
        """Convert current content to string"""
        return str(self.value)


    def __len__(self):
        return len(self.list)


    def __iter__(self):
        for self._index in range(len(self)):
            yield self

        
    @property
    def list(self):
        """Access entire list
        
        Return:
            list: List containing items of this List
        """
        return getattr(self._obj, self._attr)


    @property
    def value(self):
        """Access current value
        
        Return:
            list: List containing items of this List
        """
        return self.list[self._index]


    @value.setter
    def value(self, val):
        """Append value to internal list
        """
        self.list.append(val)
        self._index= len(self) - 1 


    def reset(self):
        """Reset counter and clear internal buffer
        """
        super(Mixin, self).reset() #skip Value.reset
        setattr(self._obj, self._attr, list())



def lst(obj=None, attr=None, cls=str):
    return List(obj=obj, attr=attr, cls=cls)