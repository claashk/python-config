# -*- coding: utf-8 -*-
from .sax_locator_adapter import SaxLocatorAdapter
from schema import ErrorHandler


class SaxErrorHandler(object):
    """Turns ErrorHandler objects into valid SAX error handlers
    
    Adapter turning an :class:`~schema.ErrorHandler` into a SAX error handler.
    
    SAX error handlers are used to receive error and warning information from
    the :class:`XMLReader`. If you create an object that implements this
    interface, then register the object with your XMLReader, the parser will
    call the methods in your object to report all warnings and errors. There
    are three levels of errors available: warnings, (possibly) recoverable
    errors, and unrecoverable errors. All methods take a
    :class:`SAXParseException` as the only parameter. Errors and warnings may
    be converted to an exception by raising the passed-in exception object.
    
    Arguments:
        errorHandler (:class:`schema.ErrorHandler`): Error handler to wrap
    """
    def __init__(self, errorHandler=ErrorHandler()):
        self._logger= errorHandler


    def error(self, exception):
        """Called when the parser encounters a recoverable error.
        
        If this method does not raise an exception, parsing may continue, but
        further document information should not be expected by the application.
        Allowing the parser to continue may allow additional errors to be
        discovered in the input document.
        
        Arguments:
            exception (:class:`SAXParseException`): SAX Exception object.
        """
        self._logger.error(exception.getMessage(),
                           locator=SaxLocatorAdapter(exception) )


    def fatalError(self, exception):
        """Called when the parser encounters an error it cannot recover from
        
        Parsing is expected to terminate when this method returns.
        
        Arguments:
            exception (:class:`SAXParseException`): SAX Exception object.
        """
        #SAXParseException provides the SAX Locator interface
        self._logger.fatal(exception.getMessage(),
                           locator=SaxLocatorAdapter(exception) )


    def warning(self, exception):
        """Called when the parser presents minor warning information to the application.
        Parsing is expected to continue when this method returns, and document
        information will continue to be passed to the application. Raising an
        exception in this method will cause parsing to end.
        
        Arguments:
            exception (:class:`SAXParseException`): SAX Exception object.
        """
        self._logger.warn(exception.getMessage(),
                          locator=SaxLocatorAdapter(exception) )
