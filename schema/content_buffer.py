# -*- coding: utf-8 -*-

class ContentBuffer(object):
    """Buffer for content strings
    
    Several parsers (such as XML SAX) return content in chunks. Often it is
    desireable to direct content to context objects in a single chunk. This
    requires intermediate buffering. This implementation provides a very basic
    buffer mechanism, which interfaces nicely with the
    :class:`~schema.ContentHandler` interface.
    """
    def __init__(self):
        self._buffer= [] #list of string chunks received as content


    def __len__(self):
        return len(self._buffer)


    @property
    def empty(self):
        """Check if buffer is empty
        
        Return:
            ``True`` if and only if buffer contains no data
        """
        return not bool(self._buffer)


    def isSpace(self):
        """Check if buffer content consists entirely of spaces
        
        Return:
            bool: ``True`` if and only if buffer consists exclusively of space
               characters
        """
        for chunk in self._buffer:
            if not chunk.isspace():
                return False
                
        return True


    def add(self, chunk):
        """Add content chunk to buffer
        
        Appends a content chunk to the buffer if it is not empty or ``None``.

        Arguments:
            chunk(str): Content chunk to add to this buffer
        """
        if chunk:
            self._buffer.append(chunk)


    def clear(self):
        """Discard content from buffer
        """
        self._buffer.clear()


    def getContent(self):
        """Get buffered content as string
        
        This does not clear the buffer.
        
        Return:
            str : String with buffer content
        
        """
        return "".join(self._buffer)


    def flush(self):
        """Return buffer content as string and clear buffer

        Return:
            str : String containing buffer content
        """
        retval= self.getContent()
        self.clear()
        
        return retval

   
       

    