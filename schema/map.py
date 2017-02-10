# -*- coding: utf-8 -*-

class Map(object):
    """Map parser usable as type
    
    Intended to be used as type argument for :func:`~schema.context.ref`
    function.
    
    Restricts parsed values to a dictionary of key value pairs. The default
    value of ``None`` can be reset by adding the desired value with ``None`` as
    key.
    
    Arguments:
        *args: Arguments forwarded to dictionary constructor
        **kwargs: Keyword arguments forwarded to dict constructor
    """
    def __init__(self, *args, **kwargs):
        self._values= dict(*args, **kwargs)

        for name, value in self._values.items():
            if type(name) != str and name is not None:
                raise ValueError("Expected key of type string, got '{}'"
                                 .format(type(name)))


    def __call__(self, content=None):
        """Parser implementation
        
        Arguments:
            content (str): Content string to parse        
        
        Return:
            value: Value assigned to content
            
        Raises:
            :class:`KeyError`: if no matching content is found
        """
        if content is None:
            return self._values.get(None)
        else:
            return self._values[content]
            
            
class Bool(Map):
    """:class:`~schema.Map` specialisation for boolean values
    
    Arguments:
        default (bool): Default value. Defaults to ``False``
    """
    def __init__(self, default=False):
        super().__init__({"on": True,
                          "off":False,
                          "yes":True,
                          "no":False,
                          "true":True,
                          "false":False,
                          None: default})
    
   