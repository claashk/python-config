# -*- coding: utf-8 -*-
from xml.sax.handler import ContentHandler as SaxContentHandler
from .sax_locator_adapter import SaxLocatorAdapter


class SaxReader(SaxContentHandler):
    """Adapter for ContentHandler instances to act as SAX2 ContentHandler
    
    This adapter turns any class implementing the
    :class:`~schema.ContentHandler` interface into a SAX2 ContentHandler. It
    provides e.g. a convenient way to validate XML input in combination with
    a :class:`~schema.Validator` object: The SaxReader forwards content
    obtained from a SAX2 parser to the :class:`~schema.Validator` object.
    
    Another way to use this reader is to convert xml content to another format
    by using a suitable writer implementaing the :class:`~schema.ContentHandler`
    interface (see e.g. :class:`~schema.WriterBase` or
    :class:`~schema.XmlWriter`).
    
    Arguments:
        contentHandler (:class:`~schema.ContentHandler`): Content handler.   
    """
    def __init__(self, contentHandler):
        self._impl= contentHandler
   

    def setDocumentLocator(self, saxLocator):
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
        
        Arguments:
            saxLocator(:class:`sax.Locator`): Locator object provided by SAX
               parser.
        """
        self._impl.locator= SaxLocatorAdapter(saxLocator)


    def startDocument(self):
        """Receive notification of the beginning of a document.

        The SAX parser will invoke this method only once, before any other
        methods in this interface or in DTDHandler (except for
        setDocumentLocator()).
        """
        self._impl.open()

        
    def endDocument(self):
        """Receive notification of the end of a document.

        The SAX parser will invoke this method only once, and it will be the
        last method invoked during the parse. The parser shall not invoke this
        method until it has either abandoned parsing (because of an
        unrecoverable error) or reached the end of input.
        """
        self._impl.close()
        
        
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
        self._impl.enter(name, **attrs)     

        
    def endElement(self, name):
        """Signals the end of an element in non-namespace mode.

        Arguments:
            name (str): Contains the name of the element type, just as with the
               :meth:`~.XmlAdapter.startElement` event.
        """
        self._impl.leave()


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
        self._impl.content(content)

        
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
        self._impl.ignore(whitespace)

    
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
