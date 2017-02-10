# -*- coding: utf-8 -*-

class Mixin(object):
    """Base class for mixins used to extend context functionality
    
    The functionality of context objects is mainly implemented in terms of
    different mixins, which shall be derived from this class.
    """
   
    def moveTo(self, dest):
        """Initialise destination by moving content of ``self``
        
        This default implementation performs a shallow copy of all elements
        in ``self.__dict__`` to ``dest``
        
        Arguments:
            dest (:class:`schema.Context`): Destination context to initialise
        """
        for name, value in self.__dict__.items():
            setattr(dest, name, value)
        
        
        
        

        
        

