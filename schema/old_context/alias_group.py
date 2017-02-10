# -*- coding: utf-8 -*-
from .group import Group

class AliasGroup(Group):
    """Similar to :class:`config.context.Group` which allows aliases for names
    
    Allows to specify aliases for each group member, which will be invoked
    instead of the real name of the group.
    
    Arguments:
        aliases (dict): Dictionary of aliases with alias as key and destination
           keyword as value.
        keepOriginalNames (bool): If ``True``, the original names of the group
           members remain valid. Otherwise they will not be recognised.
        kwargs: Keyword arguments forwarded to
           :class::class:`~config.context.Group` constructor
    """
    def __init__(self, aliases= dict(), keepOriginalNames=True, **kwargs):
        self._aliases= dict()
        super().__init__(**kwargs)
        self.addAliases(aliases)


    def addAliases(self, aliases):
        """Add aliases
        
        Arguments:
            aliases (dict): Dictionary containing new name alias as key and
               registred name as value.
               
        Raise:
            KeyError: A value in aliases is not a recognised subcontext name
        """
        for alias, dest in aliases.items():
            i= self._index(dest)
            if i is None:
                raise KeyError("Alias for invalid key {0}".format(dest))
            self._aliases[alias]= i
            

    def clearAliases(self):
        """Clear all aliases
        """
        self._aliases.clear()


    def _index(self, name):
        """Get index of subcontext
        
        Arguments:
            name (string): Name of subcontext
            
        Return:
            int: Index of subcontext or ``None``, if ``name`` is not a valid
            subcontext
        """
        retval= super()._index(name)
        if retval is not None:
            return retval
        return self._aliases.get(name, None)
        
