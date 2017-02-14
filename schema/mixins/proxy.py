# -*- coding: utf-8 -*-

from ..mixin import Mixin
from .group import Group


class Proxy(Mixin):
    """Proxy contexts represent one of a number of possible delegate contexts
    
    Can impersonate any number of contexts depending on the attributes used
    during open.
    
    Example:
    <root>
      <item name="first">1</item>
      <item name="second">1</item>
      <item name="third">1</item>
    </root>
    
    In this case <item> can be implemented as a proxy with Value contexts
    first, second and third as delegates.
    
    Note that this kind of schema is probably not considered good practice xml,
    as it cannot be represented in a xml schema.
    
    Arguments:
        name (str): Name of the attribute used to specify the delegate
    """
    def __init__(self, key="name"):
        self._delegates= Group()
        self.key= key#name of attribute specifying the delegate
        self._cur= None # The current delegate Context

        
    def __str__(self):
        """Convert content of current context to string"""
        return str(self._cur)


    def __len__(self):
        """Get multiplicity
        
        Return:
            int: Number of delegates
        """
        return len(self._delegates._children)
    

    def __iter__(self):
        """Iterate over all delegates
        
        Yield:
            :class:`~schema.Context`: Delegates
        """
        yield from self._delegates.children()


    def __contains__(self, name):
        """Check if this context contains a subcontext with a given name
        
        Arguments:
            name(str): Name of subcontext to search for
        
        Return:
            bool: ``True`` if and only if ``self`` has a subcontext called
            `name``
        """
        return name in self._cur


    def __getitem__(self, delegates):
        """Square bracket implementation for child insertion
        
        Arguments:
            delegates (iterable): Iterable of delegate :class:`~schema.Context`
                objects.
            
        Return:
            ``self``
        """
        self._delegates[delegates]
        return self


    @property    
    def attributes(self):
        """Get dictionary of attributes for this context

        Attributes are intended to be passed to the context, when the open
        method is called. This default implementation returns an empty
        dictionary.
        """
        return {self.key: self._cur.name}

           
    def children(self):
        """Iterate over child contexts
        
        Yield:
            :class:`~schema.Context`: Sub context
        """
        yield from self._cur.children()


    def moveTo(self, other):
        """Move all attributes to other and reset 
        """
        for delegate in self._delegates.children():
            delegate.parent= other
            
        super().moveTo(other)


    def fromString(self, string):
        """Assign content to this context from a string

        This default implementation does nothing

        Arguments:
           string (str): String containing data. Ignored in this implementation
        """
        self._cur.fromString(string)


    def validate(self):
        """Make sure this context is valid.

        This default implementation does nothing
        """
        self._cur.validate()
        
        
    def reset(self):
        """Resets all delegates
        """
        self._delegates.reset()


    def open(self, **kwargs):
        """Open the current context
        
        Arguments:
           resetChildren (bool): If ``True`` all children are reset.
           **kwargs: Keyword arguments
        """
        try:
            key= kwargs.pop(self.key)
            self._cur= self._delegates.getChild(key)
        except KeyError:
            raise ValueError("In Proxy '{}': Missing mandatory attribute {}"
                             .format(self.name, self.keyAttr))
        except ValueError:
            raise ValueError("In Proxy '{}': No such delegate: {}"
                             .format(self.name, key))
                             
        self._cur.open(**kwargs)


    def close(self):
        """Close the current context
        """
        self._cur.close()

        
    def getChild(self, name):
        """Get sub-context
        
        Called by the schema to obtain a sub-context during parsing.
        
        Arguments:
            name (str): Name of child context

        Return:
             :class:`~schema.Context`: Child context called `name`.
        """
        return self._cur.getChild(name)


def proxy(key="key"):
    """Decorate existing context with children
    
    Arguments:
        name (str): Name of new group
        
    Return:
        DataModelCreator: Wrapper for new group
    """
    return Proxy(key=key)
