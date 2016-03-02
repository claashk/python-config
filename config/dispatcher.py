#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .error_handler import ErrorHandler
from .error import ContextError, ConfigWarning, ConfigError




class Dispatcher(object):
    """Directs content to the appropriate context.
    
    Arguments:
        context (object): Main context object.
        errorHandler (:class:`~.ErrorHandler`): Error handler.
    """
    def __init__(self, context, errorHandler=ErrorHandler() ):
        self._stack       = list()  #: context stack   
        self._errorHandler= errorHandler
        self._root        = context


    @property
    def currentContext(self):
        """Access the currently active context
        
        Invokes fatalError of the errorHandler if no active context exists.        
        
        Return:
            Active context
        """
        try:
            return self._stack[-1]
        except IndexError:
            self.fatalError("No active context!")
            

    @property
    def locator(self):
        return self._errorHandler.locator


    @locator.setter
    def locator(self, locator):
        self._errorHandler.locator= locator


    def startDocument(self):
        """Start a new document
        
        Clears the current context stack and invokes :meth:`~.Context.enter`
        on the main context.
        """
        self._stack.clear()
        
        if not self._root:
            self.fatalError("Missing root context")
        
        self._root.reset()
        

    def endDocument(self):
        """End parsing the current document.

        Checks that the context stack is empty.
        
        Raise:
            :class:`~.ContextError` if the context stack is not empty
        """
        if self._stack:
            self.warn("{0} context(s) were not closed properly."
                      .format(len(self._stack)))

        self.locator= None


    def enterContext(self, name, attrs=None):
        """Enter context
        
        Retrieves the new context from the current context with a call to
        :meth:`~.Context.getContext`(''name''). Then the current context is
        added to the context stack and the retrieved context is assigned to
        the active context. Finally :meth:`~.Context.enter` is invoked.        
        
        Arguments:
            name (str): Name of context to enter
            attrs (dict): Attributes
        """
        if self._stack:
            try:
                self._stack.append( self.currentContext.getContext(name) )
            except Exception as ex:
                self.fatalError( str(ex) )
        else:
            self._stack.append( self._root )
            
        try:
            self.currentContext.enter(attrs=attrs)
        except ConfigWarning as ex:
            self.warn( ex.message )
        except ConfigError as ex:
            self.fatalError( ex.message )
        except Exception as ex:
            self.fatalError( str(ex) )

    
    def leaveContext(self):
        """Leave current context
        
        Assigns the first context on the stack to the current context and
        invokes :meth:`~.Context.leave´. 
        """
        try:
            self.currentContext.leave()
        except ConfigWarning as ex:
            self.warn( ex.message )
        except ConfigError as ex:
            self.fatalError( ex.message )
        except Exception as ex:
            self.fatalError( str(ex) )
               
        self._stack.pop() 
            
    
    def addContent(self, content):
        """Add content to current context

        Arguments:
            content(:class:`str`): String containing content
        """
        self.currentContext.addContent(content)
       
       
    def addComment(self, comment):
        """Add comment to current context

        Arguments:
            comment(:class:`str`): String containing comment
        """
        if not self._stack:
            return  #ignore comments before main context
        self.currentContext.ignoreContent(comment)


    def ignoreContent(self, content):
        """Add ignorable content to current context

        Arguments:
            content(:class:`str`): String containing potentially ignorable
               content
        """
        self.currentContext.ignoreContent(content)
               
        
    def warn(self, message, level=0):
        """Report warning messages

        Arguments:
            message (str): Error message. Passed verbatim to errorHandler
            level (int): Log level. Passed verbatim to errorHandler            
        """        
        self._errorHandler.warn(message, level)
        
        
    def error(self, message, level=0):
        """Report an error
        
        Arguments:
            message (str): Error message. Passed verbatim to errorHandler
            level (int): Log level. Passed verbatim to errorHandler            
        """
        self._errorHandler.error(message, level)
        
        
    def fatalError(self, message):
        """Report a fatal error

        Arguments:
            message (str): Error message
            
        Raise:
            ContextError
        """
        raise ContextError(message, self.locator)
        