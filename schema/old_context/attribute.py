# -*- coding: utf-8 -*-

from .context import Context
from ..data_model_creator import DataModelCreator


class Attribute(Context):
    """Attribute Context
    
    Attributes store data, but not allow any children.
    
    Arguments:
        name (str): Name of attribute
        parent(:class:`~config.context.Context`): Parent context. Defaults to
           ``None``.
        destObj (object): Destination object. Defaults to ``self``.
        destName (str): Attribute name in destObj. Defaults to ``name``.
        valueType (type): Attribute type capable of converting a string. An
           unary functor accepting a string could be passed as well. Defaults
           to the current value of ``destObj.destName`` if it exists or ``str``
           otherwise.
    """
    def __init__(self, name,
                       parent= None,
                       destObj=None,
                       destName=None,
                       valueType=None ):
        super().__init__(name)
        self._destObj  = destObj
        self._destName = destName
        self._valueType = valueType
        self._decorator= self
        self._parent= parent
       
        if self._destObj is None:
            self._destObj= self
            
        if self._destName is None:
            self._destName= self.name
        
        if self._valueType is None:
            try:
                self._valueType= type(self.data)
            except AttributeError:
                if self.default is not None:
                    self._valueType= type(self.decorator.default)
                else:
                    self._valueType= str #better than an exception ?
        
        self.assign(self.decorator.default)


    def __str__(self):
        """Convert current content to string"""
        return str(self.data)


    @property
    def parent(self):
        """Access parent of this context

        Return:
            :class:~config.context.Context: Parent of this context
        """
        return self._parent


    @parent.setter
    def parent(self, ctx):
        """Set parent of this context
        """
        if ctx is not None and not isinstance(ctx, Context):
            raise TypeError("Invalid context type")
        self._parent= ctx


    @property
    def data(self):
        """Access current value
        """
        return getattr(self._destObj, self._destName)


    @property
    def decorator(self):
        """Access decorator of this Context

        Required if call backs to routines overridden in decorator shall be
        called. 

        Return:
            Active decorator or ``self``, if no decorator is attached.
        """
        return self._decorator


    def fromString(self, string):
        """Convert buffered string to desired target type and clear buffer
        
        Arguments:
            content(str): Ignored argument.
            
        Return:
            Content string converted to desired type
        """
        self.assign(self._valueType(string))


    def fromDataset(self, dset):
        """Assign content to this context from a HDF dataset

        Arguments:
            dset (:class:~config.context.Context): Source dataset

        Raise:
            :class:`NotImplementedError`
        """
        raise NotImplementedError("To be implemented by derived class")


    def fromAttribute(self, att):
        """Assign content to this context from a HDF attribute

        Arguments:
            att (:class:~config.context.Context): Source attribute

        Raise:
            :class:`NotImplementedError`
        """
        raise NotImplementedError("To be implemented")


    def clear(self):
        """Reset counter and clear internal buffer
        """
        super().clear()
        self.assign( self.decorator.default )


    def decorate(self, decorator):
        """Add decorator to this class

        Arguments:
            decorator (:class:~config.context.decorator.Decorator): Decorator
               to add to this context.
        """
        self._decorator= decorator

        
    def assign(self, value=None):
        """Assign value to the current instance
        
        Arguments:
            value (valueType): Value to assign to this instance
        """
        setattr(self._destObj, self._destName, value)


def attr(name, **kwargs):
    """Create a new Attribute
    
    Arguments:
        name (str): Name of new group
        kwargs: Keyword arguments forwarded to Attribute constructor
        
    Return:
        DataModelCreator: Wrapper for new attribute
    """
    return DataModelCreator( Attribute(name, **kwargs) )
