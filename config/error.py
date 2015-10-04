#! /usr/bin/env python
# -*- coding: utf-8 -*-

class ConfigError(Exception):
    """Raised if errors occur during context management.
    
    Arguments:
        message(str): Message string containing error message
        locator (:class:`object`): :class:`~.Locator` object (or any
           object with identical interface )
    """
    def __init__(self, message=None, locator=None):

        # Call the base class constructor with the parameters it needs
        super(ConfigError, self).__init__(message, locator)

    @property
    def message(self):
        return self.args[0]


    @property
    def line(self):
        if self.args[1] is None:
            return "?"
            
        return self.args[1].line
        

    @property
    def column(self):
        if self.args[1] is None:
            return "?"
        
        return self.args[1].column


    def __str__(self):
        return "In line {0}:{1}: {2}".format( self.line,
                                              self.column,
                                              self.message )


class ContextError(ConfigError):
    """Error object thrown on context errors
    
    The interface is identical to :class:`~.ConfigError`
    """
    pass


class ConfigWarning(ConfigError):
    """Exception object used for warning messages
    """
    pass
    
    