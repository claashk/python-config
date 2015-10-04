#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .context import Context

class Ignore(Context):
    """Context which basically ignores all input.   
    """          
    def __init__(self, maxCount=-1):
        super(Ignore, self).__init__(maxCount=maxCount)


    def getContext(self, name):
        """Get sub-context
        
        Arguments:
            name (str): Name of context to enter        
        
        Return:
             self
        """
        return self


    def addContent(self, content):
        """Add content
        
        Arguments:
            content (str): Content string. All content is ignored..
        
        Ignores all content
        """
        return
