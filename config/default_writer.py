#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .error_handler import ErrorHandler
from .error import ContextError

from sys import stdout

NO_CONTEXT    = 0
PENDING       = 1
IN_CONTEXT    = 2
IN_ASSIGNMENT = 3


class DefaultWriter(object):
    """Default writer for ASCII files
    
    Fulfills the Dispatcher interface.

    Arguments:
        os: Output stream    
    """
    def __init__(self, os=stdout,
                       errorHandler=ErrorHandler(),
                       assignChar= "=",
                       commentChar= "#" ):

        self._errorHandler= errorHandler
        self._os   = os
        self._assignChar= assignChar
        self._commentChar= commentChar
        self._state= NO_CONTEXT
        self._buffer= []
        self._level= 0
        self._foundContent= False
                           

    @property
    def locator(self):
        return self._errorHandler.locator


    @locator.setter
    def locator(self, locator):
        self._errorHandler.locator= locator


    def startDocument(self):
        self._state= NO_CONTEXT
        self._level= 0
        self._buffer= list()
        self._foundContent= False
    
    
    def endDocument(self):
        return
    
    
    def enterContext(self, name, attrs=None):
        if self._state == PENDING:
            # This is a sub-context, so the parent cannot be an assignment
            self._beginContext()

        if self._level == 0:
            self._state= IN_CONTEXT
        else:
            self._buffer.append(name)
        
            if attrs:
                self._buffer.append("[{0}] "
                                    .format(", ".join(self._iterAttrs(attrs)) ))            

            self._buffer.append(None)
            self._state= PENDING
        
        self._level+= 1
                   
        
    def leaveContext(self):
        self._level-= 1

        if self._state == PENDING:
            # There has been neither a newline nor a sub context in this
            # context -> Assume it's an assignment
            self._beginAssignment()
            
            if not self._foundContent:
                self._os.write("''")

        self._foundContent= False

        if self._level == 0:
            self._state= NO_CONTEXT
            return

        if self._state != IN_ASSIGNMENT:
            self._os.write("}")

        self._state= IN_CONTEXT
        


    def addContent(self, content):
        """Add content to current context

        Arguments:
            content(:class:`str`): String containing content
        """
        if not content:
            return
        
        if not content.isspace():
            self._foundContent= True
            
        if self._state == PENDING:
            if "(" in content:
                self._beginAssignment()
                self._os.write(content)
            elif "\n" in content:
                self._beginContext()
                self._os.write(content)
            else:
                self._buffer.append(content)
        else:
            self._os.write(content)
       
       
    def addComment(self, comment):
        """Add comment to current context

        Arguments:
            comment(:class:`str`): String containing comment
        """
        if self._state == PENDING:
            self._beginContext()
            
        self._os.write("{0}{1}".format(self._commentChar, comment))


    def ignoreContent(self, content):
        """Add ignorable content to current context

        Arguments:
            content(:class:`str`): String containing potentially ignorable
               content
        """
        self.addContent(content)
               
        
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
            
            
    def _iterAttrs(self, attrs):
        """Iterate over attributes
        
        Yield:
            String containing key-value pair
        """
        for key, value in sorted(attrs.items()):
            yield "{0}='{1}'".format(key, value)

            
    def _dumpBuffer(self, fill=u"<?>"):
        """Dump buffer content to output stream and clear buffer
        
        Arguments:
            fill (:class:`str`): Fill character for None fields 
        """
        for string in self._buffer:
            if string is None:
                self._os.write(fill)
            else:
                self._os.write(string)
        self._buffer=list()
        
        
    def _beginAssignment(self):
        """Begin a new assignment
        
        Writes the assignment character followed by a start string character
        and dumps the buffer. Finally the current state is set to IN_ASSIGNMENT.
        """
        self._dumpBuffer( u"{0} ".format(self._assignChar) )
        self._state= IN_ASSIGNMENT
        
        
    def _beginContext(self):
        """Begin a new context
        
        Writes an opening curly bracket followed by the buffer content to the
        output stream. The current state is set to `IN_CONTEXT`.        
        """
        self._dumpBuffer(u"{")
        self._state= IN_CONTEXT
        