The Config Package
==================
The config package contains several modules and 4 sub-packages:

Content
-------

.. toctree::
   :maxdepth: 2

   default_reader
   ini_reader
   xml_reader

   context_reader
   default_writer
   xml_writer
   
   dispatcher
   error
   error_handler
   locator
   
Design Concept
--------------
The main concept of this package is the context. A context describes an entity,
which handles content passed to it. In terms of xml, a context can be an element.
There exist several different context implementations for different kind of input.
Contexts which process content such as key value pairs and contexts which may
hold other content derived objects for nesting. All context dervived objects are
gathered in the sub-package context.

Thus the 