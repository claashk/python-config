# -*- coding: utf-8 -*-
from .group import Group


class AttributeGroup(Group):
    """Attribute groups are groups, where items are named through attributes
    
    Example:
    <root>
      <item name="first">1</item>
      <item name="second">1</item>
      <item name="third">1</item>
    </root>
    
    will be interpreted like
    <root>
      <item>
          <first>1</first>
      </item>
      <item>
          <second>2</second>
      </item>
      <item>
          <third>3</third>
      </item>
    </root>
    
    
    All members of the group share the same name and are distinguished by a
    defined key attribute.    
    
    """
    def __init__(self):
        self._children= list()
        self._index= dict()
        #Context cannot be stored as dict, as this would not allow to iterate
        #over the items in the order in which they were defined. Thus we
        #use a list in combination with a dictionary for lookup by name
        self._keyAttr= key#name of attribute specifying the actual name

        
    def moveTo(self, other):
        """Move all attributes to other and reset 
        """
        for child in self._children:
            child.parent= other
            
        super().moveTo(other)
        

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
