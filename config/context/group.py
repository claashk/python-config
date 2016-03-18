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
            :class:`TypeError` if no context with matching name is found.
        """
        return self._contexts[self._index(name)]
        
        
    def __contains__(self, name):
        """Check if this context contains a subcontext with a given name
        
        Arguments:
            name(str): Name of subcontext to search for
        
        Return:
            bool: ``True`` if and only if ``self`` has a subcontext called
            `name``
        """
        return name in self._contextIndices        
        
        
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
        index= self._index(name)
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
        i= self._index(name)

        if i is not None:
            return self._contexts[i]
        
        raise KeyError("Unknown context '{0}'".format(name))
        
        
    def translate(self, dictionary):
        """Translate keys into another dialect
        
        Translates the names of all subcontexts into another language/dialect.
        The mapping of new names to old names is provided in terms of a
        dictionary. Old names, for which no translation is provided in the
        dictionary will remain valid identifiers, while translated names will
        replace their counterparts.
        
        Arguments:
            dictionary (dict): Dictionary containing new subcontext names as
               key and old subcontext names as value.
               
        Raise:
            KeyError: Dictionary maps to an invalid identifier
        """
        indices= dict() #new dictionary
        for newName, oldName in dictionary.items():
            i= self._contextIndices.pop(oldName)
            indices[newName]= i
            
        #Add old names, for which no translation was provided
        indices.update( self._contextIndices )
        self._contextIndices= indices


    def _index(self, name):
        """Get index of subcontext
        
        Arguments:
            name (string): Name of subcontext
            
        Return:
            int: Index of subcontext or ``None``, if ``name`` is not a valid
            subcontext
        """
        return self._contextIndices.get(name,
                                        self._contextIndices.get(None, None))
