# -*- coding: utf-8 -*-
from ..mixin import Mixin

class Value(Mixin):
    """Value parser mixin adding the ability to parse numeric values
    
    Provides only a parse method and no sub-contexts. Contains a reference to
    an object member in terms of the object and the name of the member, which
    will be set to the parsed value after type conversion.
    
    Arguments:
        obj (:class:`object`): Destination object.
        attr (str): Attribute name in destination.
        cls (type): Attribute type capable of converting a string. An
           unary functor accepting a string could be passed as well.
    """
    def __init__(self, obj=None, attr=None, cls=str):
        self._obj  = obj
        self._attr = attr
        self._type = cls

        if self._obj is None:
            self._obj= self

    def __str__(self):
        """Convert current content to string"""
        return str(self.value)


    @property
    def value(self):
        """Access current value
        """
        return getattr(self._obj, self._attr)


    @value.setter
    def value(self, val):
        """Set data value
        """
        setattr(self._obj, self._attr, val)


    def reset(self):
        """Reset counter and clear internal buffer
        """
        super().reset()
        self.value= self._type()


    def fromString(self, string):
        """Convert buffered string to desired target type and clear buffer
        
        Arguments:
            content(str): Ignored argument.
        """
        self.value= self._type(string)


    def moveTo(self, dest):
        """Move local attributes to destination context

        Overrides default implementation to add name extraction from
        destination context.

        Arguments:
            dest (:class:`schema.Context`): Destination context to initialise
        """
        if self._attr is None:
            self._attr= dest.name
        super().moveTo(dest)


def ref(obj=None, attr=None, cls=str):
    return Value(obj=obj, attr=attr, cls=cls)