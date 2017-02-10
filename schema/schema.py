# -*- coding: utf-8 -*-

from .context import Context

class Schema(object):
    """Schema implements a user defined data model
    
    A Schema implements a user-defined data model in terms of a graph of
    :class:`~config.Context` objects. The schema provides methods to traverse
    the graph and direct input to the appropriate context.
    
    Arguments:
        context (:class:`~schema.Context`): Root context forming the base of
            the data model
    """
    def __init__(self, context=None):
        self._root= None
        self._stack= list()
        
        if context is not None:        
            self.open(context)


    @property
    def activeContext(self):
        """Access currently active context
        
        Return:
            :class:`~schema.Context` : Currently active context
            
        Raises:
            IndexError: If no context has been opened yet
        """
        return self._stack[-1]


    def __iter__(self):
        """Iterate over sub-context names
        """
        try:
            for ctx in self.activeContext:
                yield ctx.name
        except IndexError:
            yield self._root.name

        
    @property
    def isActive(self):
        return bool(self._stack)

        
    def open(self, context):
        """Open new context
        
        Arguments:
            context (:class:Context): New root context
        """
        self.close()
        self._root= context            

        if self._root is None:
            raise ValueError("No context specified.")
            
        if not isinstance(self._root, Context):
            raise TypeError("Expected a context, got {}"
                            .format(type(self._root)))
        

    def close(self):
        """Close all remaining open contexts
        """
        while self.isActive:
            self.leave()


    def reset(self):
        """Close all contexts and re-open root context
        
        Raises:
            ValueError: if root context has not been specified.
        """
        self.open(self._root)


    def enter(self, name, **kwargs):
        """Enter a new context
        
        Retrieves the new context from the current context with a call to
        :meth:`~.Context.getContext`(''name''). Then the current context is
        added to the context stack and the retrieved context is assigned to
        the active context. Finally :meth:`~.Context.enter` is invoked.        
        
        Calling this method on a Schema which is not open, results in
        undefined behaviour.
        
        Arguments:
            name (str): Name of context to enter
            **kwargs : Additional arguments passed to context upon opening
            
        Raises:
            ValueError: If no child with the provided name exists
            RuntimeError: If no root context has been specified
        """
        child= self._root
        try:
            child= self.activeContext.getChild(name)
        except IndexError:
            #root context is not open -> open it if name fits
            if child is None:
                raise RuntimeError("No root context specified. Call open first")
            if name != child.name:
                raise ValueError("Invalid root context", name, child.name)
        
        child.open(**kwargs)
        self._stack.append(child)

    
    def leave(self):
        """Leave the current context

        Calling this method on a Schema which is not open, results in
        undefined behaviour.
        """
        self.activeContext.close()
        self._stack.pop()
        
    
    def content(self, content):
        """Add content to content buffer
        
        Arguments:
            content (str): Content string
        """
        self.activeContext.fromString(content)
        