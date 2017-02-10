# -*- coding: utf-8 -*-

class SaxLocatorAdapter(object):
    """Adapter for an XML SAX2 Locator object
    
    Wraps a SAX2 locator to behave like a :class:`schema.Locator`.
    
    About SAX2 Locators:
        If a SAX parser provides location information to the SAX application,
        it does so by implementing this interface and then passing an instance
        to the application using the content handler's setDocumentLocator
        method. The application can use the object to obtain the location of
        any other SAX event in the XML source document.

        Note that the results returned by the object will be valid only during
        the scope of each callback method: the application will receive
        unpredictable results if it attempts to use the locator at any other
        time, or after parsing completes.

        SAX parsers are not required to supply a locator, but they are very
        strongly encouraged to do so. If the parser supplies a locator, it must
        do so before reporting any other document events. If no locator has
        been set by the time the application receives the startDocument event,
        the application should assume that a locator is not available.
    
    Arguments:
        locator (sax2.Locator): XML Sax locator to wrap
        
    Attributes:
        locator (sax2.Locator): Wrapped locator
    """
    def __init__(self, locator=None):
        self.locator= locator


    def __str__(self):
        """Convert current locator to string
        
        This method is used by various error reporting routines
        """
        return "{:d}:{:d}".format(self.line, self.column)


    @property
    def line(self):
        return self.locator.getLineNumber()

        
    @property
    def column(self):
        return self.locator.getColumnNumber()

