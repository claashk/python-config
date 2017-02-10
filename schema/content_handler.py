# -*- coding: utf-8 -*-


class ContentHandler(object):
    """Processes content obtained from a reader
    
    ContentHandler derived objects are similar to xml.sax content handlers.
    They are intended to provide a defined interface for readers to pass in
    data and to distribute or process this data. Writers or validators are
    classes typically derived from this class.
    
    This is a pure base class defining the interface. For possible
    implementations refer to
    * :class:`~schema.Validator`
    * :class:`~schema.XmlWriter`
    """
    @property
    def locator(self):
        """Return the currently used locator
        
        Return:
            :class:`schema.Locator`: Locator object
        """
        return None


    @locator.setter
    def locator(self, locator):
        """Set locator used by this handler.
        
        Arguments:
            locator(`schema.Locator`): Locator object.
        """
        return


    def open(self):
        """Open a new data source
        
        This default implementation does nothing
        """
        return
        

    def close(self):
        """Close the currently openened source

        This default implementation does nothing.
        """
        return
        

    def enter(self, name, attrs=None):
        """Enter a new context
        
        Arguments:
            name (str): Name of context to enter
            attrs (dict): Attributes
        """
        return

    
    def leave(self):
        """Leave the current context
        """
        return
            
    
    def content(self, content):
        """Add content to current context

        Arguments:
            content(str): String containing content
        """
        return
       
       
    def comment(self, comment):
        """Add comment to current context

        Arguments:
            comment(str): String containing comment
        """
        return


    def ignore(self, content):
        """Add padding such as whitespaces or format characters

        Arguments:
            content(str): String containing potentially ignorable
               padding
        """
        return
