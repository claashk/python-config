#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .error_handler import ErrorHandler
from .error import ContextError

PENDING= 1
BRANCH = 2
LEAF   = 3


class WriterBase(object):
    """Generic base class for writer objects
    
    When pretty printing content, it is required to know whether or not the
    current context is a branch node or a leaf node in the parse tree. This
    information may not be available upon entering the context. This abstract
    base class determines the context type and invokes the functions enterLeaf
    and enterBranch, which shall be implemented in the derived class.
    
    Fulfills the Dispatcher interface.

    Arguments:
        os: Output stream
        errorHandler : Error handler
    """
    def __init__(self, errorHandler=ErrorHandler() ):

        self._errorHandler  = errorHandler
        self._currentContext= None
        self._pendingContext= None
        self._pendingContent= bytearray()
                           

    @property
    def locator(self):
        return self._errorHandler.locator


    @locator.setter
    def locator(self, locator):
        self._errorHandler.locator= locator


    def startDocument(self):
        self._currentContext= None
        self._pendingContext= None
        self._pendingContent.clear()
    
    
    def endDocument(self):
        self._currentContext= None
        return
    
    
    def enterContext(self, name, attrs=dict()):
        """Enter a new context

        Enter the context and try to determine whether it is a leaf or a
        branch. If the context type cannot be determined set current context
        type to pending and store name and attributes in pending context.
        
        Arguments:
            name (:class:`str`): Context name
            attrs (:class:`dict`): Optional attributes
            
        """
        if self._currentContext is None:
            self._enterBranch(name, attrs)
            return

        if self._currentContext == PENDING:
            # parent must be a node
            self.enterBranch(*self._pendingContext)

        self._pendingContext= (name, dict(attrs)) #copy not ref
        self._pendingContent.clear()
        self._currentContext= PENDING
                   
        
    def leaveContext(self):
        """Leave current context
        
        If current context is a leaf, all pending content is written and the
        context is closed.
        """
        if self._currentContext == PENDING:
            #neither sub contexts nor content so far -> assume it's a leaf
            self._enterLeaf(*self._pendingContext)
            self._pendingContext= None

        if self._currentContext == LEAF:
            self.writeContent(self._pendingContent.decode())
            self._pendingContent.clear()
            self.exitLeaf();
        elif self._currentContext == BRANCH:
            self._pendingContent.clear() # content in branch is ignored
            self.exitBranch()
        else:
            self.fatalError("Attempt to leave context without opening it")
            
        self._currentContext= BRANCH


    def addContent(self, content):
        """Add content to current context

        Arguments:
            content(:class:`str`): String containing content
        """
        if not content:
            return
            
        if self._currentContext == BRANCH:
            if content.isspace():
                return
            else:
                self.fatalError("Content is not allowed here")
        
        if self._currentContext == PENDING and not content.isspace():
            self._enterLeaf(*self._pendingContext)
            self._pendingContext= None
        
        self._pendingContent.extend( content.encode() )

       
    def addComment(self, comment):
        """Add comment to current context

        Arguments:
            comment(:class:`str`): String containing comment
        """
        if self._currentContext == LEAF:            
            self.fatalError("Comment not allowed here")
        
        if self._currentContext == PENDING:
            #comment only allowed in branch node
            self._enterBranch(*self._pendingContext)
            self._pendingContext= None

        self.writeComment(comment)
        

    def ignoreContent(self, content):
        """Add ignorable content to current context

        Arguments:
            content(:class:`str`): String containing potentially ignorable
               content
        """
        return
               
        
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
            

    def enterBranch(self, name, attrs):
        """Enter a branch node
        
        This function shall be implemented by the derived class
        """
        raise NotImplementedError("To be implemented by derived class")

        
    def enterLeaf(self, name, attrs):
        """Enter a terminal or leaf node
        
        This function shall be implemented by the derived class
        """
        raise NotImplementedError("To be implemented by derived class")


    def exitBranch(self, name, attrs):
        """Exit from a branch node
        
        This function shall be implemented by the derived class
        """
        raise NotImplementedError("To be implemented by derived class")

        
    def exitLeaf(self, name, attrs):
        """Exit from a terminal or leaf node
        
        This function shall be implemented by the derived class
        """
        raise NotImplementedError("To be implemented by derived class")


    def writeContent(self, content):
        """Write content to leaf node
        
        This function shall be implemented by the derived class
        """
        raise NotImplementedError("To be implemented by derived class")


    def writeComment(self, content):
        """Write comment to branch node
        
        This function shall be implemented by the derived class
        """
        raise NotImplementedError("To be implemented by derived class")


    def _enterBranch(self, name, attrs):
        """Wrapper for enterBranch"""
        self.enterBranch(name, attrs)
        self._currentContext= BRANCH
        
        
    def _enterLeaf(self, name, attrs):
        """Wrapper for enterBranch"""
        self.enterLeaf(name, attrs)
        self._currentContext= LEAF