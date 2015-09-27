#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .decorator import Decorator

class Help(Decorator):
    """Base class for decorators.
    
    Arguments:
        helpMsg (:class:`str`): Help message
        parent (:class:`Context`): Context derived object to decorate
    """
    def __init__(self, helpMsg, parent):
        super(Help, self).__init__(parent)
        self._help= helpMsg

   
    @property
    def help(self):
        """Print help message"""
        return self._help
