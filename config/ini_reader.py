#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .default_reader import DefaultReader


class IniReader(DefaultReader):
    """Reader for INI files
    
    Arguments:
        contentHandler (:class:`~.ContentHandler`): Content handler.   
    """
    def __init__(self, contentHandler, assignChar='=', commentChar=';'):

        super().__init__( contentHandler=contentHandler,
                          assignChar=assignChar,
                          commentChar=commentChar)

        self._actions.clear()        
        
        # Default actions
        self.actions([
            (r"{0}([^\n]*)".format(commentChar), "comment"),
            (r"[\t ]*(\r?\n)", "newline"),
            (r"([\t ]*)'([^']*)'", "quoted_identifier"),
            (r"([\t ]*)\"([^\"]*)\"", "quoted_identifier"),
            (r"[ \t]*{0}[ \t]*".format(assignChar), "beginAssignment"),
            (r"(\s*)\[(\s*)(\S+)(\s*)\](\s*)", "newContext"),
            (r"([\ ]*)([^\s{0}{{}}\[\],;{1}\(\)]+)"
              .format(assignChar, commentChar), "identifier"),
            (r"([\t ]+)", "ignore")
        ])
       
        
    def parse(self, inputStream):
        """Parse input stream
        
        Arguments:
            inputStream: Stream to parse.
        """
        self._inContext= False
        self.startDocument()
        self.tokenize(inputStream)
        
        if self._inContext:
            self.leaveContext()
        
        self.endDocument()


    def newContext(self, match):
        """Enter a new context
        
        Arguments:
            match: Match object.
        """
        if self._inContext:
            self.leaveContext()
        else:
            self._inContext= True
        
        self._impl.ignoreContent( match.group(1) )
        self._impl.ignoreContent( match.group(2) )
        
        self._buffer.append( match.group(3) )
       
        self.enterContext()
        
        self._impl.ignoreContent( match.group(4) )
        self._impl.ignoreContent( match.group(5) )
       