#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler as SaxContentHandler
from xml.sax.handler import ErrorHandler as SaxErrorHandler


class XmlReader(SaxContentHandler, SaxErrorHandler):
    """Adapter for ContentHandler instances to act as SAX2 ContentHandler &
       ErrorHandler
    
    Arguments:
        contentHandler (:class:`~.ContentHandler`): Content handler.   
    """
    def __init__(self, contentHandler ):
        self._impl   = contentHandler
        self._locator= None
    
    
    @property
    def line(self):
        """Get current line number        
        """
        return self._locator.getLineNumber()


    @property
    def column(self):
        """Get current column number 
        """
        return self._locator.getColumnNumber()


    def setDocumentLocator(self, locator):
        """Called by the parser to give the application a locator for locating
           the origin of document events.

        SAX parsers are strongly encouraged (though not absolutely required)
        to supply a locator: if it does so, it must supply the locator to the
        application by invoking this method before invoking any of the other
        methods in the DocumentHandler interface.

        The locator allows the application to determine the end position of any
        document-related event, even if the parser is not reporting an error.
        Typically, the application will use this information for reporting its
        own errors (such as character content that does not match an
        application’s business rules). The information returned by the locator
        is probably not sufficient for use with a search engine.

        Note that the locator will return correct information only during the
        invocation of the events in this interface. The application should not
        attempt to use it at any other time.
        """
        self._locator= locator
        self._impl.locator=self


    def startDocument(self):
        """Receive notification of the beginning of a document.

        The SAX parser will invoke this method only once, before any other
        methods in this interface or in DTDHandler (except for
        setDocumentLocator()).
        """
        self._impl.startDocument()

        
    def endDocument(self):
        """Receive notification of the end of a document.

        The SAX parser will invoke this method only once, and it will be the
        last method invoked during the parse. The parser shall not invoke this
        method until it has either abandoned parsing (because of an
        unrecoverable error) or reached the end of input.
        """
        self._impl.endDocument()
        
        
    def startPrefixMapping(self, prefix, uri):
        raise NotImplementedError("Prefix mapping is not supported")
        

    def endPrefixMapping(self, prefix):
        raise NotImplementedError("Prefix mapping is not supported")


    def startElement(self, name, attrs):
        """Signals the start of an element in non-namespace mode.

        Arguments:
            name (str): Contains the raw XML 1.0 name of the element type
            attrs (:class:`dict`): Holds an object of the Attributes interface
               (see The Attributes Interface) containing the attributes of the
               element. The object passed as *attrs* may be re-used by the
               parser; holding on to a reference to it is not a reliable way to
               keep a copy of the attributes. To keep a copy of the attributes,
               use the copy() method of the attrs object.
        """
        self._impl.enterContext(name, attrs)        

        
    def endElement(self, name):
        """Signals the end of an element in non-namespace mode.

        Arguments:
            name (str): Contains the name of the element type, just as with the
               :meth:`~.XmlAdapter.startElement` event.
        """
        self._impl.leaveContext()


    def characters(self, content):
        """Receive notification of character data.

        The Parser will call this method to report each chunk of character
        data. SAX parsers may return all contiguous character data in a single
        chunk, or they may split it into several chunks; however, all of the
        characters in any single event must come from the same external entity
        so that the Locator provides useful information.

        Arguments:
            content (str): may be a :class:`string` or :class:`bytes` instance;
               the expat reader module always produces strings               
        """
        if content.isspace():
            self._impl.ignoreContent(content)
        else:
            self._impl.addContent(content)

        
    def ignorableWhitespace(self, whitespace):
        """Receive notification of ignorable whitespace in element content.

        Validating Parsers must use this method to report each chunk of
        ignorable whitespace (see the W3C XML 1.0 recommendation,
        section 2.10): non-validating parsers may also use this method if they
        are capable of parsing and using content models.

        SAX parsers may return all contiguous whitespace in a single chunk, or
        they may split it into several chunks; however, all of the characters
        in any single event must come from the same external entity, so that
        the Locator provides useful information.
        
        Note that non-validating parsers are not required to invoke this method
        and may forward whitespaces using the :meth:`~.characters` method.

        Arguments:
            whitespace (str): String containing whitespace characters
        """
        self._impl.ignoreContent(whitespace)

    
    def processingInstruction(self, target, data):
        """Receive notification of a processing instruction.

        The Parser will invoke this method once for each processing
        instruction found: note that processing instructions may occur before
        or after the main document element.

        A SAX parser should never report an XML declaration (XML 1.0,
        section 2.8) or a text declaration (XML 1.0, section 4.3.1) using this
        method.
        """
        raise NotImplementedError("Processing Instructions are not supported")

    
    def error(self, exception):
        """Implementation of error handler interface
        
        Called when the parser encounters a recoverable error. If this method
        does not raise an exception, parsing may continue, but further document
        information should not be expected by the application. Allowing the 
        parser to continue may allow additional errors to be discovered in the
        input document.

        This implementation forwards the exception to the ContextManagers error
        handler.
        
        Arguments:
            exception (:class:`SaxParseException`): Exception object
        """
        self._impl.error( "Line {0}:{1}:\n:{2}\n\n"
                          .format( exception.getLineNumber(),
                                   exception.getColumnNumber(),
                                   exception.getMessage()  ))
        
        
    def fatalError(self, exception):
        """Implementation of error handler interface
        
        Called when the parser encounters an error it cannot recover from;
        parsing is expected to terminate when this method returns.

        This implementation forwards the exception to the ContextManagers error
        handler.
        
        Arguments:
            exception (:class:`SaxParseException`): Exception object
            
        Raise:
            ``exception``
        """
        raise exception
        
        
    def warning(self, exception):
        """Implementation of error handler interface
        
        Called when the parser presents minor warning information to the
        application. Parsing is expected to continue when this method returns,
        and document information will continue to be passed to the application.
        Raising an exception in this method will cause parsing to end.
 
        This implementation forwards the exception to the ContextManagers error
        handler.
        
        Arguments:
            exception (:class:`SaxParseException`): Exception object
        """
        self._impl.warn( "Line {0}:{1}:\n:{2}"
                         .format( exception.getLineNumber(),
                                  exception.getColumnNumber(),
                                  exception.getMessage()  ))
        