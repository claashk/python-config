# -*- coding: utf-8 -*-

class SchemaReader(object):
    """Reader for :class:`~Schema` objects
    
    Extracts data from a :class:`~schema.Schema` and forwards it to any 
    :class:`schema.ContentHandler` derived content handler. 
        
    Arguments:
        contentHandler (:class:`~schema.ContentHandler`): Destination content
            handler. All content extracted from the input schema is directed
            to this handler.
    """
    def __init__(self, contentHandler):
        self._dest= contentHandler
        self._attrs  = dict()


    def __call__(self, schema):
        """Invoke reader
        
        Arguments:
            schema (:class:`~schema.Schema`): Schema to read
        """
        schema.reset()
        self._dest.open()
        self._dump(schema)
        self._dest.close()

   
    def _dump(self, schema):
        """Forward context to dispatcher
        
        Arguments:
           context (:class:`~schema.Context`): Context to read and forward to
               destination handler.
        """
        for ctxName in schema():
            schema.enter(ctxName)
            ctx= schema.activeContext
            self._dest.enter(ctxName, attrs=ctx.attributes)
            self._dest.content( str(ctx) )
            self._dump(schema)
            self._dest.leave()
            schema.leave()
    