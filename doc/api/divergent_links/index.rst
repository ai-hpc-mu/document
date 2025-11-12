divergent_links
===============

.. py:module:: divergent_links

.. autoapi-nested-parse::

   This script help checking inconsistent links.

   That is to say, links that have the same title but go to different places.
   This is useful for screen-reader and accessibility devices, where the user may
   say "Go to X", but if there are 2 links named "X" this creates ambiguity.


   Example (links that have the same name, but different URL):

      We have a JavaScript <a href="javascript.html">API</a> and
      a Python <a href="python.html">API</a>.

   How to fix (give the links different names):

      We have a <a href="javascript.html">JavaScript API</a> and
      a <a href="python.html">Python API</a>.

   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   divergent_links.c
   divergent_links.ignores


Classes
-------

.. autoapisummary::

   divergent_links.Checker


Functions
---------

.. autoapisummary::

   divergent_links.find_html_files


Module Contents
---------------

.. py:class:: Checker

   
   Link checker.
















   ..
       !! processed by numpydoc !!

   .. py:method:: duplicates()

      
      Print potential duplicates.
















      ..
          !! processed by numpydoc !!


   .. py:method:: scan(html_content, file_path)

      
      Scan given file for html links.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: links
      :type:  dict[str, list]


.. py:function:: find_html_files(folder_path)

   
   Find all html files in given folder.
















   ..
       !! processed by numpydoc !!

.. py:data:: c

.. py:data:: ignores
   :value: ['#', 'next', 'previous', '[source]', 'edit on github', '[docs]', 'read more ...', 'show...


