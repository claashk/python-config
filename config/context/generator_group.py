# -*- coding: utf-8 -*-
from .context import Context

class GeneratorGroup(Context):
    """Context which creates subcontexts on the fly
    
    Implemented in terms of a 
    
    
    Arguments:
        factory (callable): Factory class, which creates new contexts.
    """
    def __init__(self, factory, maxCount=1):
        super().__init__(maxCount=maxCount)
        
        self._obj= None # associated object
        self._ctx= None #template context


    def __getitem__(self, name):
        """Get sub-context by name

        Arguments:
            name (:class:`str`): Name of context to access
            
        Return:
            Context matching name
            
        Raise:
            :class:`TypeError` if no context with matching name is found.
        """
        self._ctx.obj= self.obj[name]
        return self._ctx
        
        
    def __contains__(self, name):
        """Check if this context contains a subcontext with a given name
        
        Arguments:
            name(str): Name of subcontext to search for
        
        Return:
            bool: ``True`` if and only if ``self`` has a subcontext called
            `name``
        """
        return name in self.obj
        
        
    def __iter__(self):
        """Iterate over member contexts
        
        Return:
            Iterator object
        """
        #create dictionary for reverse lookup of names
        for name, obj in self.obj:
            self._ctx.obj=  obj
            yield (name, self._ctx)


    @property
    def obj(self):
        return self._obj
        
    @obj.setter
    def obj(self, obj):
        self._obj= obj


    def reset(self):
        """Resets this context and all sub-contexts
        """
        super().reset()
        self._ctx.reset()
        self.obj= None


    def enter(self, attrs=None):
        """Routine called by context manager, after the context is invoked

        Increases count by one and reset count of each sub-context
        
        Arguments:
            attrs (:class:`dict`): Attributes
        """
        super().enter(attrs=attrs)
        

    def getContext(self, name):
        """Get sub-context
        
        Called by the context manager to obtain a sub-context during parsing.
        Shall be implemented by derived class. 
        
        This is a pure base method raising a :class:`NotImplementedError`.        
        
        Raise:
            :class:`KeyError` if no such context exists
            
        Return:
             Context instance
        """
        return self[name]
