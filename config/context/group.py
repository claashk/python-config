#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .context import Context

class Group(Context):
    """Collection of context objects which does not support content
    
    Arguments:
        contexts (iterable): Iterable of (str, context) tuples.
        maxCount (int): Maximum number of allowed occurences.
    """
    def __init__(self, contexts=dict(), maxCount=1):
        super().__init__(maxCount=maxCount)
        
        #Context cannot be stored as dict, as this would not allow to iterate
        #over the items in the order in which they were defined. Thus we
        #use a list in combination with a dictionary for lookup by name
        self._contexts= []
        self._contextIndices= dict()
        
        if isinstance(contexts, dict):
            for name, ctx in contexts.items():
                self.addContext(name, ctx)
        else:
            for name, ctx in contexts:
                self.addContext(name, ctx)


    def __getitem__(self, name):
        """Get sub-context by name

        Arguments:
            name (:class:`str`): Name of context to access
            
        Return:
            Context matching name
            
        Raise:
            :class:`KeyError` if no context with matching name is found.
        """
        return self._contexts[ self._contextIndices[name] ]
        
        
    def __iter__(self):
        """Iterate over member contexts
        
        Return:
            Iterator object
        """
        #create dictionary for reverse lookup of names
        names= []
        for name,index in self._contextIndices.items():
            names.append((index, name))
        names.sort() #sort in ascending order by indices        
        
        #iterate contexts in order of definition
        for (index, name), ctx in zip(names, self._contexts):
            yield (name, ctx)
        
        return


    def addContext(self, name, context):
        """Add context to collection
        
        Arguments:
            name (str): Context to add. A context with name `None` can be
               added, which will be invoked if no matching context can be found.
            context (:class:`Context`): Context object to add
            
        """
        index= self._contextIndices.get(name)
        if index is None:
            self._contextIndices[name]= len(self._contexts)
            self._contexts.append(context)
        else:
            self._contexts[index]= context


    def reset(self):
        """Resets this context and all sub-contexts
        """
        super().reset()
        
        for ctx in self._contexts:
            ctx.reset()


    def enter(self, attrs=None):
        """Routine called by context manager, after the context is invoked

        Increases count by one and reset count of each sub-context
        
        Arguments:
            attrs (:class:`dict`): Attributes
        """
        for ctx in self._contexts:
            ctx.reset()

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
        i= self._contextIndices.get(name, self._contextIndices.get(None, None))

        if i is not None:
            return self._contexts[i]
        
        raise KeyError("Unknown context '{0}'".format(name))

