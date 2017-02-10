# -*- coding: utf-8 -*-
import sys
import logging

                
#Level dependent log formats
DEFAULT_FORMAT= "%(locator)s: %(message)s\n"
ERROR_FORMAT  = "%(levelname)s (%(locator)): %(message)s\n"

LOG_FORMATS= { logging.WARNING : ERROR_FORMAT,
               logging.ERROR   : ERROR_FORMAT}


class DefaultFormatter(logging.Formatter):
    """Formatter allowing log level depending formatting
    
    This formatter extends the capability of :class:`logging.Formatter` to
    allow log level dependent formatting.
    
    Arguments:
        fmt (dict): Dictionary containing numeric log level as key and
            associated format for this level as value
        default (str): Default log format for log levels not listed explicitly
            in ``fmt``.
        **kwargs : Keyword arguments forwarded to the constructor of
            :class:`logging.Formatter`
    """
    def __init__(self, fmt=dict(), default=DEFAULT_FORMAT, **kwargs):
        self.formats= dict(fmt)
        self.default= default
        super().__init__(fmt=default, **kwargs)
        
        
    def format(self, record):
        """Format routine
        
        Sets the internal attribute :attr:`_style` to the desired log format
        based on ``record.levelno`` before invoking :meth:`Formatter.format`.
        
        Return:
            str: Formatted record. Refer to :meth:`Formatter.format` for
            details.
        """
        self._style._fmt= self.formats.get(record.levelno, self.default)
        self._fmt= self._style._fmt
        return super().format(record)


class ErrorHandler(object):
    """Error handler implementation
    
    This class is intended to be used as a mixin by all classes producing user
    output such as logs, warnings or error messages. In case user code wishes
    to replace the error handling of a derived class using this mixin, this is
    best achieved as follows:

    .. code-block: python

       # Assuming an existing class Derived using ErrorHandler, replace the
       # default error handler with MyErrorHandler
       Derived.__bases__= tuple(c if c is not ErrorHandler
                                  else MyErrorHandler for c in B.__mro__)

    This implementation uses the python logging module. It adds inclusion of
    locator information into error messages, if either a `locator` keyword is
    passed to any of its methods or the inheriting class provides a ``locator``
    attribute.
    
    Messages are passed to the internal :attr:`~schema.ErrorHandler.logger`
    instance.
    
    If the root logger is not initalised, a single :class:`StreamHandler`
    writing to ``logStream`` will be installed. The root handler will use
    :class:`~schema.logger.DefaultFormatter` as formatter.
    
    Attributes:
        nErrors (int): Number of errors encountered during runtime. Increased
            on each invocation of
            :meth:`~pyassyst.utils.Logger.error`
        nWarnings (int): Number warning encountered during runtime. Increased
            on each invocation of
            :meth:`~pyassyst.utils.Logger.warn`
        logger (:class:`logging.Logger`): Logging interface
            
    Arguments:
        name (str): Name of logger to use. ``None`` will result in the root
            logger to be used. Passed verbatim to meth:`logging.getLogger`.
        logStream (stream): Stream used for the logging interface, if no root
            logger is configured.
    """
    def __init__(self, name=None, logStream=sys.stderr):
        self.nErrors  = 0
        self.nWarnings= 0
        
        #attempt to configure root logger
        logger  = logging.getLogger()
        if not logger.hasHandlers():
            handler= logging.StreamHandler(logStream)

            #this adds an instance attribute and does not alter the static
            #class variable -> modification is restricted to this handler
            handler.terminator= "" 
            formatter= DefaultFormatter(fmt=LOG_FORMATS,default=DEFAULT_FORMAT)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        #set app logger
        self.logger= logging.getLogger(name)


    def debug(self, message, *args, **kwargs):
        """Print message with level DEBUG on internal logger.
        
        Arguments:
            message (string): Message to print to stream
            *args: Positional arguments forwarded to
                :class:`Logger`. Refer to :meth:`logging.Logger.debug` for
                details.
            **kwargs: Keyword arguments forwarded to
                :class:`Logger`. Refer to :meth:`logging.Logger.debug` for
                details.
        """
        self.logger.debug(message, *args, **self._setLocator(kwargs))


    def info(self, message, *args, **kwargs):
        """Print message with level INFO on internal logger.
        
        Arguments:
            message (string): Message to print to stream
            *args: Positional arguments forwarded to
                :class:`Logger`. Refer to :meth:`Logger.debug` for details.
            **kwargs: Keyword arguments forwarded to
                :class:`Logger`. Refer to :meth:`Logger.debug` for details.
        """
        self.logger.info(message, *args, **self._setLocator(kwargs))


    def warn(self, message, *args, **kwargs):
        """Print message with level WARN on internal logger.
        
        Arguments:
            message (string): Message to print to stream
            *args: Positional arguments forwarded to
                :class:`Logger`. Refer to :meth:`Logger.debug` for details.
            **kwargs: Keyword arguments forwarded to
                :class:`Logger`. Refer to :meth:`Logger.debug` for details.
        """
        self.logger.warning(message, *args, **self._setLocator(kwargs))
        self.nWarnings += 1


    def error(self, message, *args, **kwargs):
        """Print message with level ERROR on internal logger.
        
        Arguments:
            message (string): Message to print to stream
            *args: Positional arguments forwarded to
                :class:`Logger`. Refer to :meth:`Logger.debug` for details.
            **kwargs: Keyword arguments forwarded to
                :class:`Logger`. Refer to :meth:`Logger.debug` for details.
        """
        self.logger.error(message, *args, **self._setLocator(kwargs))
        self.nErrors+= 1


    def exception(self, message, *args, **kwargs):
        """Print exception on internal logger
        
        If current log level is DEBUG, a stack trace is added to the error
        message.
        
        Arguments:
            message (string): Message to print to stream
            *args: Positional arguments forwarded to
                :class:`Logger`. Refer to :meth:`Logger.debug` for details.
            **kwargs: Keyword arguments forwarded to
                :class:`Logger`. Refer to :meth:`Logger.debug` for details.
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.exception(message, *args, **self._setLocator(kwargs))
            self.nErrors+= 1
        else:
            self.error(message, *args, **self._setLocator(kwargs))
            
            
    def fatal(self, message, *args, **kwargs):
        """Raise exception
        
        Raises:
            ContextError: context error.
        """
        raise RuntimeError(message%args, **kwargs)


    def _setLocator(self, d=dict()):
        """Set locator attribute in dictionary
        
        Extracts a Locator object from the input dictionary and replaces it
        by a string representing the locator. If no 'locator' keyword argument
        exists, locator is attempted to be retrieved from self.locator (which
        has to be implemented by the parent)
        
        
        Arguments:
            d (dict): Input dictionary
            
        Return:
            dict: Input dictionary with 'locator' key set to an appropriate
            string
        """
        loc= d.get("locator", getattr(self, "locator", None))
        if loc is None:
            d["locator"]= "?:?"
        else:
            d["locator"]= str(loc)

        return d
        