# -*- coding: utf-8 -*-

from sys import stderr
from .error import ContextError


class ErrorHandler(object):
    """Error handler implementation
    
    Arguments:
        out (stream): Stream used for log messages. Defaults to stdout
        err (stream): Stream used for warning and error messages. Defaults to
           stderr.
        logLevel (int):  Log level. Defaults to 1.
        locator (:class:`object`): Locator object with same interface as
            :class:`~.Locator`
    """
    
    def __init__(self, out=stderr, err=stderr, logLevel=1, locator=None):
        self.locator   = locator
        self._err      = err
        self._log      = out
        self._logLevel = logLevel
        self._nErrors  = 0
        self._nWarnings= 0

    @property
    def nErrors(self):
        return self._nErrors


    @property
    def nWarnings(self):
        return self._nWarnings


    def log(self, message, logLevel=1):
        """Print log message
        
        Arguments:
            message (str): Log message
            logLevel (int): Log level at which to print this message. The
               message will be suppressed if this value is greater than the
               current application logLevel
        """
        if logLevel <= self._logLevel:
            self.writeLocator(self._log)
            self._log.write(message)


    def warn(self, message, logLevel=0):
        """Print warning message
        
        Arguments:
            message (str): Log message
            logLevel (int): Log level at which to print this message. The
               message will be suppressed if this value is greater than the
               current application logLevel
        """
        self._nWarnings+= 1
        if logLevel <= self._logLevel:
            self._err.write(u"WARNING: ")
            self.writeLocator(self._err)
            self._err.write(message)
        

    def error(self, message, logLevel=0):
        """Print error message
        
        Arguments:
            message (str): Log message
            logLevel (int): Log level at which to print this message. The
               message will be suppressed if this value is greater than the
               current application logLevel
        """
        self._nWarnings+= 1
        if logLevel <= self._logLevel:
            self._err.write(u"ERROR: ")
            self.writeLocator(self._err)
            self._err.write(message)

        
    def fatalError(self, message):
        """Report a fatal error

        Arguments:
            message (:class:`str`): Error message
            
        Raise:
            ContextError
        """
        raise ContextError(message, self.locator)


    def writeLocator(self, stream):
        """Write locator information to stream
        
        Arguments:
            stream (:class:`stream`): Stream to write to
        """
        if not self.locator:
            return
            
        stream.write(u"In line {0}:{1}:\n".format(self.locator.line,
                                                  self.locator.column) )
