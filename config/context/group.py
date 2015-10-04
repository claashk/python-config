#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .context import Context

class Group(Context):
    """Collection of context objects which does not support content
    
    Arguments:
        contexts (iterable): Iterable of (str, context) tuples.
        maxCount (int): Maximum number of allowed occurences.
    """
    def __init__(self, contexts=dict(), maxCount=1):
        super(Group, self).__init__(maxCount=maxCount)        
        self._contexts= dict()

        for name, ctx in contexts.items():
            self.addContext(name, ctx)


    def __getitem__(self, name):
        """Get sub-context by name

        Arguments:
            name (:class:`str`): Name of context to access
            
        Return:
            Context matching name
            
        Raise:
            :class:`KeyError` if no context with matching name is found.
        """
        return self._contexts[name]        
        
        
    def __iter__(self):
        """Iterate over member contexts
        
        Return:
            Iterator object
        """
        return iter( self._contexts.items() )


    def addContext(self, name, context):
        """Add context to collection
        
        Arguments:
            name (str): Context to add. A context with name `None` can be
               added, which will be invoked if no matching context can be found.
            context (:class:`Context`): Context object to add
            
        """
        self._contexts[name]= context


    def reset(self):
        """Resets this context and all sub-contexts
        """
        super(Group, self).reset()
        
        for name, ctx in self:
            ctx.reset()


    def enter(self, attrs=None):
        """Routine called by context manager, after the context is invoked

        Increases count by one and reset count of each sub-context
        
        Arguments:
            attrs (:class:`dict`): Attributes
        """
        for name, ctx in self:
            ctx.reset()

        super(Group, self).enter(attrs=attrs)
        

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
        retval= self._contexts.get(name, self._contexts.get(None, None))

        if retval is not None:
            return retval
        
        raise KeyError("Unknown context '{0}'".format(name))

