#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Map(object):
    """Map parser usable as type
    
    Restricts parsed values to a dictionary of key value pairs.    
    
    Arguments:
        values (:class:`dict`): Allowed keys with their respective value. Each
            value must be of the expected type of the parent.
    """
    def __init__(self, values):
        self._values= values

        for name, value in self._values.items():
            if type(name) != str:
                raise ValueError("Expected key of type string, got '{0}'"
                                 .format(type(name)))


    def __call__(self, content):
        """Parser implementation
        
        Arguments:
            content (:class:`str`): Content string to parse        
        
        Return:
            Value assigned to content
            
        Raise:
            :class:`KeyError` if no matching content is found.
        """
        return self._values[content]
   