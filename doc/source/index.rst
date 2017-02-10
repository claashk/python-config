.. PyConfig documentation master file, created by
   sphinx-quickstart on Tue Sep 15 13:21:10 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pySchema's documentation!
====================================
pySchema is a python package supporting various configuration files. The package
supports INI, XML and a custom ASCII format similar in functionality to XML, but
with a little less text.



Design Concept
--------------
The main concept of this package is the context. A context describes an entity,
which handles content passed to it. In terms of xml, a context can be an element.
There exist several different context implementations for different kind of input.
Contexts which process content such as key value pairs and contexts which may
hold other content derived objects for nesting. All context dervived objects are
gathered in the sub-package context.


Contents:

.. toctree::
   :maxdepth: 2

   schema
   



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

