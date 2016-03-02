#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ..error import ConfigWarning

class Context(object):
    """Basic handler for events emitted by the lexer
    
    This is a pure base class, which does nothing except counting the number of
    calls.
    """
    def __init__(self, maxCount=1):
        self._count   = 0
        self._maxCount= maxCount
    
    
    def __iter__(self):
        """Iterate over sub-contexts. This function simply returns.
        """
        return
        yield #necessary to turn this method into a generator
        
    
    def __str__(self):
        """Convert content of current context to string"""
        return ""
        
    
    @property
    def count(self):
        """Return number of times, this key was found
        
        To be implemented by derived class.
        """
        return self._count


    @property
    def maxCount(self):
        """Return maximum number of times, this key may be found.
        
        Return:
            Maximum number of times, this key may be found in any given context.
            A value of -1 indicates an infinite number of times.
        """
        return self._maxCount


    @property
    def help(self):
        """Print help message"""
        return ""


    @property
    def content(self):
        """Access content of current context"""
        return None


    def reset(self):
        """Reset context to initial state

        This example implementation simply resets the counter to zero.        
        """
        self._count= 0


    def increaseCount(self):
        """Increase internal counter

        Raise:
            IOError if count exceeds maxCount.        
        """
        if self._maxCount != -1 and self._count >= self._maxCount:
            raise IOError("Max count exceeded!")
        self._count += 1


    def enter(self, attrs=None):
        """Routine called by context manager, after the context is invoked
        
        Default routine increases count by one and checks if maxCount is
        exceeded. A :class:`NotImplementedError` is raised, if any attributes
        are passed.        
        
        Arguments:
            manager (:class:~.ContextManager): Context manager.
            attrs (:class:`dict`): Attributes. If not ``None``, an exception
               will be raised.
        """
        self.increaseCount()
        
        if attrs:
            msg="Ignored attributes:\n"
            
            for key, value in attrs.items():
                msg+= "  '{0}' ('{1}')\n".format(key, value)

            raise ConfigWarning(msg)
    
    
    def leave(self):
        """Routine called by context manager, when leaving the context
        """
        pass
    
    
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
        raise NotImplementedError("Sub context not supported ('{0}')"
                                  .format(name))


    def parse(self, content):
        """Parse content within this context
        
        Called by the context manager, when content is found in a context.        
        
        Arguments:
            content(str): String to process
            
        Return:
            Parsed value
        """
        raise NotImplementedError("Context unable to parse")


    def addContent(self, content):
        """Add content to context.
        
        If the content consists entirely of spaces, it is forwarded to
        :meth:`~ignoreContent`        
        
        Arguments:
            content (:class:`str`): Content string.
        """
        if not content:
            return
        
        if content.isspace():
            self.ignoreContent(content)
            return
        
        raise NotImplementedError("Context does not support content ('{0}')"
                                  .format(content))


    def ignoreContent(self, content):
        """Add ignorable content to this context.

        This default implementation quietly ignores any content. A classic
        does-nothing-o'matic.

        Arguments:
            content(:class:`str`): Content, which may be ignored (e.g spaces)
        """
        pass