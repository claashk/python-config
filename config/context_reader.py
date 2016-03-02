#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .context import Map
from .context import MultiValue

class ContextReader(object):
    """Reader for :class:`~Context` objects
    
    Iterates over a context and all sub-contexts and forwards the content to a 
    Dispatcher object.
    
    Arguments:
        handler (:class:`Dispatcher`): Dispatcher object.
    """
    def __init__(self, handler):
        self._handler= handler
        self._attrs  = dict()


    def __call__(self, context):
        """Invoke reader
        
        Arguments:
            context (:class:`~Context`): Context to dispatch
        """
        self._handler.startDocument()
        self._dispatch(context)
        self._handler.endDocument()

   
    def _dispatch(self, context, name="root"):
        """Forward context to dispatcher
        
        Arguments:
           context (:class:`~Context`): context to dispatch
           name (:class:`str`): Name of context to dispatch
        """
        self._handler.addComment( context.help )

        if isinstance(context, MultiValue):
            for x in context.content:
                self._handler.enterContext(name, attrs=self._attrs)
                self._handler.addContent( str(x) )
                self._handler.leaveContext()
            return

        self._handler.enterContext(name, attrs=self._attrs)
        
        contentType= getattr(context, "_type", None)
        if isinstance(contentType, Map):
           self._handler.addContent( self.toString(contentType,
                                                   context.content ))
        else:
           self._handler.addContent( str(context) )
            
        for ctxName, ctx in context:
            self._dispatch(ctx, ctxName)
            
        self._handler.leaveContext()


    @staticmethod
    def toString(m, content):
        """Convert current value to string
        
        Arguments:
            m (:class:`Map`): Map object
            content: content
            
        Return:
            first key in m which whose value matches content. `str(content)`
            if no such key is found.
        """
        for key, value in m._values.items():
            if value == content:
                return key
        
        return str(content)
    