Schema Interface
================

A schema defines the content expected in configuration files in an abstract
form. Class :class:~schema.Schema implements a structure to store schema
information based on a directed graph: Each node of the graph represents a
:class:`schema.Context`, which defines how to handle content within this context.


Schema API
----------

.. autoclass:: schema.Schema
   :members:
