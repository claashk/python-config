#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ..context import Context

class Decorator(Context):
    """Base class for decorators.
    
    Arguments:
        parent (object): Object to decorate
    """
    def __init__(self, parent):
        self._parent= parent

   
    def __iter__(self):
        return iter(self._parent)


    @property
    def count(self):
        """Return number of times, this key was found
        
        Return:
            count of parent
        """
        return self._parent.count
        
        
    @property
    def maxCount(self):
        """Return maximum number of times, this key may be found.
        
        Return:
            maxCoutn of parent
        """
        return self._maxCount


    @property
    def help(self):
        """Print help message"""
        return self._parent.help


    def reset(self):
        """Reset counter to zero
        """
        self._parent.reset()


    def increaseCount(self):
        """Increase counter by one
        """
        self._parent.increaseCount()


    def enter(self, attrs=None):
        """Routine called by context manager, after the context is invoked
        
        Default routine increases count by one and checks if maxCount is
        exceeded. *attrs* is ignored.        
        
        Arguments:
            attrs (:class:`dict`): Attributes
        """
        self._parent.enter(attrs)
    
    
    def leave(self):
        """Routine called by context manager, when leaving the context
        """
        self._parent.leave()
    
    
    def getContext(self, name):
        """Get sub-context
        
        Called by the context manager to obtain a sub-context during parsing.
        Shall be implemented by derived class. 
        
        This is a pure base method raising a :class:`NotImplementedError`.        
        
        Raise:
            :class:`KeyError` if no such context exists
            
        Return:
             Context instance
        """
        return self._parent.getContext(name)


    def parse(self, content):
        """Parse content within this context
        
        Called by the context manager, when content is found in a context.        
        
        Arguments:
            content(str): String to process
        """
        return self._parent.parse(content)
        
        
    def addContent(self, content):
        """Add content to this context
        
        Arguments:
            content (str): Content to add to this context.
        """
        self._parent.addContent(content)

        
    def ignoreContent(self, content):
        """Add ignorable content to this context.

        Arguments:
            content(:class:`str`): Content, which may be ignored (e.g spaces)
        """
        self._parent.ignore(content)