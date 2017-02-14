# -*- coding: utf-8 -*-

class ContextError(RuntimeError):
    pass

#TODO Context should provide error handler interface, which mixins can use e.g.
# to produce warnings. How do we obtain a locator ?
# Mabe context should provide state flags instead of direct error output, which
# can be queried by application. Somthing like isGood, hasWarnings, hasErrors,
# ...

class Context(object):
    """Context base class with minimal functionality

    The data model consists of a tree, where each node is represented by an
    instance of a :class:`~schema.Context` derived class. Context objects are
    designed to provide minimal functionality themselves. Additional
    functionality can be added through mixins. This allows for simple and
    versatile customization with little overhead.
    
    For more information on mixins refer to the `:mod:~schema.mixins` sub
    package.
    
    Attributes:
        name (str): Context name
        parent (:class:`schema.Context`): Parent context. `None` if no parent
            exists.
    """
    def __init__(self, name="", parent=None):
        self.name= name
        self.parent= parent


    def __str__(self):
        """Convert content of current context to string"""
        return ""


    def __len__(self):
        """Get multiplicity of this context.

        Return:
            int: 1
        """
        return 1


    def __iter__(self):
        """Iterate over occurences of this context.
        
        Yield:
            :class:`~schema.Context`: ``self``
        """
        yield self

    def __contains__(self, name):
        """Check if this context contains a subcontext with a given name
        
        Arguments:
            name(str): Name of subcontext to search for
        
        Return:
            bool: ``True`` if and only if ``self`` has a subcontext called
            `name``
        """
        return False


    def __getattr__(self, name):
        """ Used for group access.

        Called only if no attribute called ''name'' is defined.
        
        Arguments:
            name (str): Attribute name
            
        Return:
            object: Identical to :meth:~schema.Context.getChild`(name)
        """
        return self.getChild(name)


    def __lshift__(self, mixin):
        """Add mixin to current context
        
        Arguments:
            decorator (:class:`~schema.Mixin`): Mixin derived object
            
        Return:
            :class:~schema.Context`: ``self``
        """
        #create anonymous new type, which is derived from mixin and the current
        #type
        T= type("", (type(mixin), type(self)), {})

        self.__class__= T  #reset type of this object
        mixin.moveTo(self) #init mixin related attributes

        return self


    @property    
    def attributes(self):
        """Get dictionary of attributes for this context

        Attributes are intended to be passed to the context, when the open
        method is called. This default implementation returns an empty
        dictionary.
        """
        return dict()


    def children(self):
        """Iterate over sub-contexts. This function simply returns.

        Yield:
            :class:`~schema.Context`: Sub context
        """
        return
        yield #necessary to turn this method into a generator


    def fromString(self, string):
        """Assign content to this context from a string

        This default implementation does nothing

        Arguments:
           string (str): String containing data. Ignored in this implementation
        """
        return


    def validate(self):
        """Make sure this context is valid.

        This default implementation does nothing
        """
        return


    def reset(self):
        """Reset the current context

        This default implementation does nothing.
        """
        return


    def open(self, **kwargs):
        """Open the current context

        This default implementation does nothing.

        Arguments:
           **kwargs : Keyword arguments
        """
        return


    def close(self):
        """Close the current context

        This default implementation does nothing.
        """
        return


    def getChild(self, name):
        """Get sub-context
        
        Called by the schema to obtain a sub-context during parsing.
        
        Raise:
            :class:`~schema.ContextError` if no such context exists
            
        Return:
             :class:`~schema.Context`: Child context called `name`.
        """
        raise ContextError("Error accessing child '{}': Context '{}' does not "
                           "support children".format(name, self.name, name))
    
    
def node(name):
    """Create a context node
    
    Arguments:
        name (str): Name of context node
        
    Return:
        :class:`~schema.Context`: New context object
    """
    return Context(name)

        
