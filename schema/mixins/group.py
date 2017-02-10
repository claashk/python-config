# -*- coding: utf-8 -*-
from ..mixin import Mixin
from ..context import Context


class Group(Mixin):
    """Group mixin adds capability to add child contexts to a parent context
    """
    def __init__(self):
        self._children= list()
        self._index= dict()
        #Context cannot be stored as dict, as this would not allow to iterate
        #over the items in the order in which they were defined. Thus we
        #use a list in combination with a dictionary for lookup by name

        
    def __iter__(self):
        """Iterate over member contexts
        
        Return:
            Iterator object
        """
        return iter(self._children)


    def __contains__(self, name):
        """Check if this context contains a subcontext with a given name
        
        Arguments:
            name(str): Name of subcontext to search for
        
        Return:
            bool: ``True`` if and only if ``self`` has a subcontext called
            `name``
        """
        return name in self._index


    def __getitem__(self, children):
        """Square bracket implementation for child insertion
        
        Arguments:
            children (iterable): Iterable of child contexts
            
        Return:
            ``self``
        """
        self._children.clear()
        self._index.clear()
        
        #add elements
        for child in children:
            if not isinstance(child, Context):
                raise TypeError("In {}: {} is not a Context derived class"
                                .format(self.name, type(child)))
            self.insert(child)
        return self


    def moveTo(self, other):
        """Move all attributes to other and reset 
        """
        for child in self._children:
            child.parent= other
            
        super().moveTo(other)
        

    def validate(self):
        """Validates all children
        """
        for child in self._children:
            child.validate()


    def reset(self):
        """Resets all children
        """
        for child in self._children:
            child.reset()


    def open(self, resetChildren=True, **kwargs):
        """Open the current context
        
        Resets all children

        Arguments:
           resetChildren (bool): If ``True`` all children are reset.
           **kwargs: Keyword arguments
        """
        if resetChildren:     
            #do not call self.reset, because it might be overridden
            for child in self._children:
                child.reset() 


    def close(self):
        """Close the current context

        This default implementation does nothing.
        """
        return


    def getChild(self, name):
        """Get child context
        
        Arguments:
            name (str): Name of child context to access
        
        Raise:
            `ValueError: If context with the given name exists
            
        Return:
             :class:`schema.Context`: Child context 
        """
        i= self._index.get(name)

        if i is not None:
            return self._children[i]
        
        raise ValueError("In Group '{}': No such context : '{}'"
                         .format(self.name, name))
        

    def insert(self, element):
        """Insert a child element into the current group
        
        Inserts the element into the group. If an element with same name
        already exists, it will be overwritten.
        
        Arguments:
            element (:class:~config.Context): Child element to insert.
        """
        if isinstance(self, Context):
            element.parent= self
        else:
            element.parent= None
            
        i= self._index.get(element.name)
        if i is None:
            # Element with this name does not exist -> append new
            i= len(self._index)
            self._index[element.name]= i
            self._children.append(element)
        else:
            #Element with same name exists -> overwrite
            self._children[i]= element
            
            
           
def children():
    """Decorate existing context with children
    
    Arguments:
        name (str): Name of new group
        
    Return:
        DataModelCreator: Wrapper for new group
    """
    return Group()
