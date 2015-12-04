# -*- coding: utf-8 -*-

from .context import Group

class ContextReader(object):
    """Reader for :class:`.~Context` objects
    
    Iterates over a context and all sub-contexts and forwards the content to a 
    Dispatcher object.
    
    Arguments:
        handler (:class:`Dispatcher`): Dispatcher object.
    """
    def __init__(self, handler):
        self._handler= handler
        self._attrs  = dict()
        self._maxLineLength= 80
        self._indentSize = 2
        self._indentCount= 0


    def __call__(self, context):
        self._indentCount= 0
        self._handler.startDocument()
        self._dispatch(context)
        self._handler.endDocument()


    @property
    def indent(self):
        return self._indentCount * self._indentSize * u" "
   
   
    def _dispatch(self, context, name="root"):
        self._comment( context.help )
        self._handler.ignoreContent(self.indent)
        self._handler.enterContext(name, attrs=self._attrs)

        isGroup= isinstance(context, Group)
        
        if isGroup:
            self._indentCount+= 1
            self._handler.ignoreContent(u"\n")

        if context.content is not None: 
            self._handler.addContent( str(context.content) )

        for ctxName, ctx in context:
            self._dispatch(ctx, ctxName)
    
        if isGroup:
            self._indentCount-= 1
            self._handler.ignoreContent(self.indent)
    
        self._handler.leaveContext()
        self._handler.ignoreContent(u"\n")



    def _comment(self, comment):
        """Print long comment lines
        
        Lines are truncated to enable a line length of no more than 80
        characters. Any additional line breaks are removed.
        
        Arguments:
           msg: Message to print as comment
           stream: Output stream. If None, it is set to self._logStream
           maxLineLength: Maximum number of characters per line. Defaults to 80.
        """
        maxLen= self._maxLineLength - self._indentCount * self._indentSize - 1
        
        for line in comment.split("\n"):
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

                self._handler.ignoreContent(self.indent)
                self._handler.addComment(line[pos:x])
                self._handler.ignoreContent("\n")
                pos= x + 1
