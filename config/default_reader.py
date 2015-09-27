#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
from .locator import Locator


class DefaultReader(object):
    """Default reader for ASCII files
    
    Arguments:
        contentHandler (:class:`~.ContentHandler`): Content handler object.   
        assignChar (:class:`str`): Assignment character. Defaults to '='.
        commentChar (:class:`str`): Comment character. Defaults to '#'.
    """
    def __init__(self, contentHandler,
                       assignChar= "=",
                       commentChar= "#" ):
                           
        self._impl            = contentHandler
        self._actions         = list()
        self._locator         = Locator()
        self._onLhs           = True #: Whether or not we are on left-hand side of expr
        self._inAttributes    = False #: Whether we are parsing attributes
        self._inBlock         = False #: Whether we are inside a () block 
        self._buffer          = []
        self._attributes      = dict()
        self._currentAttribute= None
        self._stack           = list()

        # Default actions
        self.actions([
            (r"{0}(.*)".format(commentChar), "comment"),
            (r"[\t ]*(\r?\n)", "newline"),
            (r"([\t ]*)'([^']*)[\t ]*'", "quoted_identifier"),
            (r"([\t ]*)\"([^\"]*)\"[\t ]*", "quoted_identifier"),
            (r"([\t ]*)\(", "beginBlock"),    
            (r"\)[\t ]*", "endBlock"),    
            (r"[ \t]*{0}[ \t]*".format(assignChar), "beginAssignment"),
            (r"[\t ]*\{", "enterContext"),
            (r"\}[\t ]*", "leaveContext"),
            (r"([\t ]*)(\[)([\t ]*)", "beginAttributes"),
            (r"([\t ]*)(\])([\t ]*)", "endAttributes"),
            (r"(,)[\t ]*", "comma"),
            (r"(;)[\t ]*", "semicolon"),
            (r"([\ ]*)([^\s{0}{{}}\[\],;{1}\(\)]+)[\t *]*"
              .format(assignChar, commentChar), "identifier"),
            (r"([\t ]+)", "ignore")
        ])


    def actions(self, actions):
        """Register regular expression for a method
        
        Assigns a regular expression to a class method to execute, when the
        regular expression matches an input line.
        
        Arguments:
            name (str): Name of class method to invoke. The method is invoked
               with a match object as single parameter.
            pattern (str): Regular expression pattern to match.
        """
        for pattern, name in actions:
            self._actions.append((re.compile(pattern), getattr(self, name))) 
        
        
    def parse(self, inputStream):
        self.startDocument()
        self.tokenize(inputStream)
        self.endDocument()        
        
        
    def startDocument(self):
        """Start parsing a new document/stream
        """
        self._stack.clear()
        self._impl.startDocument()
        self._impl.locator= self._locator
        self._impl.enterContext("root") #Enter root context
        

    def endDocument(self):
        """End parsing the current document
        """
        #leave root context
        if self._stack:
            msg= "The following contexts were not closed:\n"
            for name in self._stack:
                msg= "\n - ".join([msg, name])
            self._impl.warn(msg)

        self._impl.leaveContext() #leave root context
        self._impl.endDocument()


    def tokenize(self, inputStream):
        """Tokenize input stream and process tokens
        
        Arguments:
            inputStream: Input stream
        """

        for self._locator.line, line in enumerate(inputStream, start=1):
            self._locator.column= 0
            end= len(line)

            while self._locator.column != end:
                match= None
                for regex, action in self._actions:
                    match= regex.match(line[self._locator.column:])
                    if match:
                        try:
                            action(match)
                        except Exception as ex:
                            self._impl.fatalError( str(ex) )

                        self._locator.column+= match.end()
                        break
                
                if not match:
                    self._impl.error("Undefined pattern")
            

    def comment(self, match):
        """Parse a comment string
        
        Arguments:
            match (:class:`re.MatchObject`): Regular expression match object
        """
        self._endAssignment()
        self._impl.addComment(match.group(1))


    def beginBlock(self, match):
        if self._inBlock:
            raise ValueError("Nested blocks are not allowed")
        
        if self._inAttributes:
            raise ValueError("Blocks not allowed inside attributes.")
        
        if self._onLhs:
            raise ValueError("Blocks are not allowed on RHS expressions")
        
        self._impl.addContent(match.group(0))
        self._inBlock= True


    def endBlock(self, match):
        if not self._inBlock:
            raise ValueError("Spourious ')'")
        
        self._impl.addContent(match.group(0))
        self._inBlock= False


    def quoted_identifier(self, match):
        if not self._inAttributes:
            self._impl.ignoreContent("'")
        
        self.identifier(match)
        
        if not self._inAttributes:
            self._impl.ignoreContent("'")


    def identifier(self, match):
        if self._inAttributes:
            if self._onLhs:
                if self._currentAttribute is not None:
                    raise ValueError("Expected assignment")
                    
                self._currentAttribute= match.group(2)
            else:
                self._attributes[self._currentAttribute]= match.group(2)
                self._endAssignment()
        else:
            # Not in attribute mode
            self._impl.ignoreContent( match.group(1) )
            if self._onLhs:
                self._buffer.append( match.group(2) )
            else:
                self._impl.addContent( match.group(2) )
        

    def beginAssignment(self, match):
        """Called if an assignment character is found
        
        Arguments:
            match: Ignored match object.
        """
        if self._inBlock:
            # Inside a block assignment chars are ignored.
            self._impl.addContent(match.group(0))
            return
            
        if not self._onLhs:
            # An assignment character on RHS shall be quoted
            raise ValueError("Assignment character on RHS must be quoted")            

        if not self._inAttributes:        
            self.enterContext()
        
        self._onLhs= False


    def comma(self, match):
        """Called if a comma is found
        
        Arguments:
            match (:class:'MatchObject'): match object
        """
        if self._inBlock:
            self._impl.addContent(match.group(1))
        elif self._inAttributes:
            self._endAssignment()
        else:
            self._impl.addContent(match.group(1))
        

    def semicolon(self, match):
        """Called if a semicolon is found
        
        Arguments:
            match (:class:'MatchObject'): match object
        """
        self._endAssignment()
        

    def _endAssignment(self):
        """Invoked on the end of an assignment
        """
        if self._onLhs:
            #Nothing to do
            return
        
        if self._inAttributes:
            if not self._currentAttribute:
                raise ValueError("Incomplete Attribute")
            
            if self._attributes.get(self._currentAttribute, None) is None:
                raise ValueError("Missing value for attribute '{0}'!"
                                 .format(self._currentAttribute))
            
            self._currentAttribute= None
        else:
            self._stack.pop()
            self._impl.leaveContext()
        
        self._onLhs= True


    def enterContext(self, match=None):
        """Enter a new context
        
        Called if either an opening curly bracket or an assignment character
        is found.        
        
        Arguments:
            match: Ignored match object.
        """
        if self._inBlock:
            raise ValueError("Cannot start context in block")
            
        if not self._onLhs:
            raise ValueError("Invalid RHS expression")
            
        if self._inAttributes:
            raise ValueError("Cannot start scope in attribute")
            
        if len(self._buffer) != 1:
            raise ValueError("Expected exactly one identifier, got {0}"
                             .format(len(self._buffer)) )

        self._stack.append(self._buffer[0])

        try:
            self._impl.enterContext(self._buffer[0], self._attributes)
        finally:
            self._buffer.clear()
            self._attributes.clear()


    def leaveContext(self, match=None):
        """Called if a closing curly bracket is encountered
        """
        if self._inBlock:
            raise ValueError("Cannot end scope in block")
        self._endAssignment() #end assignment if we are on RHS, else do nothing        

        if self._attributes:
            raise ValueError("Cannot end scope in attribute expression.")

        if self._buffer:
            self._impl.addContent("".join(self._buffer))
            self._buffer.clear()
            
        self._stack.pop()
        self._impl.leaveContext()


    def newline(self, match):
        """Invoked each time a line is complete

        Arguments:
            match (): Match object        
        """
        if self._inBlock:
            self._impl.ignoreContent(match.group(0))
            return
            
        self._endAssignment()
        
        if self._inAttributes:
            if not self._currentAttribute:
                return
            raise ValueError("Illegal line break before incomplete attribute")
        else:
            self._endAssignment() #If on RHS, end assignment, else do nothing

            if self._attributes:
                raise ValueError("Superflous attributes")
    
            # If buffer is not empty, we are facing content without assignment            
            for content in self._buffer:
                self._impl.addContent(content)

            self._buffer.clear()
            self._impl.addContent(match.group(0))                


    def beginAttributes(self, match):
        if not self._onLhs:
            # An RHS '[' is treated as content
            self._impl.addContent( match.group(0) )
            return
            
        if self._inBlock:
            raise ValueError("'[' not allowed in block")

        if self._inAttributes:
            raise ValueError("Nested attributes are not allowed")
        
        self._inAttributes= True


    def endAttributes(self, match=None):
        if self._inBlock:
            raise ValueError("']' not allowed in block")

        if not self._inAttributes:
            raise ValueError("Cannot end attributes.")
            
        if not self._onLhs:
            raise ValueError("Incomplete attributes")
        
        self._inAttributes= False
        
        
    def ignore(self, match):
        """Ignore matched content
        
        Forwards the entire content to :meth:`~.ContextManager.ignoreContent`        
        
        Arguments:
            match (:class:re.MatchObject): Match object.
        """
        if self._inBlock:
            return
            
        if not self._inAttributes:
            self._impl.ignoreContent( match.group(0) )
      