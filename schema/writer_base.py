# -*- coding: utf-8 -*-
from .content_handler import ContentHandler
from .content_buffer import ContentBuffer

PENDING= 1
BRANCH = 2
LEAF   = 3

class WriterBase(ContentHandler):
    """Generic base class for writer objects
    
    When pretty printing content, it is required to know whether or not the
    current context is a branch or a leaf in the parse tree. This information
    may not be available upon entering the context. This abstract base class
    determines the context type and invokes the functions enterLeaf and
    enterBranch, which shall be implemented in the derived class.
    """
    def __init__(self):
        self._currentContext= None
        self._pendingContext= None
        self._buffer        = ContentBuffer()
        self._locator       = None


    @property
    def locator(self):
        """Return the currently used locator
        
        The locator is typically provided by the parser to track the current
        state of the parser.
        
        Return:
            :class:`~schema.Locator`: Locator object
        """
        return self._locator


    @locator.setter
    def locator(self, locator):
        """Set locator used by this handler
        
        Parsers are encourated to provide a locator through this interface.
        
        Arguments:
            locator(`schema.Locator`): Locator object.
        """
        self._locator= locator


    def open(self):
        """Open the schema
        
        Make sure the current schema is valid and the cursor is placed at the
        root node.
        """
        self._currentContext= None
        self._pendingContext= None
        self._buffer.flush()
    
    
    def close(self):
        """End current document
        """
        self._currentContext= None
        return
    
    
    def enter(self, name, **kwargs):
        """Enter a sub context of the currently active context of the schema

        Enter the context and try to determine whether it is a leaf or a
        branch. If the context type cannot be determined set current context
        type to pending and store name and attributes in pending context.
        
        Arguments:
            name (:class:`str`): Context name
            **kwargs: Keyword arguments passed verbatim to schema
        """
        if self._currentContext is None:
            self._enterBranch(name, **kwargs)
            return

        if self._currentContext == PENDING:
            # parent must be a node
            self._invoke(self.enterBranch)

        self._pendingContext= (name, dict(kwargs)) #copy not ref
        self._currentContext= PENDING
        self._buffer.flush()
                   
        
    def leave(self):
        """Leave current context
        
        If current context is a leaf, all pending content is written and the
        context is closed.
        """
        if self._currentContext == PENDING:
            #neither sub contexts nor content so far -> assume it's a leaf
            self._invoke(self._enterLeaf)            

        if self._currentContext == LEAF:
            self.writeContent(self._buffer.flush())
            self.exitLeaf()
        elif self._currentContext == BRANCH:
            self._buffer.flush() # content in branch is ignored
            self.exitBranch()
        else:
            raise IOError("Attempt to leave context without opening it")
            
        self._currentContext= BRANCH


    def content(self, content):
        """Add content to current context

        Arguments:
            content(str): String containing content
        """
        if not content:
            return
            
        if self._currentContext == BRANCH:
            if content.isspace():
                return
            else:
                self.fatalError("Content is not allowed here")
        
        if self._currentContext == PENDING and not content.isspace():
            self._invoke(self._enterLeaf)
        
        self._buffer.add(content)

       
    def comment(self, comment):
        """Add comment to current context

        Arguments:
            comment(str): String containing comment
        """
        if not comment:
            return
            
        if self._currentContext == LEAF:            
            raise IOError("Comment not allowed here")
        
        if self._currentContext == PENDING:
            #comment only allowed in branch node
            self._invoke(self._enterBranch)

        self.writeComment(comment)
        

    def ignore(self, content):
        """Add ignorable content to current context

        Arguments:
            content(str): String containing potentially ignorable content
        """
        return
               
        
    def enterBranch(self, name, **kwargs):
        """Enter a branch node

        This function shall be implemented by the derived class
        
        Arguments:
            name (str): Name of branch to enter
            **kwargs: Optional keyword arguments passed to branch
        """
        raise NotImplementedError("To be implemented by derived class")

        
    def enterLeaf(self, name, **kwargs):
        """Enter a terminal or leaf node
        
        This function shall be implemented by the derived class

        Arguments:
            name (str): Name of branch to enter
            **kwargs: Optional keyword arguments passed to branch
        """
        raise NotImplementedError("To be implemented by derived class")


    def exitBranch(self):
        """Exit from a branch node
        
        This function shall be implemented by the derived class
        """
        raise NotImplementedError("To be implemented by derived class")

        
    def exitLeaf(self):
        """Exit from a terminal or leaf node
        
        This function shall be implemented by the derived class
        """
        raise NotImplementedError("To be implemented by derived class")


    def writeContent(self, content):
        """Write content to leaf node
        
        This function shall be implemented by the derived class
        """
        raise NotImplementedError("To be implemented by derived class")


    def writeComment(self, content):
        """Write comment to branch node
        
        This function shall be implemented by the derived class
        """
        raise NotImplementedError("To be implemented by derived class")


    def split(self, content, maxLen=80):
        """Split long content lines
        
        Lines are truncated to enable a line length of no more than 80
        characters. Any additional line breaks are removed.
        
        Arguments:
           content(:class:`str`): Content string to split
           MaxLen(:class:`int`): Maximum number of characters per line.
              Defaults to 80.
              
        Yield:
            Line of content
        """
        for line in content.split("\n"):
            pos= 0
            end= len(line)
            x=pos
            
            while(x != end):
                if end - pos > maxLen:
                    x= line.rfind(" ", pos, pos + maxLen)

                    if x == -1:
                        x= line.find(" ", pos + maxLen)
                    
                    if x == -1:
                        x=end
                else:
                    x= end

                yield line[pos:x]
                pos= x + 1
        return


    def _enterBranch(self, name, **kwargs):
        """Wrapper for enterBranch"""
        self.enterBranch(name, **kwargs)
        self._currentContext= BRANCH
        
        
    def _enterLeaf(self, name, **kwargs):
        """Wrapper for enterBranch"""
        self.enterLeaf(name, **kwargs)
        self._currentContext= LEAF
        
        
    def _invoke(self, method):
        name, kwargs= self._pendingContext
        method(name, **kwargs)
        self._pendingContext= None
        